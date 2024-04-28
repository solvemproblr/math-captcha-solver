import numpy as np
from PIL import Image
import re
import cv2
import easyocr


def preprocess_image(image):
    # Resize and upscale the image
    const = 4
    resized_image = cv2.resize(image, (image.shape[1] * const, image.shape[0] * const))

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_RGBA2GRAY)

    # Enhance contrast using histogram equalization
    # enhanced_image = cv2.equalizeHist(gray_image)

    # Apply Gaussian blurring for noise reduction
    # blurred_image = cv2.GaussianBlur(enhanced_image, (3, 3), 0)

    # Apply adaptive thresholding
    _, thresholded = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresholded


def solve_math_expression(image):
    preprocessed_image = preprocess_image(image)

    extracted_text = reader.readtext(preprocessed_image, detail=0, allowlist='0123456789+/x=')

    final_text = "".join(extracted_text)
    final_text = final_text.replace('x', '*')
    final_text = final_text.rstrip('-=')

    cleaned_text = re.sub(r'[^\d+\-*/]', '', final_text)
    cleaned_text = cleaned_text.replace(' ', '')

    try:
        result2 = eval(cleaned_text)
        return result2
    except:
        extracted_text2 = reader.readtext(preprocessed_image, detail=0, allowlist='0123456789-=')
        final_text = "".join(extracted_text2)
        cleaned_text = re.sub(r'[^\d+\-*/]', '', final_text)
        cleaned_text = cleaned_text.replace(' ', '')
        try:
            result2 = eval(cleaned_text)
            return result2
        except:
            return "Invalid expression"


reader = easyocr.Reader(lang_list=['en'], gpu=False)
