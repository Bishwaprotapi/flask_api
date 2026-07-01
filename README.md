# Flask OCR API

A Flask-based OCR API that uses EasyOCR and Tesseract to extract text from images, with additional functionality to extract specific information like emails, phone numbers, addresses, passport numbers, and more.

## Author

**Bishwaprotap Ray**

- **Role:** Software Developer Intern | AI & Machine Learning Engineer
- **Education:** B.Sc. in Computer Science & Engineering (International University of Business Agriculture and Technology)
- **Specialization:** AI, Machine Learning, LLM, FastAPI, Voice Assistant Development
- **Location:** Dhaka, Bangladesh
- **Mobile:** +8801788974534
- **Email:** baburay214@gmail.com
- **LinkedIn:** [https://www.linkedin.com/in/bishwaprotap-ray/](https://www.linkedin.com/in/bishwaprotap-ray/)
- **GitHub:** [https://github.com/Bishwaprotapi](https://github.com/Bishwaprotapi)

## Features

- **Dual OCR Engine:** Uses both EasyOCR and Tesseract for accurate text extraction
- **Text Cleaning:** Regex-based text cleaning to remove unwanted characters
- **Information Extraction:**
  - Email addresses
  - Phone numbers
  - Addresses
  - Passport numbers
  - Dates of birth
  - MRZ (Machine Readable Zone) data
- **API Documentation:** Integrated Swagger documentation at `/swagger/`
- **CORS Enabled:** Cross-Origin Resource Sharing for frontend integration

## Technologies Used

- **Flask:** Web framework
- **EasyOCR:** Deep learning-based OCR engine
- **Tesseract OCR:** Google's OCR engine
- **OpenCV (cv2):** Image processing
- **Flasgger:** Swagger API documentation
- **Flask-CORS:** CORS support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Bishwaprotapi/flask_api.git
cd flask_api/flask_api_ocr
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install flask flask-cors flasgger easyocr pytesseract opencv-python
```

4. Install Tesseract OCR:
   - **Windows:** Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Linux:** `sudo apt-get install tesseract-ocr`
   - **Mac:** `brew install tesseract`

## Usage

1. Run the application:
```bash
python main.py
```

2. Access the API:
   - **Health Check:** `GET http://localhost:5000/`
   - **Process Image:** `POST http://localhost:5000/process`
   - **API Documentation:** `http://localhost:5000/swagger/`

## API Endpoints

### POST /process

Process an image and extract text using both EasyOCR and Tesseract.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
  "easyocr": {
    "raw": "extracted text",
    "extracted": {
      "visiting_card": {
        "emails": [],
        "phones": [],
        "addresses": []
      },
      "passport": {
        "passport_numbers": [],
        "date_of_birth": [],
        "mrz": []
      }
    }
  },
  "tesseract": {
    "raw": "extracted text",
    "extracted": { ... }
  },
  "combined": { ... }
}
```

## Project Structure

```
flask_api/
├── flask_api_ocr/
│   ├── main.py          # Main Flask application
│   ├── trst.html        # Test HTML file
│   └── uploads/         # Temporary upload directory
└── .gitignore
```

## License

This project is open source and available under the MIT License.
