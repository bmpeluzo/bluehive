# bluehive

## runcry.sh

Update the .bashrc/.zshrc file:

alias runcry='/home/bteixeir/scr/runcry.sh'

syntax:
`runcry -j *job_name* -c *number_of_cores* -p *partition*`



required flags:
-j job name
-c number of cores (between 1 and the max number of cores in the node)
-p cluster partition (teraeth, vermont)

optional flags:
-r project - project name for organization
-n number of nodes
-f additional file e.g. file1.f9, file2.f33...
-F additional file e.g. FREQINFO.DAT

