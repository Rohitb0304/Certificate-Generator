from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import pandas as pd
from pptx import Presentation
import os
import zipfile
import shutil

from utils import generate_certificate

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# File paths
UPLOAD_FOLDER = 'uploads/'
CERTIFICATES_FOLDER = 'certificates/'
ZIP_FOLDER = 'zips/'

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CERTIFICATES_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)

def check_pptx_tags(pptx_path):
    prs = Presentation(pptx_path)
    tags_found = any('<<FULL NAME>>' in shape.text for slide in prs.slides for shape in slide.shapes if shape.has_text_frame)
    return tags_found

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pptx_file' not in request.files or 'csv_file' not in request.files:
            flash('Please upload both PPTX and CSV files!')
            return redirect(request.url)

        pptx_file = request.files['pptx_file']
        csv_file = request.files['csv_file']

        # Save uploaded files
        pptx_path = os.path.join(UPLOAD_FOLDER, pptx_file.filename)
        csv_path = os.path.join(UPLOAD_FOLDER, csv_file.filename)

        pptx_file.save(pptx_path)
        csv_file.save(csv_path)

        if not check_pptx_tags(pptx_path):
            flash('Tag <<FULL NAME>> not found in PPTX template.')
            return redirect(request.url)

        flash('Tag <<FULL NAME>> found. Now fetching CSV data...')

        # Load CSV
        student_data = pd.read_csv(csv_path)
        if len(student_data) > 40:
            flash('The limit is 40 records. Please upload a smaller file.')
            return redirect(request.url)

        # Process each student
        for idx, row in student_data.iterrows():
            print(f"Generating certificate for: {row['Full_Name']}")
            generate_certificate(row, pptx_path, CERTIFICATES_FOLDER)

            # Check if the certificate was created
            certificate_path = os.path.join(CERTIFICATES_FOLDER, f"{row['Full_Name']}.pptx")
            if os.path.exists(certificate_path):
                print(f"Certificate saved at: {certificate_path}")
            else:
                print(f"Error: Certificate not saved for {row['Full_Name']}")

        flash('Certificates generated successfully! Preparing download...')

        # Create a ZIP of the certificates
        zip_filename = os.path.join(ZIP_FOLDER, 'certificates.zip')
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(CERTIFICATES_FOLDER):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f"Adding {file_path} to ZIP")
                    zipf.write(file_path, os.path.relpath(file_path, CERTIFICATES_FOLDER))

        # Clear old certificates
        shutil.rmtree(CERTIFICATES_FOLDER)
        os.makedirs(CERTIFICATES_FOLDER, exist_ok=True)

        return send_file(zip_filename, as_attachment=True, download_name='certificates.zip')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
