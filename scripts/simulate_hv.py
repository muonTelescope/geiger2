#!/usr/bin/env python3
"""Run real ngspice transients; preserve decks, logs, sampled data and metrics."""
from pathlib import Path
import argparse, csv, hashlib, json, os, re, subprocess
os.environ.setdefault('MPLCONFIGDIR', '/tmp/geiger2-matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/hv'; BUILD=ROOT/'build/hv'; OUT.mkdir(parents=True,exist_ok=True); BUILD.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18,'figure.facecolor':'#f8fafc','axes.facecolor':'#f8fafc','savefig.facecolor':'#f8fafc'})
parser=argparse.ArgumentParser(); parser.add_argument('--reuse',action='store_true'); args=parser.parse_args()
base=(ROOT/'sim/hv/converter.cir').read_text()
cases=[(f'v{v:g}_load{i:g}',{'VBAT':v,'ILOAD':i*1e-6}) for v in (1.8,2.4,3.2) for i in (0,1,5,20)]
cases += [('half_cap',{'VBAT':2.4,'ILOAD':1e-6,'CW':5e-9}),('high_dcr',{'VBAT':1.8,'ILOAD':5e-6,'DCR':16}),('low_L',{'VBAT':3.2,'ILOAD':1e-6,'LVAL':.0008}),('high_L',{'VBAT':1.8,'ILOAD':5e-6,'LVAL':.0012})]
metrics=[]; waves={}
for name,params in cases:
    deck=base
    for key,value in params.items(): deck=re.sub(rf'\b{key}=\S+',f'{key}={value:g}',deck,count=1)
    work=BUILD/name; work.mkdir(exist_ok=True)
    if not args.reuse:
        (work/'converter.cir').write_text(deck)
        subprocess.run(['ngspice','-b','-o','run.log','converter.cir'],cwd=work,check=True,stdout=subprocess.DEVNULL,timeout=180)
    log=(work/'run.log').read_text()
    if any(s in log.lower() for s in ('timestep too small','fatal error','error:')): raise RuntimeError(f'{name}: {log[-2000:]}')
    x=np.loadtxt(work/'wave.txt',skiprows=1); t=x[:,0]
    if t[-1]<.29999 or not np.isfinite(x).all(): raise RuntimeError(f'{name}: incomplete data')
    waves[name]=x; y=x[t>=.2]; duration=y[-1,0]-y[0,0]
    avg=lambda v:float(np.trapezoid(v,y[:,0])/duration)
    # Linearized data is for visualization only. Exact adaptive samples are used
    # for peak stress and energy metrics via the second export below.
    raw=np.loadtxt(work/'metrics.txt',skiprows=1); tail=raw[raw[:,0]>=.2]; dt=tail[-1,0]-tail[0,0]
    avg_raw=lambda v:float(np.trapezoid(v,tail[:,0])/dt)
    hit=np.flatnonzero(raw[:,1]>=396)
    pin=avg_raw(-tail[:,4])*params['VBAT']
    pout=avg_raw(tail[:,1]**2/(132e6+412e3)+tail[:,1]*params['ILOAD']*np.clip(tail[:,1]/100,0,1))
    metrics.append(dict(case=name,vbat=params['VBAT'],load_uA=params['ILOAD']*1e6,hv_mean=avg_raw(tail[:,1]),hv_min=float(tail[:,1].min()),hv_max=float(tail[:,1].max()),ripple_pp=float(np.ptp(tail[:,1])),startup_ms=float(raw[hit[0],0]*1e3) if len(hit) else None,peak_switch_v=float(raw[:,2].max()),peak_inductor_mA=float(raw[:,3].max()*1e3),input_mA=avg_raw(-tail[:,4])*1e3,power_stage_efficiency=pout/pin if pin>0 else None,within_360_440=bool(tail[:,1].min()>=360 and tail[:,1].max()<=440)))
    print(name,json.dumps(metrics[-1]),flush=True)
    # Compressed trace preserves time steps without committing 100 MB text files.
    np.savez_compressed((OUT if name in ('v1.8_load1','v2.4_load1','v3.2_load1') else work)/f'{name}.npz',wave=x,columns=np.array(['time_s','hv_V','switch_V','inductor_A','battery_A','sense_V','gate','stage1_V','stage2_V','stage3_V']))
    del raw
(OUT/'results.json').write_text(json.dumps({'model':'exploratory non-vendor switch/diode model; no controller or gate-drive supply current','measurement_window_s':[.2,.3],'netlist_sha256':hashlib.sha256(base.encode()).hexdigest(),'ngspice':subprocess.check_output(['ngspice','--version'],text=True).splitlines()[1],'cases':metrics},indent=2)+'\n')
with (OUT/'results.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=metrics[0]); w.writeheader(); w.writerows(metrics)
def save(fig,name):
    fig.savefig(OUT/f'{name}.png',dpi=180,bbox_inches='tight'); fig.savefig(OUT/f'{name}.svg',bbox_inches='tight'); plt.close(fig)
    p=OUT/f'{name}.svg'; p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
fig,ax=plt.subplots(2,1,figsize=(10,7),layout='constrained')
for v,c in zip((1.8,2.4,3.2),('#2563eb','#059669','#d97706')):
    x=waves[f'v{v:g}_load1']; ax[0].plot(x[:,0]*1e3,x[:,1],color=c,label=f'{v:g} V battery'); idx=x[:,0]>=.25; ax[1].plot(x[idx,0]*1e3,x[idx,1],color=c)
ax[0].axhspan(360,440,color='#059669',alpha=.08); ax[0].set(title='HV startup and regulation · 1 µA external load',ylabel='HV output (V)',xlabel='Time (ms)'); ax[0].legend(loc='lower right'); ax[1].set(ylabel='HV output (V)',xlabel='Time (ms)',title='Final 50 ms · divider current is included')
fig.suptitle('geiger2 / exploratory ngspice model',fontsize=16,fontweight='bold'); save(fig,'startup')
fig,ax=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
for v,c in zip((1.8,2.4,3.2),('#2563eb','#059669','#d97706')):
    m=[r for r in metrics[:12] if r['vbat']==v]; load=[r['load_uA'] for r in m]; means=np.array([r['hv_mean'] for r in m]); bounds=np.array([[r['hv_mean']-r['hv_min'] for r in m],[r['hv_max']-r['hv_mean'] for r in m]])
    ax[0].errorbar(load,means,yerr=bounds,marker='o',capsize=4,color=c,label=f'{v:g} V'); ax[1].plot(load,[r['input_mA'] for r in m],'-o',color=c,label=f'{v:g} V')
ax[0].axhspan(360,440,color='#059669',alpha=.08); ax[0].set(title='Output range, final 100 ms',xlabel='External load (µA)',ylabel='HV output (V)'); ax[0].legend(); ax[1].set(title='Power-stage input current',xlabel='External load (µA)',ylabel='Battery current (mA)'); ax[1].legend(); fig.suptitle('Battery / load sweep · controller, drive and BLE current excluded',fontsize=14); save(fig,'load-sweep')
fig,ax=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
r=np.geomspace(10e6,1e9,200); ax[0].loglog(r/1e6,400**2/r*1e3,color='#2563eb'); ax[0].scatter([132.412],[400**2/132.412e6*1e3],color='#d97706',zorder=5); ax[0].annotate('132.412 MΩ / 1.21 mW',(132.412,400**2/132.412e6*1e3),xytext=(25,4),arrowprops={'arrowstyle':'->'}); ax[0].set(xlabel='Total divider resistance (MΩ)',ylabel='Continuous power at 400 V (mW)',title='HV monitoring has a real energy cost')
cap=np.geomspace(1e-9,100e-9,200); n=4; current=4.02e-6; f=10000; drop=current/(f*cap)*(2*n**3/3+n*n/2-n/6); ripple=current/(f*cap)*n*(n+1)/2
ax[1].loglog(cap*1e9,drop,label='CW sag estimate'); ax[1].loglog(cap*1e9,ripple,label='CW ripple estimate'); ax[1].axvline(10,color='#64748b',ls='--'); ax[1].set(title='CW screening calculation · continuous 10 kHz',xlabel='Effective capacitance per capacitor (nF)',ylabel='Voltage (V)'); ax[1].legend(); fig.suptitle('Analytical trade-offs · CW formula is not a burst-mode prediction',fontsize=14); save(fig,'tradeoffs')
