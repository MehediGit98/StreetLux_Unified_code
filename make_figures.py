"""Original vector illustrations and data figures generated from saved results."""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

ROOT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':12,
 'axes.labelsize':10,'axes.spines.top':False,'axes.spines.right':False,
 'axes.edgecolor':'#74808c','axes.labelcolor':'#243646','text.color':'#243646',
 'xtick.color':'#243646','ytick.color':'#243646','pdf.fonttype':42,'svg.fonttype':'none'})
INK='#243646'; TEAL='#148486'; GOLD='#dd9a32'; BLUE='#4080b6'; RED='#b65558'; PALE='#e8f2f4'; PURPLE='#7965a4'

def load(path):return json.loads(Path(path).read_text())
def save(fig,out,name):
    out.mkdir(parents=True,exist_ok=True)
    for ext in ['png','pdf','svg']:fig.savefig(out/(name+'.'+ext),dpi=300,bbox_inches='tight',facecolor='white')
    plt.close(fig)
def arrow(ax,a,b,color=GOLD,lw=1.7,style='-|>',rad=0):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=12,lw=lw,color=color,connectionstyle=f'arc3,rad={rad}'))
def finish(ax,xlab=None):
    ax.set_axisbelow(True);ax.grid(axis='x',color='#e4e9ee',lw=.7)
    if xlab:ax.set_xlabel(xlab)

def street(data,out):
    route=load(data/'route.json'); modes=load(data/'modes.json')['rows']; design=load(data/'designs.json')['rows']
    fig,axes=plt.subplots(1,5,figsize=(12,4.5),gridspec_kw={'width_ratios':[1,1.2,1.55,1.4,1.25]})
    short=['Residential lane','Mixed use collector','Wide arterial','Concrete underpass','Office canyon']
    for i,(ax,s) in enumerate(zip(axes,route['sections'])):
        w=s['width_m'];hl=s['left_height_m'];hr=s['right_height_m'];x=s['eye_offset_m']
        ax.set_facecolor('#f2f8fb');ax.add_patch(Rectangle((-w/2-5,0),5,hl,fc='#bfcad3',ec=INK,lw=.7))
        ax.add_patch(Rectangle((w/2,0),5,hr,fc='#91a8b7',ec=INK,lw=.7))
        for h in np.arange(4,max(hl,hr),6):
            if h<hl: ax.plot([-w/2-4,-w/2-1],[h,h],color='white',lw=1)
            if h<hr: ax.plot([w/2+1,w/2+4],[h,h],color='white',lw=1)
        ax.plot([-w/2,w/2],[0,0],color=INK,lw=2)
        canopy=s['canopy'];opaque=canopy.get('transmittance')=='opaque'
        if opaque: ax.add_patch(Rectangle((-w/2,canopy['base_m']),w,3,fc='#89959b',alpha=.9))
        else:
            ax.add_patch(Rectangle((-w/2,canopy['base_m']),w,canopy['top_m']-canopy['base_m'],fc='#77ab85',alpha=.35))
            arrow(ax,(0,40),(x,4),BLUE,lw=1.3)
        ax.scatter([x],[1.55],c=RED,s=25,zorder=5)
        ax.annotate(f'{w:g} m',xy=(0,-3),ha='center',va='top',fontsize=10,fontweight='bold')
        ax.text(0,-10,f"{s['length_m']/1000:g} km\n{hl:g} / {hr:g} m height",ha='center',va='top',fontsize=9)
        ax.text(0,59,f'{i+1}  {short[i]}',ha='center',fontsize=10,fontweight='bold')
        ax.text(0,52,f"{canopy['cover']:.0%} "+('opaque cover' if opaque else 'foliage cover'),ha='center',fontsize=8.5)
        ax.set_xlim(-w/2-6,w/2+6);ax.set_ylim(-22,65);ax.axis('off')
    fig.text(.5,.025,'Section dimensions are model inputs • red point = eye position • blue arrow = diffuse sky path\nFive sequential street types, total 4.97 km; this is a schematic, not a surveyed route map.',ha='center',fontsize=10)
    fig.subplots_adjust(wspace=.28,bottom=.2)
    save(fig,out,'figure_1_street_sections')

    labels={'walk':'Walk','rickshaw':'Rickshaw','cng':'CNG auto-rickshaw','car_clear':'Clear-glazed car','car_tinted':'Bronze-glazed car','bus':'Bus window seat','car_film':'Car with film'}
    fig,axes=plt.subplots(1,2,figsize=(10,4.8),sharey=True)
    y=np.arange(len(modes));colors=[TEAL if r['key']=='walk' else BLUE for r in modes]
    for ax,key,title,unit in [(axes[0],'mean_medi_travel_lx','A  Average light level at the eye','Mean melanopic EDI (lx)'),(axes[1],'dose_travel_lxh','B  Light accumulated during the trip','Melanopic dose (lx h)')]:
        vals=[r['summary'][key] for r in modes]
        ax.barh(y,vals,color=colors,height=.64)
        for yy,v in zip(y,vals):ax.text(v+max(vals)*.025,yy,f'{v:,.0f}',va='center',fontsize=9)
        ax.set_xlim(0,max(vals)*1.23);ax.set_title(title,loc='left',pad=14);finish(ax,unit)
    axes[0].set_yticks(y,[labels[r['key']] for r in modes]);axes[0].invert_yaxis()
    fig.tight_layout(w_pad=2);save(fig,out,'figure_2_mode_exposure')

    ds=[r for r in design if r['key']!='baseline']
    ds.sort(key=lambda r:r['delta_vs_baseline_pct'])
    dn={'pale_facades':'Whitewashed façades','setback_low':'Building height capped at 18 m','widen_18':'Minimum street width 18 m','pale_paving':'Asphalt replaced by pale concrete','canopy_40':'Foliage cover 40%','canopy_70':'Foliage cover 70%'}
    fig,ax=plt.subplots(figsize=(10,4.1));vals=[r['delta_vs_baseline_pct'] for r in ds];y=np.arange(len(ds))
    ax.barh(y,vals,color=[TEAL if v>=0 else GOLD for v in vals],height=.65)
    ax.set_yticks(y,[dn[r['key']] for r in ds]);ax.axvline(0,color=INK,lw=.9)
    for yy,v in zip(y,vals):ax.text(v+3 if v>0 else v/2,yy,f'{v:+.1f}%',ha='left' if v>0 else 'center',va='center',fontweight='bold',color=INK if v>0 else 'white')
    ax.set_xlim(min(-10,min(vals)*1.15),max(10,max(vals)*1.18));finish(ax,'Change in walking melanopic dose relative to baseline (%)')
    fig.tight_layout();save(fig,out,'figure_4_design_changes')

    rows=[r for r in modes if r['key']!='walk'];y=np.arange(len(rows))
    dur=[100*r['decomposition']['duration_share_of_gap'] for r in rows]
    fig,ax=plt.subplots(figsize=(10,3.8));ax.barh(y,dur,color=GOLD,label='Duration contribution')
    ax.barh(y,100-np.array(dur),left=dur,color=BLUE,label='Exposure rate contribution')
    for i,v in enumerate(dur):ax.text(v/2,i,f'{v:.1f}%',ha='center',va='center',color=INK);ax.text(v+(100-v)/2,i,f'{100-v:.1f}%',ha='center',va='center',color='white')
    ax.set_yticks(y,[labels[r['key']] for r in rows]);ax.invert_yaxis();ax.set_xlim(0,100)
    ax.set_xlabel('Share of the dose deficit relative to walking (%)');ax.legend(ncol=2,loc='lower center',bbox_to_anchor=(.5,1.01),frameon=False)
    fig.tight_layout();save(fig,out,'figure_3_dose_decomposition')

def main(data=None, out=None):
    data = Path(data or ROOT / 'results')
    out = Path(out or ROOT / 'figures')
    street(data, out)
    print('Four figures written to', out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    main(args.data, args.out)
