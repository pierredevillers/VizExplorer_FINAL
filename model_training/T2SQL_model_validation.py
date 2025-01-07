from vanna.remote import VannaDefault
import vanna
import psycopg2
import json

dbname = "swiss_private_bank"
user = "postgres"
password = "123456789"
host = "localhost"
port = 5432

api_key = 'be920fe18e6c4a3fa6bf9436d6113657'
vanna_model_name = 'vizexplorer'
vn = VannaDefault(model=vanna_model_name, api_key=api_key)

# Connect Vanna to PostgreSQL
try:
    vn.connect_to_postgres(
        host = host,
        dbname = dbname,
        user = user,
        password = password,
        port = port
    )
    print("Vanna successfully connected to PostgreSQL.")
except Exception as e:
    print(f"Failed to connect Vanna to PostgreSQL: {e}")

def format_output(data):
    """
    Formats the output data into a readable format.

    Args:
        data (list): List of dictionaries containing question, query, and other fields.

    Returns:
        str: Formatted string with readable output.
    """
    formatted = []
    for entry in data:
        question = entry.get("question", "No question provided")
        query = entry.get("query", "No query provided")
        db_id = entry.get("db_id", "Unknown database")
        formatted.append(f"Database: {db_id}\nQuestion: {question}\nGenerated SQL:\n{query}\n{'-' * 40}")
    return "\n".join(formatted)

def test_vanna_model(vanna, test_questions):
    """
    Test the Vanna model with a list of sample questions and format the results.

    Args:
        vanna: Vanna model instance.
        test_questions (list): List of natural language questions.
    """
    print("\nStarting Vanna Model Testing...\n")
    results = []  # Store results for formatting
    for question in test_questions:
        try:
            # Generate SQL for the test question
            generated_sql = vanna.ask(question)
            results.append({
                "question": question,
                "query": generated_sql,
                "db_id": "swiss_private_bank"  # Adjust to your database ID
            })
            print(f"✔ Successfully generated SQL for: {question}")
        except Exception as e:
            print(f"❌ Failed to generate SQL for question '{question}': {e}")

    # Format and print the results
    readable_output = format_output(results)
    print("\nTest Results:\n")
    print(readable_output)
    vn._endpoint()
    # Optionally, save the output to a file
    # with open("test_results.txt", "w", encoding="utf-8") as f:
    #     f.write(readable_output)

if __name__ == "__main__":
    # List of sample questions to test the model
    test_questions = [
        "List all transactions above CHF 2,500."
    ]

    # Test the model and format the output
    test_vanna_model(vn, test_questions)
