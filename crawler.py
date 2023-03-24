import requests
from bs4 import BeautifulSoup
import mysql.connector

session = requests.session()
session.proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

def deep_scan(url):
    # Define the starting URL
    start_url = url
    
    # Define the MySQL database configuration
    mysql_config = {
        "host": "localhost",
        "user": "root",
        "password": "Girlactor@77",
        "database": "Crawler"
    }
    
    # Connect to the MySQL database
    try:
        db = mysql.connector.connect(**mysql_config)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return

    # Create a cursor to execute SQL queries
    cursor = db.cursor()

    # Create the table to store the URLs (if it doesn't exist already)
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS onion_urls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url VARCHAR(255) NOT NULL UNIQUE
            )
        """)
    except mysql.connector.Error as err:
        print(f"Error creating MySQL table: {err}")
        db.close()
        return


    # Define a set to keep track of visited URLs
    visited_urls = set()

    # Define a list to keep track of URLs to visit
    urls_to_visit = [start_url]

    # Loop until there are no more URLs to visit
    while urls_to_visit:
        # Pop the next URL from the list of URLs to visit
        url = urls_to_visit.pop(0)
        
        # Skip URLs that have already been visited
        if url in visited_urls:
		
            continue
        
        # Add the URL to the set of visited URLs
        visited_urls.add(url)
        
        # Make a request to the URL
        try:
            response = session.get(url, timeout=10)
        except requests.exceptions.RequestException as err:
            print(f"Error making request to URL: {err}")
            continue
        
        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all links on the page
        links = soup.find_all("a")
        
        # Add any new links to the list of URLs to visit
        for link in links:
            href = link.get("href")
            try:
                if href and href.startswith("http") and href.endswith(".onion") and href not in visited_urls:
                    # Insert the new URL into the database (if it doesn't exist already)
                    try:
                        cursor.execute("INSERT IGNORE INTO onion_urls (url) VALUES (%s)", (href,))
                        db.commit()
                    except mysql.connector.Error as err:
                        print(f"Error inserting URL into MySQL database: {err}")
                        continue
                        
                    # Add the new URL to the list of URLs to visit
                    urls_to_visit.append(href)
            except AttributeError as err:
                print(f"Something went wrong: {err}")
    print("done")
    db.close()
