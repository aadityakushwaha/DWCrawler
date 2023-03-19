import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import pytesseract

session = requests.session()
session.proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

def extract_text_from_url(url):
    response = session.get(url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(bw.astype(np.uint8), kernel, iterations=1)
    text = pytesseract.image_to_string(dilation)
    text = text.replace(" ", "")
    return text