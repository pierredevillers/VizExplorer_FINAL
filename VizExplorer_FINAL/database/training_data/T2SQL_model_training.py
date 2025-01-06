import vanna
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
def load_training_data(file_path):
    """
    Loads training data from the JSON file.

    Args:
        file_path (str): Path to the JSON file containing training data.
    
    Returns:
        list: List of dictionaries with 'question', 'query', and other metadata.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
                training_data = json.load(f)
        print(f"Successfully loaded {len(training_data)} training pairs: {training_data[:5]}")
        return training_data
    except Exception as e:
        print(f"Error loading training data: {e}")
        return []


def train_vanna_model(vanna, training_data):
    """
    Train the Vanna model using the provided training data.

    Args:
        vanna (MyVanna): Vanna instance.
        training_data (list): List of dictionaries containing training pairs.
    """
    for entry in training_data:
        question = entry.get("question")
        sql_query = entry.get("query")

        # Train the Vanna model on each question-SQL pair
        try:
            vanna.train(question=question, sql=sql_query)
            print(f"Trained on question: {question}")
        except Exception as e:
            print(f"Failed to train on question '{question}': {e}")

# Path to the JSON file with training data
training_file_path = "VizExplorer_CURRENT/database/training_data/training_queries.json"

# Load training data
training_data = load_training_data(training_file_path)

if training_data:
    train_vanna_model(vn, training_data)
else:
    print("No training data available for training.")