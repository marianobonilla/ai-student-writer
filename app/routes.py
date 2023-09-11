from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from .services.s3_service import upload_file_to_s3
import os
from .utils import extract_text_from_pdf, extract_text_from_doc
import app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def init_app(app):
    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file_extension = os.path.splitext(file.filename)
                if file_extension == 'pdf':
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    text = extract_text_from_pdf(filepath)
                else:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    text = extract_text_from_doc(filepath)
                return render_template('results.html', extracted_text = text)
        
        return render_template('upload.html')

    @app.route('/hello')
    def hello_world():
        return 'Hello, world!'

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file_s3():
        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                success = upload_file_to_s3(file, 'useruploadedpdfs', filename)
                if success:
                    # TODO: update db with entry for user
                    return render_template('upload.html')
                
        return render_template('upload.html')