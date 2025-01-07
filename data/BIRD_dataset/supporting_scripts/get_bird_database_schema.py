import psycopg2

def get_all_databases(user, password, host, port):
    """Retrieve a list of all databases excluding system ones and specific exclusions."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",  
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT datname 
            FROM pg_database 
            WHERE datistemplate = false 
              AND datname NOT IN ('postgres', 'swiss_private_bank');
        """)
        databases = [row[0] for row in cursor.fetchall()]
        return databases
    except Exception as e:
        print(f"Error fetching databases: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def extract_ddls_for_tables(db_name, user, password, host, port):
    """Extract DDLs for all tables in a database."""
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()

        # Fetch all tables in the database
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
              AND table_schema NOT IN ('pg_catalog', 'information_schema');
        """)
        tables = cursor.fetchall()

        ddl_statements = []
        for schema, table in tables:
            cursor.execute(
                f"SELECT dbms_metadata.get_ddl('TABLE', '{table}', '{schema}');"
            )
            ddl = cursor.fetchone()[0]
            ddl_statements.append(ddl)

        return ddl_statements

    except Exception as e:
        print(f"Error in database {db_name}: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def extract_all_ddls(user, password, host, port):
    """Extract DDLs for all databases except excluded ones."""
    databases = get_all_databases(user, password, host, port)
    all_ddls = []

    for db in databases:
        print(f"Extracting DDLs from database: {db}")
        ddls = extract_ddls_for_tables(db, user, password, host, port)
        all_ddls.extend(ddls)

    return all_ddls

# Usage
dbname = "swiss_private_bank"
user = "swiss_private_bank_owner"
password = "p3g7qazZiGle"
host = "ep-snowy-tooth-a27ji8ct.eu-central-1.aws.neon.tech"
port = 5432

ddl_statements = extract_all_ddls(user, password, host, port)

with open("ddl_statements.txt", "w") as file:
    for ddl in ddl_statements:
        file.write(ddl + "\n\n")

print("All DDLs have been saved to 'ddl_statements.txt'.")
