---
id: "03"
slug: "diagnostico_cliente"
nome: "Diagnóstico do Cliente"
responsavel: "Estrategista / Operador de IA"
itens: "031-040"
---
# Bloco 03 — Diagnóstico do Cliente

## Cliente
- Nome: {{ cliente.nome }}
- Instagram: {{ cliente.instagram or "não informado" }}
- Site: {{ cliente.site or "não informado" }}
- Produto/serviço: {{ cliente.produto }}

## Materiais disponíveis
{% if cliente.prints %}
{% for p in cliente.prints %}- {{ p }}
{% endfor %}
{% else %}
Sem prints enviados — trabalhe com hipóteses razoáveis e marque com `[SUPOSIÇÃO: ...]`.
{% endif %}

## Tarefa
Olhe o cliente como auditor e transforme cada problema em uma entrega vendável. O diagnóstico precisa apontar o que está fraco, em uma linha, e o que a Velask fará para resolver, em outra linha. Gere os 10 itens abaixo, todos no formato `### NNN — Título`. Para cada item use a estrutura:

```
**Hoje:** ...
**Problema:** ...
**Velask resolve com:** ...
```

- 031 — Diagnóstico do Instagram atual (visão geral do perfil)
- 032 — Diagnóstico da bio
- 033 — Diagnóstico do link da bio
- 034 — Diagnóstico dos destaques
- 035 — Diagnóstico dos posts (feed)
- 036 — Diagnóstico dos Reels
- 037 — Diagnóstico da oferta (clareza, irresistibilidade, preço)
- 038 — Diagnóstico do atendimento (WhatsApp / direct)
- 039 — Diagnóstico da clareza comercial (o cliente final entende o que comprar e como?)
- 040 — Lista de problemas que a Velask resolve (síntese: 5-10 bullets curtos prontos pra citar na call)
