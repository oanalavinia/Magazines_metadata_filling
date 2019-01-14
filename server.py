from flask import Flask, render_template, request
from modules import pdf_to_images, ext_paragraphsJson

import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    file = request.files['fileToUpload']
    file.save(f'{os.getcwd()}\\Uploads\\{file.filename}')
    print(f'{os.getcwd()}\\Uploads\\{file.filename}')
    pdf_to_images.runScript()
    pdf_to_images.rename()
    ext_paragraphsJson.createJson()
    pdf_to_images.rmImages()
    os.remove(f'{os.getcwd()}\\Uploads\\{file.filename}')
    return 'Saved file'

if __name__ == '__main__':
    app.run(debug=True)