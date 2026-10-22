# Como publicar o site — Corrêa Sales (via GitHub Desktop)

O site é estático: HTML, CSS e imagens. O GitHub Desktop serve para versionar e enviar os arquivos; quem coloca o site no ar é o **GitHub Pages**, que é gratuito.

Fluxo: **GitHub Desktop → repositório no GitHub → GitHub Pages publica → (opcional) domínio próprio**.

---

## Antes de começar: o que não deve subir

O arquivo `.gitignore` já está configurado para deixar de fora:

- `design_handoff_site_correa_sales/` — versão antiga de trabalho
- `*.srcmap.json` — mapas internos do editor
- `screenshots/` — capturas de tela
- `.thumbnail.jpg`

Não é necessário fazer nada: ao criar o repositório, esses arquivos ficam automaticamente ignorados.

---

## Passo 1 — Criar o repositório no GitHub Desktop

1. Abra o **GitHub Desktop** e faça login na sua conta.
2. Menu **File → Add local repository…**
3. Selecione a pasta onde está este site (a que contém o `index.html`).
4. Se aparecer o aviso *"this directory does not appear to be a Git repository"*, clique em **create a repository**.
5. Confirme:
   - **Name:** `site-correa-sales`
   - **Description:** Site institucional da Corrêa Sales Assessoria Contábil
   - **Local path:** a pasta do site
   - Deixe marcado **Initialize this repository with a README** apenas se não houver README — se marcar, o GitHub Desktop pode pedir para substituir arquivos. O mais seguro é deixar desmarcado.
6. Clique em **Create repository**.

---

## Passo 2 — Fazer o primeiro commit

1. Na aba **Changes**, você verá todos os arquivos novos.
2. Confirme que a lista **não** inclui `design_handoff_site_correa_sales`, `screenshots` nem os `.srcmap.json`. Se aparecerem, o `.gitignore` não foi reconhecido — avise que eu ajusto.
3. No campo **Summary** (canto inferior esquerdo), escreva:
   `Site Corrêa Sales — versão inicial`
4. Clique em **Commit to main**.

---

## Passo 3 — Enviar para o GitHub

1. Clique em **Publish repository** (canto superior direito).
2. Marque **Keep this code private**? — **deixe desmarcado**. O GitHub Pages só publica repositórios públicos no plano gratuito.
3. Clique em **Publish repository**.

Pronto: o código está no GitHub.

---

## Passo 4 — Ativar o GitHub Pages

1. Abra o repositório no navegador (o GitHub Desktop tem o botão **Repository → View on GitHub**).
2. Vá em **Settings** (engrenagem no topo do repositório).
3. No menu lateral, clique em **Pages**.
4. Em **Source**, selecione **Deploy from a branch**.
5. Em **Branch**, escolha **main** e a pasta **/ (root)**. Clique em **Save**.
6. Aguarde de 1 a 3 minutos e recarregue a página. Aparecerá o endereço:

   ```
   https://SEU-USUARIO.github.io/site-correa-sales/
   ```

O site já está no ar nesse endereço, com HTTPS.

> O arquivo `.nojekyll` já está incluído. Ele impede que o GitHub tente processar o site com Jekyll e é o que garante que a pasta `assets` funcione corretamente.

---

## Passo 5 — Testar no endereço publicado

Abra no computador e no celular:

- [ ] As 5 páginas abrem pelo menu
- [ ] Fotos aparecem (Home, Sobre)
- [ ] O telefone do rodapé disca ao clicar
- [ ] O botão verde do WhatsApp abre a conversa com a mensagem pronta
- [ ] "Consultoria gratuita" leva à agenda
- [ ] **Abrir a agenda** abre a página do Zoho
- [ ] O QR code é lido pela câmera do celular
- [ ] O formulário abre o WhatsApp com os dados preenchidos
- [ ] O cadeado (HTTPS) aparece na barra de endereço

---

## Passo 6 (recomendado) — Colocar o domínio próprio

Endereço `usuario.github.io/site-correa-sales` funciona, mas passa menos credibilidade. Com o domínio `correasalesassessoria.com.br`, o endereço fica profissional.

**No GitHub:**

1. **Settings → Pages → Custom domain**: digite `correasalesassessoria.com.br` e salve.
2. O GitHub vai sugerir criar um arquivo `CNAME`. Aceite — ele aparece no repositório e você precisa fazer um novo commit no GitHub Desktop.
3. Marque **Enforce HTTPS** (pode levar alguns minutos para liberar).

**No Registro.br (onde o domínio está registrado):**

4. Entre em *Meus domínios → correasalesassessoria.com.br → Editar zona DNS*.
5. Crie ou edite os registros do site:

   | Tipo | Nome | Valor |
   |---|---|---|
   | A | `@` (vazio) | `185.199.108.153` |
   | A | `@` (vazio) | `185.199.109.153` |
   | A | `@` (vazio) | `185.199.110.153` |
   | A | `@` (vazio) | `185.199.111.153` |
   | CNAME | `www` | `SEU-USUARIO.github.io` |

6. **Não mexa nos registros MX.** Eles são o que mantém o e-mail `diego@correasalesassessoria.com.br` funcionando no Zoho. Se apagar os MX, o e-mail para de receber.

A propagação do DNS leva de 1 a 24 horas.

---

## Passo 7 (recomendado) — Ajustar os endereços no código

As páginas têm tags `canonical` e o `sitemap.xml` apontando para `https://correasalesassessoria.com.br/`. Isso está correto **se você usar o domínio próprio**.

Se for publicar apenas no endereço do GitHub Pages, esses endereços precisam ser trocados — me avise qual será o endereço final e eu ajusto.

---

## Depois de publicar

**Google Search Console** — em search.google.com/search-console, adicione a propriedade do domínio, verifique e envie o `sitemap.xml`. É o que faz o Google indexar as páginas.

**Google Business Profile** — crie o perfil da Corrêa Sales. Como o atendimento é online, escolha a opção "empresa que atende clientes no local deles".

---

## Como atualizar o site depois

O ciclo é sempre o mesmo, e é rápido:

1. Altere os arquivos (aqui no editor de design ou direto na pasta).
2. Abra o **GitHub Desktop** — ele mostra o que mudou na aba **Changes**.
3. Escreva um resumo no campo **Summary** (ex.: "Atualiza telefone").
4. Clique em **Commit to main** e depois em **Push origin**.
5. Em 1 ou 2 minutos o site publicado se atualiza sozinho.

Se o botão **Push origin** não aparecer, clique em **Fetch origin** primeiro.

---

## Situação atual do site

| Item | Situação |
|---|---|
| Telefone / WhatsApp (21) 98466-0882 | ✅ todas as páginas |
| Fotos do time e do ambiente | ✅ |
| Agenda de consultoria (Zoho Calendar) | ✅ link + QR |
| Formulário de mensagem | ✅ envia pelo WhatsApp |
| Endereço físico | ✅ removido |
| Política de privacidade | ✅ |
| Favicon, sitemap, robots | ✅ |
| Logo da Corrêa no Zoho | ⏳ upload no painel do Zoho |
| Buffer da agenda | ⏳ trocar de 45 para 15 min |
| Renovar a agenda do Zoho | ⏳ até 21/04/2027 |
