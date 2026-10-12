import time

from dotenv import load_dotenv
from google import genai

# Load the Gemini API key from the local .env file
load_dotenv()

# Create a Gemini API client
client = genai.Client()

prompt = "In one sentence, explain what an AI agent is."

# Start measuring before the API request
start_time = time.perf_counter()

# Send the prompt and limit the generated response
response = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input=prompt,
    generation_config={"max_output_tokens": 120},
)

# Calculate how long the request took
elapsed_seconds = time.perf_counter() - start_time

print("Answer:", response.output_text)
print(f"Latency: {elapsed_seconds:.2f} seconds")