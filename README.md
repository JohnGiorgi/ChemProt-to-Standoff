# ChemProt To Standoff

A simple script that converts the ChemProt corpus to a Brat flavoured standoff format.

## Usage

Clone (or download) this repo:

```
$ git clone https://github.com/JohnGiorgi/ChemProt-to-Standoff.git
$ cd ChemProt-to-Standoff
```

Download and extract the ChemProt corpus from [here](https://biocreative.bioinformatics.udel.edu/resources/corpora/chemprot-corpus-biocreative-vi/).

> Note, you will need to create an account and sign in.

For each partition `'chemprot_training'`, `'chemprot_development'`, and `'chemprot_test_gs'` in the extracted ChemProt directory, call

```
$ python chemprot_to_standoff.py -i <original_chemprot_partition_filepath> -o <standoff_chemprot_partition_filepath>
```