import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import logging
from text_processor import process_documents

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "resume-shortlister-secret-key"

# Configure upload folder
UPLOAD_FOLDER = 'view_pdf/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_pdf/<path:filename>')
def view_pdf(filename):
    filepath = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
    if os.path.exists(filepath) and filepath.startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
        return send_file(filepath, mimetype='application/pdf')
    return "PDF not found", 404

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'requirements' not in request.form or 'resumes[]' not in request.files:
            logger.error("Missing requirements or resumes in request")
            return jsonify({'error': 'Missing requirements or resumes'}), 400

        requirements_text = request.form['requirements']
        resume_files = request.files.getlist('resumes[]')

        if not requirements_text or not resume_files:
            logger.error("No requirements text or resume files provided")
            return jsonify({'error': 'No requirements text or resume files provided'}), 400

        # Process resume files
        resume_paths = []
        for resume in resume_files:
            if resume and allowed_file(resume.filename):
                filename = secure_filename(resume.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                resume.save(filepath)
                resume_paths.append(filepath)
                logger.debug(f"Saved resume file: {filepath}")

        try:
            # Process documents and get results
            logger.info("Processing documents...")
            results = process_documents(requirements_text, resume_paths)
            return render_template('results.html', results=results)
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            return jsonify({'error': f'Error processing documents: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
