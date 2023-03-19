from crawler import deep_scan
# Read the list of URLs from a file
with open('urls.txt', 'r') as f:
    urls = f.read().splitlines()

# Call the deep_scan function for each URL
for url in urls:
    deep_scan(url)