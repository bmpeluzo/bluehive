def file_io(cry_out):   # open crystal output file and store file content as string

	import os

	cry_str=[]
	with open('%s' %cry_out, 'r') as out_file:
        	for line in out_file:
            		cry_str.append(line)
	out_file.close()

	return cry_str


def get_scf_cycles(cry_out): # get the number of scf cycles
	for line in range(len(file_io(cry_out))):
		scf_str=file_io(cry_out)[line].find("SCF ENDED")
		if scf_str!=-1:
			n_scf=int(file_io(cry_out)[line].split()[len(file_io(cry_out)[line].split())-1])
			break
	return(n_scf)


def get_telapse(cry_out):  # get the telapse time
	for line in range(len(file_io(cry_out))):
		telapse_str=file_io(cry_out)[line].find("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT END")
		if telapse_str!=-1:
			for i in range(len(file_io(cry_out)[line].split())):
				telapse_str2=file_io(cry_out)[line].split()[i].find("TELAPSE")
				if telapse_str2!=-1:
					telapse=float(file_io(cry_out)[line].split()[i+1])
					break
			break
	return(telapse)


def get_tcpu(cry_out): # get the cpu time
	for line in range(len(file_io(cry_out))):
		tcpu_str=file_io(cry_out)[line].find("TOTAL CPU TIME")
		if tcpu_str!=-1:
			tcpu=float(file_io(cry_out)[line].split()[len(file_io(cry_out)[line].split())-1])
			break
	return(tcpu)

def get_opt_cycles(cry_out):
	for line in range(len(file_io(cry_out))):
		opt_str=file_io(cry_out)[line].find("OPT END")
		if opt_str!=-1:
			n_opt=int(file_io(cry_out)[line].split()[len(file_io(cry_out)[line].split())-2])
			break
	return(n_opt)

##################### loop over files ########################

import numpy as np

path='/home/bteixeir/parallel_tests/'
list_part=['teraeth', 'vermont1', 'vermont2']
list_nodes=[1, 2]
sys='ice'
#list_calc=['sp']
calc='sp'
vers='barbara'
dft='pbe'
run=1
init_core=4
final_core=48
step_core=4

if dft == 'b3lyp':
    name=sys
else:
    name=sys+'_'+dft

out_file=open(path+'results_%s_%s.dat'%(name,calc),'w+')
out_file.write('n_nodes\tn_tasks_per_node\tn_cores\tt_elapse_teraeth\tt_cpu_teraeth\tspeed_up_teraeth\tpar_eff_teraeth\tt_elapse_vermont1\tt_cpu_vermont1\tspeed_up_vermont1\tpar_eff_vermont1\tt_elapse_vermont2\tt_cpu_vermont2\tspeed_up_vermont2\tpar_eff_vermont2\n')
tex_file=open(path+'results_%s_%s.tex'%(name,calc),'w+')

for n_nodes in list_nodes:
    #for calc in list_calc:
    if n_nodes == 1:
        tex_file.write('1 & 1 & 1 &')
        out_file.write('1\t1\t1\t')
        for part in list_part:
            t_serial=get_telapse(path+'%s/1node/%s/%s/%d/%s_%s_1.out'%(part,sys,vers,run,name,calc))
            cry_out=path+'%s/%snode/%s/%s/%d/%s_%s_1.out'%(part,n_nodes,sys,vers,run,name,calc)
            telapse=get_telapse(cry_out=cry_out)
            #tcpu=get_tcpu(cry_out=cry_out)
            tex_file.write(' %.1f &  N/A & N/A &'%(telapse))
            out_file.write('%.1f\t1\t100'%(telapse))
            if part == list_part[len(list_part)-1]:
                tex_file.write('\\\\ \n')
                out_file.write('\n')
    for i in np.arange(init_core,final_core+1,step_core):
        tex_file.write('%d & %d & %d &' %(n_nodes, i, n_nodes*i)) 
        out_file.write('%d\t%d\t%d\t' %(n_nodes, i, n_nodes*i)) 
        for part in list_part: 
            t_serial=get_telapse(path+'%s/1node/%s/%s/%d/%s_%s_1.out'%(part,sys,vers,run,name,calc))
            cry_out=path+'%s/%snode/%s/%s/%d/%s_%s_%s.out'%(part,n_nodes,sys,vers,run,name,calc,i)
            telapse=get_telapse(cry_out=cry_out)
            #tcpu=get_tcpu(cry_out=cry_out)
        #if calc == 'opt':
            #n_cyc=get_opt_cycles(cry_out=cry_out) ## we are not taking the number of scf cycles in a geom opt
        #else:
            #n_cyc=get_scf_cycles(cry_out=cry_out)
            par_eff=(t_serial/(telapse*i*n_nodes))*100
            speedup=t_serial/telapse
            tex_file.write(' %.1f & %.2f & %.2f'%(telapse,speedup,par_eff))
            out_file.write('%.1f\t%.2f\t%.2f'%(telapse,speedup,par_eff))
            if part == list_part[len(list_part)-1]:
                tex_file.write('\\\\ \n')
                out_file.write('\n')
            else:
                tex_file.write('&')
        #out_file.write('%d\t%d\t%d\t%d\t%f\t%f\t%.1f\n'%(n_nodes,i,n_nodes*i,n_cyc,telapse,tcpu,par_eff))
out_file.close()
tex_file.close()
