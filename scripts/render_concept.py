"""Deterministic Blender mechanical concept. No routing/fabrication claims."""
import bpy, math, json
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1]; O=R/'cad/renders'; O.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(name,color,metal=0,rough=.35):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Metallic'].default_value=metal;b.inputs['Roughness'].default_value=rough;return m
black=mat('Black solder mask',(.016,.022,.026),0,.3);fr4=mat('FR4 edge',(.26,.19,.09),0,.6);metal=mat('Nickel plated steel',(.52,.57,.6),.88,.28);gold=mat('ENIG',(.68,.48,.16),.8,.25);white=mat('White legend',(.85,.88,.87));body=mat('Tube metal',(.38,.40,.35),.72,.4);label=mat('Battery sleeve',(.045,.11,.12),.35,.32);rubber=mat('Insulator',(.035,.035,.03),0,.55);orange=mat('HV marking',(.95,.35,.05));stage=mat('Stage',(.055,.068,.085),0,.6)
def box(name,loc,dim,material,bevel=.15):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 if bevel: b=o.modifiers.new('Edge radii','BEVEL');b.width=bevel;b.segments=4;o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return o
def cyl(name,loc,radius,depth,material,axis='X'):
 bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=radius,depth=depth,location=loc);o=bpy.context.object;o.name=name
 if axis=='X':o.rotation_euler[1]=math.pi/2
 o.data.materials.append(material);b=o.modifiers.new('Small edge bevel','BEVEL');b.width=.12;b.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL');return o
def text(s,loc,size,material=white,rot=0):
 c=bpy.data.curves.new('Legend','FONT');c.body=s;c.size=size;c.extrude=.003;c.align_x='CENTER';o=bpy.data.objects.new(s,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler[2]=rot;o.data.materials.append(material);return o
pcb=box('Concept board envelope 140 x 48 x 1.6 mm',(0,0,.8),(140,48,1.6),black,2)
# Bevel width limited by board thickness: rounded corners are concept geometry.
for x in (-66,66):
 for y in (-20,20):
  cutter=cyl('mount cut',(x,y,.8),1.6,5,metal,'Z');mod=pcb.modifiers.new('Mounting hole','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=pcb;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
# Tube body is a dimensioned stand-in, not a qualified CTC-5 vendor model.
cyl('CTC-5 approximate body',(-8,13,10),6,110,body)
for x in (-62,46):cyl('Tube end insulator',(x,13,10),5.2,1.2,rubber)
for x in (-63,47):cyl('Tube contact',(x,13,10),1.5,2,metal)
for x in (-52,36):box('Provisional tube support',(x,13,3.5),(4,13,3.8),rubber,.5)
text('CTC-5  /  400 V',(-8,13,16.02),2.6,white)
for n,x in enumerate((-36,20)):
 cyl(f'AA {n+1} sleeve',(x,-12,10),7.1,49,label)
 for ex in (x-24.4,x+24.4):cyl('AA steel end',(ex,-12,10),6.8,1,metal)
 cyl('AA positive button',(x+25.1,-12,10),2.5,.7,metal)
 text('AA  /  LR6',(x,-12,17.15),3,white)
 # Battery spring and positive leaf are geometric fallbacks, STEP originals retained.
 for ex in (x-26.1,x+26.2):box('Contact approximate leaf',(ex,-12,6.5),(.4,10,9),metal,.15)
# Electronics placement envelopes in the clear central corridor.
for i in range(8):
 x=-48+i*8;box(f'CW capacitor envelope {i+1}',(x,2,2.5),(3.2,1.6,1.8),body,.2)
 for px in (x-1.5,x+1.5):box('ENIG pad',(px,2,1.65),(.65,2,.08),gold,.06)
 for px in (x-1.3,x+1.3):box('Cap termination',(px,2,2.5),(.5,1.7,1.85),metal,.08)
for i in range(8):box(f'Diode envelope {i+1}',(-48+i*8,-1.5,2.1),(2.6,1.4,.9),rubber,.15)
box('Inductor allocation',(-59,0,4.4),(7,7,5.6),rubber,.65)
# Prefer the supplied MCU mesh; material groups in this OBJ are nonstandard.
before=set(bpy.data.objects)
try:
 bpy.ops.wm.obj_import(filepath=str(R/'cad/models/NRF52832-QFAA-C77540.obj'), forward_axis='Y', up_axis='Z')
 imported=set(bpy.data.objects)-before
 for o in imported:
  o.location+=Vector((41,1,1.65));o.data.materials.clear();o.data.materials.append(rubber)
except Exception:
 box('nRF52832 QFN48 envelope',(41,1,2.2),(6,6,1.1),rubber,.15)
text('geiger2',(-25,20,1.7),3.4)
text('MECHANICAL CONCEPT',(-5,-21,1.7),1.8)
text('RF RESERVE',(59,4,1.7),1.9,white,math.pi/2)
text('HV',(-60,5,1.7),2.2,orange)
# Dotted reservation boundary; antenna itself is deliberately not invented.
for y in range(-16,18,4):box('RF boundary',(51,y,1.67),(.25,2,.05),white,.01)
for x in (-64,64):
 for y in (-18,18):cyl('Standoff',(x,y,-1),2.1,2,metal,'Z')
# Export just the assembly, before studio objects.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=str(O/'geiger2-concept.glb'),export_format='GLB',use_selection=True)
box('Studio floor',(0,0,-4),(2000,2000,1),stage,.1)
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.25,.3,1);world.node_tree.nodes['Background'].inputs[1].default_value=.6
for loc,power,size in [((0,-80,150),500000,130),((-90,50,100),350000,100),((110,70,65),250000,70)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,4))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;bpy.context.scene.camera=camera;camera.data.clip_end=5000;camera.data.lens=52
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.resolution_x=1500;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
for name,loc,target in [('hero',(135,-155,145),(0,0,5)),('top',(0,-50,225),(0,0,3)),('tube',(-110,115,80),(-12,7,7)),('profile',(20,-200,48),(0,0,6))]:
 camera.location=loc;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(O/f'{name}.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'build/geiger2-concept.blend'))
(O/'manifest.json').write_text(json.dumps({'status':'mechanical concept; no routed PCB or DRC certification','board_envelope_mm':[140,48,1.6],'tube_envelope_mm':[110,12],'aa_envelope_mm':[50.5,14.5],'fallbacks':['CTC-5 cylinder','AA bodies','battery contacts','tube supports','HV parts envelopes'],'source_mesh':'cad/models/NRF52832-QFAA-C77540.obj','views':['hero','top','tube','profile']},indent=2)+'\n')
