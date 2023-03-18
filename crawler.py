import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
from ocr import extract_text_from_url

# Maintain the same proxy settings across multiple requests using session
session = requests.session()
session.proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

# Store the links already scanned in a set
links_with_in = set()

# Define a recursive function to perform a deep scan of the website
def deep_scan(url):
    try:
        # Get the root url of the website
        root_url = urlparse(url).netloc
        
        response = session.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract image links
        image_links = [img['src'] for img in soup.find_all('img')]
        for link in image_links:
            print(extract_text_from_url(link))

        # Extract meta content tags
        meta_tags = soup.find_all('meta')
        meta_content = {tag['name']: tag['content'] for tag in meta_tags if 'name' in tag.attrs and 'content' in tag.attrs}

        # Extract links and recursively call the function on the new link
        links = soup.find_all('a', href=True)
        new_links = set()
        for link in links:
            # Check if the link is a relative URL
            if link['href'].startswith('/'):
                link_url = urljoin(response.url, link['href'])
            else:
                link_url = link['href']
                
            # Check if the link is from the same domain and not already scanned
            if root_url in link_url and link_url not in links_with_in:
                new_links.add(link_url)

        links_with_in.update(new_links)
        
        # Use a ThreadPoolExecutor to scan the new links concurrently
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(deep_scan, link) for link in new_links]

        # Extract other useful information
        headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

        # Store the extracted information in a dictionary
        data = {
            'title': soup.title.string,
            'image_links': image_links,
            'meta_content': meta_content,
            'headings': headings,
            'links': links
        }

    except requests.exceptions.RequestException as e:
        print(f"An Error Occured: {e}")

    print(links_with_in)
