
import re

def cutit(s,n):
    """ Cut from the beginning of a string. """
    return s[n:]

def change_file(infile, outfile):
    """ Find numbered lines, remove the numbers, write to a new file.
    """
    for line in infile:
        string = re.search(r"^\d+", line)
        string_2 = re.search(r"^\d+", line[1:])
        if string:
            new_line = cutit(line, len(string.group(0)))
            outfile.write(new_line)
        elif string_2:
            new_line = cutit(line, len(string_2.group(0)) + 1)
            outfile.write(new_line)
        else:
            outfile.write(line)

with open('/Users/whitehat/Desktop/file_to_parse.txt', 'rb') as infile, open('/Users/whitehat/Desktop/parsed_file.py', 'wb') as outfile:
    change_file(infile, outfile)
