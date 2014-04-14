import sys

def unique(inp):
    total_count = 0
    old_field = None

    for line in inp:
        data = line.strip().split('\t')
        if len(data) != 2:
            continue

        this_field, this_count = data

        if old_field and old_field != this_field:
            print '{0}\t{1}'.format(old_field, total_count)
            total_count = 0

        old_field = this_field
        total_count += int(this_count)

    print '{0}\t{1}'.format(old_field, total_count)

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
    unique(sys.stdin)
    group_by_year_zip_ndc(sys.stdin)

if __name__ == '__main__':
    reducer()
