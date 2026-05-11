"""CLI da esteira VSK • PRE-CALL.

Uso:
    python scripts/run_pipeline.py inputs/meu_cliente.json
    python scripts/run_pipeline.py inputs/meu_cliente.json --model claude-opus-4-7
    python scripts/run_pipeline.py inputs/meu_cliente.json --only 01,02,03
    python scripts/run_pipeline.py inputs/meu_cliente.json --skip-assembly
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Permite rodar via "python scripts/run_pipeline.py" sem instalar o pacote.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from pipeline import assembly, runner  # noqa: E402


# Tabela de preço por 1M de tokens (USD). Fonte: docs Anthropic.
PRICING = {
    "claude-sonnet-4-6": {"in": 3.0, "out": 15.0, "cache_w": 3.75, "cache_r": 0.30},
    "claude-opus-4-7": {"in": 15.0, "out": 75.0, "cache_w": 18.75, "cache_r": 1.50},
    "claude-haiku-4-5-20251001": {"in": 1.0, "out": 5.0, "cache_w": 1.25, "cache_r": 0.10},
}


def estimate_cost(model: str, result: runner.PipelineResult) -> float | None:
    p = PRICING.get(model)
    if not p:
        return None
    return (
        result.total_input_tokens * p["in"]
        + result.total_output_tokens * p["out"]
        + result.total_cache_creation * p["cache_w"]
        + result.total_cache_read * p["cache_r"]
    ) / 1_000_000


def on_block(event: str, block, result):
    if event == "start":
        print(f"  → Bloco {block.id} ({block.nome})...", flush=True)
    elif event == "done":
        elapsed = result.elapsed_s
        cache_hit = result.cache_read_tokens
        print(
            f"  ✓ Bloco {block.id} concluído em {elapsed:.1f}s "
            f"(in={result.input_tokens}, out={result.output_tokens}, "
            f"cache_r={cache_hit})",
            flush=True,
        )


def main():
    parser = argparse.ArgumentParser(
        description="VSK • PRE-CALL — roda a esteira de proposta antes da call."
    )
    parser.add_argument("input", type=Path, help="Caminho do JSON do cliente")
    parser.add_argument(
        "--model",
        default=runner.DEFAULT_MODEL,
        help=f"Modelo Claude (padrão: {runner.DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "outputs",
        help="Diretório raiz de saída (padrão: outputs/)",
    )
    parser.add_argument(
        "--only",
        type=str,
        help="Rodar só blocos específicos. Ex: --only 01,02,03",
    )
    parser.add_argument(
        "--skip-assembly",
        action="store_true",
        help="Não montar PROPOSTA.md e ROTEIRO_CALL.md ao final",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"❌ Input não encontrado: {args.input}", file=sys.stderr)
        return 1

    cliente = runner.load_client(args.input)
    only = [s.strip() for s in args.only.split(",")] if args.only else None

    print(f"🔥 VSK • PRE-CALL — Cliente: {cliente['nome']}")
    print(f"   Modelo: {args.model}")
    print(f"   Blocos: {only or 'todos (01-18)'}")
    print()

    result = runner.run_pipeline(
        cliente=cliente,
        output_root=args.output_root,
        model=args.model,
        only=only,
        on_block=on_block,
    )

    print()
    print(f"📊 Resumo:")
    print(f"   Tempo total: {result.total_elapsed_s:.1f}s")
    print(f"   Tokens entrada: {result.total_input_tokens:,}")
    print(f"   Tokens saída:   {result.total_output_tokens:,}")
    print(f"   Cache write:    {result.total_cache_creation:,}")
    print(f"   Cache read:     {result.total_cache_read:,}")
    cost = estimate_cost(args.model, result)
    if cost is not None:
        print(f"   Custo estimado: US$ {cost:.3f}")
    print(f"   Saída em: {result.output_dir}/")

    if not args.skip_assembly and not only:
        print()
        print("📦 Montando documentos finais...")
        docs = assembly.assemble(result.output_dir)
        print(f"   ✓ {docs['proposta'].name}")
        print(f"   ✓ {docs['roteiro'].name}")

    print()
    print("☀️⚔️  Esteira concluída. Edison entra na call de dois pés.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
