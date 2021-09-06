# sofi_chewie
chewieSnake for SOFI.

## Installation

- Check out this repo somewhere on your filesystem.
- Install Mamba.
- Create Mamba environment: mamba create -c r -c bioconda -c conda-forge -n chewiesnake chewiesnake
- Activate the environment: conda activate chewiesnake
- Install pymongo in environment: mamba install pymongo
- Copy the folder config.template to a location of your choice. This folder will contain
species-specific configuration subfolders.
- For each species you want to run chewieSnake on, download an allele scheme and place it beneath
config/(species)/schemes.
- For each species, edit config.sh so that is has the correct parameters.

## Prepare environment
conda activate chewiesnake
cd /path/to/config/species
. config.sh
Check that environment variables are set correctly:
echo $SPECIES
echo $SCHEME
echo $PRODIGAL

## Prepare sample list
maintain_sample_list.py is a script for creating and maintaining sample lists for chewieSnake.
Normally these sample lists will be species-specific, i. e. you will maintain one "global"
sample list for all samples of a specific species. With this list, you can run chewieSnake
for that specific species. Since the list not only contains new samples but also old ones, chewieSnake
will not only calculate distances between new samples but also between old and new ones.

Example:
python maintain_sample_list.py /path/and/filename/for/sample/list -d /path/to/new/fastq/dir -s $SPECIES

## Run chewieSnake
chewiesnake -t 10 --reads \
--sample_list /path/and/filename/for/sample/list \
--scheme $SCHEME \
--prodigal $PRODIGAL \
--working_directory /directory/where/you/want/the/output

Note that the $SCHEME location has to be writeable since chewieSnake will place some temporary data in it.
Most importantly, it will place a folder named .lock which indicates that a chewieSnake process is active
using this scheme. This should prevent race conditions with more chewieSnake processes running on the same data.
