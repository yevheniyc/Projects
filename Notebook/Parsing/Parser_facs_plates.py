
import re
import os
from StringIO import StringIO
import csv
from collections import OrderedDict
import pdb
import pprint as pp

# CONSTATNTS
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# imported from ri.assays.labware
# We might simplify generation of plate dimensions
PLATE_DIMENSIONS = {
    24: (4, 6),
    48: (6, 8),
    96: (8, 12),
    384: (16, 24),
}

# Patterns for different FACS machines
CANTO_PATTERN = re.compile(r'[\w\d_-]+_[A-Z]\d+_(?P<well>[A-Z]\d{2})')
FACSCAN_PATTERN = re.compile(r'(?P<plate>\d{2})(?P<well>[A-Z]\d{2})')
ANTIGEN_PATTERN = re.compile(r'(Ag\d+)')

def parse_plate_format(plate_format):
    """ Return the number of wells and the orientation of a plate format.
    
    Args:
        plate_format: One of the formats in PLATE_FORMATS
    
    Return: An integer giving the number of wells in the format.
    """
    # pattern to match: "96|384 well vertical|horizontal"
    pattern = re.compile("^(\d{2,3}) well (vertical|horizontal)$")
    match = pattern.match(plate_format)
    return int(match.group(1)), match.group(2) # 96, horizontal

def plate_dimensions(plate_format):
    """ Return the dimensions (rows, columns) of the plate format
    
    Args:
        plate_format: One of the formats in PLATE_FORMATS.
        
    Return:
        A tuble giving the number of rows and number of columns in the format.
    """
    wells, orientation = parse_plate_format(plate_format)
    dims = PLATE_DIMENSIONS[wells]
    return dims if orientation == "horizontal" else (dims[1], dims[0]) # switch places if vertical

def well_name_position(plate_format, well_name):
    '''Convert a well name (A01-K12) or (1-96) to its position (1-96)
    '''
    match = re.match( r"^(?P<row>[A-I])?(?P<column>\d{1,2})$", well_name.upper())
    if match:
        # If there is a alphanumeric row position
        if match.group("row"):
            row = ALPHABET.index(match.group("row"))
            column = int(match.group("column"))
            _, columns = plate_dimensions(plate_format)
            return (row * columns) + column
        # Otherwise the only position is an absolute one
        else:
            return int(match.group("column"))
    else:
        raise ValueError("Invalid well_name: %s" % str(well_name))


class Plate(object):
    """ Constructor for a new type - Plate, which will be used to convert 
        csv data (including Straight ELISA) into python objects. 
    """
    def __init__(self, name, values=None, missing_value=None):
        self.name = name
        self._values = values or {}
        self._missing_value = missing_value
        
    def __getitem__(self, index):
        try:
            return self._values[index]
        except KeyError:
            return self._missing_value
        
    def __setitem__(self, index, value):
        self._values[index] = value
    
    def __eq__(self, other):
        return self.name == other.name and self._values == other.values
    
    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)
    

class FACSPlate(Plate):
    """ Inherites from Plate. Used for converting FACS text files into
        python objects.
    """
    def __init__(self, name, data_point_name, *args, **kwargs):
        super(FACSPlate, self).__init__(name, *args, **kwargs)
        self.data_point_name = data_point_name

    def __eq__(self, other):
        return (self.name == other.name and 
                self.data_point_name == other.data_point_name and
                self._values == other._values)

    def __repr__(self):
        return "<{}: {} - {}>".format(
            self.__class__.__name__, self.name, self.data_point_name)


class PlateDataParser(object):
    """ Subclassed by CSVParser, SoftmaxParser
    Methods:
        _prepare_data_file(data_file)
        _extract_data(data_file)
        parse_file(data_file)
    """
    def __init__(self, plate_format):
        self.plate_format = plate_format
    
    @classmethod
    def _prepare_data_file(cls, data_file):
        return StringIO(cls._extract_data(data_file))
    
    @staticmethod
    def _extract_data(data_file):
        data_file.seek(0) # used with StringIO to start with byte 1
        return data_file.read().replace('\r', '\n')
    
    def parse_file(self, data_file):
        raise NotImplementedError()
        

class CSVParser(PlateDataParser):
    """
    """
    def __init__(self, plate_format):
        super(CSVParser, self).__init__(plate_format)
        
    @classmethod
    def _nonempty_rows(cls, data_file):
        data = cls._extract_data(data_file)
        reader = csv.reader(StringIO(data), dialect=csv.Sniffer().sniff(data))
        return [row for row in reader if row]


class FACSParser(CSVParser):

    def parse_file(self, data_file):
        rows = self._nonempty_rows(data_file)
        filename = os.path.split(data_file.name)[1]
        if self._is_accuri_file(rows[0][0]):
            return self._parse_accuri_facs_file(rows, filename)
        else:
            return self._parse_flojo_facs_file(rows, filename)

    @staticmethod
    def _is_accuri_file(first_header):
        return first_header.startswith('Well ID')

    def _parse_accuri_facs_file(self, rows, filename):
        '''Parse a FACS data file generated by the Accuri machine.'''
        plate_name = os.path.splitext(filename)[0]
        plates = [FACSPlate(plate_name, ag_name) for ag_name in rows[0][2:]]
        for row in rows[1:]:
            position = well_name_position(self.plate_format, row[0])
            for plate, value in zip(plates, row[2:]):
                plate[position] = float(value)
        return plates

    def _parse_flojo_facs_file(self, rows, filename):
        '''Parse a FACS data file generated by FloJo.'''
        default_name = os.path.splitext(filename)[0]
        pattern = self._flowjo_pattern(rows[1][0])
        antigen_names = [self._antigen_header(c) for c in rows[0][1:]]
        plates = OrderedDict()
        for row in rows[1:]:
            match = pattern.search(row[0])
            if match:
                well = match.groupdict()['well']
                position = well_name_position(self.plate_format, well)
                for column, ag_name in zip(row[1:], antigen_names):
                    plate_name = match.groupdict().get('plate', default_name)
                    plate = plates.setdefault(
                        (plate_name, ag_name), FACSPlate(plate_name, ag_name))
                    plate[position] = float(column)
        return plates.values()

    @classmethod
    def _antigen_header(cls, antigen_header):
        match = cls.ANTIGEN_PATTERN.search(antigen_header)
        return match.group(1) if match else antigen_header

    @classmethod
    def _flowjo_pattern(cls, sample_name):
        '''Return the correct FloJo pattern for Canto or FACScan. '''
        # check the canto pattern before the facscan pattern, because the
        # plate name in a canto file could match the facscan pattern
        if CANTO_PATTERN.search(sample_name):
            return CANTO_PATTERN
        else:
            return FACSCAN_PATTERN

with open('/usr/local/var/django/code_work/tests/xabtracker/data_files/facs_table_96.txt', 'rb') as data_file:
    plates = FACSParser('96 well horizontal').parse_file(data_file)

def well_name_position(well_name, columns=12):
    '''Convert a well name (A01-K12) or (1-96) to its position (1-96)
    '''
    match = re.match( r"^(?P<row>[A-I])?(?P<column>\d{1,2})$", well_name.upper())
    if match:
        # If there is an alphanumeric row position
        if match.group("row"):
            row = ALPHABET.index(match.group("row"))
            column = int(match.group("column"))
            return (row * columns) + column
        # Otherwise the only position is an absolute one
        else:
            return int(match.group("column"))
    else:
        raise ValueError("Invalid well_name: %s" % str(well_name))

def parse_accuri_facs_file(rows, filename):
        '''Parse a FACS data file generated by the Accuri machine.'''
        plate_name = os.path.splitext(filename)[0]
        plates = [(plate_name, ag_name) for ag_name in rows[0][2:]]
        for row in rows[1:]:
            position = well_name_position(row[0])
            for plate, value in zip(plates, row[2:]):
                plate[position] = float(value)
        return plates

def flowjo_pattern(sample_name):
    '''Return the correct FloJo pattern for Canto or FACScan. '''
    # check the canto pattern before the facscan pattern, because the
    #  plate name in a canto file could match the facscan pattern
    if CANTO_PATTERN.search(sample_name):
        return CANTO_PATTERN
    else:
        return FACSCAN_PATTERN 

def antigen_header(antigen_header):
    match = ANTIGEN_PATTERN.search(antigen_header)
    return match.group(1) if match else antigen_header
    

def parse_flowjo_facs_file(rows, filename):
    '''Parse a FACS data file generated by FloJo.'''
    default_name = os.path.splitext(filename)[0]
    pattern = flowjo_pattern(rows[1][0])
    antigen_names = [antigen_header(c) for c in rows[0][1:]]
    plates = OrderedDict()
    for row in rows[1:]:
        match = pattern.search(row[0])
        if match:
            well = match.groupdict()['well']
            position = well_name_position(well)
            for column, ag_name in zip(row[1:], antigen_names):
                plate_name = match.groupdict().get('plate', default_name)
                plates.setdefault((plate_name, ag_name), []).append({position: float(column)})
    return plates


with open('/usr/local/var/django/code_work/tests/xabtracker/data_files/facs_table_96.txt') as data_file:
    data_file.seek(0)
    filename = os.path.split(data_file.name)[1]
    data = data_file.read().replace('\r', '\n')
    reader = csv.reader(StringIO(data), dialect=csv.Sniffer().sniff(data))
    rows = [ row for row in reader if row ]
    if rows[0][0].startswith('Well ID'):
        print "ACCURI: ", parse_accuri_facs_file(rows, filename)
    else:
        print "FLOWJO: ", parse_flowjo_facs_file(rows, filename)

# BIACORE file parsing
def biacore_parse_file(data_file):
    data_file.seek(0)
    data = data_file.read().replace('\r', '\n')
    reader = csv.reader(StringIO(data), dialect=csv.Sniffer().sniff(data))
    rows = [row for row in reader if row]
    plates = OrderedDict()
    for row in rows:
        if len(row) != 3:
            raise ValueError("Every row should have 3 columns")
        name = row[0].strip()
        position = well_name_position(row[1])
        value = float(row[2])
        plates.setdefault(name, []).append({position: value})
    return plates

with open('/usr/local/var/django/code_work/tests/xabtracker/data_files/biacore.csv', 'rb') as data_file:
    print biacore_parse_file(data_file)

# BIACORE 4000
class Biacore4000Parser(CSVParser):
    def parse_file(self, data_file):
        rows = self._nonempty_rows(data_file)
        plates = OrderedDict()
        # Skip first row
        for row in rows[1:]:
            sample_name = row[7]
            antigen = row[5]
            value = row[3]
            match = re.match(r'^(.+)_(\w\d{2})$', sample_name)
            if match:
                plate_name = '{0} ({1})'.format(match.group(1), antigen)
                well = labware.well_name_position(
                    self.plate_format, match.group(2))
                plate = plates.setdefault(plate_name, Plate(plate_name))
                plate[well] = float(value)
        return plates.values()


def biacore4000_parse_file(data_file):
    data_file.seek(0)
    data = data_file.read().replace('\r', '\n')
    reader = csv.reader(StringIO(data), dialect=csv.Sniffer().sniff(data))
    rows = [row for row in reader if row]
    plates = OrderedDict() # will need to sort, if ordered dict is necessary
    # skip the first line
    for row in rows[1:]:
        sample_name = row[7]
        antigen = row[5]
        value = row[3]
        match = re.match(r'^(.+)_(\w\d{2})$', sample_name)
        if match:
            plate_name = '{0} ({1})'.format(match.group(1), antigen)
            well = well_name_position(match.group(2))
            plates.setdefault(plate_name, []).append({well: float(value)})
    return plates

with open('/usr/local/var/django/code_work/tests/xabtracker/data_files/biacore_4000.txt', 'rb') as data_file:
    print biacore4000_parse_file(data_file)

# MSDParser
def msd_parse_file(data_file):
    data_file = StringIO(data_file.read().replace('\r', '\n'))
    plate_pattern = re.compile(r"^Plate #\s+:\s+([^\s]+)\s*$")
    values_pattern = re.compile(r"^[A-Z]+((\s+-?\d+){%d})\s*$" % 12)
    plate_names = []
    plates = OrderedDict()
    for line in data_file:
        plate_match = plate_pattern.match(line)
        if plate_match:
            last_position = 1
            plate_name = plate_match.group(1)
            plate_names.append(plate_name)
        else: 
            values_match = values_pattern.match(line)
            if values_match:
                values = values_match.group(1).strip().split()
                current_plate_name = plate_names[-1]
                plates.setdefault(current_plate_name, [])
                # take into account positions of the new plates
                for position, value in zip(range(last_position, last_position + len(values)), values):
                    plates[current_plate_name].append({position: float(value)})
                last_position += len(values)
    return plates
    

with open('/usr/local/var/django/code_work/tests/xabtracker/data_files/msd.txt', 'rb') as data_file:
    print msd_parse_file(data_file)
            

def softmax_parse_file(data_file):
    data_file = StringIO(data_file.read().replace('\r', '\n'))
    cols = 24
    plate_pattern = re.compile(r"^Plate:\t([^\t]+)\t")
    values_pattern = re.compile(r"^\t[^\t()A-Za-z]*((\t\d+(\.\d+)?){%d})\s*$" % cols)
    plate_names = []
    col_headers = '123456789101112131415161718192021222324' # 1-24 numeric col headers
    plates = OrderedDict()
    for line in data_file:
        plate_match = plate_pattern.match(line)
        if plate_match:
            last_position = 1
            plate_name = plate_match.group(1).strip()
            plate_names.append(plate_name)
        else:
            values_match = values_pattern.match(line)
            if values_match:
                values = values_match.group(1).strip().split("\t")
                current_plate_name = plate_names[-1]
                plates.setdefault(current_plate_name, {})
                # take into account positions of the new plates
                for position, value in zip(range(last_position, last_position + len(values)), values):
                    plates[current_plate_name].update({position: float(value)})
                last_position += len(values)
    return plates

#############################################################
def get_matrix_pos(col, row):
    """ From col and row show position in the matrix. """
    return col + 24 * (row - 1)

def split_4_quadrants(data_file):
    plates = softmax_parse_file(data_file)
    quadrants = {'UL': {'x': [1, 12], 'y': [1, 8]}, 
                 'UR': {'x': [13, 24], 'y': [1, 8]}, 
                 'LL': {'x': [1, 12], 'y': [9, 16]}, 
                 'LR': {'x': [13, 24], 'y': [9, 16]}
                 }
    quadrant_plates = OrderedDict()
    for plate, values in plates.iteritems():
        for quadrant, coordinates in quadrants.iteritems():
            # for all plates start positions from 1
            pos_list = range(1, 97)
            # plate name is the name of the quadrant for now
            plate_name = "{0}_{1}".format(quadrant, plate)
            # find values for each qudrant
            final_values = []
            cols_coordinates = coordinates['x']
            rows_coordinates = coordinates['y']
            quadrant_plates.setdefault(plate_name, {})
            for row in range(rows_coordinates[0], rows_coordinates[1] + 1):
                for col in range(cols_coordinates[0], cols_coordinates[1] + 1):
                    pos = get_matrix_pos(col, row)
                    quadrant_plates[plate_name].update({pos_list[0]: values[pos]})
                    pos_list.pop(0)
    return quadrant_plates   

##################################################
def plate_1_coordinates():
    plate_range = range(1, 385)
    coordinates = []
    for pos in range(1, 385):
        coordinates.append(pos)
    return coordinates


def split_96_quadrants(data_file):
    plates = softmax_parse_file(data_file)
    plate_coordinates = {'UL': plate_1_coordinates(), 
                         'UR': plate_1_coordinates(), 
                         'LL': plate_1_coordinates(), 
                         'LR': plate_1_coordinates()
                        }
    for plate, values in plates.iteritems():
        print plate, values
        

with open('/usr/local/var/django/code_work/tests/xabtracker/data_files/alisa_table.txt', 'rb') as data_file:
    # print split_4_quadrants(data_file)
    print split_96_quadrants(data_file)
            
            
            


