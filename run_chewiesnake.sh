#!/bin/bash

### Specify group name to resource manager
#PBS -A fvst_ssi_dtu

### Specify group name to resource manager
#PBS -W x=advres:fvst_ssi_dtu_wiki_fodevarestyrelsen.16

### Specify resources
#PBS -l nodes=1:ppn=4,mem=12gb,walltime=12:00:00,advres=fvst_ssi_dtu_wiki_fodevarestyrelsen.16

if [[ -z "${DEV_ENV}" ]]; then
  echo Load chewieSnake from module
  module load tools
  module load chewiesnake/3.0.0
fi

cmd="chewiesnake -t 10 --reads \
--sample_list /home/projects/fvst_ssi_dtu/test_data/cs/Salmonella_enterica/sample_list.tsv \
--scheme /home/projects/fvst_ssi_dtu/test_data/cs/Salmonella_enterica/schemes/enterobase_senterica_cgmlst \
--prodigal $CONDA_PREFIX/opt/chewiesnake/chewBBACA/CHEWBBACA/prodigal_training_files/Salmonella_enterica.trn \
--working_directory /home/projects/fvst_ssi_dtu/test_data/cs/Salmonella_enterica/output"

if [ "$1" == "--dryrun" ]; then
 cmd="${cmd} --dryrun"
fi

if [ "$1" == "--unlock" ]; then
 cmd="${cmd} --unlock"
fi

$cmd
