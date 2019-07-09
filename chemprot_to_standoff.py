"""
Converts the ChemProt corpus to a Brat-flavoured Standoff format.

Usage:

1. Download the ChemProt corpus from here:
    https://biocreative.bioinformatics.udel.edu/resources/corpora/chemprot-corpus-biocreative-vi/
    (Note: you will need to sign in).
2. For each partition 'chemprot_training', 'chemprot_development', 'chemprot_test_gs' in the
    extracted ChemProt directory, call

    ```
    >>> python chemprot_to_standoff.py -i <original_chemprot_partition_filepath> \
        -o <standoff_chemprot_partition_filepath>
    ```
"""
import argparse
import errno
import os
import re
from glob import glob


def main(**kwargs):
    """Converts the ChemProt corpus to a Brat-flavoured Standoff format.
    """
    make_dir(kwargs['output'])

    for filepath in glob(os.path.join(kwargs['input'], '*.tsv')):
        filename = os.path.splitext(filepath)[0]

        # Convert abstract file
        if re.search('abstracts', filename):
            with open(filepath, 'r') as in_file:
                converted_abstracts = convert_abstracts_to_standoff(in_file)

            write_to_disk(converted_abstracts, ext='txt')

        # Convert entity file
        elif re.search('entities', filename):
            with open(filepath, 'r') as in_file:
                converted_entities = convert_entities_to_standoff(in_file)

        # Convert relation file
        elif re.search('gold_standard', filename):
            with open(filepath, 'r') as in_file:
                converted_relations = convert_relations_to_standoff(in_file)

    # Concat converted entities and relations so we can save one dict to disk
    for pmid in converted_entities:
        if pmid in converted_relations:
            converted_entities[pmid] = f'{converted_entities[pmid]}\n{converted_relations[pmid]}'

    write_to_disk(converted_entities, ext='ann')


def convert_abstracts_to_standoff(f):
    """Given a file open for reading, returns a dict containing abstract texts keyed by PMID.

    Given a `*_abstracts.tsv` file from the ChemProt corpus which is open for reading, returns
    a dictionary containing the abstract texts, keyed by PubMed IDs (PMIDs)

    Args:
        f (TextIO): An `*_abstracts.tsv` fril from the ChemProt corpus, open for reading.

    Returns:
        A dictionary containing the abstract texts from `f`, keyed by PubMed IDs (PMIDs).
    """
    file_contents = f.read().strip().split('\n')

    return {abst.split('\t')[0]: '\n'.join(abst.split('\t')[1:]) for abst in file_contents}


def convert_entities_to_standoff(f):
    """Given a file open for reading, returns a dict containing entity annotations keyed by PMID.

    Given a `*_entities.tsv` file from the ChemProt corpus which is open for reading, returns
    a dictionary containing the entity annotations, keyed by PubMed IDs (PMIDs)

    Args:
        f (TextIO): An `*_entities.tsv` fril from the ChemProt corpus, open for reading.

    Returns:
        A dictionary containing the entity annotations from `f`, keyed by PubMed IDs (PMIDs).
    """
    converted_entities = {}

    for line in f:
        if line:
            pmid, T, label, start_offset, end_offset, text = line.strip().split('\t')

            if pmid not in converted_entities:
                converted_entities[pmid] = []

            converted_entities[pmid].append(f'{T}\t{label} {start_offset} {end_offset}\t{text}')

    # Convert list of annotations to a string
    converted_entities = {pmid: '\n'.join(anns) for (pmid, anns) in converted_entities.items()}

    return converted_entities


def convert_relations_to_standoff(f):
    """Given a file open for reading, returns a dict containing relation annotations keyed by PMID.

    Given a `*_relations.tsv` file from the ChemProt corpus which is open for reading, returns
    a dictionary containing the relation annotations, keyed by PubMed IDs (PMIDs)

    Args:
        f (TextIO): An `*_relations.tsv` fril from the ChemProt corpus, open for reading.

    Returns:
        A dictionary containing the relation annotations from `f`, keyed by PubMed IDs (PMIDs).
    """
    R = 1  # Counter for the relation identifier in standoff format
    converted_relations = {}

    for line in f:
        if line:
            pmid, label, arg_1, arg_2 = line.strip().split('\t')

            if pmid not in converted_relations:
                converted_relations[pmid] = []
                R = 1

            converted_relations[pmid].append(f'R{R}\t{label} {arg_1} {arg_2}')

            R += 1

    # Convert list of annotations to a string
    converted_relations = {pmid: '\n'.join(anns) for (pmid, anns) in converted_relations.items()}

    return converted_relations


def write_to_disk(converted_dict, ext='txt'):
    """
    """
    for pmid, item in converted_dict.items():
        filename = os.path.join(kwargs['output'], f'{pmid}.{ext}')

        with open(filename, 'w') as f:
            f.write(item)


# https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist#273227
def make_dir(directory):
    """Creates a directory at `directory` if it does not already exist.
    """
    try:
        os.makedirs(directory)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    description = ()
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input', help='Filepath to ChemProt corpus.',
                        type=str, required=True)
    parser.add_argument('-o', '--output', help='Directory to save converted corpus.',
                        type=str, required=True)

    kwargs = vars(parser.parse_args())

    main(**kwargs)
