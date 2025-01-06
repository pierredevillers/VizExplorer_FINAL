import vanna
from vanna.remote import VannaDefault
import json
import logging

# Configure logging
logging.basicConfig(
    filename='evaluation_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# T2SQL model details
MODEL_NAME = "bird_explorer"
API_KEY = "be920fe18e6c4a3fa6bf9436d6113657"

# Paths for output
OUTPUT_FILE = "bird_model_output.json"
GROUND_TRUTH_PATH = r"C:/Users/Pierre Devillers/Desktop/VizExplorer_FINAL/converted_ground_truth.json"

# Maximum number of queries per database
MAX_QUERIES_PER_DB = 50

def setup_vanna():
    """
    Initialize the Vanna model.
    """
    try:
        vn = VannaDefault(model=MODEL_NAME, api_key=API_KEY)
        logging.info("Vanna model initialized successfully.")
        print("Vanna model initialized successfully.")
        return vn
    except Exception as e:
        logging.error(f"Failed to initialize Vanna model: {e}")
        print(f"Failed to initialize Vanna model: {e}")
        raise

def generate_single_sql_query(vn, prompt):
    """
    Generate a single SQL query for a given prompt using the Vanna model.
£
    Args:
        vn (VannaDefault): Initialized Vanna model instance.
        prompt (dict): A single natural language question with db_id.

    Returns:
        dict or None: The formatted output containing the question, SQL query, and db_id.
    """
    try:
        response = vn.generate_sql(question=prompt["question"], allow_llm_to_see_data=True)
        logging.info(f"Raw response for prompt '{prompt['question']}': {response}")
        print(f"Raw Response for '{prompt['question']}': {response}")

        if response.strip():
            return {
                "question": prompt["question"],
                "SQL": response.strip(),
                "db_id": prompt["db_id"]
            }
        else:
            logging.warning(f"Empty SQL query generated for prompt: {prompt['question']}")
            print(f"Warning: Empty SQL query for '{prompt['question']}'")
            return None

    except Exception as e:
        logging.error(f"Error generating SQL for prompt '{prompt['question']}': {e}")
        print(f"Error generating SQL for '{prompt['question']}': {e}")
        return None

def main():
    """
    Main function to generate SQL for multiple prompts while limiting queries per database.
    """
    try:
        # Initialize model
        vn = setup_vanna()

        # Load prompts from reference JSON
        with open(GROUND_TRUTH_PATH, 'r', encoding='utf-8') as f:
            prompts = json.load(f)

        if not prompts:
            logging.error("No prompts found in the reference JSON file.")
            print("No prompts available to process.")
            return

        # Track query counts per database
        query_counts = {}
        generated_queries = []

        print("Starting SQL generation...")
        for i, prompt in enumerate(prompts, start=1):
            db_id = prompt["db_id"]

            # Initialize count for the database if not already present
            if db_id not in query_counts:
                query_counts[db_id] = 0

            # Pre-check to skip prompt if the limit for this db_id is reached
            if query_counts[db_id] >= MAX_QUERIES_PER_DB:
                logging.info(f"Skipping prompt for db_id '{db_id}' as it reached the maximum query limit.")
                print(f"Skipping '{prompt['question']}' for db_id '{db_id}' - Limit reached.")
                continue

            # Generate SQL for the prompt
            output = generate_single_sql_query(vn, prompt)

            # Add the result if valid
            if output:
                generated_queries.append(output)
                query_counts[db_id] += 1
                print(f"Generated query {i}: {output['SQL']} for db_id '{db_id}'")
            else:
                print(f"Failed to generate query for prompt {i}: '{prompt['question']}'")

        # Save all generated queries to the output JSON file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(generated_queries, f, indent=4, ensure_ascii=False)
        logging.info(f"All outputs successfully written to {OUTPUT_FILE}")
        print(f"SQL queries generated and saved successfully. Processed queries per db_id: {query_counts}")

    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
