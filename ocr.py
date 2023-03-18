import requests
import pytesseract
from PIL import Image
from io import BytesIO

proxy = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

def extract_text_from_url(url):

    # Fetch the image from the URL using requests
    response = requests.get(url, proxies=proxy)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch image from {url}")

    # Convert the image content to a PIL Image object
    image = Image.open(BytesIO(response.content))

    # Use pytesseract to extract the text from the image
    text = pytesseract.image_to_string(image)

    # Remove any extra whitespace or newlines from the extracted text
    text = ' '.join(text.split())

    return text

# print(extract_text_from_url("https://hips.hearstapps.com/hmg-prod/images/encouraging-quotes-1607057436.jpg"))