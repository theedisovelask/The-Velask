"""Monta os documentos finais a partir das saídas dos blocos.

Gera dois arquivos consolidados:
- PROPOSTA.md  : proposta + escopo + entregas + pacotes (foco no cliente)
- ROTEIRO_CALL.md : diagnóstico + oportunidades + roteiro de call (foco em Edison)
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


# Quais blocos entram em cada documento, na ordem.
PROPOSTA_BLOCKS = [
    "05",  # Proposta Velask 360
    "06",  # Escopo de execução
    "07",  # Social media
    "08",  # Criativos
    "09",  # Copy / funil / oferta
    "10",  # Landing page
    "11",  # WhatsApp / atendimento
    "12",  # Tráfego pago
    "13",  # Trello / gestão
    "14",  # Automações / IA
    "15",  # Dashboard
    "16",  # Pacotes e preço
]

ROTEIRO_BLOCKS = [
    "01",  # Pesquisa do nicho
    "02",  # Concorrentes
    "03",  # Diagnóstico
    "04",  # Oportunidades
    "16",  # Pacotes (Edison precisa lembrar na call)
    "17",  # Material da call
    "18",  # Envio e follow-up
]


def _read_block(output_dir: Path, block_id: str) -> tuple[str, str]:
    """Retorna (nome_do_bloco, conteúdo) para um id como '05'."""
    matches = list(output_dir.glob(f"{block_id}_*.md"))
    if not matches:
        return (f"Bloco {block_id}", f"_(saída do bloco {block_id} não encontrada)_")
    path = matches[0]
    # nome derivado do slug
    slug = path.stem.split("_", 1)[1].replace("_", " ").title()
    return (slug, path.read_text(encoding="utf-8").strip())


def _header(cliente: dict, titulo: str) -> str:
    hoje = date.today().isoformat()
    nome = cliente.get("nome", "Cliente")
    nicho = cliente.get("nicho", "")
    cidade = cliente.get("cidade", "")
    return (
        f"# {titulo}\n\n"
        f"**Cliente:** {nome}  \n"
        f"**Nicho:** {nicho}  \n"
        f"**Cidade/região:** {cidade}  \n"
        f"**Data:** {hoje}  \n"
        f"**Preparado por:** Velask — Edison Velask, The 5th King of Sun ☀️⚔️\n\n"
        f"---\n"
    )


def _compose(output_dir: Path, cliente: dict, titulo: str, ids: list[str]) -> str:
    parts = [_header(cliente, titulo)]
    for block_id in ids:
        _, content = _read_block(output_dir, block_id)
        parts.append(content)
        parts.append("\n---\n")
    return "\n".join(parts).rstrip() + "\n"


def assemble(output_dir: Path) -> dict[str, Path]:
    meta_path = output_dir / "_meta.json"
    cliente = {}
    if meta_path.exists():
        cliente = json.loads(meta_path.read_text(encoding="utf-8")).get("cliente", {})

    proposta = _compose(
        output_dir,
        cliente,
        f"Proposta Velask 360 — {cliente.get('nome', 'Cliente')}",
        PROPOSTA_BLOCKS,
    )
    roteiro = _compose(
        output_dir,
        cliente,
        f"Roteiro de Call — {cliente.get('nome', 'Cliente')}",
        ROTEIRO_BLOCKS,
    )

    proposta_path = output_dir / "PROPOSTA.md"
    roteiro_path = output_dir / "ROTEIRO_CALL.md"
    proposta_path.write_text(proposta, encoding="utf-8")
    roteiro_path.write_text(roteiro, encoding="utf-8")
    return {"proposta": proposta_path, "roteiro": roteiro_path}
