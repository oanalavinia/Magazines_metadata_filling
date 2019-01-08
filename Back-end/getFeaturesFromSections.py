import xml.etree.ElementTree as ET
import features
import json
import os
from pprint import pprint

MAX_PAGES = 5
delim = "  "
file = open("output.txt", "w")

for filename in os.listdir("TrainingData"):
    print(filename)
    with open("TrainingData\\" + filename) as f:
        data = json.load(f)

    for page in data:
        if page == "title":
            title=data[page]
            print(title)
        if page == "numberOfPages":
            numberOfPages=data[page]
            print(numberOfPages)
        if not (page == "numberOfPages") and not (page == "title"):

            max_word_count = 0
            max_rows_count = 0
            for i in data:
                if not (i == "numberOfPages") and not (i == "title"):
                    for section in data[i]['sections']:
                        if 'text' in data[i]['sections'][section]:
                            max_word_count = max(max_word_count, features.no_of_words(data[i]['sections'][section]['text']))
                            max_rows_count = max(max_rows_count, features.no_of_rows(data[i]['sections'][section]['text']))

            page_id = int(data[page]['page'])
            if page_id>5:
                page_id=page_id-numberOfPages+10
            # print("pageID ", page_id)
            page_height = int(data[page]['pageHeight'])
            page_width = int(data[page]['pageWidth'])

            for section in data[page]['sections']:
                # print(data[page]['sections'][section])

                section_id = str(section)
                # print(section_id)

                if 'text' in data[page]['sections'][section]:
                    section_label = data[page]['sections'][section]['text'],
                    section_coord = (data[page]['sections'][section]['x'], data[page]['sections'][section]['y'])
                    section_height = data[page]['sections'][section]['height']
                    section_width = data[page]['sections'][section]['width']
                    section_text = data[page]['sections'][section]['text']

                file.write(title)
                file.write(delim)
                file.write(str(page_id))
                file.write(delim)
                file.write(section_id)
                file.write(delim)
                file.write(str(features.x_normalized(page_width, section_coord[0])))
                file.write(delim)
                file.write(str(features.y_normalized(page_height, section_coord[1])))
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
                file.write(str(features.has_substring(section_text, page_id, MAX_PAGES, 'editura')))
                file.write(delim)
                file.write(str(features.no_of_words(section_text) / max_word_count))
                file.write(delim)
                file.write(str(features.no_of_rows(section_text) / max_rows_count))
                file.write("\n")

