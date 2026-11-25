"""Divide uma cena em blocos de quadros (um bloco = um trabalho no GitHub)."""
import json, os, sys

cena = sys.argv[1]
por_job = int(sys.argv[2])
cfg = json.load(open(f"cenas/{cena}/config.json", encoding="utf-8"))
total = cfg["total_quadros"]

itens = []
for fmt in cfg["formatos"]:
    ini = 1
    while ini <= total:
        fim = min(ini + por_job - 1, total)
        itens.append({"formato": fmt, "ini": ini, "fim": fim})
        ini = fim + 1

matriz = json.dumps(itens)
print(matriz)
with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write("matriz=" + matriz + "\n")
