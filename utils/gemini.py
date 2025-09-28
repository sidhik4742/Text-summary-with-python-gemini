# function to get the summarization of the prompt text from gemini AI
import requests
import os
import time
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
from google import genai
load_dotenv()

# Configure logging info, error, warning
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Retry decorator: 5 attempts, exponential backoff from 1s to 16s
@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=16))
def get_gemini_response(prompt: str) -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    client = genai.Client(api_key=api_key)

    start_time = time.time()  # Start latency timer
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[prompt]
        )
        latency = time.time() - start_time  # Measure latency

        logging.info(f"Latency: {latency:.2f}s")
        return response.candidates[0].content.parts[0].text

    except Exception as e:
        logging.warning(f"API call failed after {latency:.2f}s: {e}")
        logging.error(f"Exception during Gemini API call: {e}")
        latency = time.time() - start_time
        raise  # Trigger retry