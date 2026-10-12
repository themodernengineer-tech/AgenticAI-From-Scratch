from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

response = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="In one sentence, explain what an AI agent is.",
)

print(response.output_text)