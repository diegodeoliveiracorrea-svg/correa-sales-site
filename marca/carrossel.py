"""Gerador de carrosséis do Instagram no padrão Corrêa Sales.

Uso:  python3 marca/carrossel.py roteiro.json pasta_saida/
Gera <nome>_1.jpg ... <nome>_N.jpg (1080x1350).

A logo SEMPRE vem dos arquivos oficiais em assets/ (nunca redesenhe a logo).
As cores ficam em PALETAS: para mudar as cores, crie uma paleta nova ou passe
"paleta": "nome" no roteiro. A logo não muda com a paleta.

Formato do roteiro (JSON):
{
  "nome": "perdao_mei",
  "paleta": "padrao",
  "rodape_final": "Salve e envie para quem tem MEI",
  "cards": [
    {"tipo": "capa", "fundo": "escuro", "tag": "...", "titulo": "Texto <em>destaque</em>", "texto": "..."},
    {"tipo": "conteudo", "fundo": "claro", "tag": "...", "titulo": "...",
     "blocos": [
        {"caixa": "Rótulo", "texto": "... <b>negrito</b> ..."},
        {"caixa_dourada": "Rótulo", "texto": "..."},
        {"tabela": [["Esquerda", "Direita em destaque"], ["...", "..."]]},
        {"nota": "texto pequeno"},
        {"grade": {"colunas": ["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"], "linhas": [["Semana 1","F","F","T","T","T","T","T"]], "legenda": "opcional"}}
     ]},
    {"tipo": "cta", "titulo": "...", "texto": "...", "botao": "MANDA DIAGNÓSTICO NO DIRECT", "alerta": "opcional"}
  ]
}
"""
import json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
LOGO_FUNDO_ESCURO = os.path.join(RAIZ, "assets", "logo-dark-bg.png")   # texto claro
LOGO_FUNDO_CLARO = os.path.join(RAIZ, "assets", "logo-light-bg.png")   # texto marinho

PALETAS = {
    # padrão dos posts publicados (Instagram/Facebook)
    "padrao": {"escuro": "#242833", "claro": "#F5EFE4", "dourado": "#C8A472", "dourado_claro_bg": "#8f6f42"},
    # tons do site
    "site": {"escuro": "#102742", "claro": "#F6F2EB", "dourado": "#B08A57", "dourado_claro_bg": "#8a6a3f"},
}


def css(p):
    f = os.path.join(AQUI, "fontes")
    return f"""
@font-face{{font-family:CG;src:url(file://{f}/CormorantGaramond.ttf);font-weight:300 700}}
@font-face{{font-family:CG;src:url(file://{f}/CormorantGaramond-Italic.ttf);font-style:italic;font-weight:300 700}}
@font-face{{font-family:MS;src:url(file://{f}/Montserrat.ttf);font-weight:100 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;font-family:MS}}
.card{{width:1080px;height:1350px;position:relative;padding:0 96px}}
.dark{{background:{p['escuro']};color:{p['claro']}}} .light{{background:{p['claro']};color:{p['escuro']}}}
.logo{{position:absolute;left:96px;top:80px;width:228px}}
.pg{{position:absolute;right:96px;top:116px;font-weight:600;font-size:22px;letter-spacing:4px;color:{p['dourado']}}}
.light .pg{{color:{p['dourado_claro_bg']}}}
.body{{position:absolute;left:96px;right:96px;top:230px;bottom:150px;display:flex;flex-direction:column;justify-content:center}}
.tag{{display:flex;align-items:center;gap:22px;font-weight:600;font-size:25px;letter-spacing:6px;text-transform:uppercase;color:{p['dourado']};margin-bottom:34px}}
.tag:before{{content:"";width:62px;height:2px;background:{p['dourado']};flex:none}}
.light .tag{{color:{p['dourado_claro_bg']}}} .light .tag:before{{background:{p['dourado_claro_bg']}}}
h1{{font-family:CG;font-weight:500;font-size:88px;line-height:1.08;letter-spacing:-.5px}}
h1 em{{font-style:italic;color:{p['dourado']}}} .light h1 em{{color:{p['dourado_claro_bg']}}}
.lead{{font-size:30px;line-height:1.55;margin-top:34px;opacity:.88}}
.box{{margin-top:30px;border:1.5px solid rgba(0,0,0,.14);border-radius:16px;padding:26px 30px;background:rgba(255,255,255,.35)}}
.dark .box{{border-color:rgba(255,255,255,.18);background:rgba(255,255,255,.03)}}
.lbl{{font-weight:600;font-size:19px;letter-spacing:4px;text-transform:uppercase;color:{p['dourado_claro_bg']};margin-bottom:10px}}
.dark .lbl{{color:{p['dourado']}}}
.bt{{font-size:28px;line-height:1.5}} .bt b{{font-weight:700}}
.gold{{background:{p['dourado']}!important;border-color:{p['dourado']}!important;color:{p['escuro']}}}
.gold .lbl{{color:{p['escuro']};opacity:.75}}
.tbl{{margin-top:30px;background:{p['escuro']};color:{p['claro']};border-radius:16px;padding:10px 30px}}
.dark .tbl{{background:rgba(255,255,255,.05);border:1.5px solid rgba(255,255,255,.18)}}
.row{{display:flex;justify-content:space-between;gap:30px;padding:20px 0;font-size:27px;line-height:1.4;border-bottom:1px solid rgba(255,255,255,.16)}}
.row:last-child{{border-bottom:0}} .row b{{font-weight:700;color:{p['dourado']};text-align:right}}
.grade{{margin-top:30px;border-radius:16px;overflow:hidden;border:1.5px solid rgba(0,0,0,.14)}}
.dark .grade{{border-color:rgba(255,255,255,.18)}}
.grade table{{width:100%;border-collapse:collapse;font-size:22px;text-align:center}}
.grade th{{background:{p['escuro']};color:{p['dourado']};font-weight:700;letter-spacing:1px;padding:16px 4px;font-size:20px}}
.dark .grade th{{background:rgba(255,255,255,.06)}}
.grade td{{padding:14px 4px;border-top:1px solid rgba(0,0,0,.08)}}
.dark .grade td{{border-top:1px solid rgba(255,255,255,.08);color:{p['claro']}}}
.grade td.l{{text-align:left;padding-left:18px;font-weight:600;font-size:21px;white-space:nowrap}}
.grade .f{{display:inline-block;min-width:74px;padding:8px 0;border-radius:30px;background:{p['dourado']};color:{p['escuro']};font-weight:700;font-size:19px}}
.grade .t{{display:inline-block;min-width:74px;padding:8px 0;border-radius:30px;background:rgba(0,0,0,.06);font-size:19px}}
.dark .grade .t{{background:rgba(255,255,255,.08)}}
.legenda{{font-size:21px;margin-top:14px;opacity:.8}}
.note{{font-size:25px;line-height:1.5;margin-top:26px;opacity:.85}} .note b{{font-weight:700}}
.foot{{position:absolute;left:96px;right:96px;bottom:70px;border-top:1.5px solid rgba(0,0,0,.14);padding-top:26px;display:flex;justify-content:space-between;font-size:22px}}
.dark .foot{{border-color:rgba(255,255,255,.16)}}
.foot .r{{font-weight:600;letter-spacing:4px}} .foot.c{{justify-content:center}}
.center .body{{align-items:center;text-align:center;top:120px}}
.biglogo{{width:340px;margin-bottom:28px}}
.sep{{width:70px;height:2px;background:{p['dourado']};margin:0 auto 40px}}
.center h1{{font-size:80px}}
.pill{{display:inline-block;margin-top:42px;background:{p['dourado']};color:{p['escuro']};font-weight:700;font-size:25px;letter-spacing:3px;padding:24px 46px;border-radius:60px}}
.url{{margin-top:22px;font-size:23px;opacity:.8}}
.alert{{margin-top:36px;font-size:23px;line-height:1.5;opacity:.85;border:1.5px solid rgba(255,255,255,.18);border-radius:14px;padding:20px 26px;text-align:left}}
.alert b{{color:{p['dourado']}}}
"""


def bloco(b):
    if "caixa" in b:
        return f'<div class="box"><div class="lbl">{b["caixa"]}</div><div class="bt">{b["texto"]}</div></div>'
    if "caixa_dourada" in b:
        return f'<div class="box gold"><div class="lbl">{b["caixa_dourada"]}</div><div class="bt">{b["texto"]}</div></div>'
    if "tabela" in b:
        rows = "".join(f'<div class="row"><span>{a}</span><b>{c}</b></div>' for a, c in b["tabela"])
        return f'<div class="tbl">{rows}</div>'
    if "grade" in b:
        g = b["grade"]
        head = "".join(f"<th>{c}</th>" for c in [""] + g["colunas"])
        def cel(v):
            return '<span class="f">Folga</span>' if v == "F" else '<span class="t">Trab.</span>'
        rows = "".join("<tr><td class='l'>" + r[0] + "</td>" + "".join(f"<td>{cel(v)}</td>" for v in r[1:]) + "</tr>" for r in g["linhas"])
        leg = f'<div class="legenda">{g["legenda"]}</div>' if g.get("legenda") else ""
        return f'<div class="grade"><table><tr>{head}</tr>{rows}</table></div>{leg}'
    if "nota" in b:
        return f'<div class="note">{b["nota"]}</div>'
    if "texto" in b:
        return f'<div class="lead">{b["texto"]}</div>'
    raise ValueError(f"bloco desconhecido: {b}")


def html_card(c, i, n, rodape_final):
    if c["tipo"] == "cta":
        alerta = f'<div class="alert">{c["alerta"]}</div>' if c.get("alerta") else ""
        return (f'<div class="card dark center"><div class="pg">{i:02d} / {n:02d}</div><div class="body">'
                f'<img class="biglogo" src="file://{LOGO_FUNDO_ESCURO}"><div class="sep"></div>'
                f'<h1>{c["titulo"]}</h1><div class="lead">{c.get("texto","")}</div>'
                f'<div><span class="pill">{c.get("botao","MANDA DIAGNÓSTICO NO DIRECT")}</span></div>'
                f'<div class="url">correasalesassessoria.com.br</div>{alerta}</div>'
                f'<div class="foot c"><span>{rodape_final}</span></div></div>')
    escuro = c.get("fundo", "escuro") == "escuro"
    logo = LOGO_FUNDO_ESCURO if escuro else LOGO_FUNDO_CLARO
    corpo = f'<div class="tag">{c["tag"]}</div><h1>{c["titulo"]}</h1>'
    if c["tipo"] == "capa":
        corpo += f'<div class="lead">{c.get("texto","")}</div>'
    else:
        corpo += "".join(bloco(b) for b in c.get("blocos", []))
    return (f'<div class="card {"dark" if escuro else "light"}"><img class="logo" src="file://{logo}">'
            f'<div class="pg">{i:02d} / {n:02d}</div><div class="body">{corpo}</div>'
            f'<div class="foot"><span>@correasalesassessoria</span><span class="r">ARRASTE →</span></div></div>')


def logos_recortadas(saida):
    """Recorta a margem transparente dos arquivos oficiais (sem alterar a logo)."""
    global LOGO_FUNDO_ESCURO, LOGO_FUNDO_CLARO
    from PIL import Image
    novos = []
    for caminho in (LOGO_FUNDO_ESCURO, LOGO_FUNDO_CLARO):
        im = Image.open(caminho)
        destino = os.path.abspath(os.path.join(saida, "_" + os.path.basename(caminho)))
        im.crop(im.getbbox()).save(destino)
        novos.append(destino)
    LOGO_FUNDO_ESCURO, LOGO_FUNDO_CLARO = novos
    return novos


def main(roteiro, saida):
    from playwright.sync_api import sync_playwright
    r = json.load(open(roteiro, encoding="utf-8"))
    p = PALETAS[r.get("paleta", "padrao")]
    os.makedirs(saida, exist_ok=True)
    temporarios = logos_recortadas(saida)
    cards, n = r["cards"], len(r["cards"])
    estilo = css(p)
    problemas = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, c in enumerate(cards, 1):
            h = os.path.join(saida, f"_card{i}.html")
            with open(h, "w", encoding="utf-8") as f:
                f.write(f"<html><head><meta charset=utf-8><style>{estilo}</style></head><body>"
                        f"{html_card(c, i, n, r.get('rodape_final', 'Salve e envie para quem precisa ver isso'))}</body></html>")
            pg.goto("file://" + os.path.abspath(h))
            pg.wait_for_timeout(400)
            if pg.evaluate("()=>{const x=document.querySelector('.body');return x.scrollHeight>x.clientHeight+2}"):
                problemas.append(i)
            pg.screenshot(path=os.path.join(saida, f"{r['nome']}_{i}.jpg"), type="jpeg", quality=92)
            os.remove(h)
        b.close()
    for t in temporarios:
        os.remove(t)
    if problemas:
        print("ATENÇÃO: texto passou do espaço nos cards", problemas, "- encurte o texto e gere de novo.")
    print(f"{n} cards gerados em {saida}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
