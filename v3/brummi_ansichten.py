# -*- coding: utf-8 -*-
"""
BRUMMI – Ansichtsmodi (Blender-Add-on)

Erweitert das BESTEHENDE BRUMMI-v3-Modell um umschaltbare Ansichten. Das Add-on veraendert
keine Geometrie, keine Position, kein Material und loescht nichts. Es schaltet ausschliesslich
die Sichtbarkeit der Bauteile um (Auge im Outliner + Kamera-Symbol fuers Rendern) und optional
die Viewport-Darstellung (Drahtgitter) der Rumpfschale. "Full View" stellt den Originalzustand
jederzeit wieder her.

Ansichten (3D-Viewport > Seitenleiste N > Reiter "BRUMMI"):
  Full View         komplettes Modell wie gebaut (Originalzustand)
  Technical View    ohne Verkleidung/Deko: Kanzel + Kanzelring + Kanzel-Clips, Seitenblenden,
                    LED-Visier, Nummernschilder/Ziffern, Motorabdeckungen
  Structural View   Rumpfschale, Akku-Schublade, Ausleger, Motorgondeln, Propellerschutz,
                    Stossfaenger, Landegestell, Bajonette, Drehringe, Rastpins, Schrauben, Stack-Hardware
  Electronics View  ESC, Flugsteuerung, Magnetometer, Empfaenger, Kondensator, XT30, Akku,
                    Akku- und Motorkabel, Status-LED
  Propulsion View   Motoren, Propeller, Propellerkappen, Motorschrauben, Motorgondeln, Motorkabel
  Bauteile          Component Isolation: jedes Bauteil einzeln ein-/ausblenden oder isolieren

INSTALLATION
  A) Einfach: brummi_v3_ansichten.blend oeffnen. Das Add-on steckt als Text "brummi_ansichten.py"
     in der Datei. Wenn Blender fragt "Automatische Ausfuehrung von Python-Skripten erlauben" ->
     "Erlauben". Sonst: Arbeitsbereich Scripting > Text "brummi_ansichten.py" > Run Script (Alt+P).
  B) Dauerhaft fuer jede Datei: Bearbeiten > Einstellungen > Add-ons > Pfeil oben rechts >
     "Von Festplatte installieren..." > diese .py-Datei waehlen > Haken setzen.

Getestet mit Blender 5.3. Geschrieben fuer Blender 4.2 LTS und neuer.
"""

bl_info = {
    "name": "BRUMMI Ansichtsmodi",
    "author": "BRUMMI-Projekt",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "3D-Viewport > Seitenleiste (N) > BRUMMI",
    "description": "Full/Technical/Structural/Electronics/Propulsion View und Bauteil-Isolation "
                   "fuer das BRUMMI-Modell, ohne das Modell zu veraendern",
    "category": "3D View",
}

import json
import re

import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty, PointerProperty, StringProperty

ROOT_COLLECTION = "BRUMMI_Bausatz_Drohne"     # nur Objekte darunter werden umgeschaltet
CONTROLLER = "Steuerung_Explosion"
SNAPSHOT_KEY = "brummi_ansicht_original"      # Originalzustand (JSON) in den Szenen-Eigenschaften
FRAME_ASSEMBLED = 200                         # Montage-Animation: ab Bild 200 fertig montiert

# ----------------------------------------------------------------------------
# Kategorien
# ----------------------------------------------------------------------------
# Kuerzel -> Anzeigename
CATEGORIES = {
    "VERK": "Verkleidung / Deko",
    "STRU": "Struktur",
    "ELEK": "Elektronik",
    "ANTR": "Antrieb",
    "INNE": "Innenausbau",
}

# Zuordnung ueber den Objektnamen (Bauteilnummer aus der Stueckliste). Ein Teil kann in mehreren
# Kategorien stehen (z. B. Motorgondel = Struktur + Antrieb, Motorkabel = Elektronik + Antrieb).
RULES = [
    # Verkleidung, kosmetische und nicht tragende Designteile
    (r"^R07_", {"VERK"}),                       # Kanzel (Haube)
    (r"^R06_", {"VERK"}),                       # Kanzelring (traegt nur die Kanzel)
    (r"^V2[1-4]_Schnappclip_Kanzel", {"VERK"}),
    (r"^R08_", {"VERK"}),                       # Seitenblenden (Wechselblenden)
    (r"^R09_", {"VERK"}),                       # LED-Visier / Lichtleiter
    (r"^R1[1-4]_", {"VERK"}),                   # Nummernschilder Rumpf
    (r"^R2[1-4]_", {"VERK"}),                   # Ziffern Rumpf
    (r"^A\d_0[23]_", {"VERK"}),                 # Nummernschild + Ziffer Ausleger
    (r"^A\d_06_", {"VERK"}),                    # Motorabdeckung (Optik + Beruehrschutz)
    # Struktur: Rahmen, Arme, Verbindungen, tragende Elemente
    (r"^R01_", {"STRU"}),                       # Rumpfschale
    (r"^R04_", {"STRU"}),                       # Akku-Schublade
    (r"^A\d_01_", {"STRU"}),                    # Auslegertraeger
    (r"^A\d_04_", {"STRU", "ANTR"}),            # Motorgondel (Motorhalter)
    (r"^A\d_07_", {"STRU"}),                    # Propellerschutz
    (r"^A\d_08_", {"STRU"}),                    # Stossfaenger
    (r"^A\d_12_", {"STRU"}),                    # Schrauben Gondel
    (r"^V(0[1-9]|1\d|20)_", {"STRU"}),          # Bajonette, Drehringe, Rastpins
    (r"^V25_", {"STRU"}),                       # Akku-Riegel
    (r"^L\d\d_", {"STRU"}),                     # Landekufen + Gummis
    (r"^S0[12]_", {"STRU"}),                    # Schrauben Stack / Schublade
    (r"^E0[456]_", {"STRU"}),                   # Daempfer, Abstandshalter, Abstandsbolzen
    # Elektronik, Stromversorgung, Verkabelung
    (r"^E0[1237]_", {"ELEK"}),                  # ESC, FC, Magnetometer, Empfaenger
    (r"^E0[89]_", {"ELEK"}),                    # Kondensator, XT30-Buchse
    (r"^E1[02]_", {"ELEK"}),                    # Akkukabel, XT30-Stecker
    (r"^E11_", {"ELEK", "ANTR"}),               # Motorkabel
    (r"^R03_", {"ELEK"}),                       # Status-LED
    (r"^R05_", {"ELEK"}),                       # Akku-Pack
    # Antrieb
    (r"^A\d_05_", {"ANTR"}),                    # Motor
    (r"^A\d_09_", {"ANTR"}),                    # Propeller
    (r"^A\d_10_", {"ANTR"}),                    # Propellerkappe
    (r"^A\d_11_", {"ANTR"}),                    # Motorschrauben
    # Innenausbau ohne eigene Funktion fuer Struktur/Elektronik/Antrieb
    (r"^E13_", {"INNE"}),                       # Schaumpad
]
_RULES = [(re.compile(p), cats) for p, cats in RULES]

# Ansicht -> Kategorien, die sichtbar sind (None = alles / Originalzustand)
VIEWS = {
    "FULL": None,
    "TECHNICAL": {"STRU", "ELEK", "ANTR", "INNE", "?"},
    "STRUCTURAL": {"STRU"},
    "ELECTRONICS": {"ELEK"},
    "PROPULSION": {"ANTR"},
}
VIEW_ITEMS = [
    ("FULL", "Full View", "Komplettes Modell im Originalzustand", "SHADING_RENDERED", 0),
    ("TECHNICAL", "Technical View", "Ohne Verkleidung, kosmetische Teile und Deko", "MODIFIER", 1),
    ("STRUCTURAL", "Structural View", "Rahmen, Arme, Verbindungen, tragende Teile", "MOD_LATTICE", 2),
    ("ELECTRONICS", "Electronics View", "Elektronik, Stromversorgung, Verkabelung", "PLUGIN", 3),
    ("PROPULSION", "Propulsion View", "Motoren, Propeller und Zubehoer", "FORCE_WIND", 4),
    ("CUSTOM", "Eigene Auswahl", "Durch Bauteil-Isolation angepasst", "RESTRICT_SELECT_OFF", 5),
]
WIRE_PARTS = re.compile(r"^(R01_|R04_)")    # Huelle, die optional als Drahtgitter gezeigt wird


def categories_of(ob):
    cats = set()
    for rx, c in _RULES:
        if rx.match(ob.name):
            cats |= c
    return cats or {"?"}    # unbekannte Teile: in Full + Technical sichtbar, nie stillschweigend weg


def drone_objects():
    coll = bpy.data.collections.get(ROOT_COLLECTION)
    if coll is None:
        return []
    return sorted(set(coll.all_objects), key=lambda o: o.name)


def is_drone_object(ob):
    coll = bpy.data.collections.get(ROOT_COLLECTION)
    return coll is not None and ob.name in coll.all_objects


# ----------------------------------------------------------------------------
# Sichtbarkeit (einzige Stelle, die etwas am Modell umschaltet)
# ----------------------------------------------------------------------------
def _hidden(ob, view_layer):
    try:
        return ob.hide_get(view_layer=view_layer)
    except RuntimeError:          # Objekt nicht in dieser View-Layer
        return False


def set_visible(ob, visible, context, include_render):
    try:
        ob.hide_set(not visible, view_layer=context.view_layer)
    except RuntimeError:
        pass
    if include_render:
        ob.hide_render = not visible


def take_snapshot(scene, view_layer, force=False):
    """Originalzustand einmalig merken, bevor das Add-on zum ersten Mal etwas umschaltet."""
    if SNAPSHOT_KEY in scene.keys() and not force:
        return
    data = {ob.name: [_hidden(ob, view_layer), ob.hide_viewport, ob.hide_render, ob.display_type]
            for ob in drone_objects()}
    scene[SNAPSHOT_KEY] = json.dumps(data)


def restore_snapshot(context):
    scene = context.scene
    data = json.loads(scene.get(SNAPSHOT_KEY, "{}"))
    for ob in drone_objects():
        hid, hvp, hr, disp = data.get(ob.name, [False, False, False, "TEXTURED"])
        try:
            ob.hide_set(hid, view_layer=context.view_layer)
        except RuntimeError:
            pass
        ob.hide_viewport = hvp
        ob.hide_render = hr
        ob.display_type = disp


def apply_wire(context, enable):
    """Rumpfschale/Schublade als Drahtgitter (nur Viewport-Darstellung, Render bleibt gleich)."""
    data = json.loads(context.scene.get(SNAPSHOT_KEY, "{}"))
    for ob in drone_objects():
        if WIRE_PARTS.match(ob.name):
            orig = data.get(ob.name, [False, False, False, "TEXTURED"])[3]
            ob.display_type = "WIRE" if enable else orig


def apply_view(context, view):
    scene = context.scene
    props = scene.brummi_ansicht
    take_snapshot(scene, context.view_layer)
    if view == "FULL":
        restore_snapshot(context)
    else:
        visible_cats = VIEWS[view]
        for ob in drone_objects():
            ob.hide_viewport = False                      # Monitor-Symbol nie dauerhaft sperren
            set_visible(ob, bool(categories_of(ob) & visible_cats), context, props.include_render)
        apply_wire(context, props.wire_hull)
    props.view = view


def mark_custom(context):
    take_snapshot(context.scene, context.view_layer)
    context.scene.brummi_ansicht.view = "CUSTOM"


# ----------------------------------------------------------------------------
# Eigenschaften
# ----------------------------------------------------------------------------
def _upd_wire(self, context):
    if self.view != "FULL":
        take_snapshot(context.scene, context.view_layer)
        apply_wire(context, self.wire_hull)


def _upd_index(self, context):
    objs = bpy.data.objects
    if 0 <= self.list_index < len(objs):
        ob = objs[self.list_index]
        if not is_drone_object(ob):
            return
        try:
            for o in context.selected_objects:
                o.select_set(False)
            if not _hidden(ob, context.view_layer):
                ob.select_set(True)
            context.view_layer.objects.active = ob
        except (RuntimeError, AttributeError):
            pass


class BRUMMI_PG_ansicht(bpy.types.PropertyGroup):
    view: EnumProperty(name="Ansicht", items=VIEW_ITEMS, default="FULL")
    include_render: BoolProperty(
        name="Auch beim Rendern ausblenden", default=True,
        description="Ausgeblendete Teile erscheinen auch nicht im Render (F12)")
    wire_hull: BoolProperty(
        name="Rumpfschale als Drahtgitter", default=False, update=_upd_wire,
        description="Rumpfschale und Akku-Schublade im Viewport als Drahtgitter zeigen, damit das "
                    "Innenleben in Einbaulage sichtbar ist (nur Darstellung, nicht im Render)")
    list_index: IntProperty(default=-1, update=_upd_index)
    list_filter: EnumProperty(
        name="Kategorie",
        items=[("ALL", "Alle Bauteile", "")] + [(k, v, "") for k, v in CATEGORIES.items()],
        default="ALL")
    only_visible: BoolProperty(name="Nur sichtbare", default=False)


# ----------------------------------------------------------------------------
# Operatoren
# ----------------------------------------------------------------------------
class BRUMMI_OT_set_view(bpy.types.Operator):
    bl_idname = "brummi.set_view"
    bl_label = "Ansicht setzen"
    bl_description = "Ansicht umschalten (nur Sichtbarkeit, das Modell bleibt unveraendert)"
    bl_options = {"REGISTER", "UNDO"}

    view: StringProperty(default="FULL")

    @classmethod
    def description(cls, context, props):
        for key, label, desc, *_ in VIEW_ITEMS:
            if key == props.view:
                return f"{label}: {desc}"
        return cls.bl_description

    def execute(self, context):
        if not drone_objects():
            self.report({"ERROR"}, f"Collection '{ROOT_COLLECTION}' nicht gefunden")
            return {"CANCELLED"}
        apply_view(context, self.view)
        return {"FINISHED"}


class BRUMMI_OT_toggle_part(bpy.types.Operator):
    bl_idname = "brummi.toggle_part"
    bl_label = "Bauteil ein-/ausblenden"
    bl_options = {"REGISTER", "UNDO"}

    name: StringProperty()

    def execute(self, context):
        ob = bpy.data.objects.get(self.name)
        if ob is None:
            return {"CANCELLED"}
        mark_custom(context)
        ob.hide_viewport = False
        set_visible(ob, _hidden(ob, context.view_layer), context,
                    context.scene.brummi_ansicht.include_render)
        return {"FINISHED"}


class BRUMMI_OT_isolate(bpy.types.Operator):
    bl_idname = "brummi.isolate"
    bl_label = "Isolieren"
    bl_description = "Nur die ausgewaehlten Bauteile zeigen (bzw. das in der Liste markierte)"
    bl_options = {"REGISTER", "UNDO"}

    mode: EnumProperty(items=[("SELECTED", "Auswahl", ""), ("LIST", "Listeneintrag", "")],
                       default="SELECTED")

    def execute(self, context):
        if self.mode == "LIST":
            i = context.scene.brummi_ansicht.list_index
            keep = {bpy.data.objects[i]} if 0 <= i < len(bpy.data.objects) else set()
        else:
            keep = set(context.selected_objects)
        keep = {o for o in keep if is_drone_object(o)}
        if not keep:
            self.report({"WARNING"}, "Kein BRUMMI-Bauteil ausgewaehlt")
            return {"CANCELLED"}
        mark_custom(context)
        inc = context.scene.brummi_ansicht.include_render
        for ob in drone_objects():
            ob.hide_viewport = False
            set_visible(ob, ob in keep, context, inc)
        return {"FINISHED"}


class BRUMMI_OT_hide_selected(bpy.types.Operator):
    bl_idname = "brummi.hide_selected"
    bl_label = "Auswahl ausblenden"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        sel = [o for o in context.selected_objects if is_drone_object(o)]
        if not sel:
            return {"CANCELLED"}
        mark_custom(context)
        for ob in sel:
            set_visible(ob, False, context, context.scene.brummi_ansicht.include_render)
        return {"FINISHED"}


class BRUMMI_OT_show_category(bpy.types.Operator):
    bl_idname = "brummi.show_category"
    bl_label = "Kategorie einblenden"
    bl_description = "Alle Teile der gefilterten Kategorie zusaetzlich einblenden"
    bl_options = {"REGISTER", "UNDO"}

    show: BoolProperty(default=True)

    def execute(self, context):
        props = context.scene.brummi_ansicht
        mark_custom(context)
        for ob in drone_objects():
            if props.list_filter == "ALL" or props.list_filter in categories_of(ob):
                ob.hide_viewport = False
                set_visible(ob, self.show, context, props.include_render)
        return {"FINISHED"}


class BRUMMI_OT_assembled(bpy.types.Operator):
    bl_idname = "brummi.assembled"
    bl_label = "In Einbauposition bringen"
    bl_description = ("Explosion = 0, Baugruppen = 0 und Zeitleiste auf Bild 200 (fertig montiert). "
                      "Die Teile werden nicht verschoben, nur die Explosions-Regler zurueckgesetzt")
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ctrl = bpy.data.objects.get(CONTROLLER)
        if ctrl is not None:
            for k, v in (("Explosion", 0.0), ("Baugruppen", 0.0), ("Montage", 1.0)):
                if k in ctrl.keys():
                    ctrl[k] = v
        context.scene.frame_set(max(context.scene.frame_current, FRAME_ASSEMBLED))
        return {"FINISHED"}


def assembled_state(context):
    """True, wenn alle Teile in ihrer Einbauposition stehen (keine Explosion/Montage aktiv)."""
    ctrl = bpy.data.objects.get(CONTROLLER)
    if ctrl is None:
        return True
    ev = ctrl.evaluated_get(context.evaluated_depsgraph_get())
    try:
        return (abs(ev.get("Explosion", 0.0)) < 1e-4 and abs(ev.get("Baugruppen", 0.0)) < 1e-4
                and ev.get("Montage", 1.0) > 0.9999)
    except TypeError:
        return True


# ----------------------------------------------------------------------------
# Oberflaeche
# ----------------------------------------------------------------------------
class BRUMMI_UL_parts(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        ob = item
        hidden = _hidden(ob, context.view_layer)
        row = layout.row(align=True)
        op = row.operator("brummi.toggle_part", text="", emboss=False,
                          icon="HIDE_ON" if hidden else "HIDE_OFF")
        op.name = ob.name
        sub = row.row()
        sub.active = not hidden
        sub.label(text=ob.name)
        cats = categories_of(ob)
        sub2 = row.row()
        sub2.alignment = "RIGHT"
        sub2.active = False
        sub2.label(text=" / ".join(CATEGORIES.get(c, "?")[:4] for c in sorted(cats)))

    def filter_items(self, context, data, propname):
        props = context.scene.brummi_ansicht
        objs = getattr(data, propname)
        coll = bpy.data.collections.get(ROOT_COLLECTION)
        members = set(coll.all_objects) if coll else set()
        name_filter = self.filter_name.lower()
        flags = []
        for ob in objs:
            ok = ob in members
            if ok and props.list_filter != "ALL":
                ok = props.list_filter in categories_of(ob)
            if ok and props.only_visible:
                ok = not _hidden(ob, context.view_layer)
            if ok and name_filter:
                ok = name_filter in ob.name.lower()
            flags.append(self.bitflag_filter_item if ok else 0)
        order = bpy.types.UI_UL_list.sort_items_by_name(objs, "name")
        return flags, order


class BRUMMI_PT_views(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BRUMMI"
    bl_label = "Ansichten"

    def draw(self, context):
        layout = self.layout
        props = context.scene.brummi_ansicht
        if not drone_objects():
            layout.label(text=f"'{ROOT_COLLECTION}' fehlt", icon="ERROR")
            return
        col = layout.column(align=True)
        col.scale_y = 1.35
        for key, label, desc, icon, _ in VIEW_ITEMS[:5]:
            op = col.operator("brummi.set_view", text=label, icon=icon, depress=(props.view == key))
            op.view = key
        if props.view == "CUSTOM":
            layout.label(text="Eigene Auswahl aktiv", icon="INFO")

        n_vis = sum(1 for o in drone_objects() if not _hidden(o, context.view_layer))
        layout.label(text=f"Sichtbar: {n_vis} von {len(drone_objects())} Bauteilen")

        if not assembled_state(context):
            box = layout.box()
            box.label(text="Teile sind nicht in Einbauposition", icon="ERROR")
            box.label(text="(Explosion/Montage aktiv)")
            box.operator("brummi.assembled", icon="LOOP_BACK")

        box = layout.box()
        box.label(text="Optionen", icon="PREFERENCES")
        box.prop(props, "include_render")
        box.prop(props, "wire_hull")
        shading = getattr(context.space_data, "shading", None)
        if shading is not None:
            box.prop(shading, "show_xray", text="Roentgen (X-Ray) im Viewport")


class BRUMMI_PT_parts(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BRUMMI"
    bl_label = "Bauteile (Component Isolation)"

    def draw(self, context):
        layout = self.layout
        props = context.scene.brummi_ansicht
        row = layout.row(align=True)
        row.prop(props, "list_filter", text="")
        row.prop(props, "only_visible", text="", icon="HIDE_OFF")
        layout.template_list("BRUMMI_UL_parts", "", bpy.data, "objects", props, "list_index", rows=10)

        row = layout.row(align=True)
        row.operator("brummi.show_category", text="Kategorie zeigen", icon="HIDE_OFF").show = True
        row.operator("brummi.show_category", text="verbergen", icon="HIDE_ON").show = False
        col = layout.column(align=True)
        col.operator("brummi.isolate", text="Markiertes Bauteil isolieren",
                     icon="RESTRICT_SELECT_OFF").mode = "LIST"
        col.operator("brummi.isolate", text="Auswahl im Viewport isolieren",
                     icon="OBJECT_DATA").mode = "SELECTED"
        col.operator("brummi.hide_selected", text="Auswahl ausblenden", icon="HIDE_ON")
        layout.operator("brummi.set_view", text="Alles wiederherstellen (Full View)",
                        icon="FILE_REFRESH").view = "FULL"

        # Steckbrief des markierten Bauteils (nur lesen, aus der Stueckliste im Modell)
        i = props.list_index
        if 0 <= i < len(bpy.data.objects) and is_drone_object(bpy.data.objects[i]):
            ob = bpy.data.objects[i]
            box = layout.box()
            box.label(text=ob.name, icon="INFO")
            box.label(text="Kategorie: " + ", ".join(CATEGORIES.get(c, "nicht zugeordnet")
                                                    for c in sorted(categories_of(ob))))
            for key in ("Bauteil_Nr", "Baugruppe", "Funktion", "Verbindung", "Fertigung"):
                if key in ob.keys():
                    box.label(text=f"{key.replace('_', ' ')}: {ob[key]}")


CLASSES = (
    BRUMMI_PG_ansicht,
    BRUMMI_OT_set_view,
    BRUMMI_OT_toggle_part,
    BRUMMI_OT_isolate,
    BRUMMI_OT_hide_selected,
    BRUMMI_OT_show_category,
    BRUMMI_OT_assembled,
    BRUMMI_UL_parts,
    BRUMMI_PT_views,
    BRUMMI_PT_parts,
)


def register():
    unregister(quiet=True)      # erneutes "Run Script" ohne Fehlermeldung
    for c in CLASSES:
        bpy.utils.register_class(c)
    bpy.types.Scene.brummi_ansicht = PointerProperty(type=BRUMMI_PG_ansicht)


def unregister(quiet=False):
    if hasattr(bpy.types.Scene, "brummi_ansicht"):
        del bpy.types.Scene.brummi_ansicht
    for c in reversed(CLASSES):
        registered = getattr(bpy.types, c.__name__, None)
        if registered is not None:
            try:
                bpy.utils.unregister_class(registered)
            except RuntimeError:
                if not quiet:
                    raise


# "Run Script" im Texteditor (__main__) oder als Text in der .blend mit Haken "Registrieren"
# (Modulname endet auf .py). Als installiertes Add-on ruft Blender register() selbst auf.
if __name__ == "__main__" or __name__.endswith(".py"):
    register()
