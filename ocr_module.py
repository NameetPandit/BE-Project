import cv2
import easyocr
import numpy as np
import re

# ✅ Preprocessing function
def preprocess_image(image_path):
    """ Preprocess image for better OCR performance """
    img = cv2.imread(image_path)

    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Denoising with GaussianBlur
    blurred = cv2.GaussianBlur(thresh, (5, 5), 0)

    # Resize for better clarity
    img_resized = cv2.resize(blurred, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

    return img_resized


# ✅ Postprocessing function
def postprocess_text(text):
    """ Clean the detected text by removing special characters """
    clean_text = re.sub(r'[^A-Za-z0-9]', '', text)
    return clean_text


# ✅ OCR function using EasyOCR
def detect_license_plate(image_path):
    """ Detects and processes the license plate text """
    reader = easyocr.Reader(['en'], gpu=False)

    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Perform OCR
    results = reader.readtext(preprocessed_image)

    # Extract and clean detected text
    license_plate_text = ""
    for detection in results:
        detected_text = detection[1]
        clean_text = postprocess_text(detected_text)
        license_plate_text += clean_text

    return license_plate_text if license_plate_text else "No Plate Detected"
