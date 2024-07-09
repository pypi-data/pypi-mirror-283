import pandas as pd

def read_bed(file_path):
    """
    Reads a BED file and skips lines starting with '#'. 
    Expecting the file in following format: 'chrom', 'start', 'end', 'name', 'score', 'strand'
    """
    bed_data = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            if len(fields) == 6:
                fields[1] = int(fields[1])
                fields[2] = int(fields[2])
                bed_data.append(fields)
    
    return bed_data