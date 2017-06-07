'''
    MultiAlign.py - Yevheniy Chuba - 6/1/2017
    Perform multiple alignment using ClustalW

    Usage:
        multi_align = MultiAlign(clustal_input='create.fasta').perform_alignment()
        output:
            {seq_id: seq}
        commandline utility exectued:
            clustalw2 -infile=create.fasta -outfile=clustal_out.fasta
'''
from collections import OrderedDict
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO

class MultiAlign:
    '''
        MultiAlign performs multiple alignment using BioPython's
        ClustalW wrapper.

        Args:
            clustal_input(str): .fasta input file with multiple sequences
            clustal_output(str): .fasta output file in Clustal format
            clustal_w(str): the location of the clustalw2 command line utility
                            - make sure it is in the system's or user's bin directory
                            - this tool is usually downloaded manually and doesn't come
                            as BioPython's dependency
                            - make sure it has proper permissions (give it 777 if not sure)

        Returns:
            A dictionary, mapping sequence id to sequence string

        Usage:
            multi_align = MultiAlign(clustal_input='create.fasta')
            id_seq_map = multi_align.perform_alignment()
    '''
    def __init__(self, clustal_input='clustal_in.fasta',
                 clustal_output='clustal_out.fasta', clustalw='clustalw2'):
        self.clustal_input = clustal_input
        self.clustal_output = clustal_output
        self.clustalw = clustalw

    def perform_alignment(self):
        clustalw_cline = ClustalwCommandline(self.clustalw,
                                             infile=self.clustal_input,
                                             outfile=self.clustal_output)
        print(clustalw_cline)
        stdout, stderr = clustalw_cline()
        # print(stdout, '\n', stderr)

        align = AlignIO.read(self.clustal_output, "clustal")
        id_seq = self.extract_seqs(align)
        return id_seq

    def extract_seqs(self, align):
        return {record.id: str(record.seq) for record in align}
