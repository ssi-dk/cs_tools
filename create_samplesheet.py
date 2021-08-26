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

    def __init__(self, sample_sheet_path: pathlib.Path):
        self._sample_sheet_path = sample_sheet_path
        with open(self._sample_sheet_path, 'r') as sample_sheet:
            for (sample_name, file1, file2) in read_sample_sheet(sample_sheet):
                self._samples[sample_name] = (file1, file2)
    
    def add_sample(self, sample_name: str, file1: str, file2: str):
        self._samples[sample_name] = (file1, file2)

    def save():
        """Todo:
            With self._sample_sheet_path open for writing:
            Write to file overwriting any existing version
        """
        pass

def read_sample_sheet(sample_sheet):
    output = list()
    next(sample_sheet)  # Ignore header
    while True:
        try:
            line: str = next(sample_sheet)
            sample_name, file1, file2 = line.split('\t')
            output.append((sample_name, file1, file2))
        except StopIteration:
            break
    return output

def find_new_samples(fastq_dir: pathlib.Path):
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


samples = SampleContainer(SAMPLE_SHEET_PATH)

"""
new_samples = find_new_samples(FASTQ_DIR)
for new_sample in new_samples:
    try:
        samples.add(new_sample)
    except ValueError:
        print(f"Could not add sample...")
samples.save()
"""