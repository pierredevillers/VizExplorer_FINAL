import json
import datetime
import psycopg2
from psycopg2.extras import DictCursor
import sqlparse
from difflib import SequenceMatcher
from nltk.translate.bleu_score import sentence_bleu

def datetime_converter(o):
    """
    Convert non-serializable objects like datetime to serializable formats.
    """
    try:
        if isinstance(o, datetime):
            return o.isoformat()  # Convert datetime to ISO format
        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")
    except TypeError:
        return str(o)  # Fallback to converting object to string

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def execute_query(query, db_id, db_credentials, batch_size=1000):
    try:
        conn = psycopg2.connect(
            dbname=db_id,
            user=db_credentials["user"],
            password=db_credentials["password"],
            host=db_credentials["host"],
            port=db_credentials["port"]
        )
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute(query)

        rows = []
        sample_rows = []
        while True:
            batch = cur.fetchmany(batch_size)
            if not batch:
                break
            rows.extend(batch)
            if len(sample_rows) < 5:
                sample_rows.extend(batch[:5 - len(sample_rows)])

        column_names = [desc.name for desc in cur.description] if cur.description else []
        row_count = len(rows)
        column_count = len(column_names)

        cur.close()
        conn.close()

        return rows, sample_rows, column_names, row_count, column_count
    except Exception as e:
        return str(e)

def normalize_sql(query):
    formatted_query = sqlparse.format(query, reindent=True, keyword_case="upper")
    return sqlparse.format(formatted_query, strip_whitespace=True)

def compute_similarity(query1, query2):
    return SequenceMatcher(None, query1, query2).ratio()

def calculate_similarity_bleu(query1, query2):
    reference = [query1.split()]
    hypothesis = query2.split()
    return sentence_bleu(reference, hypothesis)

def compare_results(ref_rows, out_rows):
    if len(ref_rows) != len(out_rows):
        return False

    for ref_row, out_row in zip(ref_rows, out_rows):
        if ref_row.keys() != out_row.keys():
            return False
        for key in ref_row.keys():
            if ref_row[key] != out_row[key]:
                return False

    return True

def process_queries(reference_file, output_file, db_credentials, log_file):
    reference_data = load_json(reference_file)
    output_data = load_json(output_file)
    execution_log = []

    output_data_dict = {item.get("question"): item for item in output_data}

    for idx, ref_item in enumerate(reference_data):
        question = ref_item.get("question")
        ref_query = ref_item.get("SQL")
        db_id = ref_item.get("db_id")

        if question in output_data_dict:
            out_item = output_data_dict[question]
            out_query = out_item.get("SQL")

            if ref_query and out_query and db_id:
                print(f"Processing query {idx + 1}/{len(reference_data)} for question: {question}")
                normalized_ref_query = normalize_sql(ref_query)
                normalized_out_query = normalize_sql(out_query)

                ref_result = execute_query(normalized_ref_query, db_id, db_credentials)
                out_result = execute_query(normalized_out_query, db_id, db_credentials)

                if isinstance(ref_result, tuple) and isinstance(out_result, tuple):
                    ref_rows, ref_sample_rows, ref_column_names, ref_row_count, ref_column_count = ref_result
                    out_rows, out_sample_rows, out_column_names, out_row_count, out_column_count = out_result

                    sequence_similarity_score = compute_similarity(normalized_ref_query, normalized_out_query)
                    bleu_similarity_score = calculate_similarity_bleu(normalized_ref_query, normalized_out_query)

                    execution_accuracy = compare_results(ref_rows, out_rows)

                    execution_log.append({
                        "question": question,
                        "reference_query": ref_query,
                        "normalized_reference_query": normalized_ref_query,
                        "reference_sample_result": ref_sample_rows,
                        "reference_column_names": ref_column_names,
                        "reference_row_count": ref_row_count,
                        "reference_column_count": ref_column_count,
                        "output_query": out_query,
                        "normalized_output_query": normalized_out_query,
                        "output_sample_result": out_sample_rows,
                        "output_column_names": out_column_names,
                        "output_row_count": out_row_count,
                        "output_column_count": out_column_count,
                        "sequence_similarity_score": sequence_similarity_score,
                        "bleu_similarity_score": bleu_similarity_score,
                        "execution_accuracy": execution_accuracy
                    })
                else:
                    execution_log.append({
                        "question": question,
                        "reference_query": ref_query,
                        "normalized_reference_query": normalized_ref_query,
                        "reference_error": ref_result if isinstance(ref_result, str) else None,
                        "output_query": out_query,
                        "normalized_output_query": normalized_out_query,
                        "output_error": out_result if isinstance(out_result, str) else None,
                        "sequence_similarity_score": None,
                        "bleu_similarity_score": None,
                        "execution_accuracy": False
                    })
            else:
                print(f"Invalid query structure for question: {question}, skipping...")
        else:
            print(f"No matching output query found for question: {question}, skipping...")

    with open(log_file, "w", encoding="utf-8") as log_file:
        json.dump(execution_log, log_file, indent=4, default=datetime_converter)

    print(f"Execution log saved to {log_file}")

def main():
    postgres_connection_details = {
        "user": "postgres",
        "password": "123456789",
        "host": "localhost",
        "port": "5432",
    }

    reference_file_path = "VizExplorer_FINAL/data/BIRD_dataset/raw_data/converted_ground_truth.json"
    output_file_path = "model_output/bird_model_output.json"
    log_file_path = "performance_measure/query_execution_comparison_log.json"

    process_queries(reference_file_path, output_file_path, postgres_connection_details, log_file_path)

if __name__ == "__main__":
    main()
