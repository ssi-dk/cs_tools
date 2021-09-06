import argparse
import os
import pathlib

import pymongo

bifrost_db_key = os.getenv("BIFROST_DB_KEY", "mongodb://localhost/bifrost_test")
mg = pymongo.MongoClient(bifrost_db_key)
db = mg.get_default_database()
print(f"Using {db}")

def line_reader(file_name):
    """Get lines from text file one by one using a generator
    """
    with open(file_name, 'r') as file_handler:
        for row in file_handler:
            yield row

def line_splitter(line: str, splitter: str):
    """Get values from a line in a csv file one by one
    """
    # Todo: generator?
    return (value for value in line.rstrip().split(splitter))


def update_distance_matrix(distance_matrix_file: pathlib.Path, hashids_dict: dict, species_name: str):
    # Open collection for the species, or create if new
    # print(db.list_collections())

    # Note: the distance_matrix.tsv file from chewieSnake uses space as separator.
    print(f"Iterate over distance matrix file {distance_matrix_file}...")
    distance_matrix_reader = line_reader(distance_matrix_file)
    for line in distance_matrix_reader:
        elements_gen = line_splitter(line, ' ')
        sample_name = next(elements_gen)
        allele_hash_id = hashids_dict[sample_name]
        print(f"Sample {sample_name} has allele hash id {allele_hash_id}.")
        # Check if allele_hash_id already exists in for species

        # key = species_name + ':' + sample_name
        # print("Key:", key)
        # Make a Redis 'sorted set' entry with distances as scores and sample names as values
        # Todo: check for existing key.
        # r.zadd(key, {sample_name: next(elements_gen) for sample_name in sample_names})
    return True


def main():
    parser = argparse.ArgumentParser(description="Dump chewieSnake data to MongoDB.")
    parser.add_argument('working_directory', help="Directory with output data from chewieSnake.")
    parser.add_argument(
        'species', help="Species name with underscore notation, case sensitive (e. g. 'Salmonella_enterica'). " + \
        "A collection with this name will be created in MongoDB if it does not exist.")
    args = parser.parse_args()
    working_directory = pathlib.Path(args.working_directory)

    # Initialize hashids_dict
    hashids_file = pathlib.Path(working_directory, 'cgmlst', 'hashids.tsv')
    hashids_reader = line_reader(hashids_file)
    next(hashids_reader)  # Skip header line
    hashids_dict = dict()
    for line in hashids_reader:
        elements = line_splitter(line, '\t')
        sample_name = next(elements)
        hash_id = next(elements)
        hashids_dict[sample_name] = hash_id
    distance_matrix_file = pathlib.Path(working_directory, 'cgmlst', 'distance_matrix.tsv')
    result = update_distance_matrix(distance_matrix_file, hashids_dict, args.species)

if __name__ == '__main__':
    main()
