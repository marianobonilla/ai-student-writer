from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from .utils import extract_text_from_pdf, extract_text_from_doc
from app.services.fine_tunning import fine_tunning
from app import app

#app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    text = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_extension = os.path.splitext(file.filename)[1]
            print(f"File extension of uploaded file is {file_extension}")
            if file_extension == '.pdf':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                text = extract_text_from_pdf(filepath)
            elif file_extension in ['.doc', '.docx']:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                text = extract_text_from_doc(filepath)
            else: 
                return "File format not supported."
            print(f"Extracted text: {text}") 
            # call the fine_tunning function with the extracted text
            fine_tunning(text)
            return render_template('prompt.html')

    return render_template('upload.html')

@app.route('/hello')
def hello_world():
    return 'Hello, world!'