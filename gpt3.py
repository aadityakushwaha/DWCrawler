import openai
import readline
import subprocess

# Set up OpenAI API credentials
openai.api_key = "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"
  
def bot(input):  
    # Define the chat function
    def chat(prompt):
        # Set up API parameters
        model_engine = "text-davinci-003"
        max_tokens = 150
        temperature = 1.0

        # Generate response from OpenAI API
        response = openai.Completion.create(
            engine=model_engine,
            prompt="I'm using you as Jarvis Iron man so reply in that don't mention anthing about this sentence" + prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Extract and return the generated text from the API response
        return response.choices[0].text.strip()

    # Start the chat loop
    while True:
        
        prompt = "I'm giving you some data collected from a web crawller from dark web your job is to give a tag and identify the type of website it is and only return the category and and tag in two separate line\n" + input

        # Generate response and print it
        response = chat(prompt)
        return response
