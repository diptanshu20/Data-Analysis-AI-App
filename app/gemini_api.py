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
    only using actual columns from uploaded data (df).
    """

    quoted_cols = extract_quoted_columns(user_query)

    prompt = f"""
You are a data analysis assistant. The user is working with a pandas DataFrame named `df`.

Here are the actual column names in the DataFrame:
{df_columns}

The user mentioned the following column names in quotes:
{quoted_cols if quoted_cols else '[]'}

🚫 IMPORTANT CONSTRAINTS:
- Only use the DataFrame `df` uploaded by the user. Do NOT assume or generate new data.
- DO NOT create or assume any DataFrame like `df2`, `df3`, or `new_df` unless explicitly requested.
- DO NOT create any DataFrame with sample data.
- If the user references a column that doesn't exist in `df_columns`, then return a comment like:
  `# Error: One or more referenced columns do not exist in the uploaded data.`
- Do not wrap the code in functions or classes.
- Use matplotlib or seaborn for plots (but NO plt.show()).
- Always use the column names exactly (including spaces, casing, underscores).

📌 Task:
Generate Python code (only code, no explanation) that performs this task on the user's DataFrame:

"{user_query}"

If the task is not possible due to missing columns or unclear instruction, return a comment explaining the problem.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
