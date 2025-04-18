"""
@Created on: Sunday, 19 March 2023, 03:38:53 PM WAT

@Author: TelRich Data

"""
# Importing required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import io
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, text
import urllib.parse
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# setting the page size and title
st.set_page_config(layout="wide", page_title='Database Data Entry Application')

# Function to connect to the database
def connect_db():
    username = st.secrets['user']
    password = urllib.parse.quote_plus(st.secrets['pw'])  # URL encode the password
    host = st.secrets['host']
    database = st.secrets['db']
    port = st.secrets['port']
    sslmode = 'prefer'
    
    # Create SQLAlchemy connection string
    conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"
    return create_engine(conn_str)

# Create engine
engine = connect_db()

# Replace the psycopg2 connection with SQLAlchemy engine
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))  # Test connection
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    st.error("Failed to connect to database. Please check logs for details.")
    st.stop()

def init_database():
    """Initialize database by creating required tables if they don't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS phone_sales (
        id SERIAL PRIMARY KEY,
        phone_brand VARCHAR(50),
        phone_model VARCHAR(50),
        purchase_date DATE,
        sold_date DATE,
        sold_price DECIMAL(10,2),
        cost_price DECIMAL(10,2),
        profit DECIMAL(10,2) GENERATED ALWAYS AS (sold_price - cost_price) STORED
    );
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(create_table_query))
            conn.commit()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        st.error("Failed to initialize database. Please check logs for details.")

# Initialize database when app starts
init_database()

# App Setup
st.markdown("<h1 style='text-align:center;'>Streamlit Data Entry App with Azure Postgres Database</h1>", unsafe_allow_html=True)
st.markdown('''<center><h2>A sample data entry application created for business purpose.</center></h2>''', unsafe_allow_html=True)
st.markdown('''<center><h3>How to use the app: Make an entry on the left and watch the table and charts change.😊
            </center></h3>''', unsafe_allow_html=True)


# Split the page into two column
col1, col2 = st.columns([2, 8], gap='large')

# Creating Phone Brands and model
brand = {
    'Apple':[
        'iPhone 7', 'iPhone 8', 'iPhone X', 'iPhone 11', 'iPhone 12', 'iPhone 13', 'iPhone 14'
    ],
    'Oppo':[
        'Oppo Reno8', 'Oppo Reno7', 'Oppo Reno5', 'Oppo A96', 'Oppo A77', 'Oppo A57', 'Oppo A16'
    ],
    'Samsung': [
        'Galaxy F14', 'Galaxy S23', 'Galaxy Z Flip', 'Samsung S8', 'Samsung S9', 'Galaxy M14', 'Galaxy A54' 
    ],
    'Xiaomi': [
        'Xiaomi 13', 'Xiaomi 12T', 'Xiaomi 11', 'Xiaomi Mix 4', 'Redmi Note 12S', 'Redmi K60', 'Redmi Note 10'
    ]
}

# Sales Entry 
with col1.expander(label='', expanded=True):
    st.header('Sales Entry')
    phone_brand = st.selectbox('Select Brand', brand.keys())
    phone_model =  st.selectbox('Select Model', brand[phone_brand])
    purchase_date = st.date_input('Enter purchase date')
    sold_date = st.date_input('Enter sold date')
    cost_price = st.number_input('Enter cost price')
    sold_price = st.number_input('Enter sold price')

    # Saving the entry to the database.
    if st.button('Save Details'):
        try:
            query = text('''INSERT INTO phone_sales (phone_brand, phone_model, purchase_date, sold_date, sold_price, cost_price)
            VALUES (:brand, :model, :p_date, :s_date, :s_price, :c_price)''')
            with engine.connect() as conn:
                conn.execute(query, {
                    'brand': phone_brand,
                    'model': phone_model,
                    'p_date': purchase_date,
                    's_date': sold_date,
                    's_price': sold_price,
                    'c_price': cost_price
                })
                conn.commit()
            logger.info(f"Successfully added new entry for {phone_brand} {phone_model}")
            st.success("Data saved successfully!")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            st.error("Failed to save data. Please try again.")

# Counting the number of rows in the database table
try:
    row_count = '''
    SELECT COUNT(*) table_rows
    FROM phone_sales
    '''
    table_rw = pd.read_sql_query(text(row_count), engine)
    rw_num = table_rw['table_rows'][0]
    col1.write(f'There are now {rw_num} rows in the table')
except Exception as e:
    logger.error(f"Failed to count rows: {e}")
    col1.error("Failed to retrieve row count")

# Maintain 100 rows limit by deleting oldest entries
if rw_num > 100:
    query = """
    DELETE FROM phone_sales
    WHERE id IN (
        SELECT id
        FROM phone_sales
        ORDER BY id 
        LIMIT (SELECT COUNT(*) - 100 FROM phone_sales)
    );
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()
            logger.info("Deleted oldest entries to maintain 100 row limit")
    except Exception as e:
        logger.error(f"Failed to delete rows: {e}")
        st.error("Failed to delete rows. Please check logs for details.")

# Initialize session state for reset confirmation
if 'reset_clicked' not in st.session_state:
    st.session_state.reset_clicked = False

# Add danger zone section
with col1.expander('⚠️ Danger Zone', expanded=False):
    st.markdown("""
    ### Reset Database Table
    This will permanently delete all data from the table. This action cannot be undone.
    """)
    
    if not st.session_state.reset_clicked:
        if st.button('Reset Table', type='primary', use_container_width=True):
            st.session_state.reset_clicked = True
            st.rerun()
    else:
        st.warning('⚠️ Are you sure? This action cannot be undone!')
        colA, colB = st.columns(2)
        if colA.button('Yes, Reset', type='primary', use_container_width=True):
            try:
                drop_query = "DROP TABLE IF EXISTS phone_sales;"
                with engine.connect() as conn:
                    conn.execute(text(drop_query))
                    conn.commit()
                init_database()
                st.session_state.reset_clicked = False
                logger.info("Table was reset by user")
                st.success("Table has been reset successfully!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                logger.error(f"Failed to reset table: {e}")
                st.error("Failed to reset table. Please check logs for details.")
        if colB.button('No, Cancel', use_container_width=True):
            st.session_state.reset_clicked = False
            st.rerun()

# Hiding the numbers on the table
hide = """
  <style>
  thead tr th:first-child {display:none}
  tbody th {display:none}
  </style>
  """
st.markdown(hide, True)
# Displaying the last five entries in the table
query = 'SELECT * FROM phone_sales ORDER BY id DESC LIMIT 5'
df2 = pd.read_sql_query(text(query), engine)

# VISUALIZING THE ENTRIES
# Query the database
query3 = '''
SELECT 
    phone_brand,
    SUM(profit) profit, 
    SUM(cost_price) cost_price, 
    SUM(sold_price) sold_price 
FROM 
    phone_sales 
GROUP BY 
    phone_brand'''
                
# Profit By Brand
df3 = pd.read_sql_query(text(query3), engine).sort_values(by=['profit', 'sold_price'], ascending=False)
fig1 = px.bar(df3, 'phone_brand', 'profit', text_auto=True, title='<b>Profit by Brand<b>', 
              labels={'profit':'', 'phone_brand':''},
              color_discrete_sequence=px.colors.qualitative.Set3)
fig1.update_yaxes(showticklabels=False)
fig1.update_traces(textposition='outside', cliponaxis=False)
    
# Sales and Cost Price by Brand
fig2 = px.bar(df3, 'phone_brand', ['cost_price', 'sold_price'], barmode='group', title='<b>Cost and Sales by Brand<b>',
              labels={'value':'', 'phone_brand':''}, text_auto=True,
              color_discrete_sequence=px.colors.qualitative.Set2)
fig2.update_traces(textposition='outside', cliponaxis=False)
fig2.update_yaxes(showticklabels=False)
fig2.update_layout(legend = dict(
                        orientation='v',
                        title='',
                        font = dict(
                        family="Courier",
                        size=12,
                        ),
                        bgcolor='olive',
                        bordercolor='blue',
                        borderwidth=.5
                    ))

# Display table latest entry and visualization
with col2.expander(label='', expanded=True):
    st.header('The last five entries in the table')
    st.table(df2)
    
    st.header('Data Visualization')
    col21, col22 = st.columns(2)
    with col21:
        st.plotly_chart(fig1, use_container_width=True)
    with col22:
        st.plotly_chart(fig2, use_container_width=True)

# Download the data in the table        
all_data = '''
SELECT *
FROM phone_sales
'''
data = pd.read_sql_query(text(all_data), engine)

@st.cache_data
# Function to download JSON file
def download_json(df):
    json = df.to_json(indent=2)
    b64 = base64.b64encode(json.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="mydata.json">Download JSON</a>'
    return href    
        
# Create a download button that downloads the DataFrame as a CSV file
with col1.expander('Download Data'):
    # Download csv file
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="mydata.csv">Download CSV</a>'
    # Download options
    st.markdown(href, unsafe_allow_html=True)
    st.markdown(download_json(data), unsafe_allow_html=True)
    
    
with col1.expander('Contact', expanded=True):
    st.image('telrich_logo.png', width=100)
    st.markdown("[LinkedIn](https://www.linkedin.com/in/goodrichokoro/) \
        | [Twitter](https://twitter.com/OkoroGoodrich) \
        | [GitHub](https://github.com/TelRich)\
        | okorogoodrich@gmail.com", unsafe_allow_html=True)

with col2.expander('Documentation'):
    st.markdown("""
            # Streamlit Data Entry App with Azure Postgres Database

            >**Introduction**:
            
            This documentation provides an overview of a data entry application developed using Streamlit and connected to an Azure Postgres database. 
            The app allows users to enter data into a form and saves the in the database.
            The app also includes a visualization that changes with respect to the latest entry. In addition, users can download the data from the database. On the other end, Power BI is connected to the same database to generate data visualizations.

            >**Important Database Limitations**:
            
            * The database table is limited to 100 rows to optimize performance and manage data storage efficiently
            * When the limit is reached, older entries are automatically removed to make room for new ones
            * A reset function is available in the Danger Zone section to clear all data if needed

            >**Project Overview**

            *Objective*: The objective of this project is to provide a user-friendly data entry app with advanced features, such as database integration, visualization, and Power BI integration, that can be used for small to medium-sized projects.

            *Goal*: The goal of this project is to create a tool that simplifies the data entry process, allows users to view and analyze their data, and provides valuable insights that can be used to make informed decisions. 
            The app should be easy to use and accessible from anywhere, ensuring that users can collect and analyze data on-the-go.

            >**Technologies**:

            * Streamlit
            * Python
            * Azure Postgres Database
            * Python Plotly
            * Power BI

            >**Functionality**:

            1. Data Entry: The app allows users to enter data into a form and save it in an Azure Postgres database. The form has been designed to ensure that all necessary data is collected.

            2. Database Integration: The app is connected to an Azure Postgres database where all the data entered in the form is saved. The database table has been set to accumulate a maximum of 100 rows to avoid excessive data accumulation.

            3. Visualization: The app includes a plotly visualization that changes with respect to the latest entry. The visualization provides a quick overview of the data entered and helps users to understand the trends and patterns.

            4. Download Data: The app allows users to download the data from the database. This feature is useful for users who want to perform further analysis on the data using other tools.

            5. Power BI Integration: The app is integrated with Power BI, which allows users to view charts and perform additional analysis on the data. The charts have been designed for the mobile view of Power BI, ensuring that users can access the data on-the-go.

            > **Conclusion**:

            The Streamlit data entry app, combined with an Azure Postgres database and Plotly visualization, provides a robust and user-friendly solution for data collection and analysis. The app's interface and dynamic visualization make data entry and analysis quick and efficient, while also providing a way to download the data, and the connection to Power BI allows for more in-depth analysis and visualization. Overall, this app provides a comprehensive solution for data collection and analysis needs.

            > **Future Work**

            * This project can be improved/modified further by directly embedding the Power BI dashboard on the app. 
            * More data storage is provided, as are additional charts displaying various other insights.
            
             """)
