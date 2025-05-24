import cv2
import pytesseract

# Yeh path Windows ke liye hai, Mac/Linux users isko hata sakte hain
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Image not found!")
        return
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Text extract karo
    extracted_text = pytesseract.image_to_string(gray)

    print("📌 Extracted Text from Screenshot:\n")
    print(extracted_text)

# Example usage
extract_text("lakshtransaction1.jpg")
