import xml.etree.ElementTree as ET
import features
import json
from pprint import pprint

MAX_PAGES = 5

with open('js.json') as f:
    data = json.load(f)

pprint(data)

delim = "  "

tree = ET.parse('pageSections.xml')
root = tree.getroot()

file = open("output.txt", "w")

for page in data:

    page_id = int(data[page]['page'])
    print("pageID ", page_id)
    page_height = int(data[page]['pageHeight'])
    page_width = int(data[page]['pageWidth'])

    for section in data[page]['sections']:
        # print(data[page]['sections'][section])

        section_id = str(section)
        print(section_id)
        section_label = data[page]['sections'][section]['text'],
        section_coord = (data[page]['sections'][section]['x'], data[page]['sections'][section]['y'])
        section_height = data[page]['sections'][section]['height']
        section_width = data[page]['sections'][section]['width']
        section_text = data[page]['sections'][section]['text']

        file.write(str(page_id))
        file.write(delim)
        file.write(section_id)
        file.write(delim)
        file.write(str(features.upLeft_corner(section_coord[0])))
        file.write(delim)
        file.write(str(features.upLeft_corner((section_coord[1]))))
        file.write(delim)
        file.write(str(features.normalized_page_height(section_height, page_height)))
        file.write(delim)
        file.write(str(features.normalized_page_width(section_width, page_width)))
        file.write(delim)
        file.write(str(features.normalized_page_coverage(page_height, page_width, section_height, section_width)))
        file.write(delim)
        file.write(str(features.no_of_rows(section_text)))
        file.write(delim)
        file.write(str(features.no_of_words(section_text)))
        file.write(delim)
        file.write(str(features.has_substring(section_text, page_id, MAX_PAGES, 'isbn')))
        file.write(delim)
        file.write(str(features.has_substring(section_text, page_id, MAX_PAGES, 'autor')))

        file.write("\n")
