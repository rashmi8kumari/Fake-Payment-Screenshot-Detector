import pytesseract
from PIL import Image

# Tesseract ka path set karo
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Image load karo
img = Image.open("lakshtransaction1.jpg")  # Apni image ka naam yahan dalna

# Text extract karo
extracted_text = pytesseract.image_to_string(img)

print("Extracted Text:")
print(extracted_text)