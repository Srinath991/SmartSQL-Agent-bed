from langchain_community.utilities.sql_database import SQLDatabase
from app.config import SUPABASE_DB_URL

# Create SQLAlchemy-backed LangChain DB utility
db = SQLDatabase.from_uri(SUPABASE_DB_URL)
