#!/usr/bin/python

from ast import literal_eval as le
import random, sys

def unique(inp, field):
    for line in inp:
        line = line.strip()
        if line:
            try:
                record = le(line)
                if field in record:
                    print '{0}\t{1}'.format(record[field], 1)
            except SyntaxError:
                print 'IgnoredRecord'

def group_by_year_zip_ndc(inp):
    for line in inp:
        record = le(line.strip())
        if 'dispenseQuarter' in record and 'threeDigitSubsZip' in record and 'ndc' in record and 'untsDispensedQuantity' in record:
            print '{0}|{1}|{2}\t{3}'.format(record['dispenseQuarter'].strip(), record['threeDigitSubsZip'].strip(), record['ndc'].strip(), record['untsDispensedQuantity'].strip())

def group_by_year_zip(inp):
    random.seed()
    for line in inp:
        line = line.strip()
        if line:
            try:
                record = le(line)
                if 'dispenseQuarter' in record and 'threeDigitSubsZip' in record and 'untsDispensedQuantity' in record and record['threeDigitSubsZip'].strip():
                    print '{0}|{1}\t{2}'.format(random.randrange(1, 5), record['threeDigitSubsZip'].strip(), record['untsDispensedQuantity'].strip())
            except SyntaxError:
                print 'IgnoredRecord'

def mapper():
    #unique(sys.stdin, 'threeDigitSubsZip')
    group_by_year_zip(sys.stdin)

if __name__ == '__main__':
    mapper()

