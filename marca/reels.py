"""Gerador de Reels narrados no padrão Corrêa Sales (1080x1920, até 30 s).

Uso:
  python3 marca/reels.py roteiro.json saida/                  -> prévia sem voz (tempo estimado pelo texto)
  python3 marca/reels.py roteiro.json saida/ --audio voz.mp3  -> vídeo final, cenas sincronizadas com as pausas da voz
  python3 marca/reels.py roteiro.json --texto                 -> imprime o texto da narração (para o ElevenLabs)

Gera saida/<nome>.mp4 e saida/<nome>_capa.jpg. A logo SEMPRE vem dos arquivos oficiais em assets/.
Fontes, cores e estrutura seguem marca/PADRAO-VISUAL.md (Cormorant Garamond + Montserrat, paleta "padrao").

Roteiro (JSON):
{
  "nome": "escala_5x2_reels",
  "cenas": [
    {"tipo": "capa", "fundo": "escuro", "tag": "Escala 5x2 · 16 de dezembro",
     "titulo": "Tem funcionário? A hora de trabalho vai <em>ficar mais cara.</em>",
     "caixa": {"rotulo": "Faltam", "contar": 20, "sufixo": " dias", "nota": "até 16/12/2026"},
     "fala": "Tem funcionário? A partir de 16 de dezembro, a hora de trabalho fica mais cara."},
    {"tipo": "tabela", "fundo": "escuro", "tag": "A nova escala", "titulo": "Duas folgas <em>por semana.</em>",
     "linhas": [["Jornada máxima", "42 horas"], ["A partir de 16/12/2027", "40 horas"]], "nota": "opcional",
     "fala": "..."},
    {"tipo": "valor", "fundo": "claro", "tag": "Salário de R$ 3.000", "titulo": "O salário não muda. O valor da hora <em>sobe.</em>",
     "rotulo": "Valor da hora normal", "de": 13.64, "para": 14.29, "formato": "moeda", "selo": "+4,8%",
     "dourado": false, "nota": "Divisor da folha: de 220 para 210", "fala": "..."},
    {"tipo": "lista", "fundo": "claro", "tag": "O que fazer agora", "titulo": "Prepare a sua empresa <em>ainda este ano.</em>",
     "itens": ["Refaça a escala de dezembro", "Confira a convenção do seu sindicato", "Recalcule a folha"],
     "nota": "opcional", "fala": "..."},
    {"tipo": "cta", "titulo": "Quer ajuda para <em>ajustar a sua empresa?</em>", "texto": "A Corrêa Sales ...",
     "botao": "MANDA DIAGNÓSTICO NO DIRECT", "base": "Base: ... Conteúdo informativo, não substitui a análise do seu caso.",
     "fala": "Quer ajuda? Manda DIAGNÓSTICO no direct da Corrêa Sales."}
  ]
}
Use <br> no título para forçar a quebra de linha. Regras: 4 a 6 cenas; a última é "cta". "fala" é o texto que a voz lê (números por extenso quando ajudar a pronúncia);
o que aparece na tela fica em titulo/itens/linhas. "formato" do valor: "moeda", "numero" ou "pct".
"""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FONTES = os.path.join(AQUI, "fontes")
W, H, FPS = 1080, 1920, 30
MAX_SEG = 30.0
ESC = (0x24, 0x28, 0x33); CLA = (0xF5, 0xEF, 0xE4); DOU = (0xC8, 0xA4, 0x72); DOU_C = (0x8F, 0x6F, 0x42)
X0 = 96
AVISOS = []

_fc = {}
def F(kind, size):
    k = (kind, size)
    if k in _fc: return _fc[k]
    path, var = {"cg": ("CormorantGaramond.ttf", "Medium"), "cgi": ("CormorantGaramond-Italic.ttf", "Medium Italic"),
                 "ms": ("Montserrat.ttf", "Regular"), "msm": ("Montserrat.ttf", "Medium"),
                 "mss": ("Montserrat.ttf", "SemiBold"), "msb": ("Montserrat.ttf", "Bold")}[kind]
    f = ImageFont.truetype(os.path.join(FONTES, path), size); f.set_variation_by_name(var)
    _fc[k] = f; return f

_logos = {}
def logo(dark, width):
    k = (dark, width)
    if k not in _logos:
        im = Image.open(os.path.join(RAIZ, "assets", "logo-dark-bg.png" if dark else "logo-light-bg.png")).convert("RGBA")
        im = im.crop(im.getbbox())
        _logos[k] = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return _logos[k]

def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def P(t, st, dur=.5): return ease((t - st) / dur)
def mix(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))

def fmt(v, formato):
    if formato == "moeda": return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if formato == "pct": return f"{v:.1f}%".replace(".", ",")
    casas = 0 if float(v).is_integer() else 2
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def partes(html):
    """'Texto <em>destaque</em>' -> [(texto, False), (destaque, True)]"""
    out, pos = [], 0
    for m in re.finditer(r"<em>(.*?)</em>", html):
        if m.start() > pos: out.append((html[pos:m.start()], False))
        out.append((m.group(1), True)); pos = m.end()
    if pos < len(html): out.append((html[pos:], False))
    return out

def wrap(text, font, maxw):
    lines = [""]
    for w in text.split():
        t = (lines[-1] + " " + w).strip()
        if font.getlength(t) > maxw and lines[-1]: lines.append(w)
        else: lines[-1] = t
    return lines

class Card:
    def __init__(self, dark):
        self.dark = dark; self.bg = ESC if dark else CLA; self.fg = CLA if dark else ESC
        self.gold = DOU if dark else DOU_C
        self.im = Image.new("RGB", (W, H), self.bg); self.d = ImageDraw.Draw(self.im)
    def c(self, col, k): return mix(self.bg, col, k)
    def paste(self, lg, xy, k):
        if k <= 0: return
        self.im.paste(lg, (int(xy[0]), int(xy[1])), lg.split()[3].point(lambda v: int(v * k)))
    def tag(self, s, y, k):
        if k <= 0: return
        y += (1 - k) * 24; col = self.c(self.gold, k); f = F("mss", 27)
        self.d.line((X0, y + 15, X0 + 62, y + 15), fill=col, width=3); x = X0 + 84
        for ch in s.upper(): self.d.text((x, y), ch, font=f, fill=col); x += f.getlength(ch) + 6
    def lbl(self, xy, s, k, col=None):
        if k <= 0: return
        x, y = xy; col = self.c(col or self.gold, k); f = F("mss", 23)
        for ch in s.upper(): self.d.text((x, y), ch, font=f, fill=col); x += f.getlength(ch) + 4.5
    def text(self, xy, s, font, col, k, dy=24, anchor="la", spacing=10):
        if k <= 0: return
        al = "center" if anchor.startswith("m") else ("right" if anchor.startswith("r") else "left")
        self.d.multiline_text((xy[0], xy[1] + (1 - k) * dy), s, font=font, fill=self.c(col, k), anchor=anchor, spacing=spacing, align=al)
    def title(self, html, y, k, size=100, center=False, check=None):
        maxw = W - 2 * X0; sp = F("cg", size).getlength(" ")
        words = [(w, em) for s, em in partes(html.replace("<br>", " \n ")) for w in s.split(" ") if w]
        lines, cur, cw = [], [], 0
        for w, em in words:
            if w == "\n":
                if cur: lines.append((cur, cw)); cur, cw = [], 0
                continue
            ww = F("cgi" if em else "cg", size).getlength(w)
            if cur and cw + sp + ww > maxw: lines.append((cur, cw)); cur, cw = [], 0
            cw += (sp if cur else 0) + ww; cur.append((w, em, ww))
        if cur: lines.append((cur, cw))
        if check is not None and len(lines) > 4: AVISOS.append(f"{check}: título com {len(lines)} linhas (máximo 4). Encurte.")
        for i, (ln, lw) in enumerate(lines):
            x = (W - lw) / 2 if center else X0; yy = y + i * size * 1.1
            if k > 0:
                for w, em, ww in ln:
                    self.d.text((x, yy + (1 - k) * 28), w, font=F("cgi" if em else "cg", size), fill=self.c(self.gold if em else self.fg, k))
                    x += ww + sp
        return y + len(lines) * size * 1.1
    def box(self, xy, k, gold=False):
        if k <= 0: return 0
        x0, y0, x1, y1 = xy; dy = (1 - k) * 24
        if gold:
            self.d.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), 18, fill=self.c(self.gold, k))
        else:
            fill = mix(self.bg, (255, 255, 255), .04 if self.dark else .35)
            line = mix(self.bg, (255, 255, 255) if self.dark else (0, 0, 0), .18 if self.dark else .14)
            self.d.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), 18, fill=self.c(fill, k), outline=self.c(line, k), width=2)
        return dy

# Cada cena desenha com t em [0, dur]. As revelações acontecem nos primeiros 70% da cena.
def cena_padrao(c, cena, t, dur, idx):
    """Logo + tag + título. Devolve (y após o título, função de tempo relativo)."""
    R = lambda frac: frac * dur  # momento relativo
    c.paste(logo(c.dark, 236), (X0, 150), 1 if idx else P(t, 0, .4))
    c.tag(cena.get("tag", ""), 600, P(t, R(.02)))
    y = c.title(cena["titulo"], 670, P(t, R(.08)), size=cena.get("tamanho", 100), check=f"cena {idx + 1}")
    return y + 40, R

def desenha(cena, t, dur, idx):
    tipo = cena["tipo"]; dark = cena.get("fundo", "escuro") != "claro"
    if tipo == "cta": dark = True
    c = Card(dark)
    if tipo == "cta":
        lg = logo(True, 400); k = P(t, 0, .6)
        c.paste(lg, ((W - lg.width) // 2, 520 + (1 - k) * 24), k)
        y = c.title(cena["titulo"], 780, P(t, .2), size=92, center=True, check=f"cena {idx + 1}")
        if cena.get("texto"):
            ls = wrap(cena["texto"], F("ms", 34), W - 2 * X0)
            c.text((W / 2, y + 30), "\n".join(ls), F("ms", 34), CLA, P(t, .45) * .9, anchor="ma", spacing=12)
            y += 30 + len(ls) * 46
        k = P(t, .7)
        if k > 0:
            bw, bh = 800, 116; x0 = (W - bw) / 2; y0 = y + 60 + (1 - k) * 24
            c.d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), 58, fill=c.c(DOU, k))
            lbl = cena.get("botao", "MANDA DIAGNÓSTICO NO DIRECT"); f = F("msb", 32); sp = 3
            tw = sum(f.getlength(ch) + sp for ch in lbl) - sp
            if tw > bw - 60: AVISOS.append(f"cena {idx + 1}: texto do botão grande demais.")
            x = (W - tw) / 2
            for ch in lbl: c.d.text((x, y0 + bh / 2), ch, font=f, fill=mix(DOU, ESC, k), anchor="lm"); x += f.getlength(ch) + sp
            c.text((W / 2, y0 + bh + 40), "correasalesassessoria.com.br", F("ms", 30), CLA, k * .85, dy=0, anchor="ma")
        if cena.get("base"):
            ks = P(t, 1.2)
            c.d.line((X0, 1560, W - X0, 1560), fill=c.c(mix(ESC, CLA, .18), ks), width=1)
            ls = wrap(cena["base"], F("ms", 22), W - 2 * X0)
            c.text((W / 2, 1585), "\n".join(ls[:3]), F("ms", 22), CLA, ks * .7, dy=0, anchor="ma", spacing=8)
        return c.im

    y, R = cena_padrao(c, cena, t, dur, idx)
    if tipo == "capa":
        cx = cena.get("caixa")
        if cx:
            k = P(t, R(.45))
            if k > 0:
                y0 = max(y + 20, 1080); dy = c.box((X0, y0, W - X0, y0 + 220), k)
                c.lbl((X0 + 36, y0 + 32 + dy), cx.get("rotulo", ""), k)
                if "contar" in cx:
                    n = int(round(cx["contar"] * P(t, R(.47), R(.3))))
                    val = f"{n}{cx.get('sufixo', '')}"
                else:
                    val = cx.get("valor", "")
                c.text((X0 + 36, y0 + 70 + dy), val, F("msb", 96), c.fg, 1, dy=0)
                if cx.get("nota"): c.text((W - X0 - 36, y0 + 120 + dy), cx["nota"], F("ms", 30), c.fg, k * .85, dy=0, anchor="ra")
        elif cena.get("texto"):
            ls = wrap(cena["texto"], F("ms", 36), W - 2 * X0)
            c.text((X0, y + 10), "\n".join(ls), F("ms", 36), c.fg, P(t, R(.4)) * .9, spacing=14)
    elif tipo == "tabela":
        linhas = cena["linhas"][:4]; k = P(t, R(.3))
        if k > 0:
            hh = 120; y0 = y + 20; dy = c.box((X0, y0, W - X0, y0 + hh * len(linhas) + 10), k)
            for i, (a, b) in enumerate(linhas):
                kk = P(t, R(.3 + i * .14)); yy = y0 + 42 + i * hh + dy
                c.text((X0 + 34, yy), a, F("ms", 34), c.fg, kk, dy=0)
                c.text((W - X0 - 34, yy), b, F("msb", 34), c.gold, kk, dy=0, anchor="ra")
                if F("ms", 34).getlength(a) + F("msb", 34).getlength(b) > W - 2 * X0 - 110:
                    AVISOS.append(f"cena {idx + 1}: linha da tabela longa demais: {a} | {b}")
                if i: c.d.line((X0 + 34, y0 + 5 + i * hh + dy, W - X0 - 34, y0 + 5 + i * hh + dy), fill=c.c(mix(c.bg, c.fg, .16), k), width=1)
            y = y0 + hh * len(linhas) + 10
        if cena.get("nota"): c.text((X0, y + 40), "\n".join(wrap(cena["nota"], F("ms", 30), W - 2 * X0)), F("ms", 30), c.fg, P(t, R(.6)) * .75)
    elif tipo == "valor":
        gold = bool(cena.get("dourado")); k = P(t, R(.3))
        if k > 0:
            y0 = y + 20; dy = c.box((X0, y0, W - X0, y0 + 300), k, gold=gold); ink = ESC if gold else c.fg
            c.lbl((X0 + 36, y0 + 34 + dy), cena.get("rotulo", ""), k, col=(ESC if gold else None))
            a, b = float(cena["de"]), float(cena["para"]); pv = P(t, R(.5), R(.25))
            c.text((X0 + 36, y0 + 82 + dy), fmt(a + (b - a) * pv, cena.get("formato", "moeda")), F("msb", 112), ink, k, dy=0)
            c.text((X0 + 36, y0 + 222 + dy), f"Hoje: {fmt(a, cena.get('formato', 'moeda'))}", F("ms", 30), ink, k * .8, dy=0)
            kp = P(t, R(.72), .4)
            if kp > 0 and cena.get("selo"):
                bw, bh = 200, 64; x1 = W - X0 - 36; yb = y0 + 210 + dy
                c.d.rounded_rectangle((x1 - bw, yb, x1, yb + bh), 32, fill=mix(DOU if gold else c.bg, ESC if gold else DOU, kp))
                c.text((x1 - bw / 2, yb + bh / 2), cena["selo"], F("msb", 32), mix(DOU if gold else c.bg, CLA if gold else ESC, kp), 1, dy=0, anchor="mm")
            y = y0 + 300
        if cena.get("nota"): c.text((X0, y + 40), "\n".join(wrap(cena["nota"], F("ms", 30), W - 2 * X0)), F("ms", 30), c.fg, P(t, R(.6)) * .75)
    elif tipo == "lista":
        itens = cena["itens"][:4]
        if len(cena["itens"]) > 4: AVISOS.append(f"cena {idx + 1}: lista com mais de 4 itens (só 4 aparecem).")
        y0 = y + 10
        for i, s in enumerate(itens):
            st = R(.2 + i * (.5 / max(1, len(itens)))); k = P(t, st)
            yy = y0 + i * 170
            if k <= 0: continue
            dy = c.box((X0, yy, W - X0, yy + 145), k)
            cx_, cy, r = X0 + 72, yy + 72 + dy, 34; kc = P(t, st + .35, .4)
            c.d.ellipse((cx_ - r, cy - r, cx_ + r, cy + r), outline=c.c(c.gold, k), width=3, fill=mix(c.bg, c.gold, kc) if kc > 0 else None)
            c.text((cx_, cy), str(i + 1), F("msb", 30), mix(c.gold, c.bg, kc), k, dy=0, anchor="mm")
            f = F("msm", 32); ls = wrap(s, f, W - 2 * X0 - 170)
            if len(ls) > 2: AVISOS.append(f"cena {idx + 1}: item {i + 1} passa de 2 linhas. Encurte.")
            c.text((X0 + 136, cy - (len(ls) * 42) / 2 + 2), "\n".join(ls[:2]), f, c.fg, k, dy=0, spacing=8)
        y = y0 + len(itens) * 170
        if cena.get("nota"): c.text((X0, y + 20), "\n".join(wrap(cena["nota"], F("ms", 28), W - 2 * X0)), F("ms", 28), c.fg, P(t, R(.7)) * .75)
    else:
        raise SystemExit(f"tipo de cena desconhecido: {tipo}")
    if y > 1500: AVISOS.append(f"cena {idx + 1}: conteúdo desce até y={int(y)} e pode ficar atrás da legenda do Instagram. Encurte.")
    return c.im

FADE = .3
def frame(cenas, i, t, durs):
    cena = cenas[i]; dur = durs[i]
    dark = cena.get("fundo", "escuro") != "claro" or cena["tipo"] == "cta"
    im = desenha(cena, t, dur, i)
    cor = lambda j: ESC if (cenas[j].get("fundo", "escuro") != "claro" or cenas[j]["tipo"] == "cta") else CLA
    if i + 1 < len(cenas) and t > dur - FADE:
        im = Image.blend(im, Image.new("RGB", (W, H), cor(i + 1)), clamp((t - (dur - FADE)) / FADE) * (1 if cor(i + 1) != (ESC if dark else CLA) else .9))
    if i > 0 and t < FADE:
        im = Image.blend(im, Image.new("RGB", (W, H), cor(i - 1)), (1 - t / FADE) * (1 if cor(i - 1) != (ESC if dark else CLA) else .9))
    return im

def render_cena(args):
    cenas, i, durs, pasta = args
    n = int(round(durs[i] * FPS)); tmp = os.path.join(pasta, f"c{i}.tmp.mp4"); fim = os.path.join(pasta, f"c{i}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(frame(cenas, i, k / FPS, durs).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit(f"ffmpeg falhou na cena {i + 1}")
    os.rename(tmp, fim); return fim

# ---------- áudio ----------
def pausas(audio):
    """Pausas (início, fim) de pelo menos 0,15 s, e a duração do áudio."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768; hop = 800  # 50 ms
    db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(x) - hop, hop)])
    sil = db < -42; out, st = [], None
    for i, v in enumerate(list(sil) + [False]):
        if v and st is None: st = i
        if not v and st is not None:
            if (i - st) * .05 >= .15: out.append((st * .05, i * .05))
            st = None
    return out, len(x) / 16000

def tempos(cenas, audio=None):
    chars = [max(8, len(c.get("fala", ""))) for c in cenas]
    if not audio:
        durs = [max(3.2, n / 15) for n in chars]
        tot = sum(durs)
        if tot > MAX_SEG - .1: durs = [d * (MAX_SEG - .1) / tot for d in durs]
        return durs, None
    ps, total = pausas(audio)
    inicio = ps[0][1] if ps and ps[0][0] < .05 else 0.0
    fala_fim = ps[-1][0] if ps and ps[-1][1] >= total - .1 else total
    meio = [p for p in ps if p[0] > inicio + .3 and p[1] < fala_fim - .3]
    cand = [(a + b) / 2 for a, b in meio]
    cortes, acc = [], 0
    for i in range(len(cenas) - 1):
        acc += chars[i]
        alvo = inicio + (fala_fim - inicio) * acc / sum(chars)
        ok = [c for c in cand if (not cortes or c > cortes[-1] + 1.5)]
        cortes.append(min(ok, key=lambda c: abs(c - alvo)) if ok else alvo)
    fim = min(total + .35, MAX_SEG - .05)
    marcos = [0.0] + cortes + [fim]
    durs = [marcos[i + 1] - marcos[i] for i in range(len(cenas))]
    return durs, total

def main():
    args = sys.argv[1:]
    if not args: raise SystemExit(__doc__)
    rot = json.load(open(args[0], encoding="utf-8")); cenas = rot["cenas"]
    if "--texto" in args:
        print(" ".join(c.get("fala", "").strip() for c in cenas)); return
    saida = args[1]; os.makedirs(saida, exist_ok=True)
    audio = args[args.index("--audio") + 1] if "--audio" in args else None
    if not 3 <= len(cenas) <= 6: AVISOS.append("use de 4 a 6 cenas.")
    if cenas[-1]["tipo"] != "cta": AVISOS.append("a última cena deve ser do tipo cta.")
    durs, total = tempos(cenas, audio)
    for i in range(len(cenas)):  # confere o quadro cheio de cada cena (avisos de texto grande)
        desenha(cenas[i], durs[i] - FADE - .05, durs[i], i)
    if total and total > MAX_SEG - .1:
        AVISOS.append(f"a narração tem {total:.1f} s; o Reels passa de 30 s. Encurte as falas e gere a voz de novo.")
    with tempfile.TemporaryDirectory() as tmp:
        with ProcessPoolExecutor(max_workers=max(1, min(3, os.cpu_count() or 1))) as ex:
            arqs = list(ex.map(render_cena, [(cenas, i, durs, tmp) for i in range(len(cenas))]))
        lista = os.path.join(tmp, "lista.txt")
        open(lista, "w").write("".join(f"file '{a}'\n" for a in arqs))
        video = os.path.join(tmp, "video.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", video], check=True)
        dest = os.path.join(saida, f"{rot['nome']}.mp4")
        if audio:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", audio, "-filter_complex",
                            "[1:a]loudnorm=I=-15:TP=-1.5:LRA=9,apad[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", dest], check=True)
        else:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-c", "copy", "-movflags", "+faststart", dest], check=True)
    frame(cenas, 0, durs[0] - FADE - .05, durs).save(os.path.join(saida, f"{rot['nome']}_capa.jpg"), quality=92)
    print(f"OK {dest} · {sum(durs):.1f} s · cenas: " + ", ".join(f"{d:.1f}" for d in durs))
    for a in sorted(set(AVISOS)): print("AVISO:", a)

if __name__ == "__main__":
    main()
