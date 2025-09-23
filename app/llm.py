from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GOOGLE_API_KEY


# Instantiate Gemini LLM (stable streaming-compatible)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY
)
