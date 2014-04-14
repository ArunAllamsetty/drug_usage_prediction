import csv

def makeZipDb():
    zip_db = {}
    with open('zip_code_database.csv', 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            zip3 = row[0][:3]
            if zip3 not in zip_db:
                zip_db[zip3] = [row[9], row[10]]
    return zip_db

def readZipCsv():
    zip_csv = {}
    with open('unique_zips', 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')
        for row in reader:
            zip_csv[row[0]] = row[1]
    return zip_csv

def main():
    zip_db = makeZipDb()
    zip_csv = readZipCsv()
    zips = zip_csv.keys()
    zips.sort()
    
    for z in zips:
        if z in zip_db:
            coordi = zip_db[z]
            print '{0} {1} {2} {3}'.format(z, coordi[0], coordi[1], zip_csv[z])

if __name__ == '__main__':
    main()
