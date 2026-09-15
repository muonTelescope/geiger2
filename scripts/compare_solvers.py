#!/usr/bin/env python3
"""Compare both retained solver runs using adaptive samples and identical windows."""
from pathlib import Path
import gzip,json,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/geiger2-matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'docs/hv'
with gzip.open(R/'build/tsci/hv-table.txt.gz','rt') as f:
 h=f.readline().split(); w=np.loadtxt(f,usecols=[h.index(k) for k in ['time','v(hv_out)','v(switch)','i(vsimulation_voltage_source_0)']])
n=np.loadtxt(R/'build/hv/v2.4_load1/metrics.txt',skiprows=1,usecols=[0,1,2,4])
def measure(x):
 assert np.isfinite(x).all() and x[-1,0]>=.15
 t=np.r_[.1,x[(x[:,0]>.1)&(x[:,0]<.15),0],.15]
 v=np.interp(t,x[:,0],x[:,1]);i=-np.interp(t,x[:,0],x[:,3])
 start=x[x[:,1]>=396,0][0]*1000
 return {'startup_396_ms':float(start),'hv_mean_V':float(np.trapezoid(v,t)/.05),'hv_min_V':float(v.min()),'hv_max_V':float(v.max()),'hv_ripple_pp_V':float(np.ptp(v)),'battery_mean_mA':float(np.trapezoid(i,t)/.05*1000),'switch_peak_first_150ms_V':float(x[x[:,0]<=.15,2].max())}
a,b=measure(n),measure(w)
report={'conditions':{'vbat_V':2.4,'external_load_uA':1,'measurement_window_s':[.1,.15],'peak_window_s':[0,.15]},'native':a,'tscircuit_wasm':b,'wasm_minus_native':{k:b[k]-a[k] for k in a}}
(O/'solver-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['| Metric | Native ngspice | tscircuit WASM | WASM − native |','|---|---:|---:|---:|']
for k in a:lines.append(f'| {k} | {a[k]:.6f} | {b[k]:.6f} | {b[k]-a[k]:+.6f} |')
(O/'solver-comparison-table.md').write_text('\n'.join(lines)+'\n')
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.2,'svg.hashsalt':'geiger2'})
fig,ax=plt.subplots(2,1,figsize=(10,7),layout='constrained')
for x,name,c in [(n,'Native ngspice (Gear)','#059669'),(w,'tscircuit / WASM','#7c3aed')]:
 # Same display grid, but preserve actual extrema in the table, not interpolated plot.
 t=np.linspace(.13,.15,10001);v=np.interp(t,x[:,0],x[:,1]);ax[0].plot(t*1000,v,label=name,color=c,lw=1)
 # Charge-integrated input current in 1 ms bins, avoiding point-sampling of spikes.
 edges=np.linspace(.1,.15,51);current=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  ts=np.r_[lo,x[(x[:,0]>lo)&(x[:,0]<hi),0],hi]
  current.append(np.trapezoid(-np.interp(ts,x[:,0],x[:,3]),ts)/(hi-lo)*1000)
 ax[1].stairs(current,edges*1000,label=name,color=c)
ax[0].set(title='HV ripple · identical time window, 2 µs display grid',ylabel='HV (V)',xlabel='Time (ms)');ax[0].legend()
ax[1].set(title='Battery current · time-integrated 1 ms averages',ylabel='Current (mA)',xlabel='Time (ms)');ax[1].legend()
fig.suptitle('Solver comparison / 2.4 V input / 1 µA external load',fontsize=15)
fig.savefig(O/'solver-detail.png',dpi=180);fig.savefig(O/'solver-detail.svg',metadata={'Date':None});plt.close(fig)
p=O/'solver-detail.svg';p.write_text('\n'.join(z.rstrip() for z in p.read_text().splitlines())+'\n')
print('\n'.join(lines))
