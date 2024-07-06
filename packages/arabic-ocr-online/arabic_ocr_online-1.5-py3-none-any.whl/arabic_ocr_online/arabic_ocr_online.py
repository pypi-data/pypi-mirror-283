from easyocr import Reader
import cv2
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import logging

# Set logging level for EasyOCR to WARNING
logging.getLogger('easyocr').setLevel(logging.WARNING)

def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def ocring(image_path, out_image):
    # break the input languages into a comma separated list
    langs = ["ar", "en"]
    gpu = True  # Use GPU if available

    # load the input image from url
    response = requests.get(image_path)
    img = Image.open(BytesIO(response.content))

    # Convert the PIL image to a NumPy array
    imageArr = np.array(img)

    # Convert RGB to BGR (OpenCV uses BGR format)
    imageGrey = cv2.cvtColor(imageArr, cv2.COLOR_BGR2GRAY)
    imageGauss = cv2.GaussianBlur(imageGrey, (5, 5), 0)
    _, image = cv2.threshold(imageGauss, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR the input image using EasyOCR
    reader = Reader(langs, gpu=gpu)
    results = reader.readtext(image)

    # Loop over the results
    filename = out_image
    for (bbox, text, prob) in results:
        # Unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        # Cleanup the text and draw the box surrounding the text along with the OCR'd text itself
        text = cleanup_text(text)
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        cv2.putText(image, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Save the output image
    cv2.imwrite(filename, image)
    
    return results