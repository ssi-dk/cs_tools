import argparse
import os

from chewieSnake import main

# Note: the following lines are copied from chewieSnake.py
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--sample_list',
                    help='List of samples to analyze, as a two column tsv file with columns sample and assembly. Can be generated with provided script create_sampleSheet,sh',
                    required=True, type=os.path.abspath)

args = parser.parse_args()
chewie_sample_list = args.sample_list

main()