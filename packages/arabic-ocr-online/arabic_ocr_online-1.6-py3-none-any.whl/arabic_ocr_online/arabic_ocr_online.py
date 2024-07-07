import cv2
from easyocr import Reader
from PIL import Image
import requests
from io import BytesIO
import numpy as np

def cleanup_text(text):
    # Strip out non-ASCII text so we can draw the text on the image using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def ocring(image_url, out_image_path):
    # Specify the languages
    langs = ["ar", "en"]
    
    # Load the input image from URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    # Convert the PIL image to a NumPy array
    image_array = np.array(img)
    
    # Convert RGB to BGR (OpenCV uses BGR format)
    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    # Convert the image to grayscale
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the grayscale image
    image_blur = cv2.GaussianBlur(image_gray, (5, 5), 0)
    
    # Apply Otsu's thresholding
    _, image_thresh = cv2.threshold(image_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # OCR the input image using EasyOCR
    print("[INFO] OCR'ing input image...")
    reader = Reader(langs, gpu=True)
    results = reader.readtext(image_thresh)
    
    # Loop over the results
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
        cv2.rectangle(image_bgr, tl, br, (0, 255, 0), 2)
        cv2.putText(image_bgr, text, (tl[0], tl[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Save the output image
    cv2.imwrite(out_image_path, image_bgr)
    
    return results