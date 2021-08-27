import argparse
import pathlib
import os
import sys
from typing import Iterable

"""
Create and maintain a global sample list for controlling chewieSnake.

Currently only fastq files are supported, and fastq file names must follow the
Illumina standard:

{samplename}_S*_R{1,2}_001.fastq*

Author: Finn Gruwier Larsen, figl@ssi.dk
"""


class SampleContainer:
    _samples: dict = {}
    _sample_list_path: pathlib.Path

    def __init__(self, sample_list_path: pathlib.Path):
        self._sample_list_path = sample_list_path
        if self._sample_list_path.exists():
            print(f"{str(self._sample_list_path)} exists - reading file.")
            with open(self._sample_list_path, 'r') as sample_list:
                for (sample_name, file1, file2) in read_sample_list(sample_list):
                    self.add_sample(sample_name, file1, file2)
        else:
            print(f"{str(self._sample_list_path)} does not exist - new file.")
    
    def add_sample(self, sample_name: str, file1: str, file2: str):
        if sample_name in self._samples:
            print(f"Error: we already have a sample with sample name {sample_name}.")
            print("Exiting without modifying the file.")
            sys.exit()
        self._samples[sample_name] = (file1, file2)
    
    def list_samples(self):
        return ((k, v[0], v[1]) for k, v in self._samples.items())

    def save(self):
        with open(self._sample_list_path, 'w') as sample_list:
            for k, v in self._samples.items():
                line = '\t'.join((k, v[0], v[1])) + '\n'
                print(f"Adding line: {line}")
                sample_list.write(line)
            

def read_sample_list(sample_list):
    output = list()
    try:
        next(sample_list)  # Ignore header
    except StopIteration:
        print("File exists but contains no samples.")
    while True:
        try:
            line: str = next(sample_list)
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

def print_samples(sample_iter: Iterable):
    print("(SampleID , File 1)")
    for sample in sample_iter:
        print(sample[0], sample[1])

def main():
    parser = argparse.ArgumentParser(description="Create and maintain a global sample list for chewieSnake.")
    parser.add_argument('-l', '--sample_list', help="Path and filename for global sample list."
        "Default: value of envvar $GLOBAL_SAMPLE_list. If file does not exist it will be created.")
    parser.add_argument('-d', '--fastq_dir', help="Path to existing directory containing fastq files. Default: current directory.")
    args = parser.parse_args()
    try:
        SAMPLE_LIST_PATH = pathlib.Path(args.sample_list or os.getenv('GLOBAL_SAMPLE_list'))
    except TypeError:
        print("--sample_list / -l not set and no value found for $GLOBAL_SAMPLE_LIST. Exiting.")
        sys.exit(1)

    print(f"Sample list path: {SAMPLE_LIST_PATH}")
    container = SampleContainer(SAMPLE_LIST_PATH)
    print("OLD SAMPLES:")
    print_samples(container.list_samples())
    FASTQ_DIR = pathlib.Path(args.fastq_dir or os.getcwd())
    print(f"Folder to add fastq files from: {FASTQ_DIR}")

    new_samples = find_new_samples(FASTQ_DIR)
    print("NEW SAMPLES:")
    print_samples(new_samples)

    for new_sample in new_samples:
        container.add_sample(*new_sample)
    container.save()

if __name__ == '__main__':
    main()