---
id: "02"
slug: "pesquisa_concorrentes"
nome: "Pesquisa dos Concorrentes"
responsavel: "Operador de IA / Pesquisador / Prospector"
itens: "021-030"
---
# Bloco 02 — Pesquisa dos Concorrentes

## Concorrentes informados pelo cliente
{% if cliente.concorrentes %}
{% for c in cliente.concorrentes %}- {{ c }}
{% endfor %}
{% else %}
Nenhum concorrente foi enviado. Sugira concorrentes plausíveis com base no nicho **{{ cliente.nicho }}** em **{{ cliente.cidade }}** e marque com `[SUPOSIÇÃO: ...]`.
{% endif %}

## Contexto já levantado
Use a pesquisa do nicho do Bloco 01 (no histórico) para enquadrar a análise.

## Tarefa
Monte o dossiê de concorrência que Edison vai citar de cabeça na call. Para cada concorrente, identifique se é **direto** (mesmo produto/região) ou **indireto** (mesmo público, oferta diferente). Gere os 10 itens abaixo, todos no formato `### NNN — Título`.

- 021 — Lista de concorrentes diretos (com 1 linha de descrição cada)
- 022 — Lista de concorrentes indiretos (com 1 linha de descrição cada)
- 023 — O que os concorrentes postam (padrões de feed, frequência, formato dominante)
- 024 — Quais ofertas aparecem (com preço/promessa quando der pra inferir)
- 025 — Quais CTAs usam (lista dos verbos e canais que aparecem)
- 026 — Como usam Reels (formato, duração, tipo de hook)
- 027 — Como usam Stories (sequência, frequência, mecânicas)
- 028 — Como usam link da bio (ferramenta, estrutura, destino)
- 029 — Pontos fortes dos concorrentes (3-5 itens objetivos)
- 030 — Brechas que a Velask pode ocupar (3-5 brechas práticas — onde o cliente {{ cliente.nome }} pode vencer)
