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

with open(sample_sheet_path, 'a') as samples:
    print(f"Opened sample sheet: {sample_sheet_path}")

    fastq_dir = pathlib.Path(args.fastq_dir or os.getcwd())
    print(f"Looking for fastq files in {fastq_dir}")
    # sample_files = fastq_dir.glob("{samplename}_S*_R{1,2}_001.fastq*")