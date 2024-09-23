Here's a complete README file for your Certificate Generator project, including instructions for building and running the Docker container, as well as a link to the deployed site.


# Certificate Generator

A web application to generate certificates using a PPTX template and a CSV file containing names.

## Live Demo

You can access the live version of the application [here](https://certificate-generator-8a9g.onrender.com).

## Features

- Upload a PPTX template with a placeholder for names.
- Upload a CSV file with a column named `Full_Name`.
- Generate certificates based on the provided template and data.
- Download a ZIP file containing all generated certificates.

## Requirements

- Python 3.9 or higher
- Flask
- Pandas
- python-pptx
- Docker (for containerization)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Rohitb0304/Certificate-Generator.git
cd Certificate-Generator
```

### 2. Install Dependencies

If you want to run the app locally without Docker, make sure to install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Application Locally

To run the application locally, use:

```bash
export FLASK_APP=your_flask_app.py  # Replace with your actual app filename
flask run --host=0.0.0.0 --port=5000
```

### 4. Using Docker

#### To Build Docker Image

You can build the Docker image using the following command:

```bash
docker build -t certificate-generator .
```

#### To Run Docker Container

Run the Docker container with the following command:

```bash
docker run -p 5000:5000 certificate-generator
```

### 5. Access the Application

After running the application (locally or via Docker), you can access it in your web browser at:

```
http://localhost:5000
```

## How to Use

1. **Prepare Your PPTX Template**:
   - Include a placeholder for the full name in the PPTX template. Use `<<FULL NAME>>` as the placeholder text.

2. **Prepare Your CSV File**:
   - Create a CSV file with a column named `Full_Name` that contains the names for the certificates.

3. **Upload Files**:
   - Go to the application and upload your PPTX template and CSV file.

4. **Generate Certificates**:
   - Click the button to generate certificates, and once completed, download the ZIP file containing all the generated certificates.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Thanks to the contributors of the libraries used in this project.
```

Feel free to modify any sections as needed!
