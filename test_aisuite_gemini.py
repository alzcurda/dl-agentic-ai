import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("GEMINI_API_KEY", "")
os.environ["OPENAI_BASE_URL"] = "https://generativelanguage.googleapis.com/v1beta/openai/"

import aisuite
client = aisuite.Client()
response = client.chat.completions.create(
    model="openai:gemini-3.5-flash",
    messages=[{"role": "user", "content": "What is 2+2? Reply in one word."}]
)
print("Response:", response.choices[0].message.content)
