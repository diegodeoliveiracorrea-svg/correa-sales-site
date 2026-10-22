# Corrêa Sales — Site institucional

Documentação de tudo que foi feito, para retomar o trabalho no futuro sem precisar lembrar de nada.

**Última atualização:** outubro de 2026

---

## 1. O que é este projeto

Site institucional de 5 páginas + política de privacidade para a **Corrêa Sales Assessoria Contábil**, escritório de contabilidade em Rio de Janeiro que atende PMEs em todo o Brasil com atendimento 100% online.

O site é **estático** (HTML, CSS e imagens). Não tem banco de dados, não tem servidor próprio e não precisa de programação para rodar.

---

## 2. Onde está publicado

| Item | Valor |
|---|---|
| **Endereço oficial** | https://www.correasalesassessoria.com.br |
| **Sem o www** | redireciona automaticamente para a versão com www |
| **Hospedagem** | Vercel (deploy automático a cada `git push`) |
| **Domínio** | Registro.br |
| **E-mail** | Zoho Mail — `diego@correasalesassessoria.com.br` |
| **Código** | GitHub, repositório `correa-sales-site` |

> ⚠️ **Nunca altere os registros MX do domínio no Registro.br.** São eles que mantêm o e-mail funcionando no Zoho. Ao mexer no DNS, altere apenas os registros A e CNAME.

---

## 3. Estrutura de arquivos

```
index.html                      Home
sobre.html                      História, missão e equipe
servicos.html                   Serviços detalhados
blog.html                       Artigos (7 posts sobre Reforma Tributária)
contato.html                    Agenda de consultoria + formulário + dados
politica-de-privacidade.html    Documento legal (LGPD)
robots.txt                      Instruções para o Google
sitemap.xml                     Mapa do site para o Google
.nojekyll                       Necessário para o GitHub Pages / estático
.gitignore                      Arquivos que não vão para o repositório

assets/
  styles.css                    Estilo global do site
  agenda.css                    Estilo exclusivo da seção de agenda
  script.js                     Menu mobile, acordeão do FAQ, formulário
  logo-light-bg.png             Logo para fundo claro (usada no site)
  logo-dark-bg.png              Logo para fundo escuro (usada no rodapé)
  logo-correa-sales.png         Logo master (alta resolução)
  favicon.png                   Ícone da aba do navegador (monograma CS)
  hero-reuniao.jpg              Foto principal da Home (reunião consultiva)
  escritorio.jpg                Ambiente de trabalho (página Sobre)
  diego-correa.jpg              Retrato do Diego
  tatiana-sales.jpg             Retrato da Tatiana
  agenda-qr.png                 QR code da agenda de consultoria
  blog/                         7 imagens dos artigos

publicar/                       Cópia limpa pronta para subir (ZIP)
design_handoff_site_correa_sales/   Versão antiga — NÃO publicar
```

---

## 4. Identidade visual

Definida em `assets/styles.css`, no bloco `:root` no topo do arquivo.

| Token | Valor | Uso |
|---|---|---|
| `--navy` | `#102742` | Azul principal, títulos, rodapé |
| `--navy-2` | `#1a3a5f` | Azul secundário |
| `--gold` | `#B08A57` | Dourado, botões, destaques |
| `--gold-2` | `#c9a273` | Dourado claro |
| `--gold-3` | `#8f6f42` | Dourado escuro (texto sobre claro) |
| `--off` | `#F6F2EB` | Fundo bege das seções alternadas |
| `--graphite` | `#4A4F57` | Texto corrido |
| `--white` | `#ffffff` | Fundo dos cards |

**Tipografia** (Google Fonts):
- `Instrument Serif` — títulos (elegante, com itálico para destaque)
- `Inter` — texto corrido e interface
- `JetBrains Mono` — etiquetas pequenas em maiúsculas

**Padrões de layout:**
- Seções alternam entre fundo branco e bege (`--off`)
- Títulos de seção começam com uma etiqueta (`.eyebrow`) em mono dourado
- Cards com borda fina e sombra suave; hover troca a borda para dourado
- Botões: preenchido (dourado) e contorno (borda navy)

---

## 5. Dados de contato (para atualizar)

Se algum destes mudar, busque e substitua em **todos** os arquivos HTML:

| Dado | Valor atual |
|---|---|
| Telefone | (21) 98466-0882 |
| Link do telefone | `tel:+5521984660882` |
| WhatsApp | `wa.me/5521984660882` |
| E-mail | diego@correasalesassessoria.com.br |
| Instagram | @correasalesassessoria |
| CNPJ | 34.198.102/0001-85 |
| Atendimento | Online em todo o Brasil · Rio de Janeiro — RJ |
| Horário | Seg. a sex., 9h às 18h |
| Endereço físico | **Não existe** (removido em out/2026) |

**Mensagem automática do WhatsApp:**
> Olá! Vim pelo site e gostaria de falar com um contador.

---

## 6. Agenda de consultoria (Zoho Calendar)

A seção de agenda fica em `contato.html`, âncora `#agendar`.

**Como funciona:** o site **não** incorpora o calendário. O botão "Abrir a agenda" leva à página de agendamento do Zoho Calendar, que abre em nova aba. Há também um QR code para quem vem pelo celular.

**Por que não é incorporado:** o Zoho envia o cabeçalho `x-frame-options: SAMEORIGIN`, que proíbe tecnicamente exibir a página dentro de um quadro. Testado e confirmado — dentro do site o quadro fica em branco.

**Link da agenda (já configurado no HTML):**
```
https://calendar.zoho.com/zc/view/slot-booking/0801123c342b0e0d87d7045cadc52f640000963e7820bdcc9b8501696d8dd90de0e369d91d941cbf8edcfac0abbb4a7bf6443433f2ef96f0f1058032d90a5fae
```

**Configuração atual no Zoho:**
- Título: Consultoria gratuita — Corrêa Sales
- Duração: 45 minutos
- Tipo: Online — Zoho Video Meeting
- Visibilidade: Público
- Verifica disponibilidade: agenda do Diego
- Máximo: 5 agendamentos por dia
- Buffer: 45 minutos ⚠️ *(recomendado baixar para 15)*
- Validade: 21/10/2026 a **21/04/2027** ⚠️ *(renovar antes de abril/2027)*

**Pendências:**
1. Trocar o logo do Zoho pela logo da Corrêa (painel do Zoho → Identidade visual → Adicionar imagem → `logo-light-bg.png`)
2. Reduzir o buffer de 45 para 15 minutos
3. Renovar a página de agendamento antes de 21/04/2027

---

## 7. Contagem de acessos (analytics)

**Status:** ativado em outubro/2026. Script `/_vercel/insights/script.js` incluído no final das 6 páginas.

**Como ver os números:**
1. Entre em https://vercel.com/dashboard
2. Selecione o projeto da Corrêa Sales
3. Clique em **Analytics** no menu da esquerda

**O que você vê:** visitantes, visualizações de página, páginas mais acessadas, país, tipo de dispositivo (celular/computador) e origem do acesso (Google, Instagram, direto).

**Plano gratuito:** 50.000 eventos por mês — muito acima do que um site institucional consome. Se passar do limite, a coleta pausa sozinha; não há cobrança.

**Privacidade:** não usa cookies, não identifica pessoas, dados agregados. Já informado na política de privacidade.

**Para o script funcionar,** o Analytics precisa estar habilitado no painel da Vercel: *projeto → Analytics → Enable*. O script já está no HTML; falta apenas o botão no painel.

**Alternativa gratuita sem painel:** [GoatCounter](https://www.goatcounter.com) — basta criar uma conta e colar uma linha de script.

---

## 8. Formulário de contato

**Como funciona:** ao enviar, o site abre o WhatsApp do escritório com a mensagem já preenchida (nome, empresa, e-mail, telefone, serviço e texto). O cliente só toca em enviar.

**Por que assim:** o site é estático, não tem servidor para processar e-mail. Essa é a forma de a mensagem chegar de verdade sem serviço externo.

**Se quiser envio automático por e-mail no futuro:** será preciso contratar Formspree, EmailJS ou equivalente, e trocar o bloco do formulário em `assets/script.js`.

**Validação:** nome, e-mail (formato), telefone (mínimo 10 dígitos) e mensagem são obrigatórios. Campo faltando mostra aviso em vermelho e não abre nada.

---

## 9. SEO

- `sitemap.xml` com as 6 páginas — enviar no Google Search Console
- `robots.txt` liberando indexação e apontando o sitemap
- Tags `canonical` em todas as páginas, com o domínio www
- Open Graph e Twitter Card (título, descrição e imagem de compartilhamento)
- Favicon e Apple Touch Icon

**Recomendado:** criar o **Google Business Profile** (Google Meu Negócio). Como o atendimento é online, escolher "empresa que atende clientes no local deles".

---

## 10. Como atualizar o site

### Fluxo normal (recomendado)

1. Altere os arquivos nesta pasta do projeto
2. Abra o **GitHub Desktop**
3. A aba **Changes** mostra o que mudou
4. Escreva um resumo no campo **Summary**
5. **Commit to main** → **Push origin**
6. A Vercel publica sozinha em 1–2 minutos

### Atualização de emergência (sem Git)

Baixe a pasta `publicar/` (ZIP), extraia, e no Vercel Dashboard:
*Project → Deployments → ⋯ → Redeploy*. Ou substitua os arquivos no repositório pelo GitHub Desktop.

---

## 11. Histórico do que foi feito

| Data | Alteração |
|---|---|
| out/2026 | Telefone trocado de (21) 98439-5779 para (21) 98466-0882 em todas as páginas |
| out/2026 | Mensagem automática do WhatsApp adicionada |
| out/2026 | Foto da Home gerada (reunião consultiva, com Pão de Açúcar ao fundo) |
| out/2026 | Fotos reais do Diego e da Tatiana inseridas na página Sobre |
| out/2026 | Imagem do ambiente de trabalho gerada (sem escritório físico) |
| out/2026 | Endereço fictício (Av. Marechal Câmara) removido → atendimento online |
| out/2026 | Agenda de agendamento integrada (Zoho Calendar, link + QR code) |
| out/2026 | Textos ajustados: consultoria por videochamada no Zoho Meeting |
| out/2026 | Formulário passou a enviar pelo WhatsApp (antes era simulação) |
| out/2026 | Política de privacidade criada (LGPD) |
| out/2026 | Depoimentos com iniciais no lugar de fotos fictícias |
| out/2026 | Faixa de logos falsos removida |
| out/2026 | Favicon, sitemap, robots e Open Graph adicionados |
| out/2026 | Contagem de acessos (Vercel Analytics) ativada |

---

## 12. Pendências conhecidas

| Prioridade | Item |
|---|---|
| Alta | Fazer commit e push dos arquivos atualizados (site no ar ainda mostra a versão antiga) |
| Alta | Habilitar Analytics no painel da Vercel (script já está no HTML) |
| Média | Trocar logo do Zoho pela logo da Corrêa |
| Média | Buffer da agenda: 45 → 15 minutos |
| Baixa | Renovar a página de agendamento antes de 21/04/2027 |
| Baixa | Logos de clientes reais para a Home (se houver) |
| Baixa | Considerar Google Business Profile |

---

## 13. O que NÃO publicar

Estas pastas/arquivos são material de trabalho e já estão no `.gitignore`:

- `design_handoff_site_correa_sales/` — versão antiga, com nomes e endereço errados
- `*.srcmap.json` — mapas internos do editor de design
- `screenshots/` — capturas de tela
- `.thumbnail.jpg`

---

## 14. Glossário rápido

- **Vercel** — serviço que hospeda o site. Publica sozinho a cada alteração enviada ao GitHub.
- **GitHub Desktop** — programa que envia os arquivos do computador para o GitHub.
- **GitHub Pages** — alternativa gratuita de hospedagem, usada se não houver Vercel.
- **Zoho Calendar** — onde ficam os horários de consultoria.
- **Zoho Meeting** — sala de videochamada das consultorias.
- **DNS / MX** — configurações do domínio. MX é o do e-mail; mexer nele derruba o e-mail.
- **Canonical** — tag que diz ao Google qual é o endereço oficial da página.
