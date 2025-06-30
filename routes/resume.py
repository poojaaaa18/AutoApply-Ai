from flask import Blueprint, request, jsonify
import fitz  # PyMuPDF

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/upload-resume', methods=['POST'])
def upload_resume():
    try:
        print("Request content type:", request.content_type)
        print("Request files:", request.files)

        # Check if 'file' key exists
        if 'file' not in request.files:
            return jsonify({'error': 'No file field named "file" in the request'}), 400

        uploaded_file = request.files['file']

        # Check if file is selected
        if uploaded_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Check for PDF file
        if not uploaded_file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400

        # Process the PDF
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return jsonify({"parsed_resume": text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
