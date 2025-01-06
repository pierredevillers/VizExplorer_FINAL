from psycopg2 import sql
import vanna
from vanna.remote import VannaDefault
import logging
import psycopg2

# Configure logging
logging.basicConfig(
    filename='training_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# PostgreSQL connection details
postgres_connection_details = {
    'user': 'postgres',
    'password': '123456789',
    'host': 'localhost',
    'port': 5432
}

def prompt_user_confirmation():
    """
    Prompt the user to confirm whether to proceed with training.
    """
    while True:
        user_input = input("Do you want to proceed with training the Vanna model? (Y/N): ").strip().upper()
        if user_input in ["Y", "N"]:
            return user_input == "Y"
        print("Invalid input. Please enter 'Y' or 'N'.")

def connect_to_postgres(db_name):
    """
    Connect to a specific PostgreSQL database.
    """
    connection_details = postgres_connection_details.copy()
    connection_details['dbname'] = db_name
    return psycopg2.connect(**connection_details)

def get_all_databases():
    """
    Retrieve all databases excluding specific ones.
    """
    conn = connect_to_postgres('postgres')
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT datname 
                FROM pg_database 
                WHERE datistemplate = false 
                  AND datname NOT IN ('postgres', 'swiss_private_bank');
            """)
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Error fetching databases: {e}")
        return []
    finally:
        conn.close()

def extract_ddl_statements(db_name):
    """
    Extract DDL statements for all tables in a PostgreSQL database.
    """
    conn = connect_to_postgres(db_name)
    ddl_statements = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_schema = 'public' 
                  AND table_type = 'BASE TABLE';
            """)
            tables = cursor.fetchall()

            for schema, table in tables:
                cursor.execute(
                    f"SELECT dbms_metadata.get_ddl('TABLE', '{table}', '{schema}');"
                )
                ddl = cursor.fetchone()[0]
                ddl_statements.append((table, ddl))
                logging.info(f"Extracted DDL for table: {table}")
    except Exception as e:
        logging.error(f"Error extracting DDL from database '{db_name}': {e}")
    finally:
        conn.close()
    return ddl_statements

def normalize_ddl(ddl):
    """
    Normalize DDL to ensure consistency in training data.
    """
    ddl = ddl.replace('character varying', 'VARCHAR')
    ddl = ddl.replace('integer', 'INT')
    ddl = ddl.replace('real', 'REAL')
    ddl = ddl.replace('double precision', 'DOUBLE PRECISION')
    ddl = ddl.replace('serial', 'SERIAL')
    return ddl

def validate_all_databases(databases):
    """
    Validate all DDL statements for all databases and display them for user review.
    """
    all_valid = True
    for db_name in databases:
        print(f"\n--- Validating DDL Statements for Database: {db_name} ---")
        ddl_statements = extract_ddl_statements(db_name)
        for table_name, ddl in ddl_statements:
            normalized_ddl = normalize_ddl(ddl)
            print(f"\nTable: {table_name}\n{normalized_ddl}")

            # Check if the normalized DDL meets expected standards
            if not normalized_ddl.strip():
                logging.error(f"Invalid DDL for table: {table_name} in database: {db_name}")
                all_valid = False
    return all_valid

def train_vanna_on_ddl(vn, databases):
    """
    Train Vanna.AI on the DDL statements of a PostgreSQL database.
    """
    for db_name in databases:
        ddl_statements = extract_ddl_statements(db_name)
        for table_name, ddl in ddl_statements:
            normalized_ddl = normalize_ddl(ddl)
            try:
                vn.train(ddl=f"""
{normalized_ddl}
""")
                logging.info(f"Trained Vanna on table: {table_name}")
            except Exception as e:
                logging.error(f"Failed to train Vanna on table '{table_name}': {e}")

def main():
    """
    Main function to verify DDL and train the Vanna model.
    """
    # Step 1: Get all databases to process
    databases = get_all_databases()

    # Step 2: Validate All Databases
    all_valid = validate_all_databases(databases)

    if not all_valid:
        print("Validation failed for one or more databases. Fix the errors and retry.")
        return

    # Step 3: Ask for User Confirmation
    if prompt_user_confirmation():
        # Step 4: Initialize Vanna model
        vn = VannaDefault(model="bird_explorer", api_key="be920fe18e6c4a3fa6bf9436d6113657")

        # Step 5: Train Vanna.AI on DDL Statements
        train_vanna_on_ddl(vn, databases)
        print("Training completed successfully.")
    else:
        print("Training canceled by the user.")

if __name__ == "__main__":
    main()
