import os
import logging
import hashlib
import cv2
import numpy as np
import pytesseract
import random
import string
from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from PIL import Image, ExifTags
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ✅ Logging Setup
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# ✅ Upload Folder Setup
UPLOAD_FOLDER = "uploads"
REPORTS_FOLDER = "reports"  # Folder to store reports
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORTS_FOLDER"] = REPORTS_FOLDER

# ✅ Configure Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Home Route
@app.route("/")
def home():
    return "Welcome to Fake Transaction Detector API!"

# ✅ Image Upload & Processing Route
@app.route("/upload", methods=["POST"])
def upload_image():
    try:
        logging.debug("🟢 API Called: /upload")

        if "file" not in request.files:
            return jsonify({"error": "No file found"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # ✅ Generate Unique Filename to Avoid Overwrites
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        file_ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{timestamp}_{random_str}{file_ext}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

        # ✅ Save File
        file.save(file_path)

        if not os.path.exists(file_path):
            return jsonify({"error": "File was not saved properly!"}), 500

        logging.debug(f"🟢 File Saved: {file_path}")

        # ✅ Analyze Image
        result, metadata_info = analyze_image(file_path)

        # ✅ Generate PDF Report
        report_filename = f"{timestamp}_{random_str}.pdf"
        report_path = os.path.join(app.config["REPORTS_FOLDER"], report_filename)
        generate_pdf_report(report_path, file.filename, result, metadata_info)

        # ✅ Prevent Cached Responses
        response = make_response(jsonify({
            "filename": unique_filename,
            "result": result,
            "metadata": metadata_info,
            "report_url": f"http://127.0.0.1:5000/download_report/{report_filename}"
        }))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response

    except Exception as e:
        logging.error(f"🔴 Processing Failed: {str(e)}")
        return jsonify({"error": f"Processing Failed: {str(e)}"}), 500

# ✅ Image Analysis Function (Fake/Real)
def analyze_image(image_path):
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            return "Error: Could not read image", {}

        # ✅ Edge Detection
        edges = cv2.Canny(image, 50, 150)
        edge_pixels = np.sum(edges)

        # ✅ OCR-Based Text Extraction
        extracted_text = extract_text(image_path)

        # ✅ EXIF Metadata Extraction
        metadata_info = extract_metadata(image_path)

        # ✅ Fake Detection Logic
        suspicious_texts = ["Edited", "Fake", "Photoshop", "Canva"]
        if any(word in extracted_text for word in suspicious_texts) or edge_pixels > 900000:
            return "Fake", metadata_info
        elif "Transaction Successful" in extracted_text and edge_pixels < 400000:
            return "Real", metadata_info
        else:
            return "Fake", metadata_info

    except Exception as e:
        logging.error(f"🔴 Image processing failed: {str(e)}")
        return "Error: Image processing failed", {}

# ✅ OCR-Based Text Extraction
def extract_text(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        logging.error(f"🔴 OCR Extraction Failed: {str(e)}")
        return ""

# ✅ EXIF Metadata Extraction
def extract_metadata(image_path):
    try:
        with open(image_path, "rb") as f:
            file_data = f.read()

        image = Image.open(image_path)
        metadata_info = {}

        # ✅ Extract EXIF metadata
        exif_data = image.getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                metadata_info[tag_name] = str(value)

        # ✅ Extract Additional Metadata
        file_stats = os.stat(image_path)
        file_size = file_stats.st_size  
        modified_time = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

        # ✅ Unique File Hash
        file_hash = hashlib.md5(file_data).hexdigest()
        logging.debug(f"🟢 File Hash: {file_hash}")

        metadata_info.update({
            "File Name": os.path.basename(image_path),
            "File Size (Bytes)": file_size,
            "Last Modified": modified_time,
            "File Hash (MD5)": file_hash,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image Size": f"{image.width}x{image.height}",
        })

        return metadata_info

    except Exception as e:
        logging.error(f"🔴 Metadata extraction failed: {str(e)}")
        return {"Error": f"Metadata extraction failed: {str(e)}"}

# ✅ Generate PDF Report
def generate_pdf_report(report_path, filename, result, metadata):
    try:
        c = canvas.Canvas(report_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 750, "Fake Transaction Detection Report")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"File Name: {filename}")
        c.drawString(100, 710, f"Result: {result}")

        y_position = 690
        for key, value in metadata.items():
            c.drawString(100, y_position, f"{key}: {value}")
            y_position -= 20
            if y_position < 50:
                c.showPage()
                y_position = 750

        c.save()
        logging.debug(f"🟢 PDF Report Generated: {report_path}")

    except Exception as e:
        logging.error(f"🔴 PDF Report Generation Failed: {str(e)}")

# ✅ Report Download Route
@app.route("/download_report/<filename>")
def download_report(filename):
    report_path = os.path.join(app.config["REPORTS_FOLDER"], filename)
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True)
    else:
        return jsonify({"error": "Report not found"}), 404

# ✅ Start Server
if __name__ == "__main__":
    logging.debug("🟢 Flask Server Starting...")
    app.run(debug=False, threaded=False, use_reloader=False, host="0.0.0.0", port=5000)














