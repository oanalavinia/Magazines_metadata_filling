import pdf2image
import os
import cv2
from PIL import Image
import imutils
from lxml import etree
import pytesseract
import json


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
inputPath = r'C:\Users\TudorIacobuta\Desktop\PDFImages\trainingData1'
outPutPath = r'C:\Users\TudorIacobuta\Desktop\outputImages'

pdfFolderPath = r'C:\Users\TudorIacobuta\Desktop\PDFImages'

bookNumber = 1

for book in os.listdir(pdfFolderPath):

    inputPath = os.path.join(pdfFolderPath,book)
    ### Initialization ###
    count = 0
    pageCount = 1
    sectionCount = 1
    numberOfPages = len(os.listdir(inputPath))
    ####

    ### JSON ###
    book = {}
    book['numberOfPages'] = numberOfPages
    ####


    for img in os.listdir(inputPath):

        if pageCount >= 5 and pageCount < numberOfPages - 5:
            pageCount += 1
            continue

        temp_data = {}
        temp_path = os.path.join(inputPath, img)

        ### Image processing ###
        image = cv2.imread(temp_path)
        image = imutils.resize(image, width=600)
        pageWidth = 600
        pageHeight = len(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=7)
        _, contours, hierarchy = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        ####

        ### JSON ###
        temp_data['page'] = str(pageCount)
        temp_data['pageWidth'] = str(pageWidth)
        temp_data['pageHeight'] = str(pageHeight)
        temp_data['sections'] = {}
        ####

        for contour in contours:

            temp_data['sections'][sectionCount] = {}

            [x, y, w, h] = cv2.boundingRect(contour)
            if h < 20 or w < 20:
                continue
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 255), 2)
        
            ### Get text from section ###
            crop = image[y:y+h+2, x:x+w+2]
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            pillowImage = Image.fromarray(crop)
            text = pytesseract.image_to_string(pillowImage)
            ####
        
            if len(text) == 0:
                sectionCount += 1
                continue

            ### JSON ###
            temp_data['sections'][sectionCount]['class'] = 'text'
            temp_data['sections'][sectionCount]['x'] = x
            temp_data['sections'][sectionCount]['y'] = y
            temp_data['sections'][sectionCount]['height'] = h
            temp_data['sections'][sectionCount]['width'] = w
            temp_data['sections'][sectionCount]['leftCorner'] = [x, y]
            temp_data['sections'][sectionCount]['rightCorner'] = [x+w, y+h]
            temp_data['sections'][sectionCount]['text'] = text
            ####

            sectionCount += 1

        # EndForLoop

        pageCount += 1
        count += 1
        book[str('img_' + img.split('.')[0])] = temp_data

    # EndForLoop

    ### Write JSON ###
    json_data = json.dumps(book, indent=4)
    output = open(f'C:\\Users\\TudorIacobuta\\Desktop\\JSONData\\JSON_trainingData{bookNumber}.json', "w+")
    output.write(json_data)
    ####
    bookNumber += 1

# cv2.imshow("Show",dilated)
# cv2.waitKey()
# cv2.destroyAllWindows()
