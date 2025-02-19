import snowflake.connector
from config import SNOWFLAKE_CONFIG
import streamlit as st

def get_snowflake_connection():
    """Create and return a Snowflake connection."""
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_CONFIG['user'],
            password=SNOWFLAKE_CONFIG['password'],
            account=SNOWFLAKE_CONFIG['account'],
            warehouse=SNOWFLAKE_CONFIG['warehouse'],
            database=SNOWFLAKE_CONFIG['database'],
            schema=SNOWFLAKE_CONFIG['schema']
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None

@st.cache_resource
def get_tables():
    """Get list of all tables in the configured schema."""
    conn = get_snowflake_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[1] for row in cursor.fetchall()]
        return tables
    except Exception as e:
        st.error(f"Error fetching tables: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

@st.cache_data
def get_table_preview(_conn, table_name, limit=20):
    """Get a preview of the specified table."""
    conn = get_snowflake_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        return columns, data
    except Exception as e:
        st.error(f"Error fetching table preview: {str(e)}")
        return None, None
    finally:
        cursor.close()
        conn.close() 