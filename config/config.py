import os
from dotenv import load_dotenv
import google.genai as genai

# Load environment variables from .env file
load_dotenv()

# API keys - prioritize system environment variables over .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

CROP_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS1yndkdYpEMG1I1EqynWazYsyLRW3jbvoupsRChjctGozkQPN_Vd5amo47m661gIXp9paKVqh7UD3S/pub?gid=1555082969&single=true&output=csv"
FERTILIZER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSOo4fVG3L1011RtB9bcQbmC9jPQivbwZQ9lA8mK3-ajO75J1I-EUCL5ZJcx0MQ3DNxEEPgrV136qov/pub?gid=1216712628&single=true&output=csv"

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
