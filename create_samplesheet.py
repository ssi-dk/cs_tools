import argparse
import pathlib
import os
import sys

"""
Create and maintain a global sample sheet for chewieSnake.

Currently only fastq files are supported, and fastq file names must follow the
Illumina standard:

{samplename}_S*_R{1,2}_001.fastq*

Author: Finn Gruwier Larsen, figl@ssi.dk
"""

def get_new_samples(fastq_dir: pathlib.Path):
    r1_files_gen = fastq_dir.glob("*_S*_R1_001.fastq*")
    while True:
        try:
            print(next(r1_files_gen))
        except StopIteration:
            break

parser = argparse.ArgumentParser(description="Create and maintain a global sample sheet for chewieSnake.")
parser.add_argument('-s', '--sample_sheet', help="Path and filename for global sample sheet."
    "Default: value of envvar $GLOBAL_SAMPLE_SHEET. If file does not exist it will be created.")
parser.add_argument('-d', '--fastq_dir', help="Path to existing directory containing fastq files. Default: current directory.")
args = parser.parse_args()
try:
    sample_sheet_path = pathlib.Path(args.sample_sheet or os.getenv('GLOBAL_SAMPLE_SHEET'))
except TypeError:
    print("--sample_sheet not set and no value found for $GLOBAL_SAMPLE_SHEET. Exiting.")
    sys.exit(1)
print(f"Sample sheet: {sample_sheet_path}")
fastq_dir = pathlib.Path(args.fastq_dir or os.getcwd())
print(f"Folder to add: {fastq_dir}")

"""
samples = SampleContainer(sample_sheet)
new_samples = get_new_samples(fastq_dir)
for new_sample in new_samples:
    try:
        samples.add(new_sample)
    except ValueError:
        print(f"Could not add sample...")
samples.save()
"""
