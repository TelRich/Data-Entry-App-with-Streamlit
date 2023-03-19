import streamlit as st
import pandas as pd


# username = 'test'
# password = st.secrets['pw']
# host = 'telrichserver.postgres.database.azure.com'
# database = 'newdb'

# conn_str = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'



from sqlalchemy import create_engine

# Set up a connection string
username = st.secrets['user']
password = st.secrets['pw']
host = 'telrichserver.postgres.database.azure.com'
# port = 'your_port'
database = 'newdb'
conn_str = f'postgresql://{username}:{password}@{host}/{database}'

# Create a connection engine
engine = create_engine(conn_str)

# Execute a SQL query
query = 'SELECT * FROM bus_breakdown_delay LIMIT 5'
df = pd.read_sql_query(query, engine)
st.write(df)