#!/usr/bin/python

from ast import literal_eval as le
import sys

def unique_ndc(inp):
    for line in inp:
        record = le(line.strip())
        if 'ndc' in record:
            print '{0}\t{1}'.format(record['ndc'], 1)

def group_by_year_zip_ndc(inp):
    for line in inp:
        record = le(line.strip())
        if 'dispenseQuarter' in record and 'threeDigitSubsZip' in record and 'ndc' in record and 'untsDispensedQuantity' in record:
            print '{0}|{1}|{2}\t{3}'.format(record['dispenseQuarter'].strip(), record['threeDigitSubsZip'].strip(), record['ndc'].strip(), record['untsDispensedQuantity'].strip())

def mapper():
    #unique_ndc(sys.stdin)
    group_by_year_zip_ndc(sys.stdin)

if __name__ == '__main__':
    mapper()
