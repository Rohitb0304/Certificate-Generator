import os
import subprocess
from pptx import Presentation

def generate_certificate(row, pptx_template_path, output_folder):
    try:
        full_name = row['Full_Name'].title()  # Get student's full name and title case it
        reference_number = row.get('Reference_Number', 'N/A').strip()  # Get reference number if available

        # Load the PowerPoint template
        prs = Presentation(pptx_template_path)

        # Replace placeholders in all slides and shapes
        for slide in prs.slides:
            for shape in slide.shapes:
                if not shape.has_text_frame:
                    continue  # Skip if the shape does not have text
                
                # Iterate through each paragraph and run in the text frame
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        # Check for <<FULL NAME>> and replace with student's name
                        if '<<FULL NAME>>' in run.text:
                            run.text = run.text.replace('<<FULL NAME>>', full_name)

                        # You can similarly replace other placeholders (e.g., <<CNUM>>) if needed

                        # Keep original font formatting from the template (size, bold, italics, etc.)
                        run.font.size = run.font.size or Pt(24)  # Default size if missing
                        run.font.bold = run.font.bold
                        run.font.italic = run.font.italic
                        run.font.underline = run.font.underline

        # Save the modified certificate as a new PPTX file
        temp_pptx_path = os.path.join(output_folder, f"{full_name}.pptx")
        prs.save(temp_pptx_path)

        # Convert the PPTX to PDF (if needed)
        convert_to_pdf(temp_pptx_path, output_folder)

    except Exception as e:
        print(f"Error generating certificate for {full_name}: {e}")

def convert_to_pdf(pptx_file, output_folder):
    try:
        # Convert the PowerPoint to PDF using LibreOffice
        subprocess.run(['/usr/bin/libreoffice', '--headless', '--convert-to', 'pdf', pptx_file, '--outdir', output_folder], check=True)
        os.remove(pptx_file)  # Optionally delete the original .pptx file after conversion
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {pptx_file} to PDF: {e}")
