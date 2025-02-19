import streamlit as st
from config import USERS, USER_PERMISSIONS
from database import get_tables, get_table_preview

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

    # Get list of tables
    tables = get_tables()
    
    if not tables:
        st.warning("No tables found or unable to connect to database.")
        return

    st.subheader("Available Tables")
    st.write(f"Found {len(tables)} tables in the schema:")
    st.write(tables)

    # If user has preview permission, show table preview
    if "preview_data" in permissions:
        st.subheader("Table Preview")
        selected_table = st.selectbox("Select a table to preview:", tables)
        
        if selected_table:
            columns, data = get_table_preview(None, selected_table)
            if columns and data:
                st.write(f"Preview of first 20 rows from {selected_table}:")
                # Convert data to a format suitable for st.dataframe
                import pandas as pd
                df = pd.DataFrame(data, columns=columns)
                st.dataframe(df)

if __name__ == "__main__":
    main() 