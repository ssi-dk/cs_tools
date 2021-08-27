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
        if self._sample_sheet_path.exists():
            print(f"{str(self._sample_sheet_path)} exists - reading file.")
            with open(self._sample_sheet_path, 'r') as sample_sheet:
                for (sample_name, file1, file2) in read_sample_sheet(sample_sheet):
                    self.add_sample(sample_name, file1, file2)
        else:
            print(f"{str(self._sample_sheet_path)} does not exist - new file.")
    
    def add_sample(self, sample_name: str, file1: str, file2: str):
        if sample_name in self._samples:
            print(f"We already have a sample with sample name {sample_name}. Exiting.")
            sys.exit()
        self._samples[sample_name] = (file1, file2)

    def save(self):
        with open(self._sample_sheet_path, 'w') as sample_sheet:
            for k, v in self._samples.items():
                line = '\t'.join((k, v[0], v[1])) + '\n'
                print(f"Adding line: {line}")
                sample_sheet.write(line)
            

def read_sample_sheet(sample_sheet):
    output = list()
    try:
        next(sample_sheet)  # Ignore header
    except StopIteration:
        print("File exists but contains no samples.")
    while True:
        try:
            line: str = next(sample_sheet)
            sample_name, file1, file2 = line.rstrip().split('\t')
            output.append((sample_name, file1, file2))
        except StopIteration:
            break
    return output

def find_new_samples(fastq_dir: pathlib.Path):
    """
    Find samples in folder. Return a list of (sample_name, file1, file2)
    where file1, file2 have full paths.
    """
    r1_files_gen = fastq_dir.glob("*_S*_R1_001.fastq*")
    output = list()
    while True:
        try:
            file1_path = pathlib.Path(next(r1_files_gen))
            sample_name = file1_path.stem[:-22]
            file1_filename = file1_path.parts[-1]
            listified_filename = list(file1_filename)
            listified_filename[-14] = '2'
            file2_filename = ''.join(listified_filename)
            file2_path = file1_path.with_name(file2_filename)
            assert(file2_path.exists())
            output.append((sample_name, str(file1_path), str(file2_path)))
        except StopIteration:
            break
    return output

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

print(f"Sample sheet path: {SAMPLE_SHEET_PATH}")
container = SampleContainer(SAMPLE_SHEET_PATH)
print("*** OLD SAMPLES:")
print(container._samples)
FASTQ_DIR = pathlib.Path(args.fastq_dir or os.getcwd())
print(f"Folder to add fastq files from: {FASTQ_DIR}")

new_samples = find_new_samples(FASTQ_DIR)
print("*** NEW SAMPLES:")
print(new_samples)
for new_sample in new_samples:
    container.add_sample(*new_sample)
container.save()