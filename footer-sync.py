# -*- coding: utf-8 -*-
"""Footer sync для серии ШАГ: единый манифест -> одинаковый футер во всех страницах.
Манифест: FOOTER-MANIFEST.json (список статей). Прогон: python footer-sync.py
Ищет в каждом index.html блок <footer>...</footer> и перезаписывает span с навигацией.
"""
import io, sys, json, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

repo = r"C:\Users\1\.openclaw-autoclaw\workspace\.openclaw\tmp\shag-repo"
manifest = json.load(open(os.path.join(repo, "FOOTER-MANIFEST.json"), encoding="utf-8"))
brand = manifest["brand_line"]           # строка бренда до ссылок
style = 'style="color:var(--accent)"'

def nav_html(current_slug):
    parts = [f'<a href="/"{"" if True else ""} {style}>Главная страница услуг</a>',
             f'<a href="/blog/" {style}>Все статьи</a>']
    for a in manifest["articles"]:
        if a["slug"] == current_slug:
            continue  # на себя не ссылаемся
        parts.append(f'<a href="/blog/{a["slug"]}" {style}>{a["short"]}</a>')
    return " · ".join(parts)

def build_footer(current_slug, contacts):
    return (f"<footer>\n  <div class=\"wrap\">\n    <span>{brand} · "
            f"{nav_html(current_slug)}</span>\n    <span>{contacts}</span>\n  </div>\n</footer>")

pages = [{"slug": None, "path": os.path.join(repo, "index.html"),
          "contacts": manifest["home_contacts"]}]

for a in manifest["articles"]:
    pages.append({"slug": a["slug"],
                  "path": os.path.join(repo, "blog", a["slug"], "index.html"),
                  "contacts": manifest["article_contacts"]})

changed = []
for p in pages:
    if not os.path.exists(p["path"]):
        print("SKIP (no file):", p["path"])
        continue
    t = open(p["path"], encoding="utf-8").read()
    new_footer = build_footer(p["slug"], p["contacts"])
    t2 = re.sub(r"<footer>.*?</footer>", new_footer, t, flags=re.S)
    if t2 != t:
        open(p["path"], "w", encoding="utf-8", newline="").write(t2)
        changed.append(p["slug"] or "index.html")

print("updated:", changed if changed else "all already in sync")
