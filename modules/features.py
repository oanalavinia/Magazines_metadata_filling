page_id = 1
page_height = 1024
page_width = 512
section_id = 2
section_label = "Text"
section_coord = (10, 20)
section_height = 12
section_width = 43
section_text = "Thisa, is.eitura s\nome! r\nandom.issbn..                  cosmin"





def normalized_page_height(section_height, page_height):
    return section_height / page_height


def normalized_page_width(section_width, page_width):
    # return section_width / (section_width + page_width)
    return section_width / page_width


def normalized_page_coverage(page_height, page_width, section_height, section_width):
    page_area = page_height * page_width
    section_area = section_height * section_width
    return section_area / page_area


def no_of_words(section_text):
    sep = ' ,!?.\n'
    default_sep = ' '
    for sep in sep[1:]:
        section_text = section_text.replace(sep, default_sep)
    section_text = section_text.split(default_sep)
    section_text = list(filter(None, section_text))
    return len(section_text)


def no_of_rows(section_text):
    c = 0

    section_text = section_text.replace(" ", "")

    for i in range(0, len(section_text) - 1):
        if section_text[i] == '\n':
            if section_text[i + 1] == '\n':
                c = c + 1

    return len(section_text.split('\n')) - c


def has_substring(section_text, page_id, max_pages, substring):
    if page_id > max_pages:
        return 0
    if section_text.lower().find(substring) > -1:
        return 1
    return 0


def page_number(page_id):
    return page_id


def x_normalized(page_width, section_width):

    return section_width/page_width


def y_normalized(page_height, section_height):

    return section_height/page_height