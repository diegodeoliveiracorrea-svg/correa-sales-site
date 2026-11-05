# Padrão visual · Corrêa Sales (posts do Instagram e Facebook)

Este é o padrão oficial dos posts. Qualquer pessoa ou agente que for criar arte segue este arquivo.

## 1. Logo (regra que não muda)

- Use **somente** os arquivos oficiais. Nunca redesenhe, digite ou recrie a logo (nada de "CS" escrito em fonte).
  - `assets/logo-dark-bg.png`: para fundo **escuro** (letras claras).
  - `assets/logo-light-bg.png`: para fundo **claro** (letras marinho).
- Não distorça, não mude as cores da logo, não aplique sombra ou contorno.
- Posição nos cards: canto superior esquerdo, 228 px de largura (arte de 1080 x 1350). No card final, centralizada e grande (340 px).
- Variações permitidas: só as duas versões acima (fundo claro e fundo escuro). Uma versão nova da logo precisa ser aprovada antes e salva em `assets/`.

## 2. Cores

As cores podem mudar; a logo não. As paletas ficam em `marca/carrossel.py` (`PALETAS`).

| Paleta | Escuro | Claro | Dourado | Dourado em fundo claro |
|---|---|---|---|---|
| `padrao` (posts publicados) | #242833 | #F5EFE4 | #C8A472 | #8f6f42 |
| `site` | #102742 | #F6F2EB | #B08A57 | #8a6a3f |

Para usar outra cor: crie uma paleta nova com nome, mostre a prévia e só use depois de aprovada.

## 3. Fontes

- Títulos: **Cormorant Garamond** (regular), com a parte de destaque em *itálico dourado*.
- Textos, etiquetas, botões: **Montserrat**.
- Os arquivos estão em `marca/fontes/` (licença OFL, uso livre).

## 4. Estrutura do carrossel (1080 x 1350)

- Topo: logo à esquerda e numeração "01 / 08" à direita, em dourado.
- Etiqueta: fio dourado + texto em caixa alta espaçada (ex.: "—— QUANDO E COMO").
- Título grande em serifa, com destaque em itálico.
- Blocos: caixa com rótulo, caixa dourada (o ponto mais importante), tabela marinho com destaque dourado à direita, nota pequena.
- Rodapé: "@correasalesassessoria" à esquerda e "ARRASTE →" à direita.
- Card final: logo grande centralizada, título, botão "MANDA DIAGNÓSTICO NO DIRECT", site, frase de rodapé centralizada ("Salve e envie para...").
- Alterne fundo escuro e claro entre os cards.

## 5. Como gerar

```
python3 marca/carrossel.py roteiro.json pasta_de_saida/
```

O roteiro segue o formato descrito no topo de `carrossel.py`. Exemplo completo: `marca/exemplos/perdao_mei.json` (post de 05/11/2026).
O script avisa se algum texto passou do espaço. Depois de gerar, confira cada imagem antes de enviar para aprovação.

## 6. Regras de publicação

- Nada é publicado ou agendado sem aprovação do Diego ou da Tatiana.
- Imagens aprovadas vão para `assets/social/AAAA-MM/` para ter link público no Metricool.
- Informação legal ou de prazo só depois de conferida em fonte oficial.
