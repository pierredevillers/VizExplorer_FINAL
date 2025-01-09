import json
import sqlparse 

# File paths
reference_file_path = 'data/BIRD_dataset/raw_data/converted_ground_truth.json'
generated_file_path = 'model_output/bird_model_output.json'
output_file_path = 'performance_measure/cleaned_sql_queries.json'

# Load data
with open(reference_file_path, 'r') as ref_file:
    reference_data = json.load(ref_file)

with open(generated_file_path, 'r') as gen_file:
    generated_data = json.load(gen_file)

# Normalize SQL
def normalize_sql(query):
    return sqlparse.format(query, reindent=True, keyword_case='upper')

reference_lookup = {entry['question']: entry for entry in reference_data}

# Build the clean JSON structure with db_id validation
cleaned_data = []
for gen in generated_data:
    question = gen['question']
    if question in reference_lookup:  # Match questions
        ref = reference_lookup[question]
        db_id = ref.get("db_id")
        if not db_id:
            print(f"Warning: Missing db_id for question: {question}. Skipping...")
            continue

        cleaned_data.append({
            "question": question,
            "reference_sql_query": {
                "raw": ref["SQL"],
                "normalized": normalize_sql(ref["SQL"])
            },
            "generated_sql_query": {
                "raw": gen["SQL"],
                "normalized": normalize_sql(gen["SQL"])
            },
            "db_id": db_id
        })
    else:
        print(f"Warning: No match found for question: {question}. Skipping...")

# Save the cleaned data
with open(output_file_path, 'w') as outfile:
    json.dump(cleaned_data, outfile, indent=4)

print(f"Cleaned JSON file has been saved to {output_file_path}")
