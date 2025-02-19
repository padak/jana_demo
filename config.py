import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Snowflake configuration
SNOWFLAKE_CONFIG = {
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': os.getenv('SNOWFLAKE_DATABASE'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA')
}

# User credentials (hardcoded as per requirements)
USERS = {
    "test1": "password1",
    "test2": "password2"
}

# User permissions
USER_PERMISSIONS = {
    "test1": ["view_tables"],
    "test2": ["view_tables", "preview_data"]
} 