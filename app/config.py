from dotenv import load_dotenv
import os

load_dotenv(override=True)

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
