import wapiti

scan = wapiti.Scan()

# Set the target URL and scan depth
url = input("URL: ")
scan.set_url(url)
scan.set_depth(2)

# Set the Tor proxy option
proxy_url = 'socks5h://127.0.0.1:9050'
scan.set_option('proxy', proxy_url)

# Start the scan
scan.start()

# Get the scan results
results = scan.get_results()

# Print the results
for result in results:
    print('Vulnerability:', result['name'])
    print('Description:', result['description'])
    print('URL:', result['url'])
    print('Parameter:', result['parameter'])
    print('Method:', result['method'])
    print('Evidence:', result['evidence'])
    print('Solution:', result['solution'])
    print()
