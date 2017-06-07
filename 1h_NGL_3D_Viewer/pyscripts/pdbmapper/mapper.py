#!/usr/local/bin/python
import os.path
import json
from argparse import ArgumentParser
from collections import OrderedDict

import PdbParser as pp
import MultiAlign as ma
import InputProcessor as ip
import FastaGen as fg

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle


def cli_options():
    """
        Get the file name to process. This is the accepted file format
        used for Insight's fornt-end.
    """
    parser = ArgumentParser(description="Maps PDB files to Sequences")

    parser.add_argument("-f", dest="filename", required=True,
                        help="same file format loaded into Insight - csv, Excell are supported",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))

    parser.add_argument("-pdb", dest="pdb_name", required=True,
                        help="The path name to file location under PDB_Struct dir or the PDB ID")

    args = parser.parse_args()

    return args

# Retrieve file the file object
cli_args = cli_options()
file_to_process = cli_args.filename
pdb_name = cli_args.pdb_name
# generate the group: [id, seq], ... dictionary
group_id_seq = ip.InputProcessor(file_to_process).process_input()
# extract sequence from PDB
pdb_ds = pp.PdbParser(pdb_name).pdb_processing()
# generate a list of fasta files for multiple alignment
multi_align_fasta_files = fg.FastaGen(group_id_seq, pdb_ds).process_seqs()
# perfrom multiple alignment for each file
all_aligned = OrderedDict()
for fasta in multi_align_fasta_files:
    aligned_key = fasta.split('.')[0]
    all_aligned[aligned_key] = ma.MultiAlign(clustal_input=fasta,
                                       clustal_output='out_{}'.format(fasta),
                                       clustalw='clustalw2').perform_alignment()
# print(all_aligned)
    # OrderedDict([('group_1', {seq_id: seq}),
                # ...

def get_pdb_seq_chain(ds):
    chain_length = []
    for chain in ds:
        chain_length.append([chain[0], len(chain[1])])
    return chain_length

# retrieve [[chain_name, length], ...]
chain_name_length = get_pdb_seq_chain(pdb_ds)
# print ('chain names: ', chain_name_length)

def get_json(ds):
    for group_name, ma_obj in ds.iteritems():
        pdb_seq_aligned = ma_obj['pdb_seq']
        key = ma_obj.keys()[3]
        ref_seq_aligned = ma_obj[key]
        map_pdb_to_ref = OrderedDict()
        pdb_counter = 1
        chain_name = 'L'
        for i, aa in enumerate(pdb_seq_aligned):
            if aa != '-':
                map_pdb_to_ref['{}.{}'.format(pdb_counter, chain_name)] = [aa, ref_seq_aligned[i], i+1]
                if pdb_counter == 107 and chain_name == 'L':
                    pdb_counter = 0
                    chain_name = 'H'
                pdb_counter += 1
        return json.dumps(map_pdb_to_ref)

json_output = get_json(all_aligned)
print json_output
