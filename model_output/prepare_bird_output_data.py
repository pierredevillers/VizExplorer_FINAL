import json

# File paths
INPUT_FILE = "VizExplorer_FINAL/model_training_and_perf/bird_model_output.json"
OUTPUT_FILE = "VizExplorer_FINAL/model_training_and_perf/bird_model_output_formatted.json"

def reformat_bird_output(input_file, output_file):

    try:
        # Read the original bird_model_output.json file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Initialize the reformatted output dictionary
        formatted_data = {}

        # Reformat each entry in the input data
        for idx, entry in enumerate(data):
            # Extract the SQL query and db_id
            sql_query = entry.get("SQL", "").strip()
            db_id = entry.get("db_id", "").strip()
            
            # Skip entries with missing SQL or db_id
            if not sql_query or not db_id:
                continue

            # Combine SQL query and db_id with the required delimiter
            formatted_entry = f"{sql_query}\t----- bird -----\t{db_id}"
            formatted_data[str(idx)] = formatted_entry

        # Write the formatted data to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=4, ensure_ascii=False)
        
        print(f"Reformatted data successfully written to {output_file}")
    except Exception as e:
        print(f"Error during reformatting: {e}")

if __name__ == "__main__":
    reformat_bird_output(INPUT_FILE, OUTPUT_FILE)
