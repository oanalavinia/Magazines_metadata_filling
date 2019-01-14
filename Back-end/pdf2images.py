from pdf2image import convert_from_path
import os
from PyPDF2 import PdfFileReader
import shutil
import zipfile
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
folder_path = "C:\\Users\\TudorIacobuta\\Desktop\\pdf"

sets = 1
pdfs = 1
temp_folder = f"C:\\Users\\TudorIacobuta\\Desktop\\pdf\\set_{sets}"
os.mkdir(temp_folder)
for file in os.listdir(folder_path): 
        
        
        if file.endswith(".pdf"):
                temp_path = os.path.join(folder_path, file)
                if (os.path.isfile(temp_path)):
                        shutil.copy(temp_path, temp_folder)
                        pdfs += 1
                
                #pdf = PdfFileReader(open(temp_path, 'rb'))
                #nr_pages = pdf.getNumPages()
                #os.mkdir("C:\\Users\\TudorIacobuta\\Desktop\\pdf\\%s" % file.split('.')[0])
                #path = os.path.join(folder_path, file.split('.')[0])
                #pages = convert_from_path(temp_path, 200, path, 1, nr_pages, 'png', 3)
        
        if pdfs == 5:
                pdfs = 1
                sets += 1
                temp_folder = f"C:\\Users\\TudorIacobuta\\Desktop\\pdf\\set_{sets}"
                os.mkdir(temp_folder)
        
