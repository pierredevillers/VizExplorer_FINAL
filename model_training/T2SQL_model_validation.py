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

# Connect model to PostgreSQL
try:
    vn.connect_to_postgres(
        host = host,
        dbname = dbname,
        user = user,
        password = password,
        port = port
    )
    print("Model successfully connected to PostgreSQL.")
except Exception as e:
    print(f"Failed to connect Model to PostgreSQL: {e}")

def format_output(data):

    formatted = []
    for entry in data:
        question = entry.get("question", "No question provided")
        query = entry.get("query", "No query provided")
        db_id = entry.get("db_id", "Unknown database")
        formatted.append(f"Database: {db_id}\nQuestion: {question}\nGenerated SQL:\n{query}\n{'-' * 40}")
    return "\n".join(formatted)

def test_model(vanna, test_questions):

    print("\nStarting Model Testing...\n")
    results = []  # Store results for formatting
    for question in test_questions:
        try:
            # Generate SQL for the test question
            generated_sql = vanna.ask(question)
            results.append({
                "question": question,
                "query": generated_sql,
                "db_id": "swiss_private_bank" 
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

    test_model(vn, test_questions)
