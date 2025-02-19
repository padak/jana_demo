# Streamlit Snowflake Data Viewer

A Streamlit web application that allows authorized users to view and interact with Snowflake database tables.

## Features

- Secure login system with role-based access control
- View list of available tables in the configured Snowflake schema
- Preview table data (for authorized users)
- Clean and intuitive user interface

## Prerequisites

- Python 3.7+
- Snowflake account with appropriate access
- Required Python packages (see `requirements.txt`)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` file with your Snowflake credentials.

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Access the application in your web browser (typically http://localhost:8501)

3. Log in with one of the following credentials:
   - Username: test1, Password: password1 (View-only access)
   - Username: test2, Password: password2 (View and preview access)

## Security Notes

- This application uses hardcoded credentials for demonstration purposes
- In a production environment, implement proper authentication mechanisms
- Ensure proper security measures are in place for database credentials
- Review and implement additional security best practices before deployment

## Project Structure

- `app.py`: Main Streamlit application
- `config.py`: Configuration and environment variables
- `database.py`: Snowflake database connection and queries
- `requirements.txt`: Python package dependencies
- `.env.template`: Template for environment variables 