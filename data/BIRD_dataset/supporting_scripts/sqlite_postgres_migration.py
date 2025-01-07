import sqlite3
import psycopg2
from psycopg2 import sql

# Configuration
sqlite_file_path = r'C:\Users\Pierre Devillers\Desktop\VizExplorer_FINAL\BIRD_V0\dev\dev_databases\formula_1\formula_1.sqlite'  # Path to SQLite file
postgres_connection_details = {
    'dbname': 'formula_1',  # Target PostgreSQL database
    'user': 'postgres',
    'password': '123456789',
    'host': 'localhost',
    'port': 5432
}

def migrate_trans_table(sqlite_file, postgres_details):
    """
    Migrate the 'lapTimes' table from SQLite to PostgreSQL.

    Args:
        sqlite_file (str): Path to the SQLite file.
        postgres_details (dict): PostgreSQL connection details.
    """
    # Connect to SQLite
    sqlite_conn = sqlite3.connect(sqlite_file)
    sqlite_cursor = sqlite_conn.cursor()

    # Connect to PostgreSQL
    postgres_conn = psycopg2.connect(**postgres_details)
    postgres_cursor = postgres_conn.cursor()

    try:
        # Create the 'trans' table in PostgreSQL
        create_table_query = """
        CREATE TABLE IF NOT EXISTS trans (
            trans_id SERIAL PRIMARY KEY,
            account_id INT NOT NULL,
            date DATE NOT NULL,
            type VARCHAR(50) NOT NULL,
            operation VARCHAR(100),
            amount INT NOT NULL,
            balance INT NOT NULL,
            k_symbol VARCHAR(100),
            bank VARCHAR(100),
            account BIGINT
        );
        """
        postgres_cursor.execute(create_table_query)
        postgres_conn.commit()
        print("Table 'trans' created in PostgreSQL.")

        # Fetch data from SQLite
        sqlite_cursor.execute("SELECT * FROM trans;")
        rows = sqlite_cursor.fetchall()

        # Insert data into PostgreSQL
        insert_query = """
        INSERT INTO trans (trans_id, account_id, date, type, operation, amount, balance, k_symbol, bank, account)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for row in rows:
            postgres_cursor.execute(insert_query, row)

        postgres_conn.commit()
        print("Data migrated successfully into 'trans' table.")

    except Exception as e:
        print(f"Error during migration: {e}")

    finally:
        # Close connections
        sqlite_conn.close()
        postgres_cursor.close()
        postgres_conn.close()

# Run the migration
migrate_trans_table(sqlite_file_path, postgres_connection_details)
