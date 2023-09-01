# Streamlit Data Entry App with Azure Postgres Database

# [View Application](https://telrich-streamlit-database-connection-test-db-test-cdg8zc.streamlit.app/)

>**Introduction**:

This documentation provides an overview of a data entry application developed using Streamlit and connected to an Azure Postgres database. 
The app allows users to enter data into a form and saves the in the database.
The app also includes a visualization that changes with respect to the latest entry. In addition, users can download the data from the database. On the other end, Power BI is connected to the same database to generate data visualizations.

>**Project Overview**

_Objective_: The objective of the project is to build an app that takes in users input an save it to the remote database.

_Goal_: The goal is to automate the data analysis process as the data is being entered into the database

>**Technologies**:

* Streamlit
* Python
* PostgreSQL
* Azure Postgres Database
* Python Plotly
* Power BI

>**Functionality**:

1. Data Entry: The app allows users to enter data into a form and save it in an Azure Postgres database. The form has been designed to ensure that all necessary data is collected.

2. Database Integration: The app is connected to an Azure Postgres database where all the data entered in the form is saved. The database table has been set to accumulate a maximum of 55 rows to avoid excessive data accumulation.

3. Visualization: The app includes a plotly visualization that changes with respect to the latest entry. The visualization provides a quick overview of the data entered and helps users to understand the trends and patterns.

4. Download Data: The app allows users to download the data from the database. This feature is useful for users who want to perform further analysis on the data using other tools.

5. Power BI Integration: The app is integrated with Power BI, which allows users to view charts and perform additional analysis on the data. The charts have been designed for the mobile view of Power BI, ensuring that users can access the data on-the-go.

> **Conclusion**:

The Streamlit data entry app, combined with an Azure Postgres database and Plotly visualization, provides a robust and user-friendly solution for data collection and analysis. The app's interface and dynamic visualization make data entry and analysis quick and efficient, while also providing a way to download the data, and the connection to Power BI allows for more in-depth analysis and visualization. Overall, this app provides a comprehensive solution for data collection and analysis needs.

> **Future Work**

* This project can be improved/modified further by directly embedding the Power BI dashboard on the app. 
* More data storage is provided, as are additional charts displaying various other insights.
    
