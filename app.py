import streamlit as st
from config import USERS, USER_PERMISSIONS
from database import get_tables, get_table_preview, get_table_details
import pandas as pd

def check_password():
    """Returns `True` if the user had a correct password."""
    def login_form():
        """Form for getting username and password input"""
        with st.form("Credentials"):
            username = st.text_input("Username").lower()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In")
            
            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state["username"] = username
                    return True
                st.error("😕 User not known or password incorrect")
        return False

    # Return True if the username + password is already cached and valid
    if "username" in st.session_state:
        return True

    # Show inputs for username + password.
    return login_form()

def show_logout_button():
    """Display logout button"""
    if st.button("Logout"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def show_table_details(table_name):
    """Show table details in a dialog"""
    columns, data = get_table_details(table_name)
    if columns and data:
        df = pd.DataFrame(data, columns=columns)
        
        # Create a styled table details view
        st.markdown(f"### 📋 Details for table: `{table_name}`")
        st.markdown("---")
        
        # Display the schema information in a nice format
        st.dataframe(
            df,
            column_config={
                "name": "Column Name",
                "type": "Data Type",
                "kind": "Kind",
                "null?": "Nullable",
                "default": "Default Value",
                "primary key": "Primary Key",
                "unique key": "Unique Key",
                "check": "Check Constraint",
                "expression": "Expression",
                "comment": "Comment"
            },
            hide_index=True
        )

def display_tables():
    """Display available tables with refresh button and better formatting"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Available Tables")
    with col2:
        if st.button("🔄 Refresh Tables"):
            # Clear the cache for get_tables function
            get_tables.clear()
            st.rerun()
    
    tables = get_tables()
    
    if not tables:
        st.warning("No tables found or unable to connect to database.")
        return tables
    
    # Display tables in a more organized way
    st.write(f"Found {len(tables)} tables in the schema:")
    
    # Create a container with custom styling for tables
    with st.container():
        for table in tables:
            # Create a clickable table card
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"""
                <div style='
                    padding: 10px;
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                    margin: 5px 0;
                    background-color: #f8f9fa;
                    cursor: pointer;
                '>
                    📊 <code>{table}</code>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("Details", key=f"details_{table}"):
                    # Show table details in a dialog
                    with st.dialog(f"Table Details - {table}"):
                        show_table_details(table)
    
    return tables

def main():
    st.set_page_config(
        page_title="Snowflake Data Viewer",
        page_icon="❄️",
        layout="wide"
    )
    
    st.title("❄️ Snowflake Data Viewer")

    if not check_password():
        return

    # Show the logout button
    show_logout_button()

    # Get current user and their permissions
    username = st.session_state["username"]
    permissions = USER_PERMISSIONS[username]

    # Welcome message
    st.write(f"Welcome, {username}!")

    # Display tables with refresh button and better formatting
    tables = display_tables()
    
    if not tables:
        return

    # If user has preview permission, show table preview
    if "preview_data" in permissions:
        st.subheader("Table Preview")
        selected_table = st.selectbox("Select a table to preview:", tables)
        
        if selected_table:
            columns, data = get_table_preview(None, selected_table)
            if columns and data:
                st.write(f"Preview of first 20 rows from {selected_table}:")
                # Convert data to a format suitable for st.dataframe
                df = pd.DataFrame(data, columns=columns)
                st.dataframe(df)

if __name__ == "__main__":
    main() 