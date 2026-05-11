# 🔥 VSK • PRE-CALL — Esteira de Proposta antes da Call

> A Velask não entrega só conteúdo. Organiza, produz, publica, automatiza e
> acompanha a operação digital do negócio. Esta esteira faz Edison chegar na
> call com diagnóstico, oportunidades e proposta já prontos.

## Ideia

Cliente manda:

- nicho
- Instagram
- site
- concorrentes
- cidade/região
- produto/serviço
- prints (se tiver)

A esteira roda 18 blocos em sequência usando a Claude API e devolve um
pacote completo: pesquisa de nicho, análise dos concorrentes, diagnóstico,
oportunidades, proposta Velask 360, escopo de execução, pacote criativo,
funil, tráfego, gestão, automações, pacotes e roteiro de call.

Você entra na reunião não como prestador perguntando o que o cliente quer.
Você entra como solução com plano pronto na mão.

## Fluxo geral

```
00 — Input do cliente
01 — Pesquisa do nicho
02 — Pesquisa dos concorrentes
03 — Diagnóstico do cliente
04 — Oportunidades práticas
05 — Proposta Velask 360
06 — Escopo de execução
07 — Social media / conteúdo
08 — Criativos / vídeos / DR
09 — Copy / funil / oferta
10 — Landing page / link / site
11 — WhatsApp / direct / atendimento
12 — Tráfego pago
13 — Trello / gestão de projeto
14 — Automações / IA / processos
15 — Dashboard / controle
16 — Pacotes e preço
17 — Material da call
18 — Envio e follow-up
```

## Estrutura

```
.
├── inputs/                       # JSON de input por cliente
│   └── cliente_exemplo.json
├── pipeline/
│   ├── system.md                 # System prompt Velask (cacheado)
│   ├── blocks/                   # 01..18 templates de prompt
│   ├── runner.py                 # Orquestrador Anthropic SDK
│   └── assembly.py               # Monta a proposta final
├── scripts/
│   └── run_pipeline.py           # CLI
└── outputs/{cliente}/            # Markdown gerado por bloco + proposta final
```

## Como rodar

```bash
# 1. instalar dependências
pip install -e .

# 2. configurar API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. preencher o JSON do cliente
cp inputs/cliente_exemplo.json inputs/meu_cliente.json
# editar com os dados do cliente

# 4. rodar a esteira
python scripts/run_pipeline.py inputs/meu_cliente.json
```

A saída fica em `outputs/{slug_do_cliente}/`:

- `01_pesquisa_nicho.md` … `18_envio_followup.md` — saídas por bloco
- `PROPOSTA.md` — proposta final montada
- `ROTEIRO_CALL.md` — roteiro consolidado da call
- `_meta.json` — input + métricas de execução (tokens, custo, tempo)

## Modelo e custo

Padrão: `claude-sonnet-4-6`. Prompt caching ativado no system prompt + brief
acumulado do cliente. Custo estimado por cliente: ~US$ 0.50–1.50 a depender
do tamanho dos prints/concorrentes.

Para análises mais profundas (clientes ticket alto), troque para
`claude-opus-4-7` via flag `--model`.

## Frase central

> Eu analisei seu mercado.
> Olhei seus concorrentes.
> Mapeei suas oportunidades.
> E trouxe um plano prático do que a gente pode executar pela sua empresa.

Essa é a diferença entre vender serviço e vender controle operacional do
crescimento. ☀️⚔️
