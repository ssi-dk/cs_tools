# sofi_chewie
chewieSnake for SOFI.

## Installation

- Check out this repo.
- Install Mamba.
- Create Mamba environment: mamba create -c r -c bioconda -c conda-forge -n chewiesnake chewiesnake
- Activate environment: conda activate chewiesnake


## Usage

### Maintain sample list

maintain_sample_list.py is a script for creating and maintaining sample lists for chewieSnake.
Normally these sample lists will be species-specific, i. e. you will maintain one "global"
sample list for all samples of a specific species. With this list, you can run chewieSnake
for that specific species. Since the list not only contains new samples, chewieSnake will not
only calculate distances between new samples but also between old and new ones.