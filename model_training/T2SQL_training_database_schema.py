import vanna
from vanna.remote import VannaDefault

dbname = "swiss_private_bank"
user = "postgres"
password = "123456789"
host = "localhost"
port = 5432

api_key = 'be920fe18e6c4a3fa6bf9436d6113657'
vanna_model_name = 'vizexplorer'
vn = VannaDefault(model=vanna_model_name, api_key=api_key)

# Connect to PostgreSQL
vn.connect_to_postgres(
    host = host,
    dbname = dbname,
    user = user,
    password = password,
    port = port
)
print("Connected to PostgreSQL database.")

ddl_statements = [
    """
    CREATE TABLE accounts_data (
    account_id VARCHAR(7) NOT NULL,
    client_id INT NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    balance NUMERIC(15,2) DEFAULT 0.00,
    creation_date DATE NOT NULL,
    currency VARCHAR(3) DEFAULT 'CHF',
    PRIMARY KEY (account_id),
    FOREIGN KEY (client_id)
        REFERENCES clients_data (client_id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE clients_data (
    client_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    address TEXT,
    phone VARCHAR(50),
    nationality VARCHAR(50),
    date_of_birth DATE
    );
    """,
    """
    CREATE TABLE etfs_historical (
    ticker VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(15,2),
    high NUMERIC(15,2),
    low NUMERIC(15,2),
    close NUMERIC(15,2),
    volume BIGINT,
    PRIMARY KEY (ticker, date)
    );
    """,
    """
    CREATE TABLE holdings_data (
    holding_id VARCHAR(10) NOT NULL,
    portfolio_id VARCHAR(10) NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    quantity NUMERIC(15,2) NOT NULL,
    purchase_price NUMERIC(15,2),
    current_value NUMERIC(15,2),
    PRIMARY KEY (holding_id),
    FOREIGN KEY (portfolio_id)
        REFERENCES portfolios_data (portfolio_id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE market_news (
    ticker VARCHAR(10),
    headline TEXT,
    source VARCHAR(100),
    publish_date TIMESTAMP,
    url TEXT,
    language VARCHAR(2)
    );
    """,
    """
    CREATE TABLE portfolios_data (
    portfolio_id VARCHAR(10) NOT NULL,
    client_id INT NOT NULL,
    portfolio_name VARCHAR(100),
    total_value NUMERIC(15,2),
    currency VARCHAR(3),
    creation_date DATE NOT NULL,
    PRIMARY KEY (portfolio_id),
    FOREIGN KEY (client_id)
        REFERENCES clients_data (client_id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE stocks_data (
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(12,2),
    high NUMERIC(12,2),
    low NUMERIC(12,2),
    close NUMERIC(12,2),
    volume BIGINT,
    PRIMARY KEY (ticker, date)
    );
    """,
    """
    CREATE TABLE transactions_data (
    transaction_id VARCHAR(8) NOT NULL,
    client_id INT NOT NULL,
    account_id VARCHAR(7) NOT NULL,
    transaction_date TIMESTAMP DEFAULT now() NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    amount NUMERIC(15,2) NOT NULL,
    stock_ticker VARCHAR(10),
    currency VARCHAR(3) NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (account_id)
        REFERENCES accounts_data (account_id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    FOREIGN KEY (client_id)
        REFERENCES clients_data (client_id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
    );
    """
]

# # Train the Vanna model using the DDL statements
# for ddl in ddl_statements:
#     try:
#         vn.train(ddl=ddl)
#         print(f"Trained on DDL: {ddl[:50]}...")  # Print first 50 characters of DDL for confirmation
#     except Exception as e:
#         print(f"Failed to train on DDL: {e}")
# doc = 
# vn.train(documentation=)

file_path = 'documentation.txt'

with open(file_path, 'r') as file:
    file_content = ''
    line = file.readline()
    
    while line:
        file_content += line
        line = file.readline()

vn.train(documentation=file_content)