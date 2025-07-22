
# Streamlit Recipe App (SQL Edition)

This is a Streamlit web application to manage recipes with nutrition info, stored in a Microsoft SQL Server database.

## Features

- Add, view, and edit recipes
- Store in SQL Server instead of flat files
- GitHub-ready

## Setup

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Update the connection string in `app.py`:
    ```python
    def get_connection():
        return pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=your_server;"
            "DATABASE=your_db;"
            "UID=your_username;"
            "PWD=your_password"
        )
    ```

3. Create the table in SQL Server:
    ```sql
    CREATE TABLE Recipes (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255),
        ingredients TEXT,
        instructions TEXT,
        serving_size NVARCHAR(100),
        calories FLOAT,
        fat FLOAT,
        carbohydrates FLOAT,
        protein FLOAT
    );
    ```

4. Run the app:
    ```
    streamlit run app.py
    ```

## Notes

- Use trusted connection or SQL auth as needed
- Add more features like editing/deleting recipes as desired
