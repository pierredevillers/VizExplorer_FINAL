import sqlparse
import psycopg2
import json


def normalize_sql(query):

    formatted_query = sqlparse.format(query, reindent=True, keyword_case='upper')
    compact_query = sqlparse.format(formatted_query, strip_whitespace=True)
    return compact_query


def execute_query(query, db_id, db_credentials):

    try:
        conn = psycopg2.connect(
            dbname=db_id,
            user=db_credentials["user"],
            password=db_credentials["password"],
            host=db_credentials["host"],
            port=db_credentials["port"]
        )
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        conn.close()
        return result
    except Exception as e:
        
        return str(e)  # Return error as string for failed queries


def get_valid_questions(bird_model_output_path):

    with open(bird_model_output_path, 'r', encoding='utf-8') as file:
        bird_model_data = json.load(file)
    return {item["question"] for item in bird_model_data if "question" in item}


def process_json_queries(json_file_path, bird_model_output_path, db_credentials):

    # Load valid questions
    valid_questions = get_valid_questions(bird_model_output_path)
    print(f"Valid questions loaded: {len(valid_questions)}")

    # Load SQL queries from the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for idx, item in enumerate(data):
        question = item.get("question")
        query = item.get("SQL")
        db_id = item.get("db_id")

        if question in valid_questions:
            print(f"Processing query {idx + 1}/{len(data)} for question: {question}")

            if query and db_id:
                # Normalize the query
                normalized_query = normalize_sql(query)
                print(f"Normalized Query: {normalized_query}")

                # Execute the query
                result = execute_query(normalized_query, db_id, db_credentials)

                # Check for errors
                if isinstance(result, str):  # If result is an error message
                    print(f"Error encountered: {result}")
                    print(f"Stopping execution at query {idx + 1}/{len(data)}.")
                    return  # Stop processing further queries
                else:
                    print(f"Query result: {result}\n")
            else:
                print(f"Missing SQL or db_id in entry {idx + 1}, skipping...\n")
        else:
            print(f"Skipping query {idx + 1}/{len(data)}: Question not in valid set.")

    print("All matching queries processed successfully.")


def main():
    # File paths
    json_file_path = "data/BIRD_dataset/raw_data/converted_ground_truth.json"  
    bird_model_output_path = "model_output/bird_model_output.json" 

    # Database credentials
    db_credentials = {
        "user": "postgres",
        "password": "123456789",
        "host": "localhost",
        "port": "5432"  
    }

    # Process queries
    process_json_queries(json_file_path, bird_model_output_path, db_credentials)


if __name__ == "__main__":
    main()
