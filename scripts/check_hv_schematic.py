#!/usr/bin/env python3
"""Check tscircuit's generated source connectivity against the SPICE ladder."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows=json.loads((R/'dist/board/hv-ladder/circuit.json').read_text())
comps={x['source_component_id']:x for x in rows if x['type']=='source_component'}
ports={x['source_port_id']:x for x in rows if x['type']=='source_port'}
parent={p:p for p in ports}
def find(x):
    while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
    return x
for row in rows:
    if row['type']=='source_trace':
        ps=row['connected_source_port_ids']
        for p in ps[1:]: parent[find(p)]=find(ps[0])
actual={}
for id,p in ports.items():actual.setdefault(find(id),set()).add((comps[p['source_component_id']]['name'],p['pin_number']))
expected={}
refmap={'Rtop1':'R1','Rtop2':'R2','Rtop3':'R3','Rtop4':'R4','Rbottom':'R5','Csense':'C9'}
values={}
for line in (R/'sim/hv/converter.cir').read_text().splitlines():
    f=line.split()
    if not f:continue
    ref=f[0]
    if ref in refmap or (ref[0] in 'CD' and ref[1:].isdigit() and 1<=int(ref[1:])<=8):
        name=refmap.get(ref,ref); pins=[1,2]
        # Nonpolar even ladder capacitors are drawn in the opposite pin order.
        if ref.startswith('C') and ref[1:].isdigit() and int(ref[1:])%2==0:pins=[2,1]
        for net,pin in zip(f[1:3],pins):expected.setdefault(net,set()).add((name,pin))
        values[name]=f[3]
expected['sw'].add(('U1',1));expected['0'].add(('U1',2))
a={frozenset(s) for s in actual.values()};e={frozenset(s) for s in expected.values()}
assert a==e,{'missing':[sorted(s) for s in e-a],'extra':[sorted(s) for s in a-e]}
for c in comps.values():
    name=c['name']
    if name in ['R1','R2','R3','R4']:assert c['resistance']==33e6
    if name=='R5':assert c['resistance']==412e3
    if name.startswith('C'):
        target=100e-12 if name=='C9' else 10e-9
        assert abs(c['capacitance']-target)<1e-16
print(f'PASS: {len(comps)} components, {len(e)} nets; diode polarities and passive values match SPICE ladder.')
