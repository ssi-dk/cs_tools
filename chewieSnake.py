#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys

version = "3.0.0"


def check_sample_list(sample_list):
    # Check whether sample list has header
    type1 = "sample\tfq1\tfq2\n"
    type2 = "sample\tassembly\n"

    with open(sample_list, 'r') as handle:
        header_line = handle.readline()

    if header_line != type1 and header_line != type2:
        print(
            "ERROR: sample list " + sample_list + " does not have a proper header. Make sure that first line is \nsample\tfq1\tfq2\nor\nsample\tassembly\n(tab-separated)")
        sys.exit(1)


def create_config(configfile, args):
    # Check existence
    if not os.path.exists(args.scheme):
        print("path to scheme " + args.scheme + "does not exist")
        sys.exit(1)
    if not os.path.exists(args.prodigal):
        print("path to prodigal training file " + args.prodigal + "does not exist")
        sys.exit(1)
    if not os.path.exists(args.sample_list):
        print("path to sample list " + args.sample_list + "does not exist")
        sys.exit(1)

    # check if sample list has proper format
    check_sample_list(args.sample_list)



    outfile = open(configfile, "w")
    outfile.write("#Created by chewieSnake.py v{}\n".format(version))

    outfile.write('workdir:\n    "{}"\n'.format(args.working_directory))
    outfile.write('samples:\n    "{}"\n'.format(args.sample_list))

    # general parameters:
    outfile.write('parameters:\n  threads: {}\n'.format(args.threads_sample))
    outfile.write('  remove_frameshifts: {}\n'.format(args.remove_frameshifts))

    # chewbbaca parameters:
    outfile.write(
        '  chewbbaca:\n    bsr_theshold: {}\n    size_threshold: {}\n    scheme_dir: "{}"\n    prodigal_training_file: "{}"\n'.format(
            args.bsr_threshold, args.size_threshold, args.scheme, args.prodigal))

    # clustering parameters:
    outfile.write(
        '  clustering:\n    clustering_method: "{}"\n    distance_threshold: {}\n    address_range: "{}"\n    comparison_allele_database: "{}"\n    joining_threshold: {}\n    grapetree_distance_method: {}\n'.format(
            args.clustering_method, args.distance_threshold, args.address_range, args.comparison_db,
            args.joining_threshold, args.distance_method))

    # frameshift parameters
    outfile.write('  frameshift_removal:\n    remove_frameshifts: {}\n    mode: {}\n    threshold: {}\n'.format(
        args.remove_frameshifts, args.frameshift_mode, args.allele_length_threshold))

    # assembly paramerters
    if args.reads:
        outfile.write('  fastp:\n    length_required: {}\n'.format(args.min_trimmed_length))
        outfile.write(
            '  shovill:\n    assembler: "{}"\n    output_options: "{}"\n    depth: "{}"\n    tmpdir: "{}"\n    extraopts: "{}"\n    modules: "{}"\n'.format(
                args.assembler, args.shovill_output_options, args.shovill_depth, args.shovill_tmpdir,
                args.shovill_extraopts, args.shovill_modules))

    outfile.close()


def run_snakemake(configfile, args, snakefile):
    if args.forceall:
        forceall = "--forceall"
    else:
        forceall = ""

    if args.unlock:
        unlock = "--unlock"
    else:
        unlock = ""

    if args.comparison:
        force = "-f all_database_comparison"
    elif args.report:
        force = "-f all_report"
    else:
        force = ""

    if args.dryrun:
        dryrun = "-n"
    else:
        dryrun = ""

    if args.conda_frontend:
        frontend = "conda"
    else:
        frontend = "mamba"

    if args.use_conda:
        call = "snakemake -p --conda-prefix {CondaPrefix} --use-conda --keep-going --configfile {configfile} --snakefile {snakefile} {force} {dryrun} {forceall} {unlock} --cores {threads} --use-conda --conda-frontend {frontend}".format(
            CondaPrefix=args.condaprefix, snakefile=snakefile, configfile=configfile, force=force, dryrun=dryrun,
            forceall=forceall, unlock=unlock, threads=args.threads, frontend=frontend)
    else:
        call = "snakemake -p --keep-going --configfile {configfile} --snakefile {snakefile} {force} {dryrun} {forceall} {unlock} --cores {threads}".format(
            CondaPrefix=args.condaprefix, snakefile=snakefile, configfile=configfile, force=force, dryrun=dryrun,
            forceall=forceall, unlock=unlock, threads=args.threads)

    print(call)
    subprocess.call(call, shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--sample_list',
                        help='List of samples to analyze, as a two column tsv file with columns sample and assembly. Can be generated with provided script create_sampleSheet,sh',
                        required=True, type=os.path.abspath)
    parser.add_argument('-d', '--working_directory', help='Working directory where results are saved', required=True,
                        type=os.path.abspath)
    parser.add_argument('--condaprefix',
                        help='Path of default conda environment, enables recycling built environments, default is in folder conda_env in repository directory.',
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "conda_env"), required=False)
    parser.add_argument('--reads',
                        help='Input data is reads. Assemble (using shovill) prior to allele calling (default is contigs)',
                        action='store_true', default=False, required=False)
    parser.add_argument('--scheme', help='Path to directory of the cgmlst scheme', required=True)
    parser.add_argument('--prodigal',
                        help='Path to prodigal_training_file (e.g. provided in chewbbaca, path/to/chewieSnake/chewBBACA/CHEWBBACA/prodigal_training_files, e.g. ' + os.path.join(
                            os.path.dirname(os.path.realpath(__file__)), "chewBBACA/CHEWBBACA/prodigal_training_files",
                            "Salmonella_enterica.trn"), required=True)
    parser.add_argument('--bsr_threshold', help='blast scoring ratio threshold to use , default = 0.6', default=0.6,
                        required=False)
    parser.add_argument('--size_threshold',
                        help='size threshold, default at 0.2 means alleles with size variation of +-20 percent will be tagged as ASM/ALM , default = 0.2',
                        default=0.2, required=False)
    parser.add_argument('--distance_method', help='Grapetree distance method; default = 3', default=3, required=False)
    parser.add_argument('--clustering_method',
                        help=' The agglomeration method to be used for hierarchical clustering. This should be (an unambiguous abbreviation of) one of "ward.D", "ward.D2", "single", "complete", "average" (= UPGMA), "mcquitty" (= WPGMA), "median" (= WPGMC) or "centroid" (= UPGMC); default = single',
                        default="single", required=False)
    parser.add_argument('--distance_threshold',
                        help='A single distance threshold for the extraction of sub-trees; default = 10', default=10,
                        required=False)
    parser.add_argument('--address_range',
                        help='A comma separated set of cutoff values for defining the clustering address (Default: 1,5,10,20,50,100,200,1000)',
                        default="1,5,10,20,50,100,200,1000", required=False)
    parser.add_argument('--report', help='Create html report', default=False, action='store_true', required=False)
    parser.add_argument('--comparison', help='Compare these results to pre-computed allele database', default=False,
                        action='store_true', required=False)
    parser.add_argument('--comparison_db', help='Path to pre-computed allele database for comparison', required=False)
    parser.add_argument('--joining_threshold',
                        help='A distance threshold for joining data with comparsion_db; default = 30', default=30,
                        required=False)

    # frameshifts
    parser.add_argument('-f', '--remove_frameshifts', help='remove frameshift alleles by deviating allele length',
                        default=False, action='store_true', required=False)
    parser.add_argument('--allele_length_threshold',
                        help='Maximum tolerated allele length deviance compared to median allele length of locus; choose integer for "absolute frameshift mode and float (0..1) for "relative" frameshift mode ; default=0.1',
                        default=0.1, required=False)
    parser.add_argument('--frameshift_mode',
                        help='Whether to consider absolute or relative differences of allele length for frameshifts removal. Choose from "absolute" and "relative", default="relative"',
                        default="relative", required=False)

    # trimming and assembly
    parser.add_argument('--min_trimmed_length', help='Minimum length of a read to keep, default = 15', default=15,
                        required=False)
    parser.add_argument('--assembler',
                        help='Assembler to use in shovill, choose from megahit velvet skesa spades (default: spades)',
                        default="spades", required=False)
    parser.add_argument('--shovill_output_options', help='Extra output options for shovill (default: "")', default="",
                        required=False)
    parser.add_argument('--shovill_extraopts', help='Extra options for shovill (default: "")', default="",
                        required=False)
    parser.add_argument('--shovill_modules',
                        help='Module options for shovill, choose from --noreadcorr --trim --nostitch --nocorr --noreadcorr (default: "--noreadcorr")',
                        default="--noreadcorr", required=False)
    parser.add_argument('--shovill_depth',
                        help='Sub-sample --R1/--R2 to this depth. Disable with --depth 0 (default: 100)', default=100,
                        required=False)
    parser.add_argument('--shovill_tmpdir', help='Fast temporary directory (default: "")', default="/tmp/",
                        required=False)
    parser.add_argument('--use_conda',
                        help='Utilize "--useconda" option, i.e. all software dependencies are available in a single env',
                        default=False, action='store_true',
                        required=False)
    parser.add_argument('--conda_frontend',
                        help='Do not mamba but conda as frontend to create individual module\' software environments',
                        default=False, action='store_true',
                        required=False)
    parser.add_argument('--threads_sample', help='Number of Threads to use per sample, default = 10', default=10,
                        required=False)
    parser.add_argument('-t', '--threads',
                        help='Number of Threads to use. Note that samples can only be processed sequentially due to the required database access. However the allele calling can be executed in parallel for the different loci, default = 10',
                        default=10, required=False)
    parser.add_argument('-n', '--dryrun', help='Snakemake dryrun. Only calculate graph without executing anything',
                        default=False, action='store_true', required=False)
    parser.add_argument('--forceall', help='Snakemake force. Force recalculation of all steps', default=False,
                        action='store_true', required=False)
    parser.add_argument('--unlock', help='unlock snakemake', default=False, action='store_true', required=False)
    parser.add_argument('--logdir', help='Path to directory whete .snakemake output is to be saved', default='NA',
                        required=False)

    args = parser.parse_args()

    if not os.path.exists(args.working_directory):
        os.makedirs(args.working_directory)

    configfile = os.path.join(args.working_directory, "config.yaml")
    create_config(configfile, args)

    if args.reads:
        print("Executing the read-based version including assembly step")
        snakefile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chewieSnake_readbased.smk")
    else:
        print("Executing the contig-based version")
        snakefile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chewieSnake_fromcontigs.smk")

    if os.path.exists(configfile):
        run_snakemake(configfile, args, snakefile)
    else:
        print("Path to configfile does not exist: " + configfile)


if __name__ == '__main__':
    main()
