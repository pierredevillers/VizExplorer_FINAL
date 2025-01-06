import os
import logging
import streamlit as st
import pandas as pd
import numpy as np
from vanna.remote import VannaDefault
import vanna
import re
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# Streamlit configuration for Replit compatibility
os.environ["STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
os.environ["STREAMLIT_SERVER_PORT"] = "8501"

# Streamlit configuration
st.set_page_config(
    page_title="VizExplorer V-NLI",
    page_icon="https://www.shareicon.net/data/128x128/2016/08/18/810361_multimedia_512x512.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Sidebar Configuration
st.sidebar.title("Settings")
show_sql = st.sidebar.checkbox("Show SQL", value=True)
show_table = st.sidebar.checkbox("Show Table", value=True)
show_chart = st.sidebar.checkbox("Show Chart", value=True)
st.title("VizExplorer V-NLI")
st.markdown(    
    """
    Welcome to VizExplorer, a Virtual Natural Language Interface (V-NLI). 
    This tool allows users to query our database in natural language 
    and retrieve dynamic results, including tables and visualizations.
    """)

avatar_url = "https://www.shareicon.net/data/128x128/2016/08/18/810361_multimedia_512x512.png"

# Add Session History
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "query_active" not in st.session_state:
    st.session_state.query_active = False

@st.cache_resource(ttl=3600)

def setup_vanna():
    api_key = 'be920fe18e6c4a3fa6bf9436d6113657'
    vanna_model_name = 'vizexplorer'
    vn = VannaDefault(model=vanna_model_name, api_key=api_key)
    dbname = "swiss_private_bank"
    user = "swiss_private_bank_owner"
    password = "p3g7qazZiGle"
    host = "ep-snowy-tooth-a27ji8ct.eu-central-1.aws.neon.tech"
    port = 5432

    # Connect tool to PostgreSQL
    try:
        vn.connect_to_postgres(
            host = host,
            dbname = dbname,
            user = user,
            password = password,
            port = port
        )
        print("Tool successfully connected to PostgreSQL.")
        
    except Exception as e:
        print(f"Failed to connect tool to PostgreSQL: {e}")
    return vn

@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)

@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)

@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str):
    vn = setup_vanna()
    return vn.run_sql(sql=sql)

@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)

@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)

@st.cache_data
def get_table_schema(table_name):
    sql = f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = '{table_name}';
    """
    result = run_sql_cached(sql)
    if result is not None and not result.empty:
        return result
    return None

def extract_table_names(sql_query):
    # Regex to match table names in FROM and JOIN clauses
    table_pattern = r'(?i)(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    matches = re.findall(table_pattern, sql_query)
    return set(matches)

# Dashboard Widgets
st.sidebar.subheader("Output Sample")
total_rows = st.sidebar.number_input("Total Rows to Display", min_value=1, max_value=100, value=10)

# Input Section
user_query = st.text_input("Enter your query in natural language:", "")

if user_query:
    st.session_state.query_active = True
    st.session_state.query_history.append(user_query)

if st.session_state.query_active:
    user_message = st.chat_message("user")
    user_message.write(f"{user_query}")

    sql = generate_sql_cached(question=user_query)
    st.session_state["sql_query"] = sql
    
    if sql:
        if is_sql_valid_cached(sql=sql):
            if show_sql:
                assistant_message_sql = st.chat_message(
                    "assistant", avatar=avatar_url
                )
                assistant_message_sql.code(sql, language="sql", line_numbers=True)
        else:
            assistant_message = st.chat_message(
            "assistant", avatar=avatar_url
            )
            assistant_message.write(sql)
            st.stop()

        df = run_sql_cached(sql=sql)

        if df is not None:
            st.session_state["df"] = df

        if st.session_state.get("df") is not None:
            if show_table:
                df = st.session_state.get("df")
                assistant_message_table = st.chat_message(
                    "assistant",
                    avatar=avatar_url,
                )
                if len(df) > total_rows:
                    assistant_message_table.text(f"First {total_rows} rows of data")
                    assistant_message_table.dataframe(df.head(total_rows))
                else:
                    assistant_message_table.dataframe(df)

            if should_generate_chart_cached(question=user_query, sql=sql, df=df):

                code = generate_plotly_code_cached(question=user_query, sql=sql, df=df)

                if st.session_state.get("show_plotly_code", False):
                    assistant_message_plotly_code = st.chat_message(
                        "assistant",
                        avatar=avatar_url,
                    )
                    assistant_message_plotly_code.code(
                        code, language="python", line_numbers=True
                    )

                if code is not None and code != "":
                    if show_chart:
                        assistant_message_chart = st.chat_message(
                            "assistant",
                            avatar=avatar_url,
                        )
                        fig = generate_plot_cached(code=code, df=df)
                    if fig is not None:
                        assistant_message_chart.plotly_chart(fig)
                    else:
                        assistant_message_chart.error("I couldn't generate a chart")
                else:
                    st.warning("No relevant chart produced.")
                    
# Display Used Tables and Columns
if st.session_state.get("query_active") and st.session_state.get("sql_query"):
    st.subheader("Tables and Columns Used in the Query")
    tables = extract_table_names(st.session_state.get("sql_query", ""))

    for table in tables:
        st.markdown(f"### Table: `{table}`")
        schema = get_table_schema(table)

# Export Functionality
if st.session_state.get("df") is not None:
    st.sidebar.subheader("Export Data")
    csv = st.session_state.get("df").to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download CSV", csv, "data.csv", "text/csv", key="download-csv")

# Sidebar: Query History
st.sidebar.subheader("Query History")
if st.session_state.query_history:
    unique_queries = list(dict.fromkeys(st.session_state.query_history)) 
    for query in unique_queries:
        st.sidebar.write(query)