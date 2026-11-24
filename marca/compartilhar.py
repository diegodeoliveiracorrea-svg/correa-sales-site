"""Card vertical para compartilhar (status do WhatsApp e stories), padrão Corrêa Sales.

Uso:  python3 marca/compartilhar.py roteiro.json pasta_saida/
Gera <nome>.jpg (1080x1920). Usa a logo oficial (assets/logo-dark-bg.png) e as paletas do carrossel.py.
Conteúdo fica entre 260 px do topo e 300 px da base (área que o WhatsApp e o Instagram não cobrem).

Formato do roteiro (JSON):
{
  "nome": "mei_nota_2027_compartilhar",
  "paleta": "padrao",
  "tag": "MEI · 2027",
  "titulo": "Vende para pessoa física? <em>Sua declaração pode valer como nota.</em>",
  "itens": ["Primeira ideia curta", "Segunda ideia", "Terceira ideia"],   # 2 a 4 itens
  "rodape": "Salve e envie para quem tem MEI",
  "botao": "RESPONDA: DIAGNÓSTICO"
}
"""
import json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import carrossel  # noqa: E402  (paletas, fontes e recorte da logo oficial)


def css(p):
    f = os.path.join(AQUI, "fontes")
    return f"""
@font-face{{font-family:CG;src:url(file://{f}/CormorantGaramond.ttf);font-weight:300 700}}
@font-face{{font-family:CG;src:url(file://{f}/CormorantGaramond-Italic.ttf);font-style:italic;font-weight:300 700}}
@font-face{{font-family:MS;src:url(file://{f}/Montserrat.ttf);font-weight:100 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:MS;background:{p['escuro']};color:{p['claro']}}}
.wrap{{position:absolute;left:96px;right:96px;top:260px;bottom:300px;display:flex;flex-direction:column;justify-content:center}}
.logo{{width:300px;margin-bottom:70px}}
.tag{{display:flex;align-items:center;gap:22px;font-weight:600;font-size:28px;letter-spacing:7px;text-transform:uppercase;color:{p['dourado']};margin-bottom:36px}}
.tag:before{{content:"";width:70px;height:2px;background:{p['dourado']};flex:none}}
h1{{font-family:CG;font-weight:500;font-size:98px;line-height:1.06;letter-spacing:-.5px}}
h1 em{{font-style:italic;color:{p['dourado']}}}
.itens{{margin-top:60px;display:flex;flex-direction:column;gap:22px}}
.it{{display:flex;gap:26px;align-items:flex-start;border:1.5px solid rgba(255,255,255,.18);border-radius:18px;padding:28px 32px;background:rgba(255,255,255,.03)}}
.n{{flex:none;width:54px;height:54px;border-radius:50%;background:{p['dourado']};color:{p['escuro']};font-weight:700;font-size:28px;display:flex;align-items:center;justify-content:center}}
.t{{font-size:33px;line-height:1.4}} .t b{{font-weight:700;color:{p['dourado']}}}
.pill{{align-self:flex-start;margin-top:64px;background:{p['dourado']};color:{p['escuro']};font-weight:700;font-size:30px;letter-spacing:3px;padding:28px 52px;border-radius:70px}}
.rod{{margin-top:30px;font-size:27px;opacity:.85}}
.arroba{{margin-top:10px;font-size:25px;opacity:.7}}
"""


def main(roteiro, saida):
    from playwright.sync_api import sync_playwright
    r = json.load(open(roteiro, encoding="utf-8"))
    p = carrossel.PALETAS[r.get("paleta", "padrao")]
    os.makedirs(saida, exist_ok=True)
    temporarios = carrossel.logos_recortadas(saida)
    logo = temporarios[0]
    itens = "".join(f'<div class="it"><div class="n">{i}</div><div class="t">{t}</div></div>'
                    for i, t in enumerate(r["itens"], 1))
    html = (f"<html><head><meta charset=utf-8><style>{css(p)}</style></head><body><div class='wrap'>"
            f"<img class='logo' src='file://{logo}'><div class='tag'>{r['tag']}</div><h1>{r['titulo']}</h1>"
            f"<div class='itens'>{itens}</div><div class='pill'>{r.get('botao', 'RESPONDA: DIAGNÓSTICO')}</div>"
            f"<div class='rod'>{r.get('rodape', 'Salve e envie para quem precisa ver isso')}</div>"
            f"<div class='arroba'>@correasalesassessoria · correasalesassessoria.com.br</div></div></body></html>")
    h = os.path.join(saida, "_story.html")
    open(h, "w", encoding="utf-8").write(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + os.path.abspath(h))
        pg.wait_for_timeout(400)
        estourou = pg.evaluate("()=>{const x=document.querySelector('.wrap');return x.scrollHeight>x.clientHeight+2}")
        pg.screenshot(path=os.path.join(saida, f"{r['nome']}.jpg"), type="jpeg", quality=90)
        b.close()
    os.remove(h)
    for t in temporarios:
        os.remove(t)
    if estourou:
        print("ATENÇÃO: o texto passou do espaço - encurte o título ou os itens e gere de novo.")
    print(f"card gerado: {os.path.join(saida, r['nome'] + '.jpg')}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
