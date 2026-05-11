# Schema do input do cliente

Arquivo JSON por cliente, colocado em `inputs/`. Campos:

| Campo          | Tipo       | Obrigatório | Descrição                                                       |
| -------------- | ---------- | ----------- | --------------------------------------------------------------- |
| `nome`         | string     | sim         | Nome do cliente / marca                                         |
| `nicho`        | string     | sim         | Nicho/segmento de atuação                                       |
| `produto`      | string     | sim         | Produto ou serviço principal                                    |
| `instagram`    | string     | não         | @ do Instagram                                                  |
| `site`         | string     | não         | URL do site                                                     |
| `cidade`       | string     | não         | Cidade/região onde o cliente atua                               |
| `ticket_medio` | string     | não         | Faixa de ticket médio (texto livre, ex: "R$ 350 por encomenda") |
| `concorrentes` | string[]   | não         | Lista de concorrentes (@ do Instagram, site, ou nome)           |
| `prints`       | string[]   | não         | Observações textuais de prints/materiais enviados pelo cliente  |
| `objetivo`     | string     | não         | Objetivo declarado pelo cliente                                 |

## Como usar

1. Copie `cliente_exemplo.json` para um arquivo novo com o nome do cliente.
2. Preencha tudo que tiver. Quanto mais campo preenchido, melhor a saída.
3. Em vez de mandar imagens, descreva o que apareceu nos prints em uma lista de strings em `prints`.

## Como o input é usado

- Bloco 01–02 usam `nicho`, `cidade`, `concorrentes`.
- Bloco 03 (diagnóstico) usa `instagram`, `site`, `prints`.
- Bloco 04+ usa tudo, mais a saída dos blocos anteriores.
- Bloco 16 (preço) usa `ticket_medio` para calibrar pacotes.
