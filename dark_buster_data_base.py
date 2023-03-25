import csv
import requests
from bs4 import BeautifulSoup
import mysql.connector

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Crawler"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Create a table to store the data
# Create a table to store the data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS url_responses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url LONGTEXT,
        status_code INT NOT NULL,
        reason VARCHAR(255),
        page VARCHAR(255),
        response_details VARCHAR(255)
    )
""")


# Set up proxies for requests if needed
session = requests.session()
session.proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

def buster(wordlist, url):
    if url[-1] != "/":
        url += "/"

    with open(wordlist) as f:
        reader = csv.reader(f)
        s1 = (row[0] for row in reader)
        
        # Insert the data into the table
        sql = "INSERT INTO url_responses (url) VALUES (%s)"
        val = (url,)
        cursor.execute(sql, val)
        db.commit()
        print(url)

        for i in s1:
            try:
                response = session.get(url+i, timeout=10)
                if response.status_code == 200:
                    print(url+i)
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Combine the status code, reason, and page values as a string separated by commas
                    response_details = f"{response.status_code}, {response.reason}, {i}"

                    # Insert the data into the table
                    sql = "INSERT INTO url_responses (status_code, reason, page, response_details) VALUES (%s, %s, %s, %s)"
                    val = (response.status_code, response.reason, i, str(response_details))
                    cursor.execute(sql, val)
                    db.commit()
            

                # else:
                #     print(f"Error: {response.status_code} - {response.reason}")

            except requests.exceptions.RequestException as err:
                print(f"Error making request to URL: {err}")
                continue

# Prompt the user for the path to the wordlist and the URL to target
wordlist_given="w1.csv"
url_given = "http://ozgunsbxgra7huwedjymobzswzk3hdysncrfrhdv2kledvjaqydtzdyd.onion/"

buster(wordlist_given, url_given)

# Close the database connection
db.close()
