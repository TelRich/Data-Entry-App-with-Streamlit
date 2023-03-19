import streamlit as st
import pandas as pd


username = st.secrets('user')
password = st.secrets('pw')
host = 'telrichserver.postgres.database.azure.com'
database = 'newdb'

conn_str = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'

df = pd.read_sql_query("select * from bus_breakdown_delay limit 5", conn_str)
st.write(df)