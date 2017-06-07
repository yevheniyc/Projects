'''
    InputProcessor.py - Yevheniy Chuba - 6/1/2017
    Currently Parses input CSV file and extracts: Sequence ID, Group, Sequence.
    It then returns the following data structure for further pre-processing:
        {group_id: [['seq_id', 'seq], ... ],
         ...
         }

    Usage:
        input_processor = InputProcessor('Hetero-IgG.xlsx')
        ds = input_processor.process_input()
        output: OrderedDict([('group_name', [[seq_id, seq], ...])])
'''

import os
from collections import OrderedDict
import csv
import pandas as pd

class InputProcessor:
    '''
        Takes in any data format (various excell versions, csv, tsv)
        and then extracts group, seq_id, seq information

        Args:
            input_file(str): the input file to be processed

        Returns:
            {group_id: [['seq_id', 'seq], ... ],
             ...
             }

        Usage:
            input_processor = InputProcessor('Hetero-IgG.xlsx')
            ds = input_processor.process_input()
    '''
    def __init__(self, input_file):
        self.input_file = input_file

    def process_input(self):
        """
            Combines file conversion and sequence information extraction
        """
        csv_file_name = self.convert_to_csv()
        group_id_seq = self.get_sequences(csv_file_name)
        return group_id_seq


    def convert_to_csv(self):
        """
            Convert any given format to csv for cleaner processing
        """
        # csv_file_name = ''
        # with open(self.input_file, 'r+') as input_f:
        # open either excell or csv file
        file_ext = self.input_file.name.lower()
        if file_ext.endswith(('.xlsx', 'xls', 'xlt')):
            df = pd.read_excel(self.input_file, header=None)
        else:
            df = pd.read_csv(self.input_file, header=None)
        # convert to .csv
        csv_file_name = os.path.splitext(self.input_file.name)[0] + ".csv"
        df.to_csv(csv_file_name, header=None, index=None, sep=',')
        return csv_file_name

    def get_sequences(self, file_name):
        """
            Extract Group Name, Sequence ID, Sequence String (no gaps)
        """
        main_ds = OrderedDict()
        with open(file_name, 'r+') as input_f:
            for line in input_f:
                flag = line.split(',')[3]
                if line.split(',')[3] in ('0', '1'):
                    column_data = line.split(',')
                    molecule_name = column_data[1]
                    group_id = column_data[2]
                    seq = column_data[4].replace('-', '')
                    if group_id in main_ds.keys():
                        main_ds[group_id].append([molecule_name, seq])
                    else:
                        main_ds[group_id] = [[molecule_name, seq]]
        return main_ds
