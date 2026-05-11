---
id: "01"
slug: "pesquisa_nicho"
nome: "Pesquisa do Nicho"
responsavel: "Operador de IA / Pesquisador"
itens: "011-020"
---
# Bloco 01 — Pesquisa do Nicho

## Cliente em foco
- Nome: {{ cliente.nome }}
- Nicho: {{ cliente.nicho }}
- Cidade/região: {{ cliente.cidade }}
- Produto/serviço: {{ cliente.produto }}
- Ticket médio: {{ cliente.ticket_medio or "não informado" }}
- Objetivo declarado: {{ cliente.objetivo or "não informado" }}

## Tarefa
Pesquise e descreva o nicho **{{ cliente.nicho }}** com foco em ação comercial para Edison usar na call. Gere os 10 itens abaixo, todos eles, no formato `### NNN — Título`. Sem omissão.

- 011 — Resumo prático do nicho (3-5 linhas: o que esse mercado é hoje, em {{ cliente.cidade }} se relevante)
- 012 — Como esse nicho vende (canais, mecanismos, ciclo médio de venda)
- 013 — Principais dores do público (3-5 dores reais e específicas)
- 014 — Principais desejos do público (3-5 desejos concretos)
- 015 — Tipos de oferta mais comuns (lista)
- 016 — Tipos de conteúdo mais usados (lista)
- 017 — O que costuma gerar confiança (3-5 elementos)
- 018 — O que costuma gerar desejo (3-5 elementos)
- 019 — O que costuma gerar lead (3-5 mecanismos)
- 020 — O que a Velask pode fazer nesse nicho (lista de entregas concretas que viram receita)
