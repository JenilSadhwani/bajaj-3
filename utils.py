
import cv2
import numpy as np
from PIL import Image
import re

import pytesseract

# Only needed on Windows
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_lab_tests(image_file):
    # Load image using PIL
    image = Image.open(image_file)
    
    # Convert to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Run OCR
    text = pytesseract.image_to_string(image_cv)

    # Pattern: TestName 13.5 (12.0 - 15.5)
    pattern = r'([A-Za-z\s]+)\s+([\d\.]+)\s*(?:[a-zA-Z\/]*)\s*\(?([\d\.]+)\s*-\s*([\d\.]+)\)?'
    matches = re.findall(pattern, text)

    results = []
    for match in matches:
        test_name = match[0].strip()
        test_value = float(match[1])
        ref_low = float(match[2])
        ref_high = float(match[3])
        is_out = not (ref_low <= test_value <= ref_high)

        results.append({
            "test_name": test_name,
            "test_value": str(test_value),
            "bio_reference_range": f"{ref_low} - {ref_high}",
            "lab_test_out_of_range": is_out
        })

    return results
