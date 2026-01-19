import os
from groq import Groq

# Read key from environment (already loaded by settings.py)
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise Exception("GROQ_API_KEY not found")

# ✅ THIS IS THE LINE YOU ASKED FOR
client = Groq(api_key=API_KEY)


def ai_parse_query(text):
    response = client.chat.completions.create(
       model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an AI that extracts job search intent like skills, experience, and work mode."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
