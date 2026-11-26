import bpy, math, random, sys, os
sys.path.insert(0, os.environ.get("TRICKNET_LIB", "/home/claude"))
import tricknet_lib as L
from tricknet_lib import M, add, entre, cil, esf, cubo, cone

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
FORMATO = argv[0] if argv else "h"            # h = horizontal 16:9 | v = vertical 9:16
MODO = argv[1] if len(argv) > 1 else "still"  # still | anim
SAIDA = argv[2] if len(argv) > 2 else "/home/claude/out/e1.png"
QUADRO = int(argv[3]) if len(argv) > 3 else 40
RES = float(argv[4].replace(",", ".")) if len(argv) > 4 else 0.5
AMOSTRAS = int(argv[5]) if len(argv) > 5 else 14
F_INI = int(argv[6]) if len(argv) > 6 else 1
F_FIM = int(argv[7]) if len(argv) > 7 else 60

TOTAL = 84
FPS = 24

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
scn.frame_start, scn.frame_end = 1, TOTAL
scn.render.fps = FPS
L.make_materials()


def sm(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def pressao(f):            # 0 = caixa baixa, 1 = caixa elevada
    return sm((f - 16) / 26.0)


HMAX = 1.1                 # quanto a caixa sobe (m)
LAJE_TOPO = 2.76
Z_DUCHA = 2.20
PX, PY = 2.3, 2.72         # posição do cano vertical


def kf(o, f, loc=None, esc=None, rot=None, interp="BEZIER"):
    bpy.context.preferences.edit.keyframe_new_interpolation_type = interp
    if loc is not None:
        o.location = loc
        o.keyframe_insert("location", frame=f)
    if esc is not None:
        o.scale = esc
        o.keyframe_insert("scale", frame=f)
    if rot is not None:
        o.rotation_euler = rot
        o.keyframe_insert("rotation_euler", frame=f)


# ---------- terreno e casa em corte ----------
add(cubo, "terreno", loc=(1.7, 1.4, -0.35), esc=(30, 30, 0.25), size=2, liso=False)
add(cubo, "piso", loc=(1.7, 1.4, -0.05), esc=(1.82, 1.52, 0.05), size=2, liso=False)
add(cubo, "casa", loc=(1.7, 2.86, 1.3), esc=(1.82, 0.06, 1.3), size=2, nome="parede_fundo", liso=False)
add(cubo, "casa", loc=(-0.06, 1.4, 1.3), esc=(0.06, 1.46, 1.3), size=2, liso=False)
add(cubo, "casa", loc=(3.46, 1.4, 1.3), esc=(0.06, 1.46, 1.3), size=2, liso=False)
add(cubo, "laje", loc=(1.7, 1.5, 2.68), esc=(1.9, 1.6, 0.08), size=2, nome="laje", liso=False)
# painel de azulejos do banheiro
add(cubo, "parede", loc=(2.35, 2.795, 1.3), esc=(1.05, 0.008, 1.3), size=2, liso=False)
for i in range(6):
    add(cubo, "rejunte", loc=(1.3 + i * 0.42, 2.785, 1.3), esc=(0.010, 0.008, 1.3), size=2, liso=False)
for j in range(7):
    add(cubo, "rejunte", loc=(2.35, 2.785, 0.2 + j * 0.4), esc=(1.05, 0.008, 0.010), size=2, liso=False)

# ---------- caixa-d'água (sobe junto com o pedestal) ----------
raiz_tq = bpy.data.objects.new("raiz_tanque", None)
scn.collection.objects.link(raiz_tq)
add(cil, "laje", loc=(0, 0, 0.03), esc=(0.43, 0.43, 0.03), vertices=40, pai=raiz_tq)
add(cil, "tanque", loc=(0, 0, 0.46), esc=(0.36, 0.36, 0.40), vertices=48, pai=raiz_tq, nome="tanque")
add(cil, "agua_tq", loc=(0, 0, 0.40), esc=(0.345, 0.345, 0.33), vertices=48, pai=raiz_tq, nome="agua_tanque")
add(cil, "ouro", loc=(0, 0, 0.46), esc=(0.367, 0.367, 0.02), vertices=48, pai=raiz_tq)
add(cil, "tampa", loc=(0, 0, 0.88), esc=(0.38, 0.38, 0.04), vertices=48, pai=raiz_tq)
add(cil, "tampa", loc=(0, 0, 0.94), esc=(0.07, 0.07, 0.04), vertices=24, pai=raiz_tq)
NIVEL_REL = 0.73           # nível da água em relação à base da caixa

# pedestal: duas colunas
cols = [add(cubo, "laje", loc=(PX + sx * 0.28, PY, LAJE_TOPO), esc=(0.09, 0.09, 0.001), size=2, liso=False)
        for sx in (-1, 1)]

# cano vertical (PVC marrom) e cotovelo + braço da ducha
cano = add(cil, "pvc", loc=(PX, PY, 2.5), esc=(0.04, 0.04, 0.3), vertices=24, nome="cano_vertical")
add(esf, "pvc", loc=(PX, PY, Z_DUCHA), esc=(0.05, 0.05, 0.05), segments=16, ring_count=10)
entre((PX, PY, Z_DUCHA), (PX, 2.2, Z_DUCHA), 0.035, "pvc")
add(cil, "cromo", loc=(PX, 2.2, Z_DUCHA - 0.03), esc=(0.20, 0.20, 0.025), vertices=40, nome="ducha")
add(cone, "cromo", loc=(PX, 2.2, Z_DUCHA + 0.02), esc=(0.07, 0.07, 0.06), vertices=24, radius1=1, depth=1)
# registro vermelho no cano
reg = add(cil, "registro", loc=(PX, PY - 0.08, 2.42), rot=(math.pi / 2, 0, 0), esc=(0.10, 0.10, 0.04), vertices=24)
add(cubo, "registro", loc=(PX, PY - 0.13, 2.42), esc=(0.10, 0.015, 0.015), size=2, liso=False)

# ---------- marcador de altura "h" ----------
MX, MY = 1.45, 2.45
linha = add(cil, "ouro_brilho", loc=(MX, MY, 3.0), esc=(0.018, 0.018, 0.5), vertices=12, nome="linha_h")
seta_c = add(cone, "ouro_brilho", loc=(MX, MY, 3.5), esc=(0.07, 0.07, 0.12), vertices=16, radius1=1, depth=1)
seta_b = add(cone, "ouro_brilho", loc=(MX, MY, Z_DUCHA), rot=(math.pi, 0, 0), esc=(0.07, 0.07, 0.12), vertices=16, radius1=1, depth=1)
guia_c = add(cubo, "ouro_brilho", loc=((MX + PX - 0.36) / 2, MY, 3.5), esc=((PX - 0.36 - MX) / 2, 0.012, 0.012), size=2, liso=False)
guia_b = add(cubo, "ouro_brilho", loc=((MX + PX - 0.2) / 2, MY, Z_DUCHA), esc=((PX - 0.2 - MX) / 2, 0.012, 0.012), size=2, liso=False)
bpy.ops.object.text_add(location=(MX - 0.42, MY, 3.0), rotation=(math.pi / 2, 0, 0))
rot_h = bpy.context.active_object
rot_h.data.body = "h"
rot_h.data.size = 0.42
rot_h.data.extrude = 0.02
rot_h.data.materials.append(M["ouro_brilho"])

# ---------- manômetro na parede ----------
GX, GZ, GY = 3.0, 1.7, 2.745
add(cil, "ouro", loc=(GX, 2.775, GZ), rot=(math.pi / 2, 0, 0), esc=(0.29, 0.29, 0.015), vertices=48)
add(cil, "visor", loc=(GX, 2.762, GZ), rot=(math.pi / 2, 0, 0), esc=(0.26, 0.26, 0.015), vertices=48)
for k in range(7):
    a = math.radians(-60 + 20 * k)
    mn = "t_verm" if k < 2 else ("t_amar" if k < 4 else "t_verde")
    add(cubo, mn, loc=(GX + 0.19 * math.sin(a), GY + 0.005, GZ + 0.19 * math.cos(a)),
        rot=(0, a, 0), esc=(0.014, 0.006, 0.032), size=2, liso=False)
pivo = bpy.data.objects.new("pivo", None)
scn.collection.objects.link(pivo)
pivo.location = (GX, GY - 0.005, GZ)
add(cubo, "ponteiro", loc=(0, 0, 0.085), esc=(0.013, 0.007, 0.095), size=2, pai=pivo, liso=False)
add(esf, "ouro", loc=(GX, GY - 0.012, GZ), esc=(0.03, 0.02, 0.03), segments=16, ring_count=10)

# ---------- mascote ----------
L.build_mascote(scn, (1.95, 2.0, 0), 20)

# ---------- água: pulsos no cano e gotas do chuveiro ----------
pulsos = []
for i in range(8):
    esf(location=(PX, PY, Z_DUCHA), radius=0.05, segments=12, ring_count=8)
    g = bpy.context.active_object
    g.data.materials.append(M["agua"])
    bpy.ops.object.shade_smooth()
    g.name = f"pulso_{i}"
    pulsos.append(g)

rnd = random.Random(21)
N_MAX = 120
gotas = []
for i in range(N_MAX):
    esf(location=(PX, 2.2, Z_DUCHA - 0.05), radius=0.042, segments=10, ring_count=8)
    g = bpy.context.active_object
    g.data.materials.append(M["agua"])
    bpy.ops.object.shade_smooth()
    g.name = f"gota_{i:03d}"
    g["fase"] = rnd.random()
    g["ang"] = rnd.random() * 2 * math.pi
    g["raio"] = rnd.random()
    gotas.append(g)

fase_p = [i / 8 for i in range(8)]
fase_g = [g["fase"] for g in gotas]

for f in range(1, TOTAL + 1):
    scn.frame_set(f)
    p = pressao(f)
    H = HMAX * p
    zb = LAJE_TOPO + H                              # base da caixa
    nivel = zb + NIVEL_REL                          # nível da água

    kf(raiz_tq, f, loc=(PX, PY, zb))
    for c in cols:
        kf(c, f, loc=(c.location.x, PY, LAJE_TOPO + max(H, 0.002) / 2),
           esc=(0.09, 0.09, max(H, 0.002) / 2))
    comp = zb - Z_DUCHA
    kf(cano, f, loc=(PX, PY, Z_DUCHA + comp / 2), esc=(0.04, 0.04, comp / 2))
    # marcador h
    hz0, hz1 = Z_DUCHA, nivel
    kf(linha, f, loc=(MX, MY, (hz0 + hz1) / 2), esc=(0.018, 0.018, (hz1 - hz0) / 2))
    kf(seta_c, f, loc=(MX, MY, hz1 - 0.06))
    kf(guia_c, f, loc=((MX + PX - 0.36) / 2, MY, hz1))
    kf(rot_h, f, loc=(MX - 0.42, MY, (hz0 + hz1) / 2 - 0.15))
    # manômetro
    kf(pivo, f, rot=(0, math.radians(-60 + 120 * p), 0))

    # pulsos de água descendo pelo cano (mais rápidos com mais pressão)
    vel = 0.020 + 0.050 * p
    for i, g in enumerate(pulsos):
        fase_p[i] = (fase_p[i] + vel) % 1.0
        s = fase_p[i]
        kf(g, f, loc=(PX, PY, zb - s * comp), esc=(1, 1, 1), interp="LINEAR")

    # gotas do chuveiro
    n_vis = int(8 + (N_MAX - 8) * p)
    dur = 50 - 34 * p
    largura = 0.12 + 0.34 * p
    for i, g in enumerate(gotas):
        fase_g[i] = (fase_g[i] + 1.0 / dur) % 1.0
        t = fase_g[i]
        if i >= n_vis:
            kf(g, f, loc=(PX, 2.2, Z_DUCHA - 0.05), esc=(0, 0, 0), interp="CONSTANT")
        else:
            r = (0.06 + 0.5 * g["raio"]) * largura * (0.4 + 2.2 * t)
            x = PX + math.cos(g["ang"]) * r
            y = 2.2 - 0.05 * t * 2 + math.sin(g["ang"]) * r * 0.45
            z = (Z_DUCHA - 0.05) - (Z_DUCHA - 0.05 - 0.02) * (t ** (1.6 - 0.35 * p))
            kf(g, f, loc=(x, y, z), esc=(0.8 + 0.4 * p, 0.8 + 0.4 * p, 1.1 + 3.0 * p), interp="CONSTANT")

# ---------- mundo, luzes ----------
w = bpy.data.worlds.new("mundo")
scn.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.10, 0.50, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0

bpy.ops.object.light_add(type="SUN", location=(4, -6, 8))
sol = bpy.context.active_object
sol.data.energy = 3.4
sol.data.color = (1.0, 0.95, 0.85)
sol.rotation_euler = (math.radians(50), math.radians(8), math.radians(25))

bpy.ops.object.light_add(type="AREA", location=(-3, -4, 3))
fill = bpy.context.active_object
fill.data.energy = 600
fill.data.size = 4
fill.data.color = (0.5, 0.7, 1.0)
fill.rotation_euler = (math.radians(75), 0, math.radians(-40))

bpy.ops.object.light_add(type="AREA", location=(1.7, 0.2, 2.4))
interna = bpy.context.active_object
interna.data.energy = 170
interna.data.size = 2.2
interna.data.color = (1.0, 0.95, 0.85)
interna.rotation_euler = (math.radians(90), 0, 0)

# ---------- câmera (muda só o enquadramento entre horizontal e vertical) ----------
alvo = bpy.data.objects.new("alvo", None)
scn.collection.objects.link(alvo)
bpy.ops.object.camera_add(location=(4.0, -9.0, 2.0))
cam = bpy.context.active_object
cam.data.lens = 35
tc = cam.constraints.new("TRACK_TO")
tc.target = alvo
tc.track_axis = "TRACK_NEGATIVE_Z"
tc.up_axis = "UP_Y"
scn.camera = cam

if FORMATO == "h":
    DIST, TZ0, TZ1, TX = 8.4, 1.6, 2.35, 2.35
    XOFF = 0.20
    DIST_F, TZ_F, TX_F, TY_F = 4.8, 1.75, 2.45, 2.2
    base_x, base_y = 1280, 720
else:
    DIST, TZ0, TZ1, TX = 8.6, 2.4, 2.7, 1.85
    XOFF = 0.10
    DIST_F, TZ_F, TX_F, TY_F = 4.8, 1.75, 2.4, 2.2
    base_x, base_y = 720, 1280

bpy.context.preferences.edit.keyframe_new_interpolation_type = "BEZIER"
for f in range(1, TOTAL + 1):
    p = pressao(f)
    tz = TZ0 + (TZ1 - TZ0) * p
    tx, ty, dist = TX, 1.4, DIST
    q = sm((f - 62) / 22.0)          # aproximação nos últimos quadros
    if q > 0:
        tz = tz + (TZ_F - tz) * q
        tx = tx + (TX_F - tx) * q
        ty = ty + (TY_F - ty) * q
        dist = dist + (DIST_F - dist) * q
    alvo.location = (tx, ty, tz)
    alvo.keyframe_insert("location", frame=f)
    cam.location = (tx + XOFF * dist, ty - dist, tz + 0.075 * dist)
    cam.keyframe_insert("location", frame=f)

# ---------- render ----------
scn.render.engine = "CYCLES"
try:
    scn.view_settings.view_transform = "AgX"
    scn.view_settings.look = "AgX - Punchy"
except Exception:
    try:
        scn.view_settings.look = "Punchy"
    except Exception:
        pass
scn.cycles.device = "CPU"
scn.cycles.samples = AMOSTRAS
scn.cycles.use_denoising = os.environ.get("DENOISE") == "1"
scn.cycles.max_bounces = 3
scn.cycles.transparent_max_bounces = 6
scn.render.resolution_x = int(base_x * RES)
scn.render.resolution_y = int(base_y * RES)
scn.render.resolution_percentage = 100
scn.render.image_settings.file_format = "PNG"

if MODO == "still":
    scn.frame_set(QUADRO)
    scn.render.filepath = SAIDA
    bpy.ops.render.render(write_still=True)
else:
    scn.frame_start, scn.frame_end = F_INI, F_FIM
    scn.render.filepath = SAIDA
    bpy.ops.render.render(animation=True)
