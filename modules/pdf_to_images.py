#
# //////////////////////////////Installing poppler////////////////////////////////////////////////////////////////////////////////////
#   1.    Download: https://blog.alivate.com.au/poppler-windows/?fbclid=IwAR31UcLlNPT0QNsHcjfc8iTZcpHX_M046b9KmhURqHXBxpbujFMXRFizvIw
#   2.    Unzip
#   3.    Copy the unziped folder to example: C:\Program Files (x86)\Poppler\poppler-0.68.0
#   4.    Add C:\Program Files (x86)\Poppler\poppler-0.68.0\bin to the PATH in the system environment variables
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Libraries needed pdf2image and PyPDF2
try:
    from pdf2image import convert_from_path
    from PyPDF2 import PdfFileReader
except:
    from pip._internal import main
    main(['install', 'pdf2image'])
    main(['install', 'PyPDF2'])
    from pdf2image import convert_from_path
    from PyPDF2 import PdfFileReader

import os
import shutil

# Edit this
# Path to folder with the pdf
def runScript():
        folder_path = f'{os.getcwd()}\\Uploads'
        for file in os.listdir(folder_path):
                if file.endswith(".pdf"):
                        temp_path = os.path.join(folder_path, file)
                        # Get the number of pages for each pdf
                        f = open(temp_path, 'rb')
                        pdf = PdfFileReader(f)
                        nr_pages = pdf.getNumPages()

                        # Edit this
                        # Path for the folder we create for each pdf
                        outputFolder = f"{os.getcwd()}\\PDFImages"
                        # Check if the folder already exists, if it does we delete it.
                        # Creates a folder for each pdf which will contain all the pages as images
                        #temp_folder = os.mkdir(temp_folder_path)
                        # Path to that new folder
                        path = os.path.join(outputFolder, file.split('.')[0])
                        # Converting the pages to images. The last parameter is the number of threads you want to allow it to use,      check your processor to see how many threads it has and add nr_threads-1 (or 2) to it
                        # The higher the number of threads allow, the faster it will end.
                        pages = convert_from_path(temp_path, 200, outputFolder, 1, nr_pages, 'png', 2)
                        f.close()
def rename():
    outputFolder = f"{os.getcwd()}\\PDFImages"
    for image in os.listdir(outputFolder):
        path = os.path.join(outputFolder,image)
        os.rename(path,os.path.join(outputFolder,path.split('-')[-1]))

def rmImages():
    outputFolder = f"{os.getcwd()}\\PDFImages"
    for image in os.listdir(outputFolder):
        path = os.path.join(outputFolder,image)
        os.remove(path)

if __name__ == "__main__":
    pass
