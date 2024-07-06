import os
from easyocr import Reader
import cv2
from PIL import Image
import requests
from io import BytesIO
import numpy as np

# Define the languages you want to download
langs = ["ar", "en"]

# Set the model storage path from the environment variable
model_storage_directory = os.getenv("EASYOCR_DIR", os.path.expanduser("~/.EasyOCR"))

# Initialize the reader, which will trigger the model downloads
reader = Reader(langs, gpu=False, model_storage_directory=model_storage_directory)

def cleanup_text(text):
    # Strip out non-ASCII text so we can draw the text on the image using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def ocring(image_path, out_image):
    # Load the input image from the URL
    response = requests.get(image_path)
    img = Image.open(BytesIO(response.content))

    # Convert the PIL image to a NumPy array
    imageArr = np.array(img)

    # Convert RGB to BGR (OpenCV uses BGR format)
    imageGrey = cv2.cvtColor(imageArr, cv2.COLOR_BGR2GRAY)
    imageGauss = cv2.GaussianBlur(imageGrey, (5, 5), 0)
    _, image = cv2.threshold(imageGauss, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR the input image using EasyOCR
    print("[INFO] OCR'ing input image...")
    results = reader.readtext(imageArr)

    # Loop over the results
    filename = out_image
    for (bbox, text, prob) in results:
        # Display the OCR'd text and associated probability
        print("[INFO] {:.4f}: {}".format(prob, text))
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