def plot_setup():

    from pylab import gca
    import matplotlib.pyplot as plt

    for axis in ['top', 'right', 'bottom', 'left']:
        gca().spines[axis].set_linewidth(1.5)

    gca().xaxis.set_tick_params(width=1.5,bottom=True,which='both')
    gca().yaxis.set_tick_params(width=1.5)

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)


import pandas as pd
import matplotlib.pyplot as plt
from pylab import gca
import numpy as np


dict_calc={'sp': 'orange', 'opt': 'blue', 'freq': 'purple'}
list_sys=['ice']
max_core=64

fig,ax=plt.subplots(figsize=(7,5),dpi=300)
plot_setup()
plt.xlabel('Cores')
plt.ylabel('Elapsed Time (s)')
    
for calc in dict_calc:
    df=pd.read_csv('/home/bmpeluzo/Dropbox/Rochester/Research/bluehive/results_teraeth_1node_%s_barbara_%s.dat' %(list_sys[0],calc),sep='\t')
    x=[]
    y=[]
    core=4
    while core <= max_core:
        df_2=df[df['n_cores']==core]
        x.append(core)
        y.append(df_2.t_elapse)
        core=2*core
    plt.plot(x,y,label=calc,marker='o',linestyle='--',markersize=8)#,marker='o','--',color=dict_calc[calc],markersize=8)
            #plt.title(calc)
    plt.legend(loc=0)
    plt.savefig('/home/bmpeluzo/Dropbox/Rochester/Research/bluehive/results_teraeth_1node_%s_%s.png' %(list_sys[0],calc))
    plt.show()

