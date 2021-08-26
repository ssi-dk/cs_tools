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


class SampleContainer:
    _samples: dict = {}
    _sample_sheet_path: pathlib.Path

    def __init__(self):
        self._sample_sheet_path = SAMPLE_SHEET_PATH
        """Todo:
            With SAMPLE_SHEET_PATH open for reading:
            Add existing samples to _samples
        """
    
    def add_sample(sample_name):
        """Todo: add to _samples. Directory is defined in FASTQ_DIR. Filenames follow Illumina standard."""
        pass

    def save():
        """Todo:
            With SAMPLE_SHEET_PATH open for writing:
            Write to file overwriting any existing version
        """
        pass


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
    SAMPLE_SHEET_PATH = pathlib.Path(args.sample_sheet or os.getenv('GLOBAL_SAMPLE_SHEET'))
except TypeError:
    print("--sample_sheet not set and no value found for $GLOBAL_SAMPLE_SHEET. Exiting.")
    sys.exit(1)
print(f"Sample sheet: {SAMPLE_SHEET_PATH}")
FASTQ_DIR = pathlib.Path(args.fastq_dir or os.getcwd())
print(f"Folder to add: {FASTQ_DIR}")

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
