import os
import argparse
import pathlib
import shutil
import subprocess
from datetime import datetime


start_time = datetime.now()

CHEWIESNAKE_IMAGE_ID = os.getenv("CHEWIESNAKE_IMAGE_ID")
CHEWIESNAKE_MOUNT_POINT = os.getenv("CHEWIESNAKE_MOUNT_POINT")
CHEWIESNAKE_OUTPUT_SUBFOLDER = os.getenv("CHEWIESNAKE_OUTPUT_SUBFOLDER", "output")
PATH_INSIDE_CONTAINER = "/chewieSnake/analysis"  # Should not be changed as this is what chewieSnake expects
BIFROST_DB_KEY = os.getenv("BIFROST_DB_KEY", "mongodb://localhost/bifrost_test")

parser = argparse.ArgumentParser(description='Run chewieSnake with selected samples and save allele profiles to MongoDB.')
parser.add_argument('-s','--sample_names', nargs='+', help='Sample names (strip read numbers and extension from file names).')
parser.add_argument('-d','--delete_old_output', action='store_true', help='Delete old output folder')
args = parser.parse_args()

lines = ["sample\tfq1\tfq2\n"]

for sample_name in args.sample_names:
    file_name_1 = f"{sample_name}_R1_001.fastq.gz"
    file_name_2 = f"{sample_name}_R2_001.fastq.gz"
    line = f"{sample_name}\t{PATH_INSIDE_CONTAINER}/{file_name_1}\t{PATH_INSIDE_CONTAINER}/{file_name_2}\n"
    lines.append(line)

mount_point = pathlib.Path(CHEWIESNAKE_MOUNT_POINT)
assert mount_point.exists()
output_subfolder = pathlib.Path(mount_point, CHEWIESNAKE_OUTPUT_SUBFOLDER)
if args.delete_old_output and output_subfolder.exists():
    print("Output subfolder already exists and will be deleted!")
    shutil.rmtree(output_subfolder)
samples_tsv_path = pathlib.Path(mount_point, 'samples.tsv')

with open(samples_tsv_path, 'w') as file:
    file.writelines(lines)
    file.write("\n")

command = f"""docker run --rm \
-v {CHEWIESNAKE_MOUNT_POINT}:{PATH_INSIDE_CONTAINER} \
-e LOCAL_USER_ID=$(id -u $USER) \
{CHEWIESNAKE_IMAGE_ID} \
--reads \
--sample_list {PATH_INSIDE_CONTAINER}/samples.tsv \
--scheme {PATH_INSIDE_CONTAINER}/enterobase_senterica_cgmlst \
--prodigal {PATH_INSIDE_CONTAINER}/Salmonella_enterica.trn \
--working_directory {PATH_INSIDE_CONTAINER}/output
"""
print("Command:")
print(command)

process = subprocess.Popen(
    command,
    # stdout=subprocess.PIPE,
    # stderr=subprocess.PIPE,
    shell=True,
    env=os.environ
)
process_out, process_error = process.communicate()
"""Note: if there's only one sample you'll always get an error from 
Grapetree, but it doesn't matter in our case."""

end_time = datetime.now()
processing_time = end_time - start_time
print(f"Script ran in {processing_time}.")