import requests
from bs4 import BeautifulSoup
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Crawler"
)

mycursor = mydb.cursor()

# Get list of onion URLs from database that haven't been scraped yet
mycursor.execute("SELECT id, url FROM onion_urls WHERE scraped = 0")
onion_urls = mycursor.fetchall()

# Loop through onion URLs and scrape meta content, image URLs, and other useful data
for id, url in onion_urls:
    try:
        # Make request to onion URL and parse HTML with BeautifulSoup
        response = requests.get(url, proxies={'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050', }, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get title
        title = soup.find('title').text.strip() if soup.find('title') else ""

        # Get keywords
        keywords = ""
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if tag.get('name') == 'keywords':
                keywords += tag.get('content')

        # Get description
        description = ""
        for tag in meta_tags:
            if tag.get('name') == 'description':
                description += tag.get('content')

        # Get content
        content = ""
        body_tags = soup.find_all('body')
        for tag in body_tags:
            content += tag.text.strip()

        # Get image URLs
        image_urls = ""
        img_tags = soup.find_all('img')
        for tag in img_tags:
            if tag.get('src'):
                image_urls += tag.get('src') + "\n"
                
        try:        
            # Update record in database with title, keywords, description, content, and image URLs, and mark as scraped
            sql = "UPDATE onion_urls SET url = %s, title = %s, keywords = %s, description = %s, content = %s, image_urls = %s, scraped = 1 WHERE id = %s and scraped = 0"
            val = (url.strip(), title.strip(), keywords.strip(), description.strip(), content.strip(), image_urls.strip(), id)
            mycursor.execute(sql, val)
            mydb.commit()

            print(f"Successfully scraped and updated data for {url}")
        except Exception as e:
             print(f"Error saaving data to database: {e}")
        
        def error():
            sql = "UPDATE onion_urls SET url = %s, title = %s, keywords = %s, description = %s, content = %s, image_urls = %s, scraped = -1 WHERE id = %s"
            val = (url.strip(), title.strip(), keywords.strip(), description.strip(), content.strip(), image_urls.strip(), id)
            mycursor.execute(sql, val)
            mydb.commit()

    except Exception as e:
        print(f"Error scraping: {url}")
        try:
            error()
        except Exception as e:
             print(f"Error saaving data to database: {e}")
