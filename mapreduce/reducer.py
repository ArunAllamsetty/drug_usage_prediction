import sys

def unique_ndc(inp):
    total_count = 0
    old_ndc = None

    for line in inp:
        data = line.strip().split('\t')
        if len(data) != 2:
            continue

        this_ndc, this_count = data

        if old_ndc and old_ndc != this_ndc:
            print '{0}\t{1}'.format(old_ndc, total_count)
            total_count = 0

        old_ndc = this_ndc
        total_count += int(this_count)

    print '{0}\t{1}'.format(old_ndc, total_count)

def group_by_year_zip_ndc(inp):
    total_count = 0
    old_grp = None

    for line in inp:
        data = line.strip().split('\t')
        if len(data) != 2:
            continue

        this_grp, this_count = data

        if old_grp and this_grp != old_grp:
            print '{0}\t{1}'.format(old_grp, total_count)
            total_count = 0

        old_grp = this_grp
        total_count += float(this_count)

    print '{0}\t{1}'.format(old_grp, total_count)

def reducer():
    #unique_ndc(sys.stdin)
    group_by_year_zip_ndc(sys.stdin)

if __name__ == '__main__':
    reducer()
