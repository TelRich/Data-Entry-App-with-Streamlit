import streamlit as st
import pandas as pd


# username = 'test'
# password = st.secrets['pw']
# host = 'telrichserver.postgres.database.azure.com'
# database = 'newdb'

# conn_str = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'



from sqlalchemy import create_engine

# Set up a connection string
username = 'test'
password = '1234'
host = 'telrichserver.postgres.database.azure.com'
port = '5432'
database = 'newdb'
conn_str = f'postgresql://{username}:{password}@{host}:{port}/{database}'

# Create a connection engine
engine = create_engine(conn_str)

# Execute a SQL query
query = 'SELECT * FROM bus_breakdown_delay LIMIT 5'
df = pd.read_sql_query(query, engine)
st.write(df)