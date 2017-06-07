'''
    FastaGen - Yevheniy Chuba - 6/1/2017
    Prepares sequences from various groups for multiple alignment,
    by combining sequences of the same group into a single fasta file, and
    adding PDB sequence to each file.
    The output is the list of fasta file names separated by group.

    Usage:
        multi_align_fasta_files = FastaGen(group_id_seq).process_seqs()
'''

class FastaGen:

    def __init__(self, seq_ds, pdb_ds):
        self.seq_ds = seq_ds
        self.pdb_ds = pdb_ds

    def process_seqs(self):
        file_names = []
        pdb_seq = self.get_pdb_seq()
        for group_id, seqs in self.seq_ds.iteritems():
            output_file_name = 'group_{}.fasta'.format(group_id)
            file_names.append(output_file_name)
            with open(output_file_name, 'w') as output_f:
                for record in seqs:
                    seq_id = record[0]
                    seq = record[1]
                    output_f.write('>{}\n'.format(seq_id))
                    output_f.write(seq)
                    output_f.write('\n')
                # add pdb sequence
                output_f.write('>pdb_seq\n')
                output_f.write(pdb_seq)
                output_f.write('\n')
        return file_names

    def get_pdb_seq(self):
        pdb_seq = []
        for chain in self.pdb_ds:
            pdb_seq.append(chain[1])
        return ''.join(pdb_seq)
