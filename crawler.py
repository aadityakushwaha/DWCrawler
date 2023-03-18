import requests
import sqlite3
from bs4 import BeautifulSoup
from gpt3 import bot


links_with_in = []

proxy = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

def binary_search(arr, x):
    """
    Perform binary search on a sorted array to find the index of the given URL.
    If the URL is not found, return -1.
    """
    print("Binary Search")
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        # Check if x is present at mid
        if arr[mid] == x:
            return mid

        # If x is greater, ignore left half
        elif arr[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        else:
            high = mid - 1

    # If we reach here, the element was not present
    return -1


# Define a recursive function to perform a deep scan of the website
def deep_scan(url):
    response = requests.get(url, proxies=proxy)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the website's title
    title = soup.title.string
    # print(f'Title: {title}')

    # Extract image links
    image_links = [img['src'] for img in soup.find_all('img')]
    # print(f'Image links: {image_links}')

    # Extract meta content tags
    meta_tags = soup.find_all('meta')
    meta_content = {tag['name']: tag['content'] for tag in meta_tags if 'name' in tag.attrs and 'content' in tag.attrs}
    # print(f'Meta content: {meta_content}')
    
    links = soup.find_all('a', href=True)
    print(links)

    # Iterate over the links and check if they contain ".in"
    for link in links:
        if '.onion' in link['href']:
            # print(link['href'])
            # Add the link to the list of links with ".in"
            try:
                links_with_in.append(link['href'])
                # Recursively call the function on the new link
                if binary_search(links_with_in, link['href']) != -1 and len(links_with_in) > 1:
                    deep_scan(link['href'])
            except:
                print("An Error Occured")
            
            

    # Extract other useful information
    headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

    # Store the extracted information in a dictionary
    data = {
        'title': title,
        'image_links': image_links,
        'meta_content': meta_content,
        'headings': headings,
        'links': links
    }

    # print(f'Extracted data: {data}')
    # print(data['image_links'])
    # print("")
    
    # print(links_with_in)