# app/gemini_api.py

import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_quoted_columns(query: str) -> list:
    """
    Extract column names from within double or single quotes in the query.
    """
    return re.findall(r'["\'](.*?)["\']', query)

def get_code_from_query(user_query: str, df_columns: list) -> str:
    """
    Uses Gemini to generate Python code based on a user query,
    respecting quoted column names and actual df columns.
    """
    quoted_cols = extract_quoted_columns(user_query)

    prompt = f"""
You are a data analysis assistant. The user is working with a pandas DataFrame named `df`.

Here are the actual column names in the DataFrame:
{df_columns}

The user mentioned the following column names in quotes — these are correct and MUST be used exactly:
{quoted_cols if quoted_cols else '[]'}

Instructions:
- Use the column names exactly as written (respect casing, spaces, and underscores).
- Do NOT "guess" or auto-convert column names.
- If plotting, use matplotlib or seaborn.
- Do NOT use plt.show() (it will be handled by the app).
- ❌ Do NOT wrap code inside functions like def show_plot().
- ✅ Just write the code as-is that performs the operation and generates plots.
- If creating a new DataFrame, use df2, df3, etc.
- Return code only — no text, no explanations.

User Task:
{user_query}
    """

    response = model.generate_content(prompt)
    return response.text.strip()
