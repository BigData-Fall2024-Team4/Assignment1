import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response(prompt, file_content=None):
    try:
        messages = [
            {"role": "system", "content": "You are a highly efficient AI assistant. "},
            {"role": "user", "content": prompt + "Answer the question"}
        ]
        
        if file_content:
            messages.insert(1, {"role": "user", "content": f"Here's additional context from a file:\n\n{file_content}"})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            n=1,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"