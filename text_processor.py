import PyPDF2
import docx
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import logging
import string

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except Exception as e:
    logger.error(f"Error downloading NLTK data: {str(e)}")

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
        raise

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX {docx_path}: {str(e)}")
        raise

def preprocess_text(text):
    try:
        # Convert to lowercase and remove punctuation (except commas)
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation.replace(",", "")))
        
        # Split by both space and comma
        tokens = [token.strip() for token in text.replace(",", " ").split()]

        # Remove stopwords and lemmatize
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()

        processed_tokens = [
            lemmatizer.lemmatize(token)
            for token in tokens
            if token.isalnum() and token not in stop_words
        ]

        return processed_tokens
    except Exception as e:
        logger.error(f"Error preprocessing text: {str(e)}")
        raise

def calculate_match_score(req_tokens, resume_tokens):
    try:
        req_set = set(req_tokens)
        resume_set = set(resume_tokens)

        # Calculate intersection of keywords
        matching_keywords = req_set.intersection(resume_set)

        # Calculate score based on matching keywords
        score = len(matching_keywords) / len(req_set) if len(req_set) > 0 else 0

        return {
            'score': round(score * 100, 2),
            'matching_keywords': list(matching_keywords)
        }
    except Exception as e:
        logger.error(f"Error calculating match score: {str(e)}")
        raise

def process_documents(requirements_text, resume_paths):
    try:
        logger.info("Starting document processing")
        results = []

        # Process requirements text
        logger.debug(f"Processing requirements text: {requirements_text[:100]}...")
        req_tokens = preprocess_text(requirements_text)

        # Process each resume
        for resume_path in resume_paths:
            try:
                logger.debug(f"Processing resume: {resume_path}")
                # Extract text based on file type
                if resume_path.lower().endswith('.pdf'):
                    resume_text = extract_text_from_pdf(resume_path)
                elif resume_path.lower().endswith('.docx'):
                    resume_text = extract_text_from_docx(resume_path)
                else:
                    logger.warning(f"Unsupported file format: {resume_path}")
                    continue

                # Process resume text
                resume_tokens = preprocess_text(resume_text)

                # Calculate match score
                match_result = calculate_match_score(req_tokens, resume_tokens)

                results.append({
                    'filename': resume_path.split('/')[-1],
                    'score': match_result['score'],
                    'matching_keywords': match_result['matching_keywords']
                })
                logger.debug(f"Successfully processed resume: {resume_path}")

            except Exception as e:
                logger.error(f"Error processing resume {resume_path}: {str(e)}")
                continue

        # Sort results by score in descending order
        results.sort(key=lambda x: x['score'], reverse=True)
        logger.info(f"Successfully processed {len(results)} resumes")

        return results
    except Exception as e:
        logger.error(f"Error in process_documents: {str(e)}")
        raise
