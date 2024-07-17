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
part='teraeth'
n_nodes='1'
sys='ice'
list_calc=['sp', 'opt']#, 'freq']
list_vers=['barbara']

for vers in list_vers:
    
    for calc in list_calc:
        out_file=open(path+'results_%s_%snode_%s_%s_%s.dat'%(part,n_nodes,sys,vers,calc),'w+')
        out_file.write('n_cores\tn_cyc\tt_elapse\tt_cpu\tpar_eff\n')
        tex_file=open(path+'results_%s_%snode_%s_%s_%s.tex'%(part,n_nodes,sys,vers,calc),'w+')
        t_serial=get_telapse(path+'%s/%snode/%s/%s/%s_%s_1.out'%(part,n_nodes,sys,vers,sys,calc))
        for i in np.arange(4,68,4):
            cry_out=path+'%s/%snode/%s/%s/%s_%s_%s.out'%(part,n_nodes,sys,vers,sys,calc,i)
            telapse=get_telapse(cry_out=cry_out)
            tcpu=get_tcpu(cry_out=cry_out)
            if calc == 'opt':
                n_cyc=get_opt_cycles(cry_out=cry_out) ## we are not taking the number of scf cycles in a geom opt
            else:
                n_cyc=get_scf_cycles(cry_out=cry_out)
            par_eff=(t_serial/(telapse*i))*100
            out_file.write('%d\t%d\t%f\t%f\t%.1f\n'%(i,n_cyc,telapse,tcpu,par_eff))
            tex_file.write('%d & %.1f & %.1f \\\\ \n'%(i,telapse,par_eff))
        out_file.close()
        tex_file.close()


