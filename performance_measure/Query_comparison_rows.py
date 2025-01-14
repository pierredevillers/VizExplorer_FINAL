import json
import psycopg2
import plotly.graph_objects as go

# Load the JSON file containing the queries
input_file_path = "performance_measure/cleaned_sql_queries.json"
with open(input_file_path, 'r') as infile:
    queries = json.load(infile)

# Database credentials
db_credentials = {
    "user": "postgres",
    "password": "123456789",
    "host": "localhost",
    "port": "5432"
}

# Initialize metrics and categories
metrics = {
    "valid_queries_reference": 0,
    "non_valid_reference_queries_count": 0,
    "valid_generated_queries": 0,
    "invalid_generated_queries": 0,
    "non_sql_responses_count": 0
}

categories = {"Below": 0, "Equal": 0, "Above": 0, "Error": 0, "Null Outputs": 0}

# Function to check if a query is valid SQL
def is_valid_sql(query):
    sql_keywords = {"SELECT", "FROM", "WHERE", "JOIN", "GROUP", "ORDER", "INSERT", "UPDATE", "DELETE"}
    return any(keyword in query.upper() for keyword in sql_keywords)

# Connect to the database
def connect_to_db(db_id):
    try:
        conn = psycopg2.connect(dbname=db_id, **db_credentials)
        return conn
    except Exception as e:
        print(f"Error connecting to database {db_id}: {e}")
        return None

# Execute a query and fetch row count
def execute_query_and_get_row_count(conn, sql):
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            return len(rows)
    except Exception as e:
        print(f"Query execution error: {e}")
        return None

# Process and compare query result sizes
for idx, query_pair in enumerate(queries):
    reference_query = query_pair["reference_sql_query"]["raw"]
    model_query = query_pair["generated_sql_query"]["raw"]
    db_id = query_pair["db_id"]

    # Validate reference query
    if not is_valid_sql(reference_query):
        metrics["non_sql_responses_count"] += 1
        continue

    # Validate model query
    if not is_valid_sql(model_query):
        metrics["non_sql_responses_count"] += 1
        continue

    # Connect to the database
    conn = connect_to_db(db_id)
    if not conn:
        metrics["non_valid_reference_queries_count"] += 1
        categories["Error"] += 1
        continue

    # Execute reference query
    reference_row_count = execute_query_and_get_row_count(conn, reference_query)
    if reference_row_count is None:
        metrics["non_valid_reference_queries_count"] += 1
        categories["Error"] += 1
    else:
        metrics["valid_queries_reference"] += 1

    # Execute model query
    model_row_count = execute_query_and_get_row_count(conn, model_query)
    if model_row_count is None:
        metrics["invalid_generated_queries"] += 1
        categories["Error"] += 1
    elif model_row_count == 0:
        categories["Null Outputs"] += 1
    else:
        metrics["valid_generated_queries"] += 1
        if model_row_count < reference_row_count:
            categories["Below"] += 1
        elif model_row_count == reference_row_count:
            categories["Equal"] += 1
        else:
            categories["Above"] += 1

    conn.close()

# Print metrics
print("\nMetrics:")
print(metrics)

# Create a bar chart with Plotly
fig = go.Figure(
    data=[
        go.Bar(
            x=list(categories.keys()),
            y=list(categories.values()),
            marker_color=['blue', 'green', 'orange', 'red', 'purple']
        )
    ]
)

# Update layout
fig.update_layout(
    title="Result Size Comparison of Queries",
    xaxis_title="Comparison Category",
    yaxis_title="Number of Queries",
    template="plotly_white"
)

# Show the plot
fig.show()
