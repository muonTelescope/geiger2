"""Run with FreeCAD's Python and its Resources/lib on PYTHONPATH."""
from pathlib import Path
import json
import FreeCAD, Part, MeshPart
root=Path(__file__).resolve().parents[1]; out=root/'cad/models/mesh'; out.mkdir(exist_ok=True)
report=[]
for name in ['aaCell','MY-AA-03','MY-ZJ-3030','NRF52832-QFAA-C77540']:
    shape=Part.Shape(); shape.read(str(root/f'cad/models/{name}.step'))
    mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.05,AngularDeflection=.15,Relative=False)
    mesh.write(str(out/f'{name}.stl'))
    bb=shape.BoundBox
    report.append(dict(name=name,bounds_mm=[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],facets=mesh.CountFacets))
(out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
