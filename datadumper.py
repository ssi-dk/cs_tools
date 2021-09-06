import argparse
import os
import pathlib

bifrost_db_key = os.getenv("BIFROST_DB_KEY", "mongodb://localhost/bifrost_test")

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
    # Note: the distance_matrix.tsv file from chewieSnake uses space as separator.
    distance_matrix_reader = line_reader(distance_matrix_file)
    for line in distance_matrix_reader:
        elements_gen = line_splitter(line, ' ')
        sample_name = next(elements_gen)
        print("Sample name:", sample_name)
        # key = species_name + ':' + sample_name
        # print("Key:", key)
        # Make a Redis 'sorted set' entry with distances as scores and sample names as values
        # Todo: check for existing key.
        # r.zadd(key, {sample_name: next(elements_gen) for sample_name in sample_names})


        # Todo: add argument --working_directory (chewieSnake output directory)
        # Todo: add argument --species
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
    result = update_distance_matrix(distance_matrix_file, hashids_file, args.species)

if __name__ == '__main__':
    main()
