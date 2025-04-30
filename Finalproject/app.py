import os
from flask import Flask, request, render_template
from pdf2image import convert_from_path
import pytesseract
from ai_validator import validate_contract

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['contract']
    contract_type = request.form.get('contract_type')  # <-- Get contract type from form

    if file.filename.endswith('.pdf'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Convert PDF to images
        images = convert_from_path(filepath)
        full_text = ''
        for image in images:
            text = pytesseract.image_to_string(image)
            full_text += text + '\n'

        # Validate contract (now also passes the contract_type)
        results = validate_contract(full_text, contract_type)

        return render_template('results.html', **results)

    return "Please upload a valid PDF file."

if __name__ == '__main__':
    app.run(debug=True)