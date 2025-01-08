import json
import psycopg2
import time
import pandas as pd
from collections import Counter
from difflib import SequenceMatcher
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from FINAL_performance_measure_charts import (
    plot_similarity_distribution,
    plot_bleu_distribution,
    plot_processing_time_comparison,
    plot_queries_validation_breakdown)

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

# Function to check if a query is valid SQL
def is_valid_sql(query):
    sql_keywords = {"SELECT", "FROM", "WHERE", "JOIN", "GROUP", "ORDER", "INSERT", "UPDATE", "DELETE"}
    return any(keyword in query.upper() for keyword in sql_keywords)

# Initialize metrics and logs
exact_match_count = 0
bleu_scores = []
execution_accuracy_count = 0
processing_times = {"reference": [], "generated": []}
valid_queries_reference = 0
valid_generated_queries_count = 0
invalid_generated_queries_count = 0
non_valid_reference_queries_count = 0
non_sql_responses_count = 0
reference_query_errors = []
generated_query_errors = []
similarity_scores = []

# Evaluate each query
for query in queries:
    ref_normalized = query["reference_sql_query"]["normalized"]
    gen_normalized = query["generated_sql_query"]["normalized"]
    db_id = query["db_id"]

    # Skip empty queries
    if not ref_normalized.strip() or not gen_normalized.strip():
        continue

    # Check for non-SQL responses
    if not is_valid_sql(gen_normalized):
        non_sql_responses_count += 1
        continue  # Skip non-SQL responses

    try:
        # Connect to the database
        conn = connect_to_db(db_id)
        if conn:
            # Execute reference query
            ref_result = execute_query(conn, ref_normalized)
            if isinstance(ref_result, str):  # If error occurred
                reference_query_errors.append(ref_result)
                non_valid_reference_queries_count += 1
            elif isinstance(ref_result, list):
                if ref_result:  # Valid and non-empty result
                    valid_queries_reference += 1
                else:  # Empty result
                    non_valid_reference_queries_count += 1

            # Execute generated query
            gen_result = execute_query(conn, gen_normalized)
            if isinstance(gen_result, str):  # If error occurred
                generated_query_errors.append(gen_result)
                invalid_generated_queries_count += 1
            elif isinstance(gen_result, list):
                if gen_result:  # Valid and non-empty result
                    valid_generated_queries_count += 1
                else:  # Empty result
                    invalid_generated_queries_count += 1

            # Execution Accuracy
            if isinstance(ref_result, list) and isinstance(gen_result, list) and set(ref_result) == set(gen_result):
                execution_accuracy_count += 1

            # Measure processing time
            start_time = time.time()
            execute_query(conn, ref_normalized)
            processing_times["reference"].append(time.time() - start_time)

            start_time = time.time()
            execute_query(conn, gen_normalized)
            processing_times["generated"].append(time.time() - start_time)

            conn.close()
    except Exception as e:
        print(f"Error processing queries for db_id={db_id}: {e}")

    # Exact Match Accuracy
    if ref_normalized.strip() == gen_normalized.strip():
        exact_match_count += 1

    # Similarity Score
    similarity = SequenceMatcher(None, ref_normalized, gen_normalized).ratio()
    similarity_scores.append(similarity)

    # BLEU Score
    smoothing_function = SmoothingFunction().method1
    bleu = sentence_bleu([ref_normalized.split()], gen_normalized.split(), smoothing_function=smoothing_function)
    bleu_scores.append(bleu)

# Calculate metrics

total_queries = len(queries)
valid_queries_total = total_queries - non_sql_responses_count

exact_match_accuracy = exact_match_count / valid_queries_total if valid_queries_total else 0

average_similarity_score = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0
similarity_stats = {
    "average": round(sum(similarity_scores) / len(similarity_scores), 2) if similarity_scores else 0,
    "min": round(min(similarity_scores), 2) if similarity_scores else 0,
    "max": round(max(similarity_scores), 2) if similarity_scores else 0,
}

average_bleu_score = sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0
bleu_stats = {
    "average": round(sum(bleu_scores) / len(bleu_scores), 2) if bleu_scores else 0,
    "min": round(min(bleu_scores), 2) if bleu_scores else 0,
    "max": round(max(bleu_scores), 2) if bleu_scores else 0,
}

execution_accuracy = execution_accuracy_count / valid_queries_total if valid_queries_total else 0

average_processing_time_ref = sum(processing_times["reference"]) / len(processing_times["reference"]) if processing_times["reference"] else 0
processing_time_ref_stats = {
    "average": round(sum(processing_times["reference"]) / len(processing_times["reference"]), 2) if processing_times["reference"] else 0,
    "min": round(min(processing_times["reference"]), 2) if processing_times["reference"] else 0,
    "max": round(max(processing_times["reference"]), 2) if processing_times["reference"] else 0,
}


average_processing_time_gen = sum(processing_times["generated"]) / len(processing_times["generated"]) if processing_times["generated"] else 0
processing_time_gen_stats = {
    "average": round(sum(processing_times["generated"]) / len(processing_times["generated"]) , 2)if processing_times["generated"] else 0,
    "min": round(min(processing_times["generated"]), 2) if processing_times["generated"] else 0,
    "max": round(max(processing_times["generated"]), 2) if processing_times["generated"] else 0,
}

# Display results as DataFrame
df = pd.DataFrame({
    "Metric": ["Similarity Score", "BLEU Score", "Processing Time (Reference)", "Processing Time (Generated)"],
    "Average": [similarity_stats["average"], bleu_stats["average"], str(f"{processing_time_ref_stats["average"]}s"), str(f"{processing_time_gen_stats["average"]}s")],
    "Min": [similarity_stats["min"], bleu_stats["min"], str(f"{processing_time_ref_stats["min"]}s"), str(f"{processing_time_gen_stats["min"]}s")],
    "Max": [similarity_stats["max"], bleu_stats["max"], str(f"{processing_time_ref_stats["max"]}s"), str(f"{processing_time_gen_stats["max"]}s")],
})

# Summarize error messages
reference_error_summary = Counter(reference_query_errors)
generated_error_summary = Counter(generated_query_errors)

# Display results
print("Performance Metrics:\n")

print(f"Total Queries: {total_queries}")
print(f"Valid Queries: {valid_queries_total}")
print(f"Valid Reference Queries: {valid_queries_reference} ({(valid_queries_reference / valid_queries_total) * 100:.2f}% of {valid_queries_total} valid queries)")
print(f"Non-Valid Reference Queries: {non_valid_reference_queries_count} ({(non_valid_reference_queries_count / valid_queries_total) * 100:.2f}% of {valid_queries_total} valid queries)")
print(f"Valid Generated Queries: {valid_generated_queries_count} ({(valid_generated_queries_count / valid_queries_total) * 100:.2f}% of {valid_queries_total} valid queries)")
print(f"Non-Valid Generated Queries: {invalid_generated_queries_count} ({(invalid_generated_queries_count / valid_queries_total) * 100:.2f}% of {valid_queries_total} valid queries)")
print(f"Non-SQL Responses (Out of Scope): {non_sql_responses_count} ({(non_sql_responses_count / total_queries) * 100:.2f}% of {total_queries} total queries)\n")

print(f"Exact Match Accuracy: {exact_match_accuracy:.2%}")
print(f"Execution Accuracy: {execution_accuracy:.2%}")

# Display performance metrics in console
print("\nSummary of BLEU Scores and Processing Times:")
print(df)

print("\nMost Common Errors in Generated Queries:")
for error, count in generated_error_summary.most_common(5):
    print(f"{error}: {count} occurrences")

# Save results to a JSON file
output_results = {
    "exact_match_accuracy": exact_match_accuracy,
    "average similarity score": average_similarity_score,
    "average_bleu_score": average_bleu_score,
    "execution_accuracy": execution_accuracy,
    "average_processing_time_reference": average_processing_time_ref,
    "average_processing_time_generated": average_processing_time_gen,
    "valid_queries_reference": valid_queries_reference,
    "non_valid_reference_queries_count": non_valid_reference_queries_count,
    "valid_generated_queries": valid_generated_queries_count,
    "invalid_generated_queries": invalid_generated_queries_count,
    "non_sql_responses_count": non_sql_responses_count,
    "generated_error_summary": generated_error_summary.most_common(10)
}

output_file_path = "performance_measure/performance_results.json"
with open(output_file_path, 'w') as outfile:
    json.dump(output_results, outfile, indent=4)

print(f"Performance results saved to {output_file_path}")

# Generate charts
plot_similarity_distribution(similarity_scores)
plot_bleu_distribution(bleu_scores)
plot_processing_time_comparison(processing_time_ref_stats, processing_time_gen_stats)
plot_queries_validation_breakdown(valid_generated_queries_count, invalid_generated_queries_count, non_sql_responses_count)
