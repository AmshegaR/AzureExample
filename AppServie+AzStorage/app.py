import os
import time
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from azure.storage.blob import BlockBlobService

app=Flask(__name__)

app.secret_key = "***"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['AZURE_STORAGE_CONTAINER'] = "***"
app.config['AZURE_STORAGE_ACCOUNT'] = "****"
app.config['AZURE_STORAGE_KEY'] = "***"

ALLOWED_EXTENSIONS = set(['txt', 'log'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files and 'email' not in request.form:
            flash('Missing attributes')
            return redirect(request.url)
        file = request.files['file']
        email = request.form['email']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            BlobFilename = email + '~' + str(int(time.time())) + '_' + filename
            block_blob_service = BlockBlobService(account_name=app.config['AZURE_STORAGE_ACCOUNT'], account_key=app.config['AZURE_STORAGE_KEY'])
            block_blob_service.create_blob_from_bytes(
                app.config['AZURE_STORAGE_CONTAINER'],
                BlobFilename,
                file.read())
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt and log')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000, debug = False)
