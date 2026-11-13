#!/usr/bin/env python3
"""Gera o painel de skills (um HTML único) a partir das skills instaladas.

Uso:
  python3 build_panel.py [--skills-dir ~/.claude/skills] [--out painel-skills.html]
                         [--overrides overrides.json] [--previews previews.json]
                         [--include nome1,nome2] [--exclude nome3] [--title "Painel de Skills"]

Lê o frontmatter (name, description) de cada SKILL.md. Não copia nem altera as skills.
Sem overrides, descrições e exemplos vêm do próprio arquivo (podem estar em inglês).
"""
import argparse, json, os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "template.html")

CATS = [  # (categoria, palavras que a identificam, na ordem de prioridade)
    ("3D", r"\b(3d|three\.?js|blender|mesh|render(ing)?|cad|sculpt|modelagem|modelo 3d)\b"),
    ("Vídeo", r"\b(video|vídeo|film|remotion|ffmpeg|moviepy|footage|reel|clip|timeline|after effects|motion graphics)\b"),
    ("Áudio", r"\b(audio|áudio|sound|som|music|música|voice|voz|soundtrack|sfx|tts|narra\w*)\b"),
    ("Animação", r"\b(animat\w*|animaç\w*|motion|gsap|lottie|svg|easing|transition|transiç\w*|scroll)\b"),
    ("Imagem", r"\b(image|imagem|photo|foto|logo|vector|vetor|illustrat\w*|icon|ícone|retouch\w*)\b"),
    ("Documentos", r"\b(pdf|docx?|word|slides?|deck|powerpoint|pptx|xlsx|spreadsheet|planilha|document\w*|indesign|brochure)\b"),
    ("Visual", r"\b(design|ui|ux|css|layout|palette|paleta|cor(es)?|color|landing|site|website|interface|dashboard|painel|frontend|typography|tipografia|glass)\b"),
    ("Código", r"\b(code|código|api|sdk|review|test\w*|git|refactor\w*|architecture|arquitetura|debug|build|deploy|android|react|python|rust|mcp|plugin|config\w*)\b"),
]

def frontmatter(text):
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm, cur = {}, None
    for line in parts[1].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            cur = m.group(1); v = m.group(2).strip()
            fm[cur] = v.strip(">|-").strip() if v in (">", "|", ">-", "|-") else v
        elif cur and line.strip():
            fm[cur] = (fm[cur] + " " + line.strip()).strip()
    for k in fm:
        fm[k] = re.sub(r"\s+", " ", fm[k]).strip().strip("'\"")
    return fm

def first_sentence(s, n=170):
    s = re.sub(r"\s+", " ", s).strip()
    m = re.match(r"(.{20,%d}?[.!?])(\s|$)" % n, s)
    out = m.group(1) if m else s[:n].rsplit(" ", 1)[0] + ("…" if len(s) > n else "")
    return out

def classify(name, desc):
    blob = (name.replace("-", " ") + " " + desc).lower()
    for cat, rx in CATS:
        if re.search(rx, blob, re.I):
            return cat
    return "Outros"

def use_when(desc):
    m = re.search(r"(?i)((?:use|usar|utilize)[^.]{10,200}\.)", desc)
    return m.group(1)[:200] if m else ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills-dir", default=os.path.expanduser("~/.claude/skills"))
    ap.add_argument("--out", default="painel-skills.html")
    ap.add_argument("--overrides")
    ap.add_argument("--previews")
    ap.add_argument("--include", default="")
    ap.add_argument("--exclude", default="")
    ap.add_argument("--title", default="Painel de Skills")
    a = ap.parse_args()

    ov = json.load(open(a.overrides, encoding="utf-8")) if a.overrides else {}
    inc = {x.strip() for x in a.include.split(",") if x.strip()}
    exc = {x.strip() for x in a.exclude.split(",") if x.strip()}
    data = []
    for d in sorted(os.listdir(a.skills_dir)):
        p = os.path.join(a.skills_dir, d, "SKILL.md")
        if not os.path.isfile(p) or (inc and d not in inc) or d in exc:
            continue
        fm = frontmatter(open(p, encoding="utf-8", errors="ignore").read())
        name = fm.get("name", d)
        desc = fm.get("description", "")
        trig = [re.sub(r"\s+", " ", q) for q in re.findall(r'"([^"]{8,80})"', desc)][:3]
        uw = use_when(desc) if not trig else ""
        item = {
            "cmd": "/" + name,
            "cat": classify(name, desc),
            "desc": first_sentence(desc) or "Sem descrição no arquivo.",
            "ex": (trig[0][0].upper() + trig[0][1:]) if trig else (uw or first_sentence(desc, 110)),
            "tr": trig, "uw": uw,
        }
        item.update({k: v for k, v in ov.get(name, ov.get("/" + name, {})).items() if k in item})
        data.append(item)

    pv, cat = {}, {}
    out_dir = os.path.dirname(os.path.abspath(a.out)) or "."
    if a.previews:
        spec = json.load(open(a.previews, encoding="utf-8"))
        base = os.path.dirname(os.path.abspath(a.previews))
        for cmd, items in spec.get("previews", {}).items():
            pv[cmd] = items
        cat = spec.get("catalogs", {})
        # copia as mídias para ao lado do HTML, mantendo os caminhos relativos
        files = {x["i"] for v in pv.values() for x in v} | {x["v"] for v in pv.values() for x in v if x.get("v")}
        for c in cat.values():
            files |= {x["i"] for x in c["items"] if x.get("i")} | {x["v"] for x in c["items"] if x.get("v")}
        for rel in sorted(files):
            src, dst = os.path.join(base, rel), os.path.join(out_dir, rel)
            if os.path.isfile(src) and os.path.abspath(src) != os.path.abspath(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)

    html = open(TEMPLATE, encoding="utf-8").read()
    html = html.replace("<title>Painel de Skills</title>", "<title>%s</title>" % a.title)
    j = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__DATA__", j(data)).replace("__PV__", j(pv)).replace("__CAT__", j(cat))
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(html)
    cats = {}
    for s in data: cats[s["cat"]] = cats.get(s["cat"], 0) + 1
    print("%d skills -> %s (%d KB)" % (len(data), a.out, len(html) // 1024))
    print("categorias:", ", ".join("%s %d" % kv for kv in sorted(cats.items())))

if __name__ == "__main__":
    main()
