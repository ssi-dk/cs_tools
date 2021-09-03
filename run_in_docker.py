import os
import argparse
import pathlib
import shutil
import subprocess
from datetime import datetime

PATH_INSIDE_CONTAINER = "/chewieSnake/analysis"  # Should not be changed as this is what chewieSnake expects

parser = argparse.ArgumentParser(description="Run chewieSnake in Docker container.")
parser.add_argument('-m','--mount_point', help="Path that the Docker container will use for 'everything'.")
args = parser.parse_args()

chewiesnake_image_id = os.getenv("CHEWIESNAKE_IMAGE_ID")
chewiesnake_output_subfolder = os.getenv("CHEWIESNAKE_OUTPUT_SUBFOLDER", "output")
start_time = datetime.now()

command = f"""docker run --rm \
-v {args.mount_point}:{PATH_INSIDE_CONTAINER} \
-e LOCAL_USER_ID=$(id -u $USER) \
{chewiesnake_image_id} \
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