import xml.etree.ElementTree as ET
import features

delim = "  "

tree = ET.parse('pageSections.xml')
root = tree.getroot()

file = open("output.txt", "w")

for page in root.iter('page'):

    page_id = page.find('pageId').text
    page_height = int(page.find('pageHeight').text)
    page_width = int(page.find('pageWidth').text)
    """"
    page_id = 1
    page_height = 1024
    page_width = 512
    section_id = 2
    section_label = "Text"
    section_coord = (10, 20)
    section_height = 12
    section_width = 43
    section_text = "Thisa, is.eitura s\nome! r\nandom.issbn..                  cosmin"
    """

    for section in page.iter('section'):
        section_id = section.find('id').text,
        section_label = section.find('class').text,
        section_coord = (int(section.find('x').text), int(section.find('y').text))
        section_height = int(section.find('height').text)
        section_width = int(section.find('width').text)

        file.write(page_id)
        file.write(delim)
        file.write(section.find('id').text)
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
        file.write("\n")
