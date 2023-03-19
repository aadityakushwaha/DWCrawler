import mysql.connector

def insert_data_to_database(data, url):
    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Girlactor@77"
        # database="Crawler"
    )
    
    # Create a cursor object to interact with the database
    mycursor = mydb.cursor()

    # Create the 'Crawler' database if it doesn't exist
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Crawler")

    # Switch to the 'Crawler' database
    mycursor.execute("USE Crawler")

    # Create the 'url' table if it doesn't exist
    mycursor.execute("CREATE TABLE IF NOT EXISTS url (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255))")

    # Create the 'websites' table if it doesn't exist
    mycursor.execute("CREATE TABLE IF NOT EXISTS websites (id INT AUTO_INCREMENT PRIMARY KEY, url_id INT, title TEXT, image_links LONGTEXT, meta_content LONGTEXT, headings TEXT, paragraphs LONGTEXT, links LONGTEXT, FOREIGN KEY (url_id) REFERENCES url(id))")
    # Insert the URL into the 'urls' table and get the ID
    sql = "INSERT INTO url (url) VALUES (%s)"
    val = (url,)
    mycursor.execute(sql, val)
    url_id = mycursor.lastrowid

    # Insert the data into the 'data' table with the URL ID
    sql = "INSERT INTO websites (url_id, title, image_links, meta_content, headings, paragraphs, links) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (url_id, data['title'], str(data['image_links']), str(data['meta_content']), str(data['headings']), str(data['paragraphs']), str(data['links']))
    mycursor.execute(sql, val)

    # Commit the changes to the database and close the connection
    mydb.commit()
    mycursor.close()
    mydb.close()
