import os
import tempfile
import subprocess
from pptx import Presentation

def generate_certificate(row, pptx_template_path, output_folder):
    try:
        full_name = row['Full_Name'].title()
        reference_number = row.get('Reference_Number', 'N/A').strip()

        # Load the PowerPoint template
        prs = Presentation(pptx_template_path)

        # Replace placeholders in the slide
        slide = prs.slides[0]
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                if '<<FULL NAME>>' in paragraph.text:
                    paragraph.text = paragraph.text.replace('<<FULL NAME>>', full_name)
                if '<<REFERENCE NO>>' in paragraph.text:
                    paragraph.text = paragraph.text.replace('<<REFERENCE NO>>', str(reference_number))

        # Save the PPTX
        temp_pptx_path = os.path.join(output_folder, f"{full_name}_{reference_number}.pptx")
        prs.save(temp_pptx_path)

        # Convert to PDF
        convert_to_pdf(temp_pptx_path, output_folder)
    except Exception as e:
        print(f"Error generating certificate for {full_name}: {e}")

def convert_to_pdf(pptx_file, output_folder):
    try:
        subprocess.run(['/usr/bin/libreoffice', '--headless', '--convert-to', 'pdf', pptx_file, '--outdir', output_folder], check=True)
        os.remove(pptx_file)  # Optionally delete the .pptx file
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {pptx_file} to PDF: {e}")