import json
import psycopg2

# Database credentials
db_credentials = {
    "user": "postgres",
    "password": "123456789",
    "host": "localhost",
    "port": "5432"
}

# Load the cleaned JSON file
input_file_path = "performance_measure/cleaned_sql_queries.json"
with open(input_file_path, 'r') as infile:
    queries = json.load(infile)

# Function to connect to the database
def connect_to_db(db_id):
    try:
        conn = psycopg2.connect(dbname=db_id, **db_credentials)
        return conn
    except Exception as e:
        print(f"Error connecting to database {db_id}: {e}")
        return None

# Function to execute a query and fetch results
def execute_query(conn, sql):
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
        return result
    except Exception as e:
        return f"Query execution error: {e}"

# Initialize variables for precision, recall, and F1-score calculation
true_positives = 0
false_positives = 0
false_negatives = 0

total_queries = len(queries)
processed_queries = 0

# Evaluate each query
for query in queries:
    ref_query = query["reference_sql_query"]["normalized"].strip()
    gen_query = query["generated_sql_query"]["normalized"].strip()
    db_id = query["db_id"]

    # Count cases where queries are empty
    if not ref_query and not gen_query:
        continue

    try:
        # Connect to the database
        conn = connect_to_db(db_id)
        if conn:
            # Execute both queries
            ref_result = execute_query(conn, ref_query)
            gen_result = execute_query(conn, gen_query)
            
            if isinstance(ref_result, list) and isinstance(gen_result, list):
                ref_set = set(tuple(row) for row in ref_result)
                gen_set = set(tuple(row) for row in gen_result)

                # Calculate TP, FP, and FN
                tp = len(ref_set.intersection(gen_set))
                fp = len(gen_set - ref_set)
                fn = len(ref_set - gen_set)

                # Update overall counts
                true_positives += tp
                false_positives += fp
                false_negatives += fn
            conn.close()

    except Exception as e:
        print(f"Error processing queries for db_id={db_id}: {e}")

    processed_queries += 1
    print(f"Processed {processed_queries}/{total_queries} queries...")

# Calculate precision, recall, and F1 score
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Display results
print("SQL Output-Based Performance Metrics:")
print(f"Total True Positive Rows: {true_positives}")
print(f"Total False Positive Rows: {false_positives}")
print(f"Total False Negative Rows: {false_negatives}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1_score:.2f}")

# Save the performance metrics
output_results = {
    "true_positives": true_positives,
    "false_positives": false_positives,
    "false_negatives": false_negatives,
    "precision": round(precision, 2),
    "recall": round(recall, 2),
    "f1_score": round(f1_score, 2),
}
output_file_path = "performance_measure/sql_output_precision_recall_f1.json"
with open(output_file_path, 'w') as outfile:
    json.dump(output_results, outfile, indent=4)

print(f"Performance results saved to {output_file_path}")
