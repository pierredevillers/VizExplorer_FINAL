import json
from typing import Dict

def load_schema() -> Dict:
    """Load database schema from JSON file"""
    try:
        with open('assets/schema.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove any SQL command keywords
    sql_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE']
    sanitized = user_input
    for keyword in sql_keywords:
        sanitized = sanitized.replace(keyword, '')
    return sanitized
