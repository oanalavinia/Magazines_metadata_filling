import features
import json
import os

MAX_PAGES = 5
delim = "|2*7|"
file = open("normalizedInstances.txt", "w")
head = ['title', 'rawText', 'pageId', 'sectionId', 'x', 'y', 'page_h', 'page_w', 'page_cov', 'rawRows', 'rawWords',
        'hasISBN', 'hasEditura', 'normRows', 'normWords', 'trainLabel']

for h in head:
    file.write(h)
    file.write(delim)
file.write('\n')
for filename in os.listdir("TrainingData"):

    with open("TrainingData\\" + filename, encoding='utf-8') as f:
        data = json.load(f)

    for page in data:
        if page == "title":
            title = data[page]
            print(filename, title)
        if page == "numberOfPages":
            numberOfPages = data[page]

        if not (page == "numberOfPages") and not (page == "title"):

            max_word_count = 0
            max_rows_count = 0
            for i in data:
                if not (i == "numberOfPages") and not (i == "title"):
                    for section in data[i]['sections']:
                        if 'text' in data[i]['sections'][section]:
                            max_word_count = max(max_word_count,
                                                 features.no_of_words(data[i]['sections'][section]['text']))
                            max_rows_count = max(max_rows_count,
                                                 features.no_of_rows(data[i]['sections'][section]['text']))

            page_id = int(data[page]['page'])
            if page_id > 5:
                page_id = page_id - numberOfPages + 10

            page_height = int(data[page]['pageHeight'])
            page_width = int(data[page]['pageWidth'])

            for section in data[page]['sections']:

                section_id = str(section)
                if 'text' in data[page]['sections'][section]:
                    section_label = data[page]['sections'][section]['text'],
                    section_coord = (data[page]['sections'][section]['x'], data[page]['sections'][section]['y'])
                    section_height = data[page]['sections'][section]['height']
                    section_width = data[page]['sections'][section]['width']
                    section_text = data[page]['sections'][section]['text']
                    section_class = data[page]['sections'][section]['class']

                file.write(title)
                file.write(delim)
                file.write(section_text.replace('\n', ' '))
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
                hasISBN = features.has_substring(section_text, page_id, MAX_PAGES, 'isbn')
                hasISSN = features.has_substring(section_text, page_id, MAX_PAGES, 'issn')
                if hasISBN == 0:
                    hasISBN = hasISSN
                file.write(str(hasISBN))
                file.write(delim)
                file.write(str(features.has_substring(section_text, page_id, MAX_PAGES, 'editura')))
                file.write(delim)
                file.write(str(features.no_of_words(section_text) / max_word_count))
                file.write(delim)
                file.write(str(features.no_of_rows(section_text) / max_rows_count))
                file.write(delim)
                file.write(section_class)

                file.write("\n")
