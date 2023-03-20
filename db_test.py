import psycopg2
import streamlit as st
import pandas as pd
import plotly.express as px


st. set_page_config(layout="wide")

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
cur = conn.cursor()

col1, col2 = st.columns([2, 8], gap='large')

with col1:
    st.subheader('Sales Entry')

    phone_brand = st.text_input('Enter brand name')
    phone_model = st.text_input('Enter phone model')
    purchase_date = st.date_input('Enter purchase date')
    sold_date = st.date_input('Enter sold date')
    sold_price = st.number_input('Enter sold price')
    cost_price = st.number_input('Enter cost price')

    if st.button('Save Details'):
        query = f'''INSERT INTO phone_sales (phone_brand, phone_model, purchase_date, sold_date, sold_price, cost_price)
        VALUES ('{phone_brand}', '{phone_model}', '{purchase_date}', '{sold_date}', '{sold_price}', '{cost_price}')'''
        cur.execute(query)
        conn.commit()

# Execute a SQL query and fetch the results
query = 'SELECT * FROM phone_sales ORDER BY id DESC LIMIT 3'

# cur.execute(query)
# results = cur.fetchall()

# Create a pandas DataFrame from the results and display it on Streamlit
# df = pd.DataFrame(results)
df2 = pd.read_sql_query(query, conn)

query3 = 'SELECT phone_brand,SUM(profit) profit, SUM(cost_price) cost_price, SUM(sold_price) sold_price FROM phone_sales GROUP BY phone_brand'
df3 = pd.read_sql_query(query3, conn)
fig1 = px.bar(df3, 'phone_brand', 'profit')
fig2 = px.bar(df3, 'phone_brand', ['cost_price', 'sold_price'], barmode='group')

with col2:
    st.header('Table From Remote Database (Last three entry)')
    # st.write(df)
    st.table(df2)
    col21, col22 = st.columns(2)
    with col21:
        st.plotly_chart(fig1)
    with col22:
        st.plotly_chart(fig2)



# Close the database connection
cur.close()
conn.close()
