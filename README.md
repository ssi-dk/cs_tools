# sofi_chewie
chewieSnake for SOFI.

## Installation

- Check out this repo somewhere on your filesystem.
- Install Mamba.
- Create Mamba environment: mamba create -c r -c bioconda -c conda-forge -n chewiesnake chewiesnake
- Check that you can activate the environment: conda activate chewiesnake.
- Copy the folder config.template to a location of your choice. This folder will contain
species-specific configuration subfolders.
- For each species you want to run chewieSnake on, download an allele scheme and place it beneath
config/(species)/schemes.
- For each species, edit config.sh so that is has the correct parameters.

## Prepare a sample list
maintain_sample_list.py is a script for creating and maintaining sample lists for chewieSnake.
Normally these sample lists will be species-specific, i. e. you will maintain one "global"
sample list for all samples of a specific species. With this list, you can run chewieSnake
for that specific species. Since the list not only contains new samples but also old ones, chewieSnake
will not only calculate distances between new samples but also between old and new ones.

(Todo: describe usage of maintain_sample_list.py)

## Run chewieSnake
conda activate chewiesnake
cd (config)/(species)
. config.sh
chewiesnake -t 10 --reads \
--sample_list (sample list location) \
--scheme $SCHEME \
--prodigal $PRODIGAL \
--working_directory output
