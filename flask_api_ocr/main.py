# ================= SSL FIX =================
# Required for EasyOCR model download on Windows + Python 3.13
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# ===========================================

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
import easyocr
import pytesseract
import cv2
import re

# ------------------ Flask App ------------------
app = Flask(__name__)
CORS(app)

# ------------------ Swagger Config (FIXED) ------------------
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",  # 🔥 FIX
    "swagger_ui": True,
    "specs_route": "/swagger/",
    "title": "OCR API",
    "description": "OCR using EasyOCR and Tesseract",
    "version": "1.0.0"
}

Swagger(app, config=swagger_config)

# ------------------ OCR Engines ------------------
easy_reader = easyocr.Reader(['en'], gpu=False)

# ------------------ OCR FUNCTIONS ------------------
def ocr_with_tesseract(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return ""
        return pytesseract.image_to_string(img)
    except Exception:
        return ""

def ocr_with_easyocr(image_path):
    try:
        result = easy_reader.readtext(image_path)
        return "\n".join([line[1] for line in result])
    except Exception:
        return ""

# ------------------ REGEX CLEAN ------------------
def clean_text_regex(text):
    if not text:
        return ""
    text = re.sub(r"[^A-Za-z0-9\s\.\,\-\(\)\/@:+<]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ------------------ EXTRACTORS ------------------
def extract_emails(text):
    return list(set(re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text
    )))

def extract_phones(text):
    return list(set(re.findall(
        r"(?:\+880|\+88|01|\+?\d{1,3})[\s\-]?\d{8,11}", text
    )))

def extract_addresses(text):
    keywords = ["road", "street", "avenue", "house", "floor", "block", "dhaka", "bangladesh"]
    lines = re.split(r"[,.]", text)
    return [l.strip() for l in lines if any(k in l.lower() for k in keywords)]

def extract_passport_number(text):
    return list(set(re.findall(r"\b[A-Z]{1,2}[0-9]{7,8}\b", text)))

def extract_dob(text):
    return list(set(re.findall(r"\b\d{2}[\/\-]\d{2}[\/\-]\d{4}\b", text)))

def extract_mrz(text):
    return list(set(re.findall(r"P[A-Z<]{20,44}", text)))

def extract_all(text):
    return {
        "visiting_card": {
            "emails": extract_emails(text),
            "phones": extract_phones(text),
            "addresses": extract_addresses(text)
        },
        "passport": {
            "passport_numbers": extract_passport_number(text),
            "date_of_birth": extract_dob(text),
            "mrz": extract_mrz(text)
        }
    }

# ------------------ HOME ------------------
@app.route('/', methods=['GET'])
def home():
    """
    API Health Check
    ---
    tags:
      - Health
    responses:
      200:
        description: API is running
    """
    return jsonify({
        "message": "OCR API running (EasyOCR + Tesseract)"
    })

# ------------------ PROCESS ------------------
@app.route('/process', methods=['POST'])
def process_document():
    """
    Process Image with EasyOCR and Tesseract
    ---
    tags:
      - OCR
    consumes:
      - multipart/form-data
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: Image for OCR
    responses:
      200:
        description: OCR result
    """
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"error": "Image is required"}), 400

    os.makedirs("uploads", exist_ok=True)
    image_path = os.path.join("uploads", image_file.filename)
    image_file.save(image_path)

    # ---- OCR ----
    easy_raw = ocr_with_easyocr(image_path)
    tess_raw = ocr_with_tesseract(image_path)

    # ---- CLEAN ----
    easy_clean = clean_text_regex(easy_raw)
    tess_clean = clean_text_regex(tess_raw)

    combined_text = clean_text_regex(
        f"{easy_clean} {tess_clean}"
    )

    os.remove(image_path)

    return jsonify({
        "easyocr": {
            "raw": easy_raw,
            "extracted": extract_all(easy_clean)
        },
        "tesseract": {
            "raw": tess_raw,
            "extracted": extract_all(tess_clean)
        },
        "combined": extract_all(combined_text)
    })

# ------------------ RUN ------------------
if __name__ == '__main__':
    app.run(debug=True)
