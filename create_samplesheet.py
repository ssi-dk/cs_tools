import argparse
import pathlib

"""
Create and maintain a global sample sheet for chewieSnake.

Currently only fastq files are supported, and fastq file names must follow the
Illumina standard:

{samplename}_S*_R{1,2}_001.fastq*

Author: Finn Gruwier Larsen, figl@ssi.dk
"""

parser = argparse.ArgumentParser(description="Create and maintain a global sample sheet for chewieSnake.")
parser.add_argument('-d', '--fastq_dir', help="Path to existing directory containing fastq files. Default: current directory.")
parser.add_argument('-s', '--sample_sheet', help="Path and filename for global sample sheet."
    "Default: value of envvar $GLOBAL_SAMPLE_SHEET. If file does not exist it will be created.")
args = parser.parse_args()

