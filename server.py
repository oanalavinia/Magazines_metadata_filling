from flask import Flask, render_template, request, send_file
from modules import pdf_to_images, ext_paragraphsJson, getFeaturesFromSections, txt_to_csv, predictModel

import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['fileToUpload']
    file.save(f'{os.getcwd()}\\Uploads\\{file.filename}')
    print(f'{os.getcwd()}\\Uploads\\{file.filename}')
    pdf_to_images.runScript()
    pdf_to_images.rename()
    ext_paragraphsJson.createJson()
    pdf_to_images.rmImages()
    getFeaturesFromSections.run()
    txt_to_csv.run()
    predictModel.run()

    os.remove(f'{os.getcwd()}\\Uploads\\{file.filename}')
    return render_template('downloads.html')

@app.route('/return-file/')
def deturn_file():
    return send_file(f'{os.getcwd()}\\userEndResult.xml')

@app.route('/file-downloads/')
def file_downloads():
    return render_template('downloads.html')


if __name__ == '__main__':
    app.run(debug=True)
