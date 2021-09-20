# sofi_chewie
chewieSnake for SOFI.

## Prerequisites
chewieSnake must be installed and available as a command. In a dev environment, the
preferred way is by using the Mamba package manager - see chewieSnake install instructions.

## How to use this repo
- Check out this repo somewhere on your filesystem.
- Copy the folder config.template as a new folder outside of the repo; call it f. ex. 'cs', so 'cp -r config.template ../cs'.
This folder will contain species-specific subfolders which will contain everything related to that species: config, schemas, sample list, output, etc.
- For each species you want to run chewieSnake on, download an allele scheme and place it beneath
cs/(species)/schemes. Some schemes can be found here: https://seafile.bfr.berlin/d/b4a619b12db14c5eab74/
- For each species, edit config.sh so that is has the correct parameters.

## Prepare environment variables
- Make sure the chewiesnake command is availableconda activate chewiesnake
- cd /path/to/cs/Species_underscored
- . config.sh
- Check that environment variables are set correctly:
echo $SPECIES
echo $SCHEME
echo $PRODIGAL
echo $OUTPUT

## Prepare sample list
maintain_sample_list.py is a script for creating and maintaining sample lists for chewieSnake.
Normally these sample lists will be species-specific, i. e. you will maintain one "global"
sample list for all samples of a specific species. With this list, you can run chewieSnake
for that specific species. Since the list not only contains new samples but also old ones, chewieSnake
will not only calculate distances between new samples but also between old and new ones.

Decide what sequence data input folder you want to run though chewieSnake. It's probably a good idea
to set the path in an envvar ($SEQDATA like in the example below).

Example:
python maintain_sample_list.py /path/to/cs/$SPECIES/sample_list.tsv -d $SEQDATA -s $SPECIES

It's important to use the $SPECIES option since this will make a list only with samples of the
relevant species. maintain_sample_list.py will looku p the species in a file named run_metadata.tsv
in the seqdata folder.

## Run chewieSnake

Example:
cd /path/to/cs/Salmonella_enterica
chewiesnake -t 10 --reads \
--sample_list sample_list.tsv \
--scheme $SCHEME \
--prodigal $PRODIGAL \
--working_directory $OUTPUT

Note that the $SCHEME location has to be writeable since chewieSnake will place temporary data in it.
Most importantly, it will place a folder named .lock which indicates that a chewieSnake process is active
using this scheme. This would prevent more chewieSnake processes running on the same data.
