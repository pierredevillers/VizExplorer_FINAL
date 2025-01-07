import psycopg2
import json

dbname = "swiss_private_bank"
user = "postgres"  # Ensure this is a string
password = "123456789"  # Ensure this is correct
host = "localhost"  # Host for the database
port = 5432  

# Database connection details
conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
)

# Load the filtered queries JSON
with open("database/training_data/training_queries.json", "r", encoding="utf-8") as f:
    queries = json.load(f)

# Insert queries into the training_data table
cursor = conn.cursor()
for query in queries:
    cursor.execute(
        "INSERT INTO training_data (question, sql_query) VALUES (%s, %s)",
        (query["question"], query["query"])
    )

# Commit and close connection
conn.commit()
cursor.close()
conn.close()
print("Data successfully inserted into the training_data table.")
