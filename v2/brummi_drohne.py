# -*- coding: utf-8 -*-
"""
BRUMMI – modulare Bausatz-Drohne für Kinder
Blender-Python-Skript (Phase 2: visuelles 3D-Designmodell) – Version 2 (gewichts- und schuboptimiert)

AENDERUNGEN v2 gegenueber v1 (Ergebnis der Flugpruefung vom 22.11.2026)
  1  Kaefigring: Wand 2,5 -> 1,2 mm, Innenradius 42,5 -> 41 mm (Spalt Propellerspitze 3,5 -> 2 mm), Hoehe bleibt 22 mm
  2  Kaefigring: obere Innenkante als Einlauflippe gerundet (R3)
  3  Gitter unten: Streben hochkant 1,6 x 3 mm statt flach 2,4 x 2 mm, Ring 1,2 mm breit
  4  Gitter oben: 8 Streben bleiben (Fingerschutz), hochkant 1,6 x 3 mm
  5  Kaefigstreben: 3 x 4,5 mm hochkant statt 4 x 4 mm (liegen bereits unter den unteren Gitterstreben)
  6  Stossfaenger: TPU-Profil 5,2 -> 4 mm
  7  Motorgondel als Topf (Wand 1,6 mm), Kaefigkragen 2 mm Wand, Motorabdeckung 1,2 mm Wand
  8  Rumpfschale: Wabentaschen auf der Unterseite
  9  Kanzel 0,8 mm statt 1,6 mm
 10  Landekufen: Rohr 6,4 -> 5 mm
 11  Akku-Schacht 34 x 70 x 15 mm fuer 2S 850 mAh (ca. 30 x 60 x 12,5 mm), Schublade als echte Wanne
  +  --stl ORDNER: exportiert alle Druckteile einzeln als STL (Masse in mm)

Getestet mit Blender 5.3 (Kommandozeile/headless). Geschrieben für Blender 4.2 LTS und neuer.

AUSFÜHREN
  A) In Blender:  Neue Datei -> Arbeitsbereich "Scripting" -> Text > Öffnen -> diese Datei -> "Run Script" (Alt+P).
     ACHTUNG: Das Skript leert die aktuelle Szene (CLEAR_SCENE = True).
  B) Kommandozeile (rendert alle 7 Ansichten automatisch):
     blender -b -P brummi_drohne.py -- --render ./renders --samples 128 --save ./brummi.blend --bom ./stueckliste.csv --stl ./stl

STEUERUNG IM MODELL
  Objekt "Steuerung_Explosion" (Collection 00_Studio) hat drei Regler (Eigenschaften-Editor > Objekt > Benutzerdefinierte Eigenschaften):
    Explosion   0..1  -> 0 = zusammengebaut, 1 = Explosionsdarstellung
    Montage     0..1  -> Bauabfolge: 0 = alle Teile ausgelegt, 1 = fertig montiert (Zeitleiste Bild 20-200 animiert)
    Baugruppen  0..1  -> 1 = Baugruppen (Rumpf, 4 Ausleger, Landegestell) getrennt, aber jeweils montiert
  Die Bewegung läuft über Treiber auf "Delta-Position". Die normale Position jedes Teils bleibt frei bearbeitbar.

Maßeinheit im Modell: Meter (Anzeige in mm). Alle Konstruktionsmaße unten sind in mm angegeben.
"""

import bpy
import bmesh
import math
import os
import sys
import csv
from mathutils import Vector, Matrix

# ----------------------------------------------------------------------------
# Einstellungen
# ----------------------------------------------------------------------------
CLEAR_SCENE = True
PRODUCT = "BRUMMI"
MM = 0.001                    # mm -> m
N_STEPS = 11                  # Montageschritte 0..10
ANIMATE_ASSEMBLY = True       # Zeitleiste animiert den Regler "Montage"
FRAME_START_ASM, FRAME_END_ASM, FRAME_END = 20, 200, 220

# Hauptmaße (mm)
HUB_R = 54.0                  # Eckradius Achteck-Rumpf
HUB_Z0, HUB_Z1 = 18.0, 46.0   # Unter-/Oberkante Rumpf
ARM_Z = 31.0                  # Mittelachse Ausleger
R_MOTOR = 105.0               # Abstand Rumpfmitte -> Motorachse
GUARD_RO, GUARD_RI = 42.2, 41.0   # v2: Wand 1,2 mm, Spalt zur Propellerspitze 2 mm
FLOOR_Z = -0.4

APOTHEM = HUB_R * math.cos(math.radians(22.5))   # Abstand Mitte -> Achteckfläche (~49.9)

# Ausleger: Nummer -> (Winkel°, Drehrichtung). Vorne = -Y.
ARMS = {
    1: (-45.0, "CW", "vorne_rechts"),
    2: (45.0, "CCW", "hinten_rechts"),
    3: (135.0, "CW", "hinten_links"),
    4: (225.0, "CCW", "vorne_links"),
}

# ----------------------------------------------------------------------------
# Hilfsfunktionen Geometrie (alles in mm, Umrechnung beim Objekt-Erzeugen)
# ----------------------------------------------------------------------------
I4 = Matrix.Identity(4)


def T(x=0.0, y=0.0, z=0.0):
    return Matrix.Translation((x, y, z))


def R(deg, axis):
    return Matrix.Rotation(math.radians(deg), 4, axis)


def S(x, y, z):
    return Matrix.Diagonal((x, y, z, 1.0))


def radial(angle, r, z):
    """Matrix: lokales +X zeigt radial nach aussen bei Winkel angle, Ursprung bei (r, z)."""
    return R(angle, 'Z') @ T(r, 0, z)


def xform(bm, m):
    bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
    return bm


def bevel_sharp(bm, offset, segs=3, angle=40.0):
    lim = math.radians(angle)
    edges = [e for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle(0.0) > lim]
    if edges and offset > 0:
        bmesh.ops.bevel(bm, geom=edges, offset=offset, offset_type='OFFSET', segments=segs,
                        profile=0.5, affect='EDGES', clamp_overlap=True)
    return bm


def box(dx, dy, dz, r=0.0, segs=3, m=I4):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(dx, dy, dz), verts=bm.verts)
    if r > 0:
        bevel_sharp(bm, r, segs)
    return xform(bm, m)


def cyl(r, h, segs=48, bev=0.0, bsegs=2, m=I4, r2=None):
    """Zylinder entlang Z, zentriert."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs,
                          radius1=r, radius2=(r if r2 is None else r2), depth=h)
    if bev > 0:
        bevel_sharp(bm, bev, bsegs)
    return xform(bm, m)


def tube(ro, ri, h, segs=48, bev=0.0, bsegs=2, m=I4):
    """Rohr / Ring entlang Z, zentriert."""
    bm = bmesh.new()
    rings = []
    for (rr, zz) in ((ro, -h / 2), (ro, h / 2), (ri, h / 2), (ri, -h / 2)):
        rings.append([bm.verts.new((rr * math.cos(2 * math.pi * i / segs),
                                    rr * math.sin(2 * math.pi * i / segs), zz)) for i in range(segs)])
    for k in range(4):
        a, b = rings[k], rings[(k + 1) % 4]
        for i in range(segs):
            j = (i + 1) % segs
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if bev > 0:
        bevel_sharp(bm, bev, bsegs)
    return xform(bm, m)


def torus(Rmaj, rmin, s1=64, s2=16, m=I4):
    bm = bmesh.new()
    vs = []
    for i in range(s1):
        a = 2 * math.pi * i / s1
        row = []
        for j in range(s2):
            b = 2 * math.pi * j / s2
            rr = Rmaj + rmin * math.cos(b)
            row.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), rmin * math.sin(b))))
        vs.append(row)
    for i in range(s1):
        for j in range(s2):
            i2, j2 = (i + 1) % s1, (j + 1) % s2
            bm.faces.new((vs[i][j], vs[i2][j], vs[i2][j2], vs[i][j2]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return xform(bm, m)


def sphere(r, m=I4, u=32, v=16):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=r)
    return xform(bm, m)


def dome(r, height, m=I4):
    """Obere Halbkugel (offen), auf height gestaucht."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=r)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=True)
    bmesh.ops.scale(bm, vec=(1, 1, height / r), verts=bm.verts)
    return xform(bm, m)


def octagon_prism(R_, z0, z1, vbevel, rbevel):
    bm = bmesh.new()
    bot, top = [], []
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        bot.append(bm.verts.new((R_ * math.cos(a), R_ * math.sin(a), z0)))
        top.append(bm.verts.new((R_ * math.cos(a), R_ * math.sin(a), z1)))
    bm.faces.new(list(reversed(bot)))
    bm.faces.new(top)
    for k in range(8):
        k2 = (k + 1) % 8
        bm.faces.new((bot[k], bot[k2], top[k2], top[k]))
    bm.edges.ensure_lookup_table()
    vert_edges = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) > 1e-6]
    bmesh.ops.bevel(bm, geom=vert_edges, offset=vbevel, offset_type='OFFSET', segments=6,
                    profile=0.5, affect='EDGES', clamp_overlap=True)
    bevel_sharp(bm, rbevel, 3)
    return bm


def merge(*bms):
    out = bmesh.new()
    for b in bms:
        vm = {v: out.verts.new(v.co) for v in b.verts}
        for f in b.faces:
            try:
                out.faces.new([vm[v] for v in f.verts])
            except ValueError:
                pass
        b.free()
    return out


def text_bm(body, size, depth):
    cu = bpy.data.curves.new("tmp_text", 'FONT')
    cu.body = body
    cu.size = size
    cu.extrude = depth / 2.0
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    ob = bpy.data.objects.new("tmp_text", cu)
    bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bm = bmesh.new()
    bm.from_mesh(me)
    bpy.data.objects.remove(ob, do_unlink=True)
    bpy.data.curves.remove(cu)
    bpy.data.meshes.remove(me)
    return bm


def curve_tube_bm(splines, radius, nurbs=False):
    """splines: Liste von Punktlisten (mm). Ergibt ein Rohr-Mesh als bmesh."""
    cu = bpy.data.curves.new("tmp_curve", 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = 4
    cu.use_fill_caps = True
    cu.resolution_u = 16
    for pts in splines:
        smooth = nurbs and len(pts) > 2
        sp = cu.splines.new('NURBS' if smooth else 'POLY')
        sp.points.add(len(pts) - 1)
        for p, c in zip(sp.points, pts):
            p.co = (c[0], c[1], c[2], 1.0)
        if smooth:
            sp.order_u = 3
            sp.use_endpoint_u = True
    ob = bpy.data.objects.new("tmp_curve", cu)
    bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bm = bmesh.new()
    bm.from_mesh(me)
    bpy.data.objects.remove(ob, do_unlink=True)
    bpy.data.curves.remove(cu)
    bpy.data.meshes.remove(me)
    return bm


# ----------------------------------------------------------------------------
# Szene, Collections, Materialien
# ----------------------------------------------------------------------------
def clear_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.curves, bpy.data.cameras,
                 bpy.data.lights, bpy.data.worlds):
        for block in list(coll):
            if block.users == 0:
                coll.remove(block)


def new_coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent.children if parent else bpy.context.scene.collection.children).link(c)
    return c


def set_input(node, names, value):
    for n in names:
        if n in node.inputs:
            try:
                node.inputs[n].default_value = value
                return True
            except Exception:
                pass
    return False


def make_mat(name, color, rough=0.35, metal=0.0, coat=0.0, transmission=0.0, ior=1.45,
             emission=None, strength=0.0):
    mat = bpy.data.materials.new(name)
    try:
        mat.use_nodes = True
    except Exception:
        pass
    mat.diffuse_color = (color[0], color[1], color[2], 1.0)   # Farbe in der Solid-Ansicht
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf is None:
        bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    set_input(bsdf, ["Base Color"], (color[0], color[1], color[2], 1.0))
    set_input(bsdf, ["Roughness"], rough)
    set_input(bsdf, ["Metallic"], metal)
    set_input(bsdf, ["Coat Weight", "Clearcoat"], coat)
    set_input(bsdf, ["Coat Roughness", "Clearcoat Roughness"], 0.08)
    set_input(bsdf, ["Transmission Weight", "Transmission"], transmission)
    set_input(bsdf, ["IOR"], ior)
    if emission:
        set_input(bsdf, ["Emission Color", "Emission"], (emission[0], emission[1], emission[2], 1.0))
        set_input(bsdf, ["Emission Strength"], strength)
    if transmission > 0:
        for attr, val in (("surface_render_method", 'BLENDED'), ("blend_method", 'BLEND')):
            try:
                setattr(mat, attr, val)
            except Exception:
                pass
        mat.diffuse_color = (color[0], color[1], color[2], 0.35)
    return mat


MATS = {}


def build_materials():
    MATS["weiss"] = make_mat("M_Weiss_Struktur", (0.80, 0.81, 0.82), 0.32, coat=0.25)
    MATS["graphit"] = make_mat("M_Graphit_Struktur", (0.035, 0.038, 0.045), 0.42, coat=0.15)
    MATS["orange"] = make_mat("M_Orange_Verbindung", (1.0, 0.27, 0.02), 0.30, coat=0.35)
    MATS["tuerkis"] = make_mat("M_Tuerkis_Elektronik", (0.0, 0.40, 0.44), 0.30, coat=0.3)
    MATS["CW"] = make_mat("M_Gelb_Rotor_CW", (1.0, 0.66, 0.0), 0.30, coat=0.3)
    MATS["CCW"] = make_mat("M_Violett_Rotor_CCW", (0.28, 0.09, 0.72), 0.30, coat=0.3)
    MATS["glas"] = make_mat("M_Kanzel_Klar_getoent", (0.78, 0.93, 0.95), 0.03, transmission=1.0, ior=1.5)
    MATS["tpu"] = make_mat("M_TPU_Soft_Grip", (0.02, 0.02, 0.022), 0.85)
    MATS["metall"] = make_mat("M_Metall_Motor", (0.75, 0.76, 0.78), 0.28, metal=1.0)
    MATS["akku"] = make_mat("M_Akku_Pack", (0.03, 0.06, 0.16), 0.5)
    MATS["led"] = make_mat("M_LED_Tuerkis_leuchtend", (0.1, 1.0, 0.9), 0.3,
                           emission=(0.1, 1.0, 0.85), strength=8.0)
    MATS["studio"] = make_mat("M_Studio_Hohlkehle", (0.16, 0.18, 0.21), 0.65)


# ----------------------------------------------------------------------------
# Bauteil-Registrierung
# ----------------------------------------------------------------------------
PARTS = []      # (obj, explode_comps, group_vec)
CTRL = None


def make_part(name, bm, coll, mat, *, nr, baugruppe, verbindung, funktion, fertigung,
              explode=(), group=(0, 0, 0), cutters=None, solidify=None, smooth_angle=35.0, note=""):
    """bm in mm, Welt-Koordinaten. Ergebnis: Mesh-Objekt mit Ursprung in der Bauteilmitte."""
    bmesh.ops.scale(bm, vec=(MM, MM, MM), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if mat:
        me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)

    tmp = None
    if cutters:
        cb = merge(*cutters)
        bmesh.ops.scale(cb, vec=(MM, MM, MM), verts=cb.verts)
        cme = bpy.data.meshes.new("tmp_cutter")
        cb.to_mesh(cme)
        cb.free()
        tmp = bpy.data.objects.new("tmp_cutter", cme)
        coll.objects.link(tmp)
        mod = ob.modifiers.new("Bool", 'BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = tmp
        try:
            mod.solver = 'EXACT'
        except Exception:
            pass
    if solidify:
        mod = ob.modifiers.new("Solid", 'SOLIDIFY')
        mod.thickness = solidify * MM
        mod.offset = -1.0
    if ob.modifiers:
        dg = bpy.context.evaluated_depsgraph_get()
        new_me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        ob.modifiers.clear()
        old = ob.data
        ob.data = new_me
        bpy.data.meshes.remove(old)
        new_me.name = name
        if tmp:
            bpy.data.objects.remove(tmp, do_unlink=True)
            bpy.data.meshes.remove(cme)
        me = new_me

    # Ursprung in die Bauteilmitte
    if len(me.vertices):
        xs = [v.co for v in me.vertices]
        c = Vector((sum((v.x for v in xs)) / len(xs), sum((v.y for v in xs)) / len(xs), 0))
        lo = min(v.z for v in xs)
        hi = max(v.z for v in xs)
        c.z = (lo + hi) / 2
        mn = Vector((min(v.x for v in xs), min(v.y for v in xs), lo))
        mx = Vector((max(v.x for v in xs), max(v.y for v in xs), hi))
        c = (mn + mx) / 2
        me.transform(Matrix.Translation(-c))
        ob.location = c

    # Glatte Schattierung mit harten Kanten ab smooth_angle
    bm2 = bmesh.new()
    bm2.from_mesh(me)
    lim = math.radians(smooth_angle)
    for f in bm2.faces:
        f.smooth = True
    for e in bm2.edges:
        if len(e.link_faces) == 2:
            e.smooth = e.calc_face_angle(0.0) < lim
        else:
            e.smooth = False
    bm2.to_mesh(me)
    bm2.free()
    if hasattr(me, "use_auto_smooth"):
        me.use_auto_smooth = True

    ob["Bauteil_Nr"] = nr
    ob["Baugruppe"] = baugruppe
    ob["Verbindung"] = verbindung
    ob["Funktion"] = funktion
    ob["Fertigung"] = fertigung
    ob["Material"] = mat.name if mat else ""
    if note:
        ob["Hinweis"] = note
    PARTS.append((ob, list(explode), tuple(group)))
    return ob


def u_vec(angle, length):
    a = math.radians(angle)
    return (math.cos(a) * length, math.sin(a) * length, 0.0)


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


# ----------------------------------------------------------------------------
# Baugruppe Rumpf
# ----------------------------------------------------------------------------
def build_hub(C):
    W, G = MATS["weiss"], MATS["graphit"]
    BG = "Rumpf"

    # Rumpfschale mit Taschen fuer Power-Core, Akku-Schublade, Bajonett-Buchsen, Rastpins
    shell = octagon_prism(HUB_R, HUB_Z0, HUB_Z1, vbevel=9.0, rbevel=3.0)
    cutters = [box(38, 30, 14, m=T(0, 0, 43)),                    # Power-Core-Schacht
               box(34, 70, 15, m=T(0, 21, 26.7))]                 # Akku-Schacht v2 (von hinten, 2S 850 mAh)
    for (hx, hy) in ((30, 12), (30, -12), (-30, 12), (-30, -12), (0, -27), (17, -27), (-17, -27)):
        cutters.append(cyl(6.5, 10, 6, m=T(hx, hy, HUB_Z0)))   # v2: Wabentaschen Unterseite (5 mm tief)
    for k, (ang, _, _) in ARMS.items():
        cutters.append(cyl(7.6, 16, 32, m=radial(ang, 48, ARM_Z) @ R(90, 'Y')))   # Bajonett-Oeffnung
    for sx in (-1, 1):
        for sy in (-1, 1):
            cutters.append(cyl(3.2, 13, 24, m=T(32 * sx, 30 * sy, 23.5)))         # Rastpin-Loecher unten
    make_part("R01_Rumpfschale", shell, C["rumpf"], W, nr="R01", baugruppe=BG,
              verbindung="Bajonett-Buchsen (4x), Rastpin-Aufnahmen (4x), Schnapp-Clip-Rand",
              funktion="mechanisch (tragend)", fertigung="FDM PETG/ASA, 2 Halbschalen in Fusion",
              cutters=cutters)

    # Power-Core: werkseitig vergossenes Elektronikmodul (Flugsteuerung, ESC, Funk)
    core = box(36, 28, 14, r=3.0, m=T(0, 0, 43))
    for sx in (-1, 1):                           # Kuehlrippen-Andeutung
        for i in range(4):
            core = merge(core, box(1.2, 18, 1.2, r=0.4, m=T(sx * (9 + i * 2.4), 0, 50.2)))
    make_part("R02_Power_Core_Elektronik", core, C["rumpf"], MATS["tuerkis"], nr="R02", baugruppe=BG,
              verbindung="Schnapp-Clip in Schacht + Federkontakte", funktion="mechanisch + elektrisch",
              fertigung="Kaufteil/Spritzguss, werkseitig geschlossen",
              explode=[((0, 0, 60), 1)], note="Kinder oeffnen dieses Modul nicht")
    make_part("R03_Status_LED", cyl(4.0, 1.2, 32, bev=0.4, m=T(0, 0, 50.4)), C["deko"], MATS["led"],
              nr="R03", baugruppe=BG, verbindung="Teil von R02", funktion="optisch / Statusanzeige",
              fertigung="Lichtleiter klar", explode=[((0, 0, 60), 1), ((0, 0, 8), 1)])

    # Akku-Schublade (hinten, +Y)
    tray = merge(box(33, 63, 1.2, r=0.4, m=T(0, 18.5, 20.0)),                 # v2: Wanne, Boden 1,2 mm
                 box(1.2, 63, 8, r=0.4, m=T(15.9, 18.5, 24.0)),
                 box(1.2, 63, 8, r=0.4, m=T(-15.9, 18.5, 24.0)),
                 box(33, 1.2, 8, r=0.4, m=T(0, -12.4, 24.0)),
                 box(33, 4, 14.5, r=1.6, m=T(0, APOTHEM + 2.0, 26.7)))
    make_part("R04_Akku_Schublade", tray, C["rumpf"], MATS["tuerkis"], nr="R04", baugruppe=BG,
              verbindung="Schublade + Akku-Riegel (Schnapp-Clip)", funktion="mechanisch",
              fertigung="FDM PETG (V-0 Material pruefen)", explode=[((0, 95, 0), 2)])
    make_part("R05_Akku_Pack", box(30, 60, 12.5, r=1.5, m=T(0, 19.0, 26.9)), C["rumpf"], MATS["akku"],
              nr="R05", baugruppe=BG, verbindung="liegt in Schublade, Steckkontakte",
              funktion="elektrisch", fertigung="Kaufteil: LiPo 2S 850 mAh mit Schutzschaltung (ca. 30 x 60 x 12,5 mm)",
              explode=[((0, 95, 0), 2), ((0, 0, 22), 2)])

    # Kanzel
    make_part("R06_Kanzelring", tube(38, 33, 3, 64, bev=0.8, m=T(0, 0, 47.5)), C["rumpf"], G,
              nr="R06", baugruppe=BG, verbindung="4x Schnapp-Clip", funktion="mechanisch",
              fertigung="FDM PETG", explode=[((0, 0, 95), 4)])
    make_part("R07_Kanzel_transparent", dome(33, 18, m=T(0, 0, 48.5)), C["rumpf"], MATS["glas"],
              nr="R07", baugruppe=BG, verbindung="im Kanzelring eingeclipst",
              funktion="optisch + Schutz", fertigung="PETG klar / tiefgezogenes PC",
              explode=[((0, 0, 125), 4)], solidify=0.8, smooth_angle=60)   # v2: 0,8 mm

    # Seitenblenden (Wabenmuster) rechts, links, vorne
    for nm, ang in (("rechts", 0.0), ("links", 180.0), ("vorne", -90.0)):
        base = radial(ang, APOTHEM + 1.0, 32.0)
        pb = box(3, 20, 15, r=1.2, m=base)
        if nm != "vorne":
            for (ty, tz) in ((-6, 3.2), (0, 3.2), (6, 3.2), (-3, -2.2), (3, -2.2)):
                pb = merge(pb, cyl(2.3, 1.6, 6, bev=0.3, m=base @ T(1.6, ty, tz) @ R(90, 'Y') @ R(30, 'Z')))
        n = u_vec(ang, 1)
        make_part(f"R08_Seitenblende_{nm}", pb, C["deko"], G, nr="R08", baugruppe=BG,
                  verbindung="Schnapp-Clip (2 Rastnasen)", funktion="optisch (Wechselblende)",
                  fertigung="FDM PETG", explode=[(tuple(c * 35 for c in n), 3)])
        if nm == "vorne":
            eyes = merge(box(2, 6.5, 3.6, r=1.0, m=base @ T(1.8, -5.0, 1.0)),
                         box(2, 6.5, 3.6, r=1.0, m=base @ T(1.8, 5.0, 1.0)))
            make_part("R09_LED_Visier_vorne", eyes, C["deko"], MATS["led"], nr="R09", baugruppe=BG,
                      verbindung="in Seitenblende vorne eingelegt", funktion="optisch / Flugrichtung",
                      fertigung="Lichtleiter", explode=[(tuple(c * 35 for c in n), 3), (tuple(c * 14 for c in n), 3)])

    # Nummernschilder + Ziffern auf der Rumpfoberseite (Farbe = Drehrichtung)
    for k, (ang, rot, pos) in ARMS.items():
        p = radial(ang, 43.5, HUB_Z1 + 0.5)
        make_part(f"R1{k}_Nummernschild_{k}", cyl(4.2, 1.2, 32, bev=0.35, m=p), C["deko"], MATS[rot],
                  nr=f"R1{k}", baugruppe=BG, verbindung="eingelegt", funktion="optisch / Montagehilfe",
                  fertigung="FDM, Farbe = Drehrichtung", explode=[((0, 0, 14), 0)])
        make_part(f"R2{k}_Ziffer_{k}", xform(text_bm(str(k), 5.5, 0.8), p @ T(0, 0, 0.9) @ R(90, 'Z')),
                  C["deko"], W, nr=f"R2{k}", baugruppe=BG, verbindung="Teil des Schilds",
                  funktion="optisch / Montagehilfe", fertigung="Mehrfarbdruck/Praegung",
                  explode=[((0, 0, 20), 0)])


# ----------------------------------------------------------------------------
# Verbindungselemente am Rumpf
# ----------------------------------------------------------------------------
def build_hub_connectors(C):
    O = MATS["orange"]
    for k, (ang, _, _) in ARMS.items():
        m = radial(ang, APOTHEM + 0.5, ARM_Z) @ R(90, 'Y')
        sock = tube(10.5, 7.6, 4, 48, bev=0.6, m=m)
        for s in (-1, 1):     # Bajonett-Rastnasen (L-Nut-Andeutung)
            sock = merge(sock, box(2.0, 3.0, 2.2, r=0.5, m=radial(ang, APOTHEM + 2.2, ARM_Z + s * 9.0)))
        make_part(f"V0{k}_Bajonett_Buchse_{k}", sock, C["verb"], O, nr=f"V0{k}", baugruppe="Rumpf",
                  verbindung="Twist-Lock-Bajonett (Typ A)", funktion="mechanisch (tragend) + elektrisch",
                  fertigung="Einlegeteil PA/POM oder FDM PETG", explode=[(u_vec(ang, 22), 0)])

    for i, ang in enumerate((0, 90, 180, 270)):
        clip = merge(box(3.5, 7, 6, r=1.2, m=radial(ang, 39.2, 47.5)),
                     box(1.6, 5, 1.6, r=0.5, m=radial(ang, 41.0, 45.4)))
        n = u_vec(ang, 1)
        make_part(f"V2{i + 1}_Schnappclip_Kanzel_{i + 1}", clip, C["verb"], O, nr=f"V2{i + 1}",
                  baugruppe="Rumpf", verbindung="Schnapp-Clip (Typ C)", funktion="mechanisch",
                  fertigung="angeformt am Kanzelring (FDM PETG)",
                  explode=[((0, 0, 95), 4), (tuple(c * 12 for c in n), 4)])

    make_part("V25_Akku_Riegel", box(9, 2.5, 3.5, r=0.9, m=T(0, APOTHEM + 5.2, 26.7)), C["verb"], O,
              nr="V25", baugruppe="Rumpf", verbindung="Schnapp-Clip mit Schiebeverriegelung (Typ C)",
              funktion="mechanisch / Kindersicherung", fertigung="FDM PETG",
              explode=[((0, 95, 0), 2), ((0, 14, 0), 2)])


# ----------------------------------------------------------------------------
# Baugruppe Ausleger (4x identisch, Farbe je Drehrichtung)
# ----------------------------------------------------------------------------
def build_arm(C, k):
    ang, rot, pos = ARMS[k]
    coll = C[f"arm{k}"]
    BG = f"Ausleger_{k}"
    G, W, O, RC = MATS["graphit"], MATS["weiss"], MATS["orange"], MATS[rot]
    A = lambda r, z=ARM_Z: radial(ang, r, z)                  # noqa: E731
    M = radial(ang, R_MOTOR, 0.0)                              # lokales System an der Motorachse
    U = lambda l: u_vec(ang, l)                                # noqa: E731
    Z = lambda l: (0.0, 0.0, l)                                # noqa: E731
    out = [(U(142), 7)]                                        # Motorende fliegt in Explosion weiter raus
    grp = U(120)

    # Traeger mit Bajonett-Hals und Wabenausschnitten
    beam = merge(box(38, 16, 12, r=4.5, segs=4, m=A(79)),
                 cyl(6.8, 18, 40, bev=0.8, m=A(53) @ R(90, 'Y')))
    for s in (-1, 1):
        beam = merge(beam, box(4, 4, 2.2, r=0.6, m=A(46.5, ARM_Z + s * 7.6)))      # Bajonett-Nocken
    hexes = [cyl(4.0, 20, 6, m=A(rr) @ R(30, 'Z')) for rr in (75, 86)]
    make_part(f"A{k}_01_Auslegertraeger", beam, coll, G, nr=f"A{k}-01", baugruppe=BG,
              verbindung="Bajonett-Stecker (Typ A) zum Rumpf", funktion="mechanisch (tragend)",
              fertigung="FDM PETG/ASA, Rippen in Fusion", explode=[(U(120), 7)], group=grp, cutters=hexes)

    # Drehring (orange) – unverlierbar auf dem Hals, Vierteldrehung bis Klick
    ring = tube(10.0, 7.0, 7, 48, bev=0.8, m=A(56.1) @ R(90, 'Y'))
    for i in range(10):
        ring = merge(ring, box(7, 1.6, 1.6, r=0.5, m=A(56.1) @ R(36 * i, 'X') @ T(0, 0, 10.2)))
    make_part(f"V0{4 + k}_Drehring_Ausleger_{k}", ring, C["verb"], O, nr=f"V0{4 + k}", baugruppe=BG,
              verbindung="Twist-Lock-Bajonett (Typ A), 90 Grad mit Rastklick",
              funktion="mechanisch (Verriegelung) + Sicherheitsschalter", fertigung="FDM PETG / POM",
              explode=[(U(92), 7)], group=grp)

    make_part(f"A{k}_02_Nummernschild_{k}", cyl(3.8, 1.2, 32, bev=0.35, m=A(65, ARM_Z + 6.5)), C["deko"], RC,
              nr=f"A{k}-02", baugruppe=BG, verbindung="eingelegt", funktion="optisch / Montagehilfe",
              fertigung="FDM", explode=[(U(120), 7), (Z(12), 7)], group=grp)
    make_part(f"A{k}_03_Ziffer_{k}", xform(text_bm(str(k), 5.0, 0.8), A(65, ARM_Z + 7.4) @ R(90, 'Z')),
              C["deko"], W, nr=f"A{k}-03", baugruppe=BG, verbindung="Teil des Schilds",
              funktion="optisch / Montagehilfe", fertigung="Mehrfarbdruck",
              explode=[(U(120), 7), (Z(18), 7)], group=grp)

    # Motorgondel, Motor, Motorabdeckung
    gondel = merge(tube(14, 12.4, 26, 48, bev=0.6, m=M @ T(0, 0, 27)),          # v2: Topf, Wand 1,6 mm
                   cyl(14, 2.4, 48, bev=0.8, m=M @ T(0, 0, 40.8)))                # Motorplatte oben
    make_part(f"A{k}_04_Motorgondel", gondel, coll, G,
              nr=f"A{k}-04", baugruppe=BG, verbindung="werkseitig verschraubt + 2 Rastpin-Aufnahmen",
              funktion="mechanisch", fertigung="FDM PETG", explode=out, group=grp)
    motor = merge(cyl(10.5, 9, 48, bev=1.0, m=M @ T(0, 0, 46.5)), cyl(1.5, 6, 16, m=M @ T(0, 0, 53.5)))
    make_part(f"A{k}_05_Motor", motor, coll, MATS["metall"], nr=f"A{k}-05", baugruppe=BG,
              verbindung="werkseitig verschraubt (nicht fuer Kinder)", funktion="elektrisch / Antrieb",
              fertigung="Kaufteil", explode=out + [(Z(20), 7)], group=grp)
    vents = [box(4, 2.6, 4, m=M @ R(30 + 60 * i, 'Z') @ T(12.6, 0, 44.5)) for i in range(6)]
    make_part(f"A{k}_06_Motorabdeckung_{rot}", tube(14.5, 13.3, 9, 48, bev=0.5, m=M @ T(0, 0, 44.5)), coll, RC,
              nr=f"A{k}-06", baugruppe=BG, verbindung="Schnapp-Clip (Typ C)", funktion="optisch + Beruehrschutz",
              fertigung="FDM PETG, Farbe = Drehrichtung", explode=out + [(Z(40), 8)], group=grp, cutters=vents)

    # Propellerschutz-Kaefig
    # v2: Ring 1,2 mm Wand, Einlauflippe oben innen, Streben hochkant (weniger Abschattung, gleiche Steifigkeit)
    g = tube(GUARD_RO, GUARD_RI, 22, 96, bev=0.4, m=M @ T(0, 0, 57))
    g = merge(g, torus(GUARD_RI + 0.4, 1.5, 96, 12, m=M @ T(0, 0, 66.6)))   # Einlauflippe (R ~3 mm gerundete Kante)
    lr, lo = GUARD_RI - 0.3, 9.3                                            # Strebenlaenge bis in den Ring
    for i in range(8):                                     # Gitter oben: 8 Lamellen 1,6 x 3 mm
        g = merge(g, box(lr - lo, 1.6, 3, r=0.5, m=M @ R(22.5 + 45 * i, 'Z') @ T((lr + lo) / 2, 0, 66.5)))
    g = merge(g, tube(10.5, 9.3, 3, 48, m=M @ T(0, 0, 66.5)), tube(27.1, 25.9, 3, 72, m=M @ T(0, 0, 66.5)))
    for i in range(6):                                     # Gitter unten: 6 Lamellen 1,6 x 3 mm
        g = merge(g, box(lr - 17, 1.6, 3, r=0.5, m=M @ R(60 * i, 'Z') @ T((lr + 17) / 2, 0, 47.5)))
    g = merge(g, tube(27.1, 25.9, 3, 72, m=M @ T(0, 0, 47.5)))
    for i in range(3):                                     # Streben 3 x 4,5 hochkant (unter den Gitterstreben 0/120/240 Grad)
        g = merge(g, box(GUARD_RO - 14.2, 3, 4.5, r=1.0, m=M @ R(120 * i, 'Z') @ T((GUARD_RO + 14.2) / 2, 0, 18.5)),
                  box(3.5, 3.5, 28.5, r=1.0, m=M @ R(120 * i, 'Z') @ T(GUARD_RO - 1.75, 0, 32.75)))
    g = merge(g, tube(16.2, 14.2, 7, 48, bev=0.6, m=M @ T(0, 0, 18.5)))   # Kragen, Wand 2 mm
    make_part(f"A{k}_07_Propellerschutz", g, coll, W, nr=f"A{k}-07", baugruppe=BG,
              verbindung="2x Rastpin (Typ B) an der Motorgondel", funktion="mechanisch + Sicherheit",
              fertigung="FDM PETG, Gitterweite in Fusion pruefen", explode=out + [(Z(62), 9)], group=grp)
    make_part(f"A{k}_08_Stossfaenger", torus(GUARD_RO + 1.2, 2.0, 96, 16, m=M @ T(0, 0, 57)), coll, MATS["tpu"],
              nr=f"A{k}-08", baugruppe=BG, verbindung="aufgezogen (elastisch)", funktion="mechanisch / Aufprallschutz",
              fertigung="FDM TPU 95A", explode=out + [(Z(88), 9)], group=grp)
    for side, nm in ((1, "a"), (-1, "b")):
        pin = merge(cyl(3.0, 10, 24, bev=0.6, m=T(0, 0, 5)), cyl(4.6, 2, 32, bev=0.6, m=T(0, 0, 11)))
        pin = xform(pin, M @ T(0, side * 7.5, 18.5) @ R(-90 * side, 'X'))
        t = (-math.sin(math.radians(ang)) * side * 14, math.cos(math.radians(ang)) * side * 14, 0)
        make_part(f"V{9 + (k - 1) * 2 + (0 if nm == 'a' else 1):02d}_Rastpin_Schutz_{k}{nm}", pin, C["verb"], O,
                  nr="V09-16", baugruppe=BG, verbindung="Rastpin (Typ B), unverlierbar",
                  funktion="mechanisch", fertigung="FDM PETG / Spritzguss POM",
                  explode=out + [(Z(62), 9), (t, 9)], group=grp)

    # Propeller + Propellerkappe
    pitch = 16 if rot == "CW" else -16
    prop = cyl(5, 5, 32, bev=0.8, m=M @ T(0, 0, 54))
    for b in (0, 180):
        blade = sphere(1.0, m=M @ T(0, 0, 54) @ R(b, 'Z') @ R(pitch, 'X') @ T(21, 0, 0) @ S(18, 5.5, 1.3))
        prop = merge(prop, blade)
    make_part(f"A{k}_09_Propeller_{rot}", prop, coll, RC, nr=f"A{k}-09", baugruppe=BG,
              verbindung="auf Welle gesteckt, gesichert durch Kappe", funktion="Antrieb (Gefahrenbereich)",
              fertigung="Spritzguss PP/flexibel – nicht drucken", explode=out + [(Z(115), 10)], group=grp,
              smooth_angle=70)
    make_part(f"A{k}_10_Propellerkappe_{rot}", sphere(5.5, m=M @ T(0, 0, 57) @ S(1, 1, 1.0)), coll, RC,
              nr=f"A{k}-10", baugruppe=BG, verbindung="Schraubkappe, nur mit Werkzeug (Erwachsene)",
              funktion="mechanisch", fertigung="Kaufteil/Spritzguss", explode=out + [(Z(135), 10)], group=grp,
              smooth_angle=80)


# ----------------------------------------------------------------------------
# Baugruppe Landegestell
# ----------------------------------------------------------------------------
def build_landing(C):
    for s, nm in ((1, "rechts"), (-1, "links")):
        x = 46 * s
        runner = [(x, -55, 10), (x, -52, 5.5), (x, -46, 3.5), (x, 46, 3.5), (x, 52, 5.5), (x, 55, 10)]
        posts = [[(45 * s, y, 3.5), (32 * s, y, 13)] for y in (-30, 30)]
        sk = merge(curve_tube_bm([runner], 2.5, nurbs=True), curve_tube_bm(posts, 2.5))   # v2: Rohr 5 mm
        for y in (-30, 30):
            sk = merge(sk, cyl(5.5, 4, 32, bev=0.8, m=T(32 * s, y, 14)))
        grp = (s * 30, -165, -75)
        make_part(f"L0{1 if s > 0 else 2}_Landekufe_{nm}", sk, C["land"], MATS["weiss"],
                  nr=f"L0{1 if s > 0 else 2}", baugruppe="Landegestell", verbindung="2x Rastpin (Typ B) in Rumpf",
                  funktion="mechanisch (tragend, federnd)", fertigung="FDM PETG oder PA",
                  explode=[((0, 0, -45), 5), ((s * 18, 0, 0), 5)], group=grp)
        for j, y in enumerate((-22, 22)):
            make_part(f"L0{3 + j + (0 if s > 0 else 2)}_Kufengummi_{nm}_{j + 1}",
                      cyl(3.3, 24, 32, bev=1.0, m=T(x, y, 3.5) @ R(90, 'X')), C["land"], MATS["tpu"],
                      nr="L03-06", baugruppe="Landegestell", verbindung="aufgeschoben", funktion="mechanisch / Rutschschutz",
                      fertigung="FDM TPU", explode=[((0, 0, -45), 5), ((s * 18, 0, 0), 5)], group=grp)
        for j, y in enumerate((-30, 30)):
            pin = merge(cyl(3.0, 12, 24, bev=0.6, m=T(32 * s, y, 24)), cyl(5.5, 2, 32, bev=0.6, m=T(32 * s, y, 17)))
            idx = 17 + j + (0 if s > 0 else 2)
            make_part(f"V{idx}_Rastpin_Kufe_{nm}_{j + 1}", pin, C["verb"], MATS["orange"], nr=f"V{idx}",
                      baugruppe="Landegestell", verbindung="Rastpin (Typ B), unverlierbar", funktion="mechanisch",
                      fertigung="FDM PETG / Spritzguss POM", explode=[((0, 0, -22), 5)], group=grp)


# ----------------------------------------------------------------------------
# Treiber: Explosion / Montage / Baugruppen
# ----------------------------------------------------------------------------
LIFT_EXPLODE = (0, 0, 55)
LIFT_GROUP = (0, 0, 80)


def build_controller(C):
    global CTRL
    CTRL = bpy.data.objects.new("Steuerung_Explosion", None)
    CTRL.empty_display_type = 'ARROWS'
    CTRL.empty_display_size = 0.03
    CTRL.location = (0, 0, 0.12)
    C["studio"].objects.link(CTRL)
    for nm, val, desc in (("Explosion", 0.0, "0 = montiert, 1 = Explosionsdarstellung"),
                          ("Montage", 1.0, "0 = Teile ausgelegt, 1 = fertig montiert"),
                          ("Baugruppen", 0.0, "1 = Baugruppen getrennt darstellen")):
        CTRL[nm] = val
        try:
            CTRL.id_properties_ui(nm).update(min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, description=desc)
        except Exception:
            pass


def add_drivers():
    simple_ok = True
    for ob, comps, grp in PARTS:
        comps = comps + [(LIFT_EXPLODE, 5)]
        grp = add(grp, LIFT_GROUP)
        for axis in range(3):
            by_step = {}
            for vec, s in comps:
                if abs(vec[axis]) > 1e-9:
                    by_step[s] = by_step.get(s, 0.0) + vec[axis]
            terms = [f"({c * MM:.6f})*max(e,1-min(max(m*{N_STEPS}-{s},0),1))" for s, c in sorted(by_step.items())]
            if abs(grp[axis]) > 1e-9:
                terms.append(f"({grp[axis] * MM:.6f})*g")
            if not terms:
                continue
            fc = ob.driver_add("delta_location", axis)
            d = fc.driver
            d.type = 'SCRIPTED'
            for vn, prop in (("e", "Explosion"), ("m", "Montage"), ("g", "Baugruppen")):
                v = d.variables.new()
                v.name = vn
                v.type = 'SINGLE_PROP'
                v.targets[0].id_type = 'OBJECT'
                v.targets[0].id = CTRL
                v.targets[0].data_path = f'["{prop}"]'
            d.expression = " + ".join(terms)
            if hasattr(d, "is_simple_expression") and not d.is_simple_expression:
                simple_ok = False
    if not simple_ok:
        print("HINWEIS: Treiber benoetigen 'Auto Run Python Scripts' (Einstellungen > Speichern & Laden).")


def animate_assembly():
    if not ANIMATE_ASSEMBLY:
        return
    scn = bpy.context.scene
    prefs = bpy.context.preferences.edit
    old = prefs.keyframe_new_interpolation_type
    prefs.keyframe_new_interpolation_type = 'LINEAR'
    CTRL["Montage"] = 0.0
    CTRL.keyframe_insert(data_path='["Montage"]', frame=FRAME_START_ASM)
    CTRL["Montage"] = 1.0
    CTRL.keyframe_insert(data_path='["Montage"]', frame=FRAME_END_ASM)
    prefs.keyframe_new_interpolation_type = old
    scn.frame_start = 1
    scn.frame_end = FRAME_END
    scn.frame_set(FRAME_END)


def set_state(explosion=0.0, montage=1.0, groups=0.0):
    scn = bpy.context.scene
    CTRL["Explosion"] = explosion
    CTRL["Baugruppen"] = groups
    CTRL["Montage"] = montage
    if ANIMATE_ASSEMBLY:
        f = FRAME_START_ASM + montage * (FRAME_END_ASM - FRAME_START_ASM)
        scn.frame_set(int(f), subframe=f - int(f))
    CTRL.update_tag()
    for ob, _, _ in PARTS:
        ob.update_tag()
    bpy.context.view_layer.update()


# ----------------------------------------------------------------------------
# Studio: Hohlkehle, Licht, Kameras, Render
# ----------------------------------------------------------------------------
def build_studio(C):
    # Hohlkehle (Boden + gerundete Rueckwand)
    bm = bmesh.new()
    prof = [(-2.0, 0.0)]
    for i in range(13):
        a = math.radians(90 * i / 12)
        prof.append((0.6 + 0.5 * math.sin(a), 0.5 - 0.5 * math.cos(a)))
    prof.append((1.1, 2.0))
    left = [bm.verts.new((-2.5, y, z + FLOOR_Z * MM)) for y, z in prof]
    right = [bm.verts.new((2.5, y, z + FLOOR_Z * MM)) for y, z in prof]
    for i in range(len(prof) - 1):
        bm.faces.new((left[i], right[i], right[i + 1], left[i + 1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        f.smooth = True
    me = bpy.data.meshes.new("Studio_Hohlkehle")
    bm.to_mesh(me)
    bm.free()
    if me.polygons[0].normal.z < 0:
        me.flip_normals()
    me.materials.append(MATS["studio"])
    ob = bpy.data.objects.new("Studio_Hohlkehle", me)
    C["studio"].objects.link(ob)

    # Welt
    world = bpy.data.worlds.new("Studio_Welt")
    bpy.context.scene.world = world
    try:
        world.use_nodes = True
    except Exception:
        pass
    bg = next((n for n in world.node_tree.nodes if n.type == 'BACKGROUND'), None)
    if bg:
        bg.inputs[0].default_value = (0.55, 0.6, 0.68, 1.0)
        bg.inputs[1].default_value = 0.15

    def area(name, loc, energy, size, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, 'AREA')
        ld.energy = energy
        ld.size = size
        ld.color = color
        lo = bpy.data.objects.new(name, ld)
        lo.location = loc
        d = Vector((0, 0, 0.04)) - Vector(loc)
        lo.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        C["studio"].objects.link(lo)
        return lo

    area("Licht_Key", (-0.55, -0.65, 0.75), 45, 0.6, (1.0, 0.97, 0.93))
    area("Licht_Fill", (0.75, -0.45, 0.35), 15, 0.8, (0.92, 0.96, 1.0))
    area("Licht_Rim", (0.25, 0.85, 0.6), 40, 0.5)
    area("Licht_Top", (0.0, 0.0, 1.0), 20, 1.0)


CAMERAS = {
    # Name: (Blickrichtung vom Ziel zur Kamera, Brennweite, orthografisch)
    "Kamera_01_Produkt": ((0.95, -1.35, 0.72), 70, False),
    "Kamera_02_Front": ((0.0, -1.0, 0.16), 85, False),
    "Kamera_03_Draufsicht": ((0.0, 0.0, 1.0), 50, True),
    "Kamera_04_Seite": ((1.0, 0.0, 0.0), 50, True),
    "Kamera_05_Explosion": ((1.0, -1.25, 0.95), 50, False),
    "Kamera_06_Baugruppen": ((0.75, -1.2, 1.15), 50, False),
    "Kamera_07_Montage": ((-1.05, -1.3, 0.75), 50, False),
}


def build_cameras(C):
    for name, (d, lens, ortho) in CAMERAS.items():
        cd = bpy.data.cameras.new(name)
        cd.lens = lens
        cd.clip_start = 0.005
        cd.clip_end = 50
        if ortho:
            cd.type = 'ORTHO'
        co = bpy.data.objects.new(name, cd)
        C["studio"].objects.link(co)
        if name.endswith("Draufsicht"):
            co.rotation_euler = (0, 0, 0)
        elif name.endswith("Seite"):
            co.rotation_euler = (math.radians(86), 0, math.radians(90))   # 4° erhöht, damit der Boden sichtbar bleibt
        else:
            co.rotation_euler = Vector(d).normalized().to_track_quat('Z', 'Y').to_euler()
        co.location = Vector(d).normalized() * 0.8


def drone_bbox_points():
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for ob, _, _ in PARTS:
        ev = ob.evaluated_get(dg)
        mw = ev.matrix_world
        for c in ev.bound_box:
            pts.append(mw @ Vector(c))
    return pts


def fit_camera(cam, margin=1.12):
    dg = bpy.context.evaluated_depsgraph_get()
    pts = drone_bbox_points()
    flat = [c for p in pts for c in p]
    co, scale = cam.camera_fit_coords(dg, flat)
    if cam.data.type == 'ORTHO':
        cam.data.ortho_scale = scale * margin
        fwd = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
        cam.location = Vector(co) - fwd * 0.45
    else:
        center = sum(pts, Vector()) / len(pts)
        cam.location = center + (Vector(co) - center) * margin


VIEWS = [
    # Dateiname, Kamera, Explosion, Montage, Baugruppen
    ("01_Produkt_Rendering", "Kamera_01_Produkt", 0.0, 1.0, 0.0),
    ("02_Perspektive_vorne", "Kamera_02_Front", 0.0, 1.0, 0.0),
    ("03_Draufsicht", "Kamera_03_Draufsicht", 0.0, 1.0, 0.0),
    ("04_Seitenansicht", "Kamera_04_Seite", 0.0, 1.0, 0.0),
    ("05_Explosionsdarstellung", "Kamera_05_Explosion", 1.0, 1.0, 0.0),
    ("06_Baugruppen", "Kamera_06_Baugruppen", 0.0, 1.0, 1.0),
    ("07_Zusammenbau", "Kamera_07_Montage", 0.0, 0.72, 0.0),
]


def setup_render(engine="CYCLES", samples=128, res_pct=100):
    scn = bpy.context.scene
    r = scn.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = 1920, 1200, res_pct
    if engine.upper().startswith("EEVEE"):
        for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                r.engine = e
                break
            except TypeError:
                continue
    else:
        r.engine = 'CYCLES'
        scn.cycles.samples = samples
        try:
            scn.cycles.use_denoising = True
        except Exception:
            pass
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            for t in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
                try:
                    prefs.compute_device_type = t
                    prefs.get_devices()
                    if any(d.type == t for d in prefs.devices):
                        for d in prefs.devices:
                            d.use = True
                        scn.cycles.device = 'GPU'
                        break
                except Exception:
                    continue
        except Exception:
            pass
    for vt in ("AgX", "Filmic"):
        try:
            scn.view_settings.view_transform = vt
            break
        except TypeError:
            continue
    for look in ("AgX - Punchy", "AgX - Medium High Contrast"):
        try:
            scn.view_settings.look = look
            break
        except TypeError:
            continue
    scn.view_settings.exposure = -0.3
    scn.unit_settings.system = 'METRIC'
    scn.unit_settings.length_unit = 'MILLIMETERS'


def render_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    scn = bpy.context.scene
    studio = None
    for fname, cam_name, e, m, g in VIEWS:
        set_state(e, m, g)
        cam = bpy.data.objects[cam_name]
        fit_camera(cam)
        scn.camera = cam
        # Hohlkehle immer hinter das Motiv drehen (Seitenansicht: Blick von +X)
        studio = bpy.data.objects.get("Studio_Hohlkehle")
        if studio:
            studio.rotation_euler = (0, 0, math.radians(90) if cam_name.endswith("Seite") else 0)
        scn.render.filepath = os.path.join(outdir, fname + ".png")
        print("Rendere", fname, "...", flush=True)
        bpy.ops.render.render(write_still=True)
    if studio:
        studio.rotation_euler = (0, 0, 0)
    set_state(0.0, 1.0, 0.0)


def prefit_cameras():
    """Kameras im Modell so ausrichten, dass sie im jeweiligen Zustand passen."""
    for fname, cam_name, e, m, g in VIEWS:
        set_state(e, m, g)
        fit_camera(bpy.data.objects[cam_name])
    set_state(0.0, 1.0, 0.0)
    bpy.context.scene.camera = bpy.data.objects["Kamera_01_Produkt"]


def write_bom(path):
    rows = []
    for ob, _, _ in PARTS:
        dims = [round(d * 1000, 1) for d in ob.dimensions]
        rows.append([ob.get("Bauteil_Nr"), ob.name, ob.get("Baugruppe"), ob.users_collection[0].name,
                     ob.get("Material"), ob.get("Fertigung"), ob.get("Verbindung"), ob.get("Funktion"),
                     f"{dims[0]} x {dims[1]} x {dims[2]}", ob.get("Hinweis", "")])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["Nr", "Objekt", "Baugruppe", "Collection", "Material (Blender)", "Fertigung",
                    "Verbindung", "Funktion", "Abmessung X x Y x Z (mm)", "Hinweis"])
        w.writerows(rows)


# ----------------------------------------------------------------------------
# STL-Export der Druckteile (v2)
# ----------------------------------------------------------------------------
# Datei-Name -> (Objekte, die zu einem Druckteil verschmolzen werden, Drehwinkel um Z zum Ausrichten, Anzahl, Material)
PRINT_PARTS = [
    ("R01_Rumpfschale",            ["R01_Rumpfschale"], 0, 1, "PETG weiss"),
    ("R04_Akku_Schublade",         ["R04_Akku_Schublade"], 0, 1, "PETG tuerkis"),
    ("R06_Kanzelring_mit_Clips",   ["R06_Kanzelring", "V21_Schnappclip_Kanzel_1", "V22_Schnappclip_Kanzel_2",
                                    "V23_Schnappclip_Kanzel_3", "V24_Schnappclip_Kanzel_4"], 0, 1, "PETG graphit + orange (AMS)"),
    ("R07_Kanzel",                 ["R07_Kanzel_transparent"], 0, 1, "PETG transparent"),
    ("R08_Seitenblende_rechts",    ["R08_Seitenblende_rechts"], 0, 1, "PETG graphit"),
    ("R08_Seitenblende_links",     ["R08_Seitenblende_links"], 0, 1, "PETG graphit"),
    ("R08_Seitenblende_vorne",     ["R08_Seitenblende_vorne"], 0, 1, "PETG graphit"),
    ("R09_LED_Visier",             ["R09_LED_Visier_vorne"], 0, 1, "PETG transparent"),
    ("R11_Nummernschild_CW",       ["R11_Nummernschild_1"], 0, 2, "PLA/PETG gelb"),
    ("R12_Nummernschild_CCW",      ["R12_Nummernschild_2"], 0, 2, "PLA/PETG violett"),
    ("V01_Bajonett_Buchse",        ["V01_Bajonett_Buchse_1"], 45, 4, "PETG orange"),
    ("V25_Akku_Riegel",            ["V25_Akku_Riegel"], 0, 1, "PETG orange"),
    ("A_01_Auslegertraeger",       ["A1_01_Auslegertraeger"], 45, 4, "PETG graphit"),
    ("V05_Drehring",               ["V05_Drehring_Ausleger_1"], 45, 4, "PETG orange"),
    ("A_02_Nummernschild_CW",      ["A1_02_Nummernschild_1"], 0, 2, "PLA/PETG gelb"),
    ("A_02_Nummernschild_CCW",     ["A2_02_Nummernschild_2"], 0, 2, "PLA/PETG violett"),
    ("A_04_Motorgondel",           ["A1_04_Motorgondel"], 45, 4, "PETG graphit"),
    ("A_06_Motorabdeckung_CW",     ["A1_06_Motorabdeckung_CW"], 45, 2, "PETG gelb"),
    ("A_06_Motorabdeckung_CCW",    ["A2_06_Motorabdeckung_CCW"], -45, 2, "PETG violett"),
    ("A_07_Propellerschutz",       ["A1_07_Propellerschutz"], 45, 4, "PETG weiss"),
    ("A_08_Stossfaenger",          ["A1_08_Stossfaenger"], 45, 4, "TPU 95A schwarz"),
    ("V09_Rastpin_Kaefig",         ["V09_Rastpin_Schutz_1a"], 0, 8, "PETG orange"),
    ("L01_Landekufe_rechts",       ["L01_Landekufe_rechts"], 0, 1, "PETG weiss"),
    ("L02_Landekufe_links",        ["L02_Landekufe_links"], 0, 1, "PETG weiss"),
    ("L03_Kufengummi",             ["L03_Kufengummi_rechts_1"], 0, 4, "TPU 95A schwarz"),
    ("V17_Rastpin_Kufe",           ["V17_Rastpin_Kufe_rechts_1"], 0, 4, "PETG orange"),
]


def export_stl(outdir):
    """Exportiert jedes Druckteil einzeln (Binaer-STL, mm, Unterseite auf z = 0, mittig)."""
    import struct
    os.makedirs(outdir, exist_ok=True)
    set_state(0.0, 1.0, 0.0)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    rows = []
    for fname, names, rot, count, mat in PRINT_PARTS:
        tris = []
        for nm in names:
            ob = bpy.data.objects[nm]
            me = ob.evaluated_get(dg).to_mesh()
            mw = Matrix.Rotation(math.radians(-rot), 4, 'Z') @ ob.matrix_world
            me.calc_loop_triangles()
            for t in me.loop_triangles:
                tris.append([(mw @ me.vertices[i].co) * 1000.0 for i in t.vertices])
            ob.evaluated_get(dg).to_mesh_clear()
        xs = [v.x for t in tris for v in t]; ys = [v.y for t in tris for v in t]; zs = [v.z for t in tris for v in t]
        off = Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, min(zs)))
        path = os.path.join(outdir, fname + ".stl")
        with open(path, "wb") as fh:
            fh.write((b"BRUMMI v2 " + fname.encode("ascii"))[:80].ljust(80, b" "))
            fh.write(struct.pack("<I", len(tris)))
            for t in tris:
                a, b, c = (v - off for v in t)
                n = (b - a).cross(c - a)
                n = n.normalized() if n.length > 0 else n
                fh.write(struct.pack("<12fH", n.x, n.y, n.z, a.x, a.y, a.z, b.x, b.y, b.z, c.x, c.y, c.z, 0))
        dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
        rows.append([fname + ".stl", count, mat, "%.1f x %.1f x %.1f" % dims])
        print("STL", fname, count, "x", flush=True)
    with open(os.path.join(outdir, "00_Druckteile.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["Datei", "Anzahl", "Material/Farbe", "Abmessung X x Y x Z (mm)"])
        w.writerows(rows)


def tune_viewport():
    try:
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for sp in area.spaces:
                        if sp.type == 'VIEW_3D':
                            sp.clip_start = 0.001
                            sp.clip_end = 100
                            sp.shading.color_type = 'MATERIAL'
    except Exception:
        pass


# ----------------------------------------------------------------------------
# Hauptprogramm
# ----------------------------------------------------------------------------
def main(argv):
    if CLEAR_SCENE:
        clear_scene()
    scn = bpy.context.scene
    PARTS.clear()

    root = new_coll(f"{PRODUCT}_Bausatz_Drohne")
    C = {
        "studio": new_coll("00_Studio_Kamera_Licht"),
        "rumpf": new_coll("10_Rumpf", root),
        "arm1": new_coll("21_Ausleger_1_vorne_rechts", root),
        "arm2": new_coll("22_Ausleger_2_hinten_rechts", root),
        "arm3": new_coll("23_Ausleger_3_hinten_links", root),
        "arm4": new_coll("24_Ausleger_4_vorne_links", root),
        "land": new_coll("30_Landegestell", root),
        "verb": new_coll("40_Verbindungselemente_orange", root),
        "deko": new_coll("50_Deko_Abdeckungen_Licht", root),
    }

    build_materials()
    build_controller(C)
    build_hub(C)
    build_hub_connectors(C)
    for k in ARMS:
        build_arm(C, k)
    build_landing(C)
    add_drivers()
    build_studio(C)
    build_cameras(C)

    args = argv[argv.index("--") + 1:] if "--" in argv else []

    def arg(name, default=None):
        return args[args.index(name) + 1] if name in args else default

    setup_render(engine=arg("--engine", "CYCLES"), samples=int(arg("--samples", 128)),
                 res_pct=int(arg("--res-pct", 100)))
    animate_assembly()
    prefit_cameras()
    tune_viewport()
    print(f"{PRODUCT}: {len(PARTS)} Bauteile erzeugt.")

    if arg("--bom"):
        write_bom(os.path.abspath(arg("--bom")))
    if arg("--save"):
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(arg("--save")))
    if arg("--stl"):
        export_stl(os.path.abspath(arg("--stl")))
    if arg("--render"):
        render_all(os.path.abspath(arg("--render")))


if __name__ == "__main__":
    main(sys.argv)
