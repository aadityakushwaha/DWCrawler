import mysql.connector
import openai

# Connect to the SQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="PASSWORD",
  database="Crawler"
)

# Retrieve the data from the database
cursor = db.cursor()
cursor.execute("SELECT * FROM onion_urls WHERE ai_tag IS NULL")
rows = cursor.fetchall()

# Set up the OpenAI API
openai.api_key = "API-KEY"
model_engine = "text-davinci-003"
initial = "Please follow reply in this format\n tags = #tage_name"
prompt_template = "Please provide some tags for this website based on the following information:\nTitle: {}\nKeywords: {}\nDescription: {}\nContent: {}\nTags:"
prompt_template = prompt_template + initial

# Loop through each row of data
for row in rows:
    # Extract the relevant data
    id_ = row[0]
    url = row[1]
    title = row[2]
    keywords = row[3]
    description = row[4]
    content = row[5]
    
    # Generate the prompt for the OpenAI API
    prompt = prompt_template.format(title, keywords, description, content)
    
    try:
        # Call the OpenAI API to generate tags
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
    
        # Extract the generated tags from the API response
        tags = response.choices[0].text.strip()
    
        
    
        # Update the corresponding row in the database with the generated tags
        update_query = "UPDATE onion_urls SET ai_tag = %s WHERE id = %s"
        cursor.execute(update_query, (tags, row[0]))
        db.commit()
        print(f"tags for {id_} and {url} : " + tags + "\n")
    except openai.error.InvalidRequestError as e:
        print("Error: String too large\n")

# Close the database connection
db.close()
