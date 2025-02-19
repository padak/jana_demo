# Developer Design Document: Streamlit Snowflake Data Viewer

## Overview

This application is a Streamlit-based web app that allows two employees (with hardcoded credentials) to log in and interact with a remote Snowflake database. The primary functions are:
- **Employee "test1"**: View a list of all available tables in a specific Snowflake schema.
- **Employee "test2"**: In addition to viewing the table list, select a table from a dropdown and view a sample of 20 rows from that table.
- Both users should also be able to log out to end their session.

## Environment Setup

### Dependencies
- **Streamlit**: For building the web interface.
- **Snowflake Connector for Python**: For connecting to the Snowflake database.
- **python-dotenv**: To load environmental variables from a `.env` file.
  
Install these packages using pip:

```bash
pip install streamlit snowflake-connector-python python-dotenv
```

### .env File Configuration
Create a `.env` file in the project root and include all necessary Snowflake connection details:

```
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

## Authentication

- **Hardcoded Credentials**:  
  The application will use hardcoded credentials within the code for the two employees, for example:
  ```python
  USERS = {
      "test1": "password1",
      "test2": "password2"
  }
  ```
- **Login Mechanism**:  
  Implement a login form with username and password fields. On successful login, the authenticated username should be stored in `st.session_state` for session management.
- **Logout**:  
  Provide a logout button that clears the session state, ensuring that the user can end the session and is redirected back to the login page.

## Database Connectivity

- **Snowflake Connection**:  
  Use the Snowflake Python Connector to connect to the database. The connection parameters should be read from the `.env` file (using `python-dotenv`), and the connection object should preferably be cached or reused during the session.
  
  Example connection code (to be modularized as needed):
  ```python
  import os
  import snowflake.connector
  from dotenv import load_dotenv
  
  load_dotenv()
  
  def get_snowflake_connection():
      conn = snowflake.connector.connect(
          user=os.getenv("SNOWFLAKE_USER"),
          password=os.getenv("SNOWFLAKE_PASSWORD"),
          account=os.getenv("SNOWFLAKE_ACCOUNT"),
          warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
          database=os.getenv("SNOWFLAKE_DATABASE"),
          schema=os.getenv("SNOWFLAKE_SCHEMA")
      )
      return conn
  ```

- **Listing Tables**:  
  Once connected, run a query (e.g., using `SHOW TABLES IN <schema>`) to retrieve all available tables for display. For example:
  ```python
  def list_tables(conn):
      cursor = conn.cursor()
      try:
          cursor.execute("SHOW TABLES")
          tables = [row[1] for row in cursor.fetchall()]  # Adjust index based on query result structure.
          return tables
      finally:
          cursor.close()
  ```

## User Interface and Workflow

1. **Login Page**:  
   - Use Streamlit's forms to display a login interface.
   - Validate credentials against the hardcoded dictionary.
   - On successful authentication, store the username in `st.session_state['username']`.

2. **Main Application Page (Post-login)**:
   - **Common Interface**:  
     Display a welcome message and the list of available tables retrieved from the Snowflake database.
     
   - **For "test1"**:  
     Simply show the list of table names.
     
   - **For "test2"**:  
     In addition to the table list, include a dropdown to select a table. On selection, execute a query such as `SELECT * FROM <selected_table> LIMIT 20` and render the result using `st.dataframe` or `st.table`.

3. **Logout Functionality**:  
   Include a logout button that, when clicked, clears the session state and navigates the user back to the login page.

## Code Organization

- Place the authentication logic and UI code in your main Streamlit app file (e.g., `app.py`).
- Modularize the connection and database query functions into separate functions or modules as needed.
- Ensure that error handling is implemented for database connectivity and query execution.

## TODO

- **Error Handling Enhancements**:  
  Provide user-friendly error messages if the connection to Snowflake fails or if queries return no data.
- **Session Management Improvements**:  
  Consider implementing more robust session management if more users or roles are to be added in the future.
- **Caching and Performance**:  
  Evaluate caching mechanisms for database queries to optimize performance.
- **UI/UX Enhancements**:  
  Explore additional UI improvements and possibly theming for a better user experience.

---

This document should serve as the main reference for developers implementing the app. Follow the instructions closely and feel free to extend the TODO section with any new insights or additional features that might be required in the future.

