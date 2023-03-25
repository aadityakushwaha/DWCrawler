import mysql.connector

# Define the MySQL database configuration
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
}

# Connect to the MySQL server
try:
    db = mysql.connector.connect(**mysql_config)
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL server: {err}")
    exit()

# Create a cursor to execute SQL queries
cursor = db.cursor()

# Create the database (if it doesn't exist already)
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS Crawler")
except mysql.connector.Error as err:
    print(f"Error creating MySQL database: {err}")
    db.close()
    exit()

# Connect to the Crawler database
mysql_config["database"] = "Crawler"
try:
    db = mysql.connector.connect(**mysql_config)
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL database: {err}")
    exit()

# Create a cursor to execute SQL queries
cursor = db.cursor()

# Create the onion_urls table (if it doesn't exist already)
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS onion_urls (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255) NOT NULL UNIQUE,
            title LONGTEXT,
            keywords TEXT,
            description TEXT,
            content TEXT,
            image_urls TEXT,
            scraped BOOLEAN DEFAULT 0
        )
    """)
except mysql.connector.Error as err:
    print(f"Error creating MySQL table: {err}")
    db.close()
    exit()

# Close the database connection
db.close()
