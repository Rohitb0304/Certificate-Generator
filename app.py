from flask import Flask, request, render_template, send_file, redirect, url_for, flash, session, jsonify
import pandas as pd
from pptx import Presentation
from fpdf import FPDF
import os
import zipfile
import shutil
import time

from utils import generate_certificate  # Assume this function exists

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

# Global progress tracking
progress_status = {
    "total": 0,
    "completed": 0,
    "current_name": ""
}

def check_pptx_tags(pptx_path):
    prs = Presentation(pptx_path)
    tags_found = any('<<FULL NAME>>' in shape.text for slide in prs.slides for shape in slide.shapes if shape.has_text_frame)
    return tags_found

@app.route('/', methods=['GET', 'POST'])
def index():
    global progress_status

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

        # Initialize progress status
        progress_status = {
            "total": len(student_data),
            "completed": 0,
            "current_name": ""
        }

        # Determine generation type and estimated time
        generation_type = request.form.get('generation_type')
        estimated_time = len(student_data) * (2 if generation_type == 'pdf' else 0)  # Assume 2 seconds per PDF

        if generation_type == 'pptx':
            for idx, row in student_data.iterrows():
                student_name = row['Full_Name']
                progress_status['current_name'] = student_name
                generate_certificate(row, pptx_path, CERTIFICATES_FOLDER)
                progress_status['completed'] += 1
        elif generation_type == 'pdf':
            for idx, row in student_data.iterrows():
                student_name = row['Full_Name']
                progress_status['current_name'] = student_name
                # Simulate PDF generation
                time.sleep(2)  # Simulate time taken to generate PDF
                generate_pdf_certificate(row, CERTIFICATES_FOLDER)  # Function to generate PDF
                progress_status['completed'] += 1

        flash('Certificates generated successfully! Preparing download...')

        # Create a ZIP of the certificates
        zip_filename = os.path.join(ZIP_FOLDER, 'certificates.zip')
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(CERTIFICATES_FOLDER):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), CERTIFICATES_FOLDER))

        # Clear old certificates
        shutil.rmtree(CERTIFICATES_FOLDER)
        os.makedirs(CERTIFICATES_FOLDER, exist_ok=True)

        return send_file(zip_filename, as_attachment=True, download_name='certificates.zip')

    return render_template('index.html')

@app.route('/progress', methods=['GET'])
def progress():
    """Return the current progress of certificate generation."""
    return jsonify(progress_status)

def generate_pdf_certificate(row, output_folder):
    """Function to generate a PDF certificate for a student."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content to PDF
    pdf.cell(200, 10, txt=f"Certificate of Achievement for {row['Full_Name']}", ln=True, align='C')

    # Save PDF to the output folder
    pdf_file_path = os.path.join(output_folder, f"{row['Full_Name']}.pdf")
    pdf.output(pdf_file_path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
