"""Orquestrador da esteira VSK • PRE-CALL.

Lê o input do cliente, roda cada bloco em sequência via Claude API
com prompt caching, e salva a saída de cada bloco em Markdown.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from anthropic import Anthropic
from jinja2 import Template

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = ROOT / "system.md"
BLOCKS_DIR = ROOT / "blocks"

DEFAULT_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096


@dataclass
class Block:
    id: str
    slug: str
    nome: str
    responsavel: str
    itens: str
    body: str
    path: Path


@dataclass
class BlockResult:
    block: Block
    output: str
    input_tokens: int
    output_tokens: int
    cache_creation_tokens: int
    cache_read_tokens: int
    elapsed_s: float


@dataclass
class PipelineResult:
    cliente_slug: str
    output_dir: Path
    blocks: list[BlockResult] = field(default_factory=list)

    @property
    def total_input_tokens(self) -> int:
        return sum(b.input_tokens for b in self.blocks)

    @property
    def total_output_tokens(self) -> int:
        return sum(b.output_tokens for b in self.blocks)

    @property
    def total_cache_creation(self) -> int:
        return sum(b.cache_creation_tokens for b in self.blocks)

    @property
    def total_cache_read(self) -> int:
        return sum(b.cache_read_tokens for b in self.blocks)

    @property
    def total_elapsed_s(self) -> float:
        return sum(b.elapsed_s for b in self.blocks)


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "cliente"


def load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def load_blocks() -> list[Block]:
    blocks: list[Block] = []
    for path in sorted(BLOCKS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            raise ValueError(f"Bloco {path.name} sem frontmatter YAML")
        _, fm, body = text.split("---\n", 2)
        meta = yaml.safe_load(fm) or {}
        blocks.append(
            Block(
                id=str(meta["id"]),
                slug=meta["slug"],
                nome=meta["nome"],
                responsavel=meta.get("responsavel", ""),
                itens=meta.get("itens", ""),
                body=body.strip(),
                path=path,
            )
        )
    blocks.sort(key=lambda b: int(b.id))
    return blocks


def render_block_prompt(block: Block, cliente: dict[str, Any]) -> str:
    return Template(block.body).render(cliente=cliente)


def build_brief(cliente: dict[str, Any], previous: list[BlockResult]) -> str:
    """Brief acumulado: input do cliente + saídas dos blocos anteriores.

    É montado como um único bloco de texto cacheável — assim, dentro de uma
    mesma execução, todos os blocos depois do primeiro batem cache no prefixo.
    """
    parts: list[str] = []
    parts.append("# Briefing do cliente\n")
    parts.append("```json")
    parts.append(json.dumps(cliente, ensure_ascii=False, indent=2))
    parts.append("```\n")

    if previous:
        parts.append("# Saídas dos blocos anteriores\n")
        for r in previous:
            parts.append(f"## Bloco {r.block.id} — {r.block.nome}\n")
            parts.append(r.output.strip())
            parts.append("")
    return "\n".join(parts)


def run_block(
    api: Anthropic,
    model: str,
    system_prompt: str,
    block: Block,
    cliente: dict[str, Any],
    previous: list[BlockResult],
) -> BlockResult:
    brief = build_brief(cliente, previous)
    block_prompt = render_block_prompt(block, cliente)

    started = time.time()
    msg = api.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": brief,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "type": "text",
                        "text": block_prompt,
                    },
                ],
            }
        ],
    )
    elapsed = time.time() - started

    output_text = "".join(
        part.text for part in msg.content if getattr(part, "type", None) == "text"
    ).strip()

    usage = msg.usage
    return BlockResult(
        block=block,
        output=output_text,
        input_tokens=getattr(usage, "input_tokens", 0) or 0,
        output_tokens=getattr(usage, "output_tokens", 0) or 0,
        cache_creation_tokens=getattr(usage, "cache_creation_input_tokens", 0) or 0,
        cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0) or 0,
        elapsed_s=elapsed,
    )


def run_pipeline(
    cliente: dict[str, Any],
    output_root: Path,
    model: str = DEFAULT_MODEL,
    only: list[str] | None = None,
    on_block: callable = None,  # type: ignore[type-arg]
) -> PipelineResult:
    api = Anthropic()
    system_prompt = load_system_prompt()
    blocks = load_blocks()
    if only:
        wanted = {b.zfill(2) for b in only}
        blocks = [b for b in blocks if b.id in wanted]

    cliente_slug = slugify(cliente.get("nome", "cliente"))
    output_dir = output_root / cliente_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    result = PipelineResult(cliente_slug=cliente_slug, output_dir=output_dir)

    for block in blocks:
        if on_block:
            on_block("start", block, None)
        br = run_block(api, model, system_prompt, block, cliente, result.blocks)
        file_path = output_dir / f"{block.id}_{block.slug}.md"
        file_path.write_text(br.output + "\n", encoding="utf-8")
        result.blocks.append(br)
        if on_block:
            on_block("done", block, br)

    meta = {
        "cliente": cliente,
        "model": model,
        "total_input_tokens": result.total_input_tokens,
        "total_output_tokens": result.total_output_tokens,
        "total_cache_creation_tokens": result.total_cache_creation,
        "total_cache_read_tokens": result.total_cache_read,
        "total_elapsed_s": round(result.total_elapsed_s, 2),
        "blocks": [
            {
                "id": b.block.id,
                "nome": b.block.nome,
                "input_tokens": b.input_tokens,
                "output_tokens": b.output_tokens,
                "cache_creation_tokens": b.cache_creation_tokens,
                "cache_read_tokens": b.cache_read_tokens,
                "elapsed_s": round(b.elapsed_s, 2),
            }
            for b in result.blocks
        ],
    }
    (output_dir / "_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


def load_client(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["nome", "nicho", "produto"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise ValueError(f"Campos obrigatórios faltando no input: {missing}")
    return data
