from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc

OUT = Path(__file__).resolve().parent / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

# PRX-like, print-safe, colorblind-friendly visual system.
BLUE = '#0072B2'
ORANGE = '#D55E00'
GREEN = '#009E73'
PURPLE = '#CC79A7'
BLACK = '#222222'
MID = '#777777'
LIGHT = '#E9ECEF'
BAND = '#D9D9D9'

mpl.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 8.5,
    'axes.labelsize': 9,
    'axes.titlesize': 9.5,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 7.5,
    'axes.linewidth': 0.7,
    'xtick.major.width': 0.7,
    'ytick.major.width': 0.7,
    'xtick.major.size': 3.0,
    'ytick.major.size': 3.0,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'mathtext.fontset': 'dejavusans',
    'savefig.dpi': 300,
})

def clean(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(direction='out')


def panel(ax, label):
    ax.text(-0.13, 1.06, label, transform=ax.transAxes, fontsize=10.5,
            fontweight='bold', va='top', ha='left')

# -------------------- data --------------------
n_generic = np.array([6,8,10,12,14,16])
generic_rho1 = np.array([0.9597782788,0.9469900032,0.9441227502,0.9425237185,0.9217211574,0.9185562026])
generic_rho1_lo = np.array([0.9464380158,0.9357077173,0.9343432653,0.9341734619,0.9096933582,0.9095784502])
generic_rho1_hi = np.array([0.9731784143,0.9586158937,0.9537345517,0.9507346398,0.9334584921,0.9273645060])
generic_rho2 = np.array([0.9781187967,0.9743283861,0.9674137739,0.9630625306,0.9545896719,0.9521610253])
generic_rho2_lo = np.array([0.9720333961,0.9701048318,0.9636100908,0.9601034112,0.9501748889,0.9483081296])
generic_rho2_hi = np.array([0.9843706698,0.9785947367,0.9712962269,0.9659852956,0.9589410816,0.9559933112])

haar_n = np.array([6,8,10,12,14,16,18])
haar_rho1 = np.array([0.9463173113,0.9251479798,0.9331164529,0.9245051916,0.9300123612,0.9267109118,0.9292457388])
haar_rho1_lo = np.array([0.9194364008,0.8962643423,0.9169939953,0.9000590888,0.9093279635,0.9053453124,0.9095915076])
haar_rho1_hi = np.array([0.9776674555,0.9545782054,0.9497414191,0.9489492885,0.9516238373,0.9457509115,0.9496901013])
haar_rho2 = np.array([0.9826203311,0.9653300539,0.9615704423,0.9568905142,0.9574997645,0.9511742275,0.9584184295])

ry_n = np.array([6,8,10,12,14,16])
ry_rho1 = np.array([0.9336939175,0.9000647959,0.8911600216,0.8855683767,0.8741854790,0.8766269484])
ry_rho1_lo = np.array([0.9009143559,0.8722132542,0.8603444637,0.8702471060,0.8540593790,0.8652478319])
ry_rho1_hi = np.array([0.9645749136,0.9276193897,0.9184165311,0.9015673821,0.8951814174,0.8922606041])

cnot_n = np.array([6,8,10,12,14,16])
cnot_rho1 = np.array([0.9942262464,0.9810976077,0.9929654451,0.9846586585,0.9609656322,0.9523307476])
cnot_rho1_lo = np.array([0.9683384363,0.9575415988,0.9711893802,0.9691602166,0.9392429731,0.9411980865])
cnot_rho1_hi = np.array([1.0187983281,1.0046012035,1.0142374741,1.0015809889,0.9806906605,0.9635793777])

u1_n = np.array([6,8,10,12,14,16,18])
u1_rho1 = np.array([2.0581664696,4.2187756440,9.8857290031,25.4858264217,71.0250501817,205.2770861818,615.4756327726])
u1_rho2 = np.array([1.1921892517,1.897678,3.605633,7.881802,18.7700619701,47.64403,128.1769534555])

npurity_n = np.array([6,8,10,12,14,16,18])
npurity_generic = np.array([1.350,1.803,2.953,6.165,17.5235,49.8400,146.7611])
npurity_u1 = np.array([2.026,4.057,9.217,23.975,65.6140,189.2472,570.9119])
deif_generic = np.array([0.746,0.569,0.359,0.1767,0.0661933,0.02330894,0.00682704])
deif_u1 = np.array([0.496,0.247,0.109,0.0418,0.0152585,0.00529255,0.00175649])

generic_ret1 = np.array([rho*n/(2**n-1) for rho,n in zip(generic_rho1,n_generic)])
generic_ret1 = np.append(generic_ret1, 6.380648462082442e-05)
u1_ret1 = np.array([0.5416227552,0.4279917320,0.3544683706,0.3037314091,0.2691126938,0.2392692744,0.2152056965])

full_f_n = npurity_n.copy()
full_f_generic = np.array([0.4880235341,0.4901108206,0.4921,0.493578,0.4941052236,0.4949499187,0.4972776336])
full_f_u1 = np.array([0.4663406057,0.4760988012,0.4691,0.474777,0.4770316536,0.4752395018,0.4762603517])

# -------------------- Fig. 1: framework + theorem --------------------
fig = plt.figure(figsize=(7.15, 2.55))
gs = fig.add_gridspec(1, 3, width_ratios=[1.15,1,1], wspace=0.38)

ax = fig.add_subplot(gs[0,0]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off'); panel(ax,'a')
# compact schematic: symbols first, labels second
box1 = FancyBboxPatch((0.03,0.57),0.25,0.27,boxstyle='round,pad=0.015,rounding_size=0.02',fc='#F5F7FA',ec=BLACK,lw=0.8)
box2 = FancyBboxPatch((0.39,0.57),0.21,0.27,boxstyle='round,pad=0.015,rounding_size=0.02',fc='#F5F7FA',ec=BLACK,lw=0.8)
box3 = FancyBboxPatch((0.70,0.57),0.27,0.27,boxstyle='round,pad=0.015,rounding_size=0.02',fc='#F5F7FA',ec=BLACK,lw=0.8)
for b in (box1,box2,box3): ax.add_patch(b)
ax.text(.155,.77,r'$C$',ha='center',va='center',fontsize=13,fontweight='bold')
vals=np.array([.12,.20,.34,.56,.83]); xs=np.linspace(.08,.23,len(vals))
for x,v in zip(xs,vals): ax.plot([x,x],[.60,.60+.08*v],color=BLUE,lw=2)
ax.text(.495,.77,r'$P$',ha='center',va='center',fontsize=13,fontweight='bold')
ax.plot([.435,.555],[.61,.77],color=ORANGE,lw=2.4)
ax.plot([.435,.555],[.64,.64],color=MID,lw=.65)
ax.plot([.435,.435],[.64,.77],color=MID,lw=.65)
ax.text(.835,.76,r'$\mathrm{Tr}(PC)$',ha='center',va='center',fontsize=11,fontweight='bold')
ax.annotate('',xy=(.375,.705),xytext=(.29,.705),arrowprops=dict(arrowstyle='-|>',lw=.8,color=BLACK))
ax.annotate('',xy=(.685,.705),xytext=(.615,.705),arrowprops=dict(arrowstyle='-|>',lw=.8,color=BLACK))
ax.text(.50,.34,'rank-only reference',ha='center',fontsize=7,color=MID)
ax.text(.50,.23,r'$r/N$',ha='center',fontsize=13,color=BLACK)
ax.text(.50,.06,'spectrum + orientation determine deviations',ha='center',fontsize=6.9,color=BLACK)

ax = fig.add_subplot(gs[0,1]); panel(ax,'b')
x = np.logspace(0,6,400)
ax.plot(x,np.sqrt(2/x),color=BLUE,lw=1.8)
ax.fill_between(x,np.sqrt(2/x),1e-3,color=BLUE,alpha=.08)
ax.axvline(1e2,color=MID,lw=.7,ls=':')
ax.text(1.7e2,.22,'concentration\nstrengthens',fontsize=7.2,color=MID)
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlim(1,1e6); ax.set_ylim(1e-3,2)
ax.set_xlabel(r'$r\,d_{\rm eff}$')
ax.set_ylabel(r'bound on SD$(\rho)$')
ax.set_title('No isotropy assumption')
clean(ax)

ax = fig.add_subplot(gs[0,2]); panel(ax,'c')
n=np.arange(4,31)
N=2**n-1
r1=n
r2=n+n*(n-1)/2
ax.plot(n,r1/N,color=BLUE,lw=1.8,label='$k=1$')
ax.plot(n,r2/N,color=ORANGE,lw=1.8,ls='--',label=r'$k\leq2$')
ax.set_yscale('log'); ax.set_xlim(4,30); ax.set_ylim(1e-8,1)
ax.set_xlabel('qubits $n$'); ax.set_ylabel('rank fraction $r_k/N$')
ax.set_title('Fixed-weight readout')
ax.legend(frameon=False,loc='lower left')
clean(ax)
fig.savefig(OUT/'fig1_framework_theory.pdf',bbox_inches='tight')
plt.close(fig)

# -------------------- Fig. 2: rank typicality / architecture / anisotropy --------------------
fig = plt.figure(figsize=(7.15, 2.75))
gs = fig.add_gridspec(1,3,wspace=.36)

ax=fig.add_subplot(gs[0,0]); panel(ax,'a')
ax.axhspan(.90,1.10,color=BAND,alpha=.65,zorder=0)
ax.axhline(1,color=BLACK,lw=.7,ls='--')
ax.errorbar(n_generic,generic_rho1,yerr=np.vstack([generic_rho1-generic_rho1_lo,generic_rho1_hi-generic_rho1]),
            color=BLUE,marker='o',mfc='white',mec=BLUE,ms=4,lw=1.2,capsize=2,label='$k=1$')
ax.errorbar(n_generic,generic_rho2,yerr=np.vstack([generic_rho2-generic_rho2_lo,generic_rho2_hi-generic_rho2]),
            color=ORANGE,marker='s',mfc='white',mec=ORANGE,ms=4,lw=1.2,capsize=2,label='$k=2$')
ax.errorbar([18],[haar_rho1[-1]],yerr=[[haar_rho1[-1]-haar_rho1_lo[-1]],[haar_rho1_hi[-1]-haar_rho1[-1]]],
            color=BLUE,marker='D',mfc=BLUE,mec=BLUE,ms=4,capsize=2,lw=0,label='$n=18$ Haar-$U(4)$')
ax.plot([18],[haar_rho2[-1]],marker='D',color=ORANGE,ms=4,lw=0)
ax.set_xlim(5.2,18.8); ax.set_ylim(.84,1.12)
ax.set_xlabel('qubits $n$'); ax.set_ylabel(r'$\rho_k$')
ax.set_title('Generic aggregate')
ax.legend(frameon=False,loc='lower left',handlelength=1.6)
clean(ax)

ax=fig.add_subplot(gs[0,1]); panel(ax,'b')
ax.axhspan(.90,1.10,color=BAND,alpha=.65,zorder=0); ax.axhline(1,color=BLACK,lw=.7,ls='--')
for nvals,y,lo,hi,c,m,label in [
    (ry_n,ry_rho1,ry_rho1_lo,ry_rho1_hi,ORANGE,'v','RY-RZ-CZ'),
    (cnot_n,cnot_rho1,cnot_rho1_lo,cnot_rho1_hi,GREEN,'s','SU2-CNOT'),
    (haar_n,haar_rho1,haar_rho1_lo,haar_rho1_hi,BLUE,'o','Haar-$U(4)$')]:
    ax.errorbar(nvals,y,yerr=np.vstack([y-lo,hi-y]),color=c,marker=m,ms=3.8,lw=1.05,capsize=1.8,label=label)
ax.set_xlim(5.2,18.8); ax.set_ylim(.82,1.035)
ax.set_xlabel('qubits $n$'); ax.set_ylabel(r'$\rho_1$')
ax.set_title('One-body families')
ax.legend(frameon=False,loc='lower left',handlelength=1.5)
clean(ax)

ax=fig.add_subplot(gs[0,2]); panel(ax,'c')
xan=np.array([1.350,1.803,2.953,6.165,17.5235,49.84])
ax.axhspan(.90,1.10,color=BAND,alpha=.65,zorder=0); ax.axhline(1,color=BLACK,lw=.7,ls='--')
ax.plot(xan,generic_rho1,color=BLUE,lw=1.2,marker='o',ms=4)
for ni,xi,yi in zip(n_generic,xan,generic_rho1):
    ax.annotate(f'{ni}',(xi,yi),xytext=(3,4),textcoords='offset points',fontsize=6.8,color=BLACK)
ax.scatter([146.7611],[haar_rho1[-1]],marker='D',s=22,color=BLUE,zorder=3)
ax.annotate('18*',(146.7611,haar_rho1[-1]),xytext=(-17,5),textcoords='offset points',fontsize=6.8)
ax.set_xscale('log'); ax.set_xlim(1,230); ax.set_ylim(.89,1.01)
ax.set_xlabel(r'$N\,\mathrm{Tr}(C^2)$')
ax.set_ylabel(r'$\rho_1$')
ax.set_title('Anisotropy coexistence')
clean(ax)
fig.savefig(OUT/'fig2_rank_architecture_anisotropy.pdf',bbox_inches='tight')
plt.close(fig)

# -------------------- Fig. 3: symmetry and accessibility --------------------
fig = plt.figure(figsize=(7.15, 2.8))
gs = fig.add_gridspec(1,3,wspace=.38)

ax=fig.add_subplot(gs[0,0]); panel(ax,'a')
ax.plot(u1_n,u1_rho1,color=ORANGE,marker='o',ms=4,lw=1.4,label='$k=1$')
ax.plot(u1_n,u1_rho2,color=PURPLE,marker='s',ms=4,lw=1.4,ls='--',label='$k=2$')
ax.axhline(1,color=BLACK,lw=.7,ls=':')
ax.set_yscale('log'); ax.set_xlim(5.2,18.8)
ax.set_xlabel('qubits $n$'); ax.set_ylabel(r'$U(1)$ enhancement $\rho_k$')
ax.set_title('Enhancement')
ax.legend(frameon=False,loc='upper left')
clean(ax)

ax=fig.add_subplot(gs[0,1]); panel(ax,'b')
ax.plot(npurity_n,generic_ret1,color=BLUE,marker='o',ms=4,lw=1.4,label='generic / Haar-$U(4)^*$')
ax.plot(npurity_n,u1_ret1,color=ORANGE,marker='s',ms=4,lw=1.4,label='$U(1)$')
ax.set_yscale('log'); ax.set_xlim(5.2,18.8); ax.set_ylim(3e-5,1)
ax.set_xlabel('qubits $n$'); ax.set_ylabel('one-body retained fraction')
ax.set_title('Retained fraction')
ax.legend(frameon=False,loc='lower left')
clean(ax)

ax=fig.add_subplot(gs[0,2]); panel(ax,'c')
ax.plot(npurity_n,npurity_generic,color=BLUE,marker='o',ms=4,lw=1.4,label='generic / Haar-$U(4)^*$')
ax.plot(npurity_n,npurity_u1,color=ORANGE,marker='s',ms=4,lw=1.4,label='$U(1)$')
ax.set_yscale('log'); ax.set_xlim(5.2,18.8)
ax.set_xlabel('qubits $n$'); ax.set_ylabel(r'$N\,\mathrm{Tr}(C^2)$')
ax.set_title('Anisotropy')
ax.legend(frameon=False,loc='upper left')
clean(ax)
fig.savefig(OUT/'fig3_symmetry_accessibility.pdf',bbox_inches='tight')
plt.close(fig)

# -------------------- Fig. 4: spectral mechanism + depth --------------------
fig = plt.figure(figsize=(7.15, 3.15))
gs = fig.add_gridspec(1,2,width_ratios=[1.35,1],wspace=.33)

ax=fig.add_subplot(gs[0,0]); panel(ax,'a')
cases=['CNOT\n$n=8$','Haar-$U(4)$\n$n=10$','Haar-$U(4)$\n$n=12$','$U(1)$\n$n=10$','$U(1)$\n$n=12$']
physical=np.array([0.0304512,0.00901370,0.00270872,0.363972,0.291544])
cross=np.array([0.0696250,0.0484132,0.0306155,0.432369,0.375421])
ky=np.array([0.126102,0.107604,0.0915351,0.483489,0.443598])
y=np.arange(len(cases))[::-1]
for yi,p,c,k in zip(y,physical,cross,ky):
    ax.plot([p,k],[yi,yi],color='#C5C7CA',lw=1.1,zorder=0)
ax.scatter(physical,y,color=ORANGE,marker='o',s=26,label='physical')
ax.scatter(cross,y,color=BLUE,marker='s',s=25,label='cross-fit')
ax.scatter(ky,y,color=BLACK,marker='D',s=22,label='sample Ky-Fan')
ax.set_xscale('log'); ax.set_xlim(1e-3,0.8)
ax.set_yticks(y,cases); ax.set_xlabel('one-body retained tangent mass')
ax.set_title('Information exists, but physical readout can miss it')
ax.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,-.28),handletextpad=.35,columnspacing=.8)
clean(ax)

ax=fig.add_subplot(gs[0,1]); panel(ax,'b')
depth=np.array([.5,1,2,4,6,8])
ng=np.array([11.62,6.79,4.03,2.41,1.905,1.686])
nu=np.array([9.015,6.721,5.304,4.424,4.182,3.864])
ax.plot(depth,ng,color=BLUE,marker='o',ms=4,lw=1.4,label='generic')
ax.plot(depth,nu,color=ORANGE,marker='s',ms=4,lw=1.4,label='$U(1)$')
ax.set_yscale('log'); ax.set_xlabel('depth factor $d/n$'); ax.set_ylabel(r'$N\,\mathrm{Tr}(C^2)$')
ax.set_title('Depth changes the spectral regime')
ax.legend(frameon=False)
clean(ax)
fig.savefig(OUT/'fig4_spectral_mechanism_depth.pdf',bbox_inches='tight')
plt.close(fig)

# -------------------- Fig. 5: full record vs low-weight accessibility --------------------
fig = plt.figure(figsize=(7.15, 2.8))
gs=fig.add_gridspec(1,3,wspace=.38)

ax=fig.add_subplot(gs[0,0]); panel(ax,'a')
ax.plot(full_f_n,full_f_generic,color=BLUE,marker='o',ms=4,lw=1.4,label='generic / Haar-$U(4)^*$')
ax.plot(full_f_n,full_f_u1,color=ORANGE,marker='s',ms=4,lw=1.4,label='$U(1)$')
ax.set_ylim(.455,.505); ax.set_xlim(5.2,18.8)
ax.set_xlabel('qubits $n$'); ax.set_ylabel(r'$F_{\rm full}/F_Q$')
ax.set_title('Full record')
ax.legend(frameon=False,loc='lower right')
clean(ax)

ax=fig.add_subplot(gs[0,1]); panel(ax,'b')
ax.plot(npurity_n,generic_ret1,color=BLUE,marker='o',ms=4,lw=1.4,label='generic / Haar-$U(4)^*$')
ax.plot(npurity_n,u1_ret1,color=ORANGE,marker='s',ms=4,lw=1.4,label='$U(1)$')
ax.set_yscale('log'); ax.set_ylim(3e-5,1); ax.set_xlim(5.2,18.8)
ax.set_xlabel('qubits $n$'); ax.set_ylabel('one-body retained fraction')
ax.set_title('Low-weight access')
clean(ax)

ax=fig.add_subplot(gs[0,2]); panel(ax,'c')
for i,nv in enumerate(npurity_n):
    ax.scatter(full_f_generic[i],generic_ret1[i],color=BLUE,marker='o',s=18)
    ax.scatter(full_f_u1[i],u1_ret1[i],color=ORANGE,marker='s',s=18)
    if nv in (6,12,18):
        ax.annotate(str(nv),(full_f_generic[i],generic_ret1[i]),xytext=(3,2),textcoords='offset points',fontsize=6.5,color=BLUE)
        ax.annotate(str(nv),(full_f_u1[i],u1_ret1[i]),xytext=(3,2),textcoords='offset points',fontsize=6.5,color=ORANGE)
ax.set_yscale('log'); ax.set_xlim(.455,.505); ax.set_ylim(3e-5,1)
ax.set_xlabel(r'$F_{\rm full}/F_Q$'); ax.set_ylabel('one-body retained fraction')
ax.set_title('Same total scale, different access')
clean(ax)
fig.savefig(OUT/'fig5_full_record_vs_accessible.pdf',bbox_inches='tight')
plt.close(fig)

# -------------------- Supplemental figures --------------------
# S1 effective dimension fraction
fig,ax=plt.subplots(figsize=(3.35,2.45))
ax.plot(npurity_n,deif_generic,color=BLUE,marker='o',ms=4,lw=1.4,label='generic / Haar-$U(4)^*$')
ax.plot(npurity_n,deif_u1,color=ORANGE,marker='s',ms=4,lw=1.4,label='$U(1)$')
ax.set_yscale('log'); ax.set_xlabel('qubits $n$'); ax.set_ylabel(r'$d_{\rm eff}/N$')
ax.legend(frameon=False); clean(ax)
fig.tight_layout(); fig.savefig(OUT/'figS1_deff_fraction.pdf',bbox_inches='tight'); plt.close(fig)

# S2 exact-vs-bound theoretical SD for several effective dimensions
fig,ax=plt.subplots(figsize=(3.35,2.45))
N=2**14-1
for deff,c,ls,label in [(10,ORANGE,'-',r'$d_{\rm eff}=10$'),(100,GREEN,'--',r'$10^2$'),(1000,BLUE,'-.',r'$10^3$')]:
    r=np.arange(1,500)
    q=1/deff
    var=2*(N-r)*(N*q-1)/(r*(N-1)*(N+2))
    ax.plot(r,np.sqrt(np.maximum(var,0)),color=c,ls=ls,lw=1.2,label=label)
ax.plot(np.arange(1,500),np.sqrt(2/np.arange(1,500)),color=BLACK,lw=.8,ls=':',label=r'$\sqrt{2/r}$')
ax.set_yscale('log'); ax.set_xscale('log'); ax.set_xlabel('readout rank $r$'); ax.set_ylabel(r'SD$(\rho)$')
ax.legend(frameon=False,ncol=2,fontsize=6.7); clean(ax)
fig.tight_layout(); fig.savefig(OUT/'figS2_exact_null_width.pdf',bbox_inches='tight'); plt.close(fig)

# S3 U1 population-null z at large n vs generic/Haar targeted values (effect direction only)
fig,ax=plt.subplots(figsize=(3.35,2.45))
labels=['generic\n$n=14$','generic\n$n=16$','Haar-$U(4)$\n$n=18$','$U(1)$\n$n=14$','$U(1)$\n$n=16$','$U(1)$\n$n=18$']
z=np.array([-1.9253,-2.1719,-1.6695,1049.6,3547.9,10870.3])
x=np.arange(len(labels))
ax.axhline(0,color=BLACK,lw=.7)
ax.scatter(x[:3],z[:3],color=BLUE,marker='o',s=22,label='generic / Haar-$U(4)^*$')
ax.scatter(x[3:],z[3:],color=ORANGE,marker='s',s=22,label='$U(1)$')
ax.set_yscale('symlog',linthresh=5); ax.set_xticks(x,labels,rotation=30,ha='right')
ax.set_ylabel('population-null orientation $z$ (diagnostic)')
ax.legend(frameon=False,fontsize=6.8); clean(ax)
fig.tight_layout(); fig.savefig(OUT/'figS3_orientation_z.pdf',bbox_inches='tight'); plt.close(fig)

# S4 rank-baseline scaling itself for k=1,2 with n range
fig,ax=plt.subplots(figsize=(3.35,2.45))
n=np.arange(4,31); N=2**n-1
r1=n; r2=n+n*(n-1)/2
ax.plot(n,r1/N,color=BLUE,lw=1.4,label='$k=1$')
ax.plot(n,r2/N,color=ORANGE,lw=1.4,ls='--',label=r'$k\leq2$')
ax.set_yscale('log'); ax.set_xlabel('qubits $n$'); ax.set_ylabel('$r_k/(2^n-1)$')
ax.legend(frameon=False); clean(ax)
fig.tight_layout(); fig.savefig(OUT/'figS4_rank_fraction.pdf',bbox_inches='tight'); plt.close(fig)

print('Wrote', len(list(OUT.glob('*.pdf'))), 'figure PDFs to', OUT)
