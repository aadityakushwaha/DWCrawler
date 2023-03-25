import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Crawler"
)

# Create a cursor to execute SQL queries
mycursor = mydb.cursor()

# Execute SQL query to fetch data and sort it by count column in descending order
mycursor.execute("SELECT * FROM onion_urls ORDER BY count DESC LIMIT 60")

# Get the results and print them out
results = mycursor.fetchall()
non_wiki_count=0
for result in results:

    if ("wikipedia" not in str(result)) & (non_wiki_count<10):
        non_wiki_count+=1
        print(result[1])


mydb.close()


