import csv
import codecs


with open('output.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split("|2*7|") for line in stripped if line)
    with codecs.open('outputcsv.csv', 'w', "utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)
