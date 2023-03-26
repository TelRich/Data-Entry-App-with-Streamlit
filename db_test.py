# Importing requires libraries
import psycopg2
import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# setting the page size
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

# Split the page into two column
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

row_count = '''
SELECT 
    COUNT(*) table_rows
FROM
    phone_sales
'''
table_rw = pd.read_sql_query(row_count, conn)
rw_num= table_rw['table_rows'][0]
col1.write(f'There are now {rw_num} rows in the table')

if rw_num == 20:
    query = """
    DELETE FROM phone_sales
    WHERE id <=5  
    """
    cur.execute(query)
    conn.commit()

query = 'SELECT * FROM phone_sales ORDER BY id DESC LIMIT 3'
df2 = pd.read_sql_query(query, conn)

query3 = '''
SELECT 
    phone_brand,
    SUM(profit) profit, 
    SUM(cost_price) cost_price, 
    SUM(sold_price) 
    sold_price 
FROM 
    phone_sales 
GROUP BY 
    phone_brand'''
                
df3 = pd.read_sql_query(query3, conn)
fig1 = px.bar(df3, 'phone_brand', 'profit')
fig2 = px.bar(df3, 'phone_brand', ['cost_price', 'sold_price'], barmode='group')

with col2:
    st.header('Table From Remote Database (Last three entry)')
    st.table(df2)
    newTableRw = pd.read_sql_query(row_count, conn)
    newRwNum = newTableRw['table_rows'][0]
    text1 = f'There are a total of {newRwNum} rows in the database'
    st.write(text1)
   
    col21, col22 = st.columns(2)
    with col21:
        st.plotly_chart(fig1)
    with col22:
        st.plotly_chart(fig2)
        
# Create a download button that downloads the DataFrame as a CSV file
if st.button('Download CSV'):
    csv = df2.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="mydata.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)


# Close the database connection
cur.close()
conn.close()
