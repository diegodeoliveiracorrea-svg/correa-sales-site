# Padrão visual · Corrêa Sales (posts do Instagram e Facebook)

Este é o padrão oficial dos posts. Qualquer pessoa ou agente que for criar arte segue este arquivo.

<!-- DIRETRIZES-INICIO -->
## 0. Diretrizes de conteúdo da semana (Líder de marketing, 28/11/2026)

Valem para posts, cards de compartilhar e Reels. Atualizadas toda segunda pela rotina "Líder de marketing".

- Público da semana: quem tem funcionário (13º, escala 5x2 em 16/12) e empresas do Simples e do Lucro Presumido se preparando para 2027. MEI no máximo 1 vez.
- O que rende: post prático com data e dia da semana, ou com a conta em reais, e uma ação clara para o dono ("o que fazer esta semana"). Disputa na Justiça e alíquota sem ação para o dono rendem pouco.
- Gancho: 1ª linha e capa falam com o dono na 2ª pessoa e citam o público ("Tem funcionário?", "Sua empresa no Simples"). Sem siglas na capa.
- Toda peça pede envio ou salvamento e tem o card de compartilhar com mensagem para o WhatsApp. O alcance cresce quando o post circula fora do Instagram.
- Busca e IA: o texto responde a pergunta do dono logo no começo (quem, o quê, até quando), com o nome da cidade quando fizer sentido. É o formato que o Google e as IAs citam.
- Horário: posts às 12h; Reels às 18h30.
- Reels da semana: 13º e escala 5x2 em dezembro. Gancho de 3 s: "Dezembro vai custar mais para quem tem funcionário." Cenas: as 2 datas do 13º; a hora mais cara a partir de 16/12; o que fazer esta semana.
- Teste da semana: comparar o alcance dos posts com e sem compartilhamento no status do WhatsApp pelos sócios.
- Evitar: superlativos, promessas, preços e comparação com outros escritórios (NBC PG 01).
<!-- DIRETRIZES-FIM -->

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

## 5a. Reels narrados (1080 x 1920, até 30 s)

```
python3 marca/reels.py roteiro.json --texto                 # texto para a voz no ElevenLabs
python3 marca/reels.py roteiro.json saida/ --audio voz.mp3  # vídeo final
```

- Mesmo padrão dos carrosséis: logo oficial, Cormorant Garamond com destaque em itálico dourado, Montserrat, paleta `padrao`, fundo escuro e claro alternados, card final com "MANDA DIAGNÓSTICO NO DIRECT".
- Voz: ElevenLabs, "Paulo Rovéglia - Jovem Carioca" (voice_id cYJOoH13XCtPQ5VT5HAE), modelo eleven_v4, 1 versão por vídeo.
- O script acha as pausas da narração e troca de cena nelas. Exemplo: `marca/roteiros/escala_5x2_reels.json`.
- A narração (MP3) chega pela pasta do Google Drive "Reels · narração (Corrêa Sales)", com o nome `<nome do roteiro>.mp3`.

## 6. Regras de publicação

- Nada é publicado ou agendado sem aprovação do Diego ou da Tatiana.
- Imagens aprovadas vão para `assets/social/AAAA-MM/` para ter link público no Metricool.
- Informação legal ou de prazo só depois de conferida em fonte oficial.
