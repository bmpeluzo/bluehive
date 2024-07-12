def file_io(cry_out):   # open crystal output file and store file content as string

	import os

	cry_str=[]
	with open('%s' %cry_out, 'r') as out_file:
        	for line in out_file:
            		cry_str.append(line)
	out_file.close()

	return cry_str


def get_scf_cycles(cry_out):
	for line in range(len(file_io(cry_out))):
		scf_str=file_io(cry_out)[line].find("SCF ENDED")
		if scf_str!=-1:
			n_scf=int(file_io(cry_out)[line].split()[len(file_io(cry_out)[line].split())-1])
			break
	return(n_scf)


def get_telapse(cry_out):
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


def get_tcpu(cry_out):
	for line in range(len(file_io(cry_out))):
		tcpu_str=file_io(cry_out)[line].find("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT END")
		if tcpu_str!=-1:
			for i in range(len(file_io(cry_out)[line].split())):
				tcpu_str2=file_io(cry_out)[line].split()[i].find("TCPU")
				if tcpu_str2!=-1:
					tcpu=float(file_io(cry_out)[line].split()[i+1])
					break
			break
	return(tcpu)



print(get_tcpu('../tests/crystal_compilation/ice_sp_barbara.out'))


