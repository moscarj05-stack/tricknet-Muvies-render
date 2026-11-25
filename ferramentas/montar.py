"""Junta os quadros renderizados em vídeo MP4, com legendas na tela (ffmpeg)."""
import argparse, json, os, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--cena", required=True)
ap.add_argument("--formato", required=True)
ap.add_argument("--quadros", required=True, help="pasta com f_0001.png ...")
ap.add_argument("--saida", required=True, help="pasta de saída dos vídeos")
a = ap.parse_args()

cfg = json.load(open(f"cenas/{a.cena}/config.json", encoding="utf-8"))
fm = cfg["formatos"][a.formato]
fonte = os.environ.get("FONTE", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def esc(t):
    return t.replace("\\", "\\\\").replace("'", "\u2019").replace(":", "\\:").replace("%", "\\%")


filtros = [f"scale={fm['largura']}:{fm['altura']}:flags=lanczos"]
for l in cfg["legendas"][a.formato]:
    filtros.append(
        "drawtext=fontfile={f}:text='{t}':fontsize={s}:fontcolor=0x{c}:borderw={bw}:bordercolor=0x{b}"
        ":x={x}:y={y}:enable='between(n\\,{de}\\,{ate})'".format(
            f=fonte, t=esc(l["texto"]), s=l["tam"], c=l["cor"], bw=l["bw"], b=l["borda"],
            x=l["x"], y=l["y"], de=l["de"], ate=l["ate"]))

os.makedirs(a.saida, exist_ok=True)
destino = os.path.join(a.saida, fm["arquivo"])
cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(cfg["fps"]),
       "-i", os.path.join(a.quadros, "f_%04d.png"),
       "-vf", ",".join(filtros),
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", destino]
subprocess.run(cmd, check=True)
print("Vídeo criado:", destino)
