import sys
import argparse
import dendropy

"""
File: taxon_pairs_freqs.py
Author: Nicholas Crawford

Created by Brant Faircloth on Wed May  1 12:53:09 EDT 2013
Copyright (c) 2012 Nicholas G. Crawford All rights reserved.

Description...

Example: Print all the taxon ids in the first tree.

    python taxon_pairs_freqs.py \
    --print-taxa turtles-genetrees.steac.trees

Example: Palculate split frequencies.

    python taxon_pairs_freqs.py \
    -p HomSapie,AnoCarol PanGutta,SphTuata \
    GalGallu,ZebFinch CroPoros,AllMissi ChrPicta,PelSubru \
    -i turtles-genetrees.steac.trees
"""


def get_args():
    """Parse sys.argv"""

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Path to output. (default is STOUT)')

    parser.add_argument('-i', '--input',
                        help='File of newick trees.')

    parser.add_argument('--print-taxa',
                        action='store_true',
                        help='Print all the taxon ids in the first tree.')

    parser.add_argument('-p', '--pairs',
                        nargs='*',
                        default=False,
                        help="List of species pairs with each pair delimited by commas.")

    args = parser.parse_args()
    return args


def print_taxon_ids(args):
    """Print out all the taxon ids in the first taxon."""

    trees = dendropy.TreeList()
    with open(args.input, mode='r') as fin:
        trees.read_from_stream(fin, 'newick')
        for label in trees[0].taxon_set.labels():
            args.output.write('{}\n'.format(label))


def calc_split_frequencies(args):
    """Calculate the split frequencies for the supplied taxon pairs."""

    trees = dendropy.TreeList()

    with open(args.input, mode='r') as fin:
        trees.read_from_stream(fin, 'newick')

        pairs = [p.split(",") for p in args.pairs]

        for p in pairs:
            f = trees.frequency_of_split(labels=p)
            args.output.write('Frequency of split {0}: {1}\n'.format(p, f))


def main():
    args = get_args()
    if args.print_taxa is True:
        print_taxon_ids(args)
        sys.exit()

    calc_split_frequencies(args)

if __name__ == '__main__':
    main()
