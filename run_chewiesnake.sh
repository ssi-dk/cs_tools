#!/bin/sh
module load tools
module load chewiesnake/3.0.0
chewiesnake -t 10 --reads \
--sample_list /home/projects/fvst_ssi_dtu/test_data/cs/Salmonella_enterica/sample_list.tsv \
--scheme /home/projects/fvst_ssi_dtu/test_data/cs/Salmonella_enterica/schemes/enterobase_senterica_cgmlst \
--prodigal $CONDA_PREFIX/opt/chewiesnake/chewBBACA/CHEWBBACA/prodigal_training_files/Salmonella_enterica.trn \
--working_directory /home/projects/fvst_ssi_dtu/test_data/cs/Salmonella_enterica/output
