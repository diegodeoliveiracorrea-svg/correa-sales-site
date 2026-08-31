# Handoff: Site Institucional — Corrêa Sales Assessoria Contábil

## Visão geral
Site institucional de 5 páginas para o escritório de contabilidade Corrêa Sales, focado em pequenas e médias empresas. Inclui home, sobre, serviços, blog (com conteúdo sobre a Reforma Tributária LC 214/2025) e contato.

## Sobre os arquivos deste pacote
Os arquivos deste bundle **já são HTML/CSS/JS estático pronto para publicação** — não é apenas mockup de design. Você pode subir a pasta inteira em qualquer hospedagem estática (Vercel, Netlify, Cloudflare Pages, GitHub Pages, Hostinger, etc.) e o site funciona.

Se for reimplementar em um framework (Next.js, Astro, WordPress, etc.), use estes arquivos como referência de fidelidade visual.

## Fidelidade
**High-fidelity (hifi)** — Cores finais, tipografia definida (Playfair Display + Inter), espaçamentos exatos, logo real do cliente, interações e responsividade prontas.

## Como publicar (3 caminhos)

### Opção A — Genspark Code (recomendado, mais rápido)
Continue nesta conversa migrando o pacote para o Genspark Code. Lá dá para fazer deploy online com um comando, receber URL pública com HTTPS e conectar domínio próprio (ex: `correasales.com.br`).

### Opção B — Vercel / Netlify / Cloudflare Pages (grátis, ~5 min)
1. Baixe a pasta `design_handoff_site_correa_sales/`
2. Crie conta em [vercel.com](https://vercel.com) ou [netlify.com](https://netlify.com)
3. Arraste a pasta na tela de "Deploy" — pronto, sai a URL pública
4. Para domínio próprio: aponte o DNS do registro.br para os servidores da plataforma

### Opção C — Hospedagem tradicional (Hostinger, Locaweb, etc.)
Suba todos os arquivos via FTP para a pasta `public_html/` do seu plano.

## Páginas incluídas

- **index.html** — Home com hero, stats, serviços, depoimentos, FAQ e CTA
- **sobre.html** — Página institucional
- **servicos.html** — Detalhamento de serviços contábeis
- **blog.html** — Blog com foco em Reforma Tributária (LC 214/2025) para PMEs, com 6 posts e fontes citadas (Planalto, Receita Federal, Sebrae, IBGE)
- **contato.html** — Formulário e informações de contato

## Design tokens

### Cores
- Navy (primária): `#0a1a2e` / `rgb(10, 26, 46)`
- Gold (accent): definido em `--gold` (assets/styles.css)
- Off-white (fundo): definido em `--off`
- Border: definido em `--border`

### Tipografia
- **Playfair Display** (serifada) — títulos hero, títulos de post, headers
- **Inter** (sans-serif) — corpo, navegação, UI

### Header
- Altura: `--header-h: 124px`
- Logo (variantes): 104px altura no desktop, 78px no mobile
- Sticky com blur backdrop

### Logo
- `assets/logo-light-bg.png` — versão navy+gold para fundos claros
- `assets/logo-dark-bg.png` — versão branca+gold para fundos escuros
- Swap automático via CSS entre header (claro) e footer/drawer (escuro)

## Componentes reutilizados
Todas as páginas compartilham:
- Header sticky com nav desktop + drawer mobile
- Footer com logo dark, links, dados de contato
- Sistema de logo com swap automático light/dark
- `assets/styles.css` — folha de estilos global
- `assets/script.js` — abertura/fechamento do drawer mobile

## Interações
- **Drawer mobile**: abre/fecha via botão hamburger em `assets/script.js`
- **Blog**: cards de post e timeline horizontal com 4 marcos (2026 / 2027 / 2029–2032 / 2033)
- **FAQ (home)**: expansível via `<details>` nativo do HTML

## Assets
- `assets/logo-correa-sales.png` — logo original em alta (1024px)
- `assets/logo-light-bg.png` — variante para uso em headers claros
- `assets/logo-dark-bg.png` — variante para uso em footers escuros
- `assets/styles.css` — folha de estilos global
- `assets/script.js` — comportamento do drawer mobile
- `assets/blog/` — 7 fotos editoriais (2K) usadas no blog:
  - `lc-214-2025.jpg` — post destaque (Reforma Tributária)
  - `simples-vs-regime.jpg` — Simples Nacional × regime regular
  - `cronograma-2026-2033.jpg` — transição ano a ano
  - `split-payment.jpg` — pagamento fatiado
  - `prestadores-servico.jpg` — impacto para serviços
  - `comercio-varejo.jpg` — varejo e cesta básica
  - `mei-reforma.jpg` — MEI na reforma

## Dados da empresa (já preenchidos)
- **CNPJ:** 34.198.102/0001-85
- **E-mail de contato:** diego@correasalesassessoria.com.br
- **Telefone/WhatsApp:** (21) 98439-5779
- **Endereço:** Av. Marechal Câmara, 160 — Sala 931, Centro, Rio de Janeiro — RJ


## Fontes externas usadas neste conteúdo
O blog cita fontes oficiais reais nos artigos sobre Reforma Tributária:
- Planalto (LC 214/2025, EC 132/2023, LC 123/2006)
- Ministério da Fazenda (portal Reforma Tributária)
- Receita Federal (Simples Nacional)
- Sebrae, IBGE, Gov.br Empreendedor, Senado
