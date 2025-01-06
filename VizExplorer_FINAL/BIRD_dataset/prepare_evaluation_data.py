import json
import logging
import re

# Configure logging
logging.basicConfig(
    filename='prepare_ground_truth.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Paths
DEV_JSON = r"C:\Users\Pierre Devillers\Desktop\VizExplorer_FINAL\BIRD_V0\dev\dev.json"
CONVERTED_GROUND_TRUTH = "converted_ground_truth.json"


def convert_sqlite_to_postgresql(sql):
    """
    Convert SQLite SQL query to PostgreSQL syntax.

    Args:
        sql (str): SQLite SQL query.

    Returns:
        str: PostgreSQL-compatible SQL query.
    """
    # Replace backticks with double quotes for identifiers
    sql = sql.replace("`", "\"")

    # Replace SQLite-specific data types
    sql = sql.replace("TEXT", "VARCHAR")
    sql = sql.replace("INTEGER", "INT")

    # Remove unnecessary spaces around double quotes
    sql = re.sub(r'\s*"\s*', '"', sql)

    # Ensure no backslashes
    sql = sql.replace("\\", "")

    # Handle CAST operations (ensure proper syntax for PostgreSQL)
    sql = re.sub(r"CAST\((.*?) AS REAL\)", r"CAST(\1 AS DOUBLE PRECISION)", sql)

    return sql.strip()


def load_and_convert_ground_truth(dev_json):
    """
    Load and convert SQLite ground truth data to PostgreSQL-compatible format.

    Args:
        dev_json (str): Path to the dev.json file.

    Returns:
        list: Converted ground truth data.
    """
    with open(dev_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    converted_data = []
    for item in data:
        question = item["question"]
        sqlite_sql = item["SQL"]
        db_id = item["db_id"]

        # Convert SQL to PostgreSQL-compatible format
        postgres_sql = convert_sqlite_to_postgresql(sqlite_sql)
        converted_data.append({"question": question, "SQL": postgres_sql, "db_id": db_id})
        logging.info(f"Converted query for question: {question}")

    return converted_data

def save_converted_ground_truth(data, output_path):
    """
    Save the converted ground truth data to a JSON file.

    Args:
        data (list): Converted ground truth data.
        output_path (str): Path to save the converted JSON.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logging.info(f"Converted ground truth saved to {output_path}")

def main():
    """
    Main function to prepare ground truth data.
    """
    # Load and convert ground truth data
    converted_data = load_and_convert_ground_truth(DEV_JSON)

    # Save converted data
    save_converted_ground_truth(converted_data, CONVERTED_GROUND_TRUTH)

    print("Ground truth preparation completed successfully.")

if __name__ == "__main__":
    main()
