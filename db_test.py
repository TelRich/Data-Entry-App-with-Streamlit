# import streamlit as st
# import pandas as pd


# # username = 'test'
# # password = st.secrets['pw']
# # host = 'telrichserver.postgres.database.azure.com'
# # database = 'newdb'

# # conn_str = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'



# from sqlalchemy import create_engine

# # Set up a connection string
# username = 'test'
# password = '1234'
# host = 'telrichserver.postgres.database.azure.com'
# port = '5432'
# database = 'newdb'
# conn_str = f'postgresql://{username}:{password}@{host}:{port}/{database}'

# # Create a connection engine
# engine = create_engine(conn_str)

# # Execute a SQL query
# query = 'SELECT * FROM bus_breakdown_delay LIMIT 5'
# df = pd.read_sql_query(query, engine)
# st.write(df)

import psycopg2
import streamlit as st
import pandas as pd

# Set up a connection string
username = st.secrets['user']
password = st.secrets['pw']
host = 'telrichserver.postgres.database.azure.com'
database = 'phone_db'
port = '5432'  # or your specified port number
sslmode = 'require'  # or 'prefer' if you don't want to use SSL encryption
conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"

# Connect to the database
conn = psycopg2.connect(conn_str)

# Execute a SQL query and fetch the results
query = 'SELECT * FROM phone_sales'
cur = conn.cursor()
cur.execute(query)
results = cur.fetchall()

# Create a pandas DataFrame from the results and display it on Streamlit
df = pd.DataFrame(results)
st.header('Table From My Remote Database on Streamlit')
st.write(df)

# Close the database connection
cur.close()
conn.close()
