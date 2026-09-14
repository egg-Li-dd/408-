#!/usr/bin/env python3
# 合并 data/*.json 与 math_data/*.json，图片转 base64 内嵌，注入 app/index.html
import json, os, base64, io, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_HTML = os.path.join(ROOT, "app", "index.html")
OUT_HTML = os.path.join(ROOT, "app", "408真题管理器.html")

all_q = []
for d in ("data", "math_data"):
    dd = os.path.join(ROOT, d)
    if not os.path.isdir(dd):
        continue
    for fp in sorted(glob.glob(os.path.join(dd, "*.json"))):
        arr = json.load(io.open(fp, encoding="utf-8"))
        all_q.extend(arr)

def img_to_datauri(path):
    if not path:
        return None
    full = path if os.path.isabs(path) else os.path.join(ROOT, path)
    if not os.path.exists(full):
        return None
    with open(full, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return "data:image/jpeg;base64," + b64

n = 0
for q in all_q:
    if q.get("image") and not str(q["image"]).startswith("data:"):
        uri = img_to_datauri(q["image"])
        if uri:
            q["image"] = uri; n += 1

html = io.open(SRC_HTML, encoding="utf-8").read()
payload = json.dumps(all_q, ensure_ascii=False)
html = html.replace("const QUESTIONS = [];", "const QUESTIONS = " + payload + ";", 1)
io.open(OUT_HTML, "w", encoding="utf-8").write(html)
print(f"共 {len(all_q)} 题，内嵌图片 {n} 张 -> {OUT_HTML}")
