import mysql.connector
import yaml

# Define the MySQL database configuration
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "Girlactor@77",
    "database": "Crawler"
}

# Connect to the MySQL server
try:
    db = mysql.connector.connect(**mysql_config)
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL server: {err}")
    exit()

# Create a cursor to execute SQL queries
cursor = db.cursor()

# Query your MySQL database to retrieve the data you want to use to modify your config.yml
cursor.execute("SELECT title, description, url, keywords FROM onion_urls where scraped = 1")
data = cursor.fetchall()

# Load the existing config.yml file
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Check for duplicates and add new items to the config file
for item in data:
    name = item[0]
    subtitle = item[1]
    keywords = item[3]
    url = item[2]
    
    # Check if the item already exists in the config file
    if any(d['name'] == name for d in config['services'][0]['items']):
        continue
    
    # Add the new item to the config file
    new_item = {
        "name": name,
        "logo": "assets/tools/sample.png",
        "subtitle": subtitle,
        "keywords": keywords,
        "url": url,
    }
    config['services'][0]['items'].append(new_item)
# Write the updated config.yml file back to disk
with open("config.yml", "w") as f:
    yaml.dump(config, f)

