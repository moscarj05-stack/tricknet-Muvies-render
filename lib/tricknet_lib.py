import bpy, math, random
from mathutils import Vector

M = {}

cil = bpy.ops.mesh.primitive_cylinder_add
esf = bpy.ops.mesh.primitive_uv_sphere_add
cubo = bpy.ops.mesh.primitive_cube_add
cone = bpy.ops.mesh.primitive_cone_add


def mat(nome, cor, rough=0.45, metal=0.0, emissao=0.0, emi_cor=None, alpha=1.0):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*cor, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Alpha"].default_value = alpha
    if emissao > 0:
        b.inputs["Emission Color"].default_value = (*(emi_cor or cor), 1)
        b.inputs["Emission Strength"].default_value = emissao
    return m


def make_materials():
    M.update({
        "parede":  mat("parede",  (0.02, 0.16, 0.62), 0.35),
        "rejunte": mat("rejunte", (1.00, 0.68, 0.08), 0.28, 0.9),
        "piso":    mat("piso",    (0.60, 0.30, 0.03), 0.30),
        "cromo":   mat("cromo",   (0.92, 0.93, 0.97), 0.12, 1.0),
        "polo":    mat("polo",    (0.02, 0.05, 0.24), 0.55),
        "colarinho": mat("colarinho", (0.04, 0.09, 0.36), 0.55),
        "branco":  mat("branco",  (0.95, 0.95, 0.95), 0.5),
        "calca":   mat("calca",   (0.08, 0.09, 0.14), 0.55),
        "sapato":  mat("sapato",  (0.03, 0.03, 0.04), 0.4),
        "pele":    mat("pele",    (0.96, 0.62, 0.40), 0.40),
        "cabelo":  mat("cabelo",  (0.30, 0.13, 0.05), 0.35),
        "preto":   mat("preto",   (0.01, 0.01, 0.015), 0.08),
        "brilho":  mat("brilho",  (1, 1, 1), 0.2, 0.0, 3.0),
        "boca":    mat("boca",    (0.65, 0.04, 0.06), 0.35),
        "ouro":    mat("ouro",    (1.00, 0.72, 0.10), 0.22, 1.0),
        "ouro_brilho": mat("ouro_brilho", (1.0, 0.75, 0.10), 0.3, 0.0, 2.4, (1.0, 0.72, 0.08)),
        "agua":    mat("agua",    (0.05, 0.50, 1.00), 0.10, 0.0, 0.9, (0.10, 0.60, 1.0)),
        "registro": mat("registro", (0.95, 0.08, 0.15), 0.28),
        # casa e instalação
        "terreno": mat("terreno", (0.04, 0.30, 0.12), 0.8),
        "casa":    mat("casa",    (0.90, 0.40, 0.07), 0.6),
        "laje":    mat("laje",    (0.40, 0.46, 0.58), 0.7),
        "pvc":     mat("pvc",     (0.55, 0.27, 0.08), 0.35),
        "tanque":  mat("tanque",  (0.05, 0.35, 1.00), 0.15, 0.0, 0.0, None, 0.35),
        "tampa":   mat("tampa",   (0.02, 0.12, 0.60), 0.3),
        "agua_tq": mat("agua_tq", (0.05, 0.60, 1.00), 0.1, 0.0, 0.6, (0.10, 0.70, 1.0), 0.9),
        "visor":   mat("visor",   (0.96, 0.97, 1.00), 0.3),
        "t_verm":  mat("t_verm",  (0.90, 0.10, 0.10), 0.4),
        "t_amar":  mat("t_amar",  (1.00, 0.80, 0.05), 0.4),
        "t_verde": mat("t_verde", (0.10, 0.75, 0.20), 0.4),
        "ponteiro": mat("ponteiro", (0.95, 0.05, 0.10), 0.3, 0.0, 0.5),
    })


def add(op, mat_nome, loc=(0, 0, 0), rot=(0, 0, 0), esc=(1, 1, 1), nome=None, pai=None, liso=True, **kw):
    op(location=loc, rotation=rot, **kw)
    o = bpy.context.active_object
    o.scale = esc
    o.data.materials.append(M[mat_nome])
    if liso:
        bpy.ops.object.shade_smooth()
    if nome:
        o.name = nome
    if pai:
        o.parent = pai
    return o


def entre(p1, p2, raio, mat_nome, pai=None, seg=20):
    a, b = Vector(p1), Vector(p2)
    d = b - a
    o = add(cil, mat_nome, loc=tuple((a + b) / 2), esc=(raio, raio, d.length / 2), vertices=seg, pai=pai)
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    return o


def build_mascote(scn, pos, yaw_graus):
    """Mascote TrickNet: boneco de brinquedo, polo azul-marinho, joinha. Frente voltada para -Y."""
    raiz = bpy.data.objects.new("mascote", None)
    scn.collection.objects.link(raiz)
    raiz.location = pos
    raiz.rotation_euler = (0, 0, math.radians(yaw_graus))

    for sx in (-1, 1):
        add(cil, "calca", loc=(sx * 0.11, 0, 0.32), esc=(0.10, 0.10, 0.32), vertices=24, pai=raiz)
        add(cubo, "sapato", loc=(sx * 0.11, -0.04, 0.04), esc=(0.11, 0.17, 0.05), size=2, pai=raiz)

    tronco = add(cubo, "polo", loc=(0, 0, 0.86), esc=(0.275, 0.18, 0.28), size=2, pai=raiz, nome="tronco")
    bv = tronco.modifiers.new("bv", "BEVEL")
    bv.width = 0.07
    bv.segments = 5
    bpy.ops.object.shade_smooth()

    add(cil, "branco", loc=(0, 0, 1.17), esc=(0.075, 0.075, 0.06), vertices=24, pai=raiz)
    for sx in (-1, 1):
        add(cubo, "colarinho", loc=(sx * 0.085, -0.17, 1.12), rot=(0, sx * math.radians(25), 0),
            esc=(0.075, 0.02, 0.07), size=2, pai=raiz, liso=False)
    for k in range(2):
        add(cil, "branco", loc=(0, -0.205, 1.04 - k * 0.07), rot=(math.pi / 2, 0, 0),
            esc=(0.014, 0.014, 0.008), vertices=12, pai=raiz)

    # emblema TRICKNET
    add(cil, "ouro", loc=(0.14, -0.208, 0.93), rot=(math.pi / 2, 0, 0), esc=(0.085, 0.085, 0.012), vertices=40, pai=raiz)
    add(cil, "polo", loc=(0.14, -0.222, 0.93), rot=(math.pi / 2, 0, 0), esc=(0.07, 0.07, 0.012), vertices=40, pai=raiz)
    bpy.ops.object.text_add(location=(0.14, -0.236, 0.925), rotation=(math.pi / 2, 0, 0))
    txt = bpy.context.active_object
    txt.data.body = "TRICKNET"
    txt.data.size = 0.03
    txt.data.align_x = "CENTER"
    txt.data.align_y = "CENTER"
    txt.data.extrude = 0.002
    txt.data.materials.append(M["ouro"])
    txt.parent = raiz
    add(cubo, "ouro", loc=(0.14, -0.234, 0.885), esc=(0.03, 0.003, 0.012), size=2, pai=raiz, liso=False)

    # cabeça
    CZ = 1.46
    add(esf, "pele", loc=(0, 0, CZ), esc=(0.275, 0.255, 0.28), segments=48, ring_count=24, pai=raiz, nome="cabeca")
    for sx in (-1, 1):
        add(esf, "pele", loc=(sx * 0.275, 0.0, CZ - 0.02), esc=(0.03, 0.045, 0.05), segments=16, ring_count=8, pai=raiz)
        add(esf, "preto", loc=(sx * 0.10, -0.235, CZ + 0.01), esc=(0.042, 0.03, 0.058), segments=24, ring_count=16, pai=raiz)
        add(esf, "brilho", loc=(sx * 0.10 - 0.012, -0.262, CZ + 0.035), esc=(0.013, 0.008, 0.016), segments=12, ring_count=8, pai=raiz)
        add(cubo, "cabelo", loc=(sx * 0.105, -0.24, CZ + 0.095), rot=(0, sx * math.radians(12), 0),
            esc=(0.055, 0.012, 0.014), size=2, pai=raiz)
    add(esf, "pele", loc=(0, -0.262, CZ - 0.04), esc=(0.026, 0.022, 0.024), segments=16, ring_count=8, pai=raiz)
    add(esf, "boca", loc=(0, -0.232, CZ - 0.125), esc=(0.095, 0.03, 0.058), segments=32, ring_count=16, pai=raiz)
    add(esf, "pele", loc=(0, -0.250, CZ - 0.092), esc=(0.105, 0.03, 0.05), segments=32, ring_count=16, pai=raiz)
    add(esf, "brilho", loc=(0, -0.246, CZ - 0.150), esc=(0.05, 0.012, 0.012), segments=16, ring_count=8, pai=raiz)

    # cabelo
    add(esf, "cabelo", loc=(0, 0.05, CZ + 0.09), esc=(0.30, 0.27, 0.24), segments=32, ring_count=16, pai=raiz)
    rnd = random.Random(5)
    for _ in range(34):
        th = rnd.uniform(0, 2 * math.pi)
        ph = math.radians(rnd.uniform(8, 78))
        px = 0.30 * math.sin(ph) * math.cos(th)
        py = 0.28 * math.sin(ph) * math.sin(th) + 0.02
        pz = CZ + 0.10 + 0.27 * math.cos(ph)
        if py < -0.08 and pz < CZ + 0.17:
            continue
        r = rnd.uniform(0.085, 0.125)
        add(esf, "cabelo", loc=(px, py, pz), esc=(r, r * 0.95, r * 0.9), segments=16, ring_count=10, pai=raiz)
    for (fx, fz, fr) in [(-0.17, 0.205, 0.085), (-0.07, 0.235, 0.095), (0.04, 0.245, 0.10),
                         (0.14, 0.225, 0.095), (0.22, 0.18, 0.08)]:
        add(esf, "cabelo", loc=(fx, -0.19, CZ + fz), esc=(fr, fr * 0.9, fr * 0.85), segments=16, ring_count=10, pai=raiz)

    # braços
    entre((-0.31, 0, 1.08), (-0.37, 0, 0.78), 0.075, "polo", raiz)
    add(esf, "pele", loc=(-0.37, 0, 0.66), esc=(0.075, 0.075, 0.085), segments=20, ring_count=12, pai=raiz)
    entre((0.31, 0, 1.08), (0.42, -0.20, 0.96), 0.075, "polo", raiz)
    entre((0.42, -0.20, 0.96), (0.40, -0.40, 1.04), 0.062, "pele", raiz)
    add(esf, "pele", loc=(0.40, -0.45, 1.07), esc=(0.105, 0.095, 0.10), segments=24, ring_count=16, pai=raiz, nome="mao")
    entre((0.40, -0.45, 1.10), (0.40, -0.45, 1.27), 0.036, "pele", raiz)
    add(esf, "pele", loc=(0.40, -0.45, 1.285), esc=(0.040, 0.040, 0.040), segments=16, ring_count=10, pai=raiz)
    return raiz
