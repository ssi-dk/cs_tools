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


if [[ -z "${PBS_O_WORKDIR}" ]]; then
  echo PBS_O_WORKDIR not set - probably this is not a qsub job.
  exit 1
fi

# Go to the directory from where the job was submitted
echo Working directory: $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

# Read parameters from species config
source config.sh
echo Species: $SPECIES
SAMPLE_LIST=$PBS_O_WORKDIR/$1
echo Sample list: $SAMPLE_LIST
SCHEME=$PBS_O_WORKDIR/schemes/$SCHEME
echo Scheme: $SCHEME
echo Prodigal file: $PRODIGAL
OUTPUT=$PBS_O_WORKDIR/$OUTPUT
echo Output directory: $OUTPUT

cmd="chewiesnake -t 10 --reads \
--sample_list $SAMPLE_LIST \
--scheme $SCHEME \
--prodigal $PRODIGAL \
--working_directory $OUTPUT"

if [ "$2" == "--dryrun" ]; then
 cmd="${cmd} --dryrun"
fi

if [ "$2" == "--unlock" ]; then
 cmd="${cmd} --unlock"
fi

$cmd
