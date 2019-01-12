import pandas as pd
import pickle
import csv
import xml.etree.cElementTree as ET

readData = pd.read_csv("outputcsv.csv")  # input path
print(1)
loaded_model = pickle.load(open('RF_30Trees_50depth_balanced.sav', 'rb'))  # model path
print(2)
labelMapping = {0: 'text',
                1: 'titlu',
                2: 'editura',
                3: 'autor',
                4: 'isbn'}

# Dan's code

root = ET.Element("labelListing")
tag_text = ET.SubElement(root, "text")
tag_titlu = ET.SubElement(root, "titlu")
tag_autor = ET.SubElement(root, "autor")
tag_editura = ET.SubElement(root, "editura")
tag_isbn = ET.SubElement(root, "isbn")

with open('outputPredictions.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if len(row) == 2:
            if row[1] == 'text':
                ET.SubElement(tag_text, 'rawText').text = row[0]
            elif row[1] == 'titlu':
                ET.SubElement(tag_titlu, 'rawText').text = row[0]
            elif row[1] == 'autor':
                ET.SubElement(tag_autor, 'rawText').text = row[0]
            elif row[1] == 'editura':
                ET.SubElement(tag_editura, 'rawText').text = row[0]
            elif row[1] == 'isbn':
                ET.SubElement(tag_isbn, 'rawText').text = row[0]

tree = ET.ElementTree(root)
tree.write("userEndResult.xml")  # this should be the received PDF name
