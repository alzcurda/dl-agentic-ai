import aisuite
from dotenv import load_dotenv

load_dotenv()
client = aisuite.Client()
response = client.chat.completions.create(
    model="google:gemini-3.5-flash",
    messages=[{"role": "user", "content": "What is 2+2? Reply in one word."}]
)
print("Response:", response.choices[0].message.content)
