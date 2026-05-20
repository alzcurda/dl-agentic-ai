import sqlite3
import pandas as pd
from IPython.display import display, HTML

def create_transactions_db(db_path='products.db'):
    """Creates an SQLite database with dummy transaction data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop table if exists to start fresh
    cursor.execute("DROP TABLE IF EXISTS transactions")
    
    # Create the transactions table
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_name TEXT,
            brand TEXT,
            category TEXT,
            color TEXT,
            action TEXT,
            qty_delta INTEGER,
            unit_price REAL,
            notes TEXT,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert some dummy data with negative qty_delta for sales
    dummy_data = [
        (1, 'Running Shoe', 'Nike', 'Shoes', 'Red', 'insert', 100, None, 'Initial stock', '2023-01-01 10:00:00'),
        (2, 'T-Shirt', 'Adidas', 'Clothing', 'Blue', 'insert', 50, None, 'Initial stock', '2023-01-01 10:05:00'),
        (1, 'Running Shoe', 'Nike', 'Shoes', 'Red', 'sale', -10, 120.00, 'Online sale', '2023-01-02 14:30:00'),
        (2, 'T-Shirt', 'Adidas', 'Clothing', 'Blue', 'sale', -5, 25.00, 'In-store sale', '2023-01-03 09:15:00'),
        (3, 'Yoga Mat', 'Lululemon', 'Accessories', 'Green', 'insert', 200, None, 'Initial stock', '2023-01-04 11:00:00'),
        (3, 'Yoga Mat', 'Lululemon', 'Accessories', 'Green', 'sale', -1, 190571.46, 'Bulk sale', '2023-01-05 16:45:00'),
        (1, 'Running Shoe', 'Nike', 'Shoes', 'Red', 'sale', -20, 120.00, 'Online sale', '2023-01-06 12:00:00'),
    ]
    
    cursor.executemany("""
        INSERT INTO transactions (product_id, product_name, brand, category, color, action, qty_delta, unit_price, notes, ts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dummy_data)
    
    conn.commit()
    conn.close()
    print(f"Database '{db_path}' created and populated with sample data.")

def get_schema(db_path='products.db'):
    """Returns the schema of the specified SQLite database as a string."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_str = ""
    for table_name in tables:
        table_name = table_name[0]
        schema_str += f"Table name: {table_name}\n"
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            schema_str += f"{col_name} ({col_type})\n"
        schema_str += "\n"
        
    conn.close()
    return schema_str.strip()

def execute_sql(sql_query, db_path='products.db'):
    """Executes a SQL query against the database and returns a pandas DataFrame."""
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(sql_query, conn)
    except Exception as e:
        df = pd.DataFrame({"Error": [str(e)]})
    finally:
        conn.close()
    return df

def print_html(content, title=None, is_image=False):
    """Utility to print content in a nice format in Jupyter notebooks."""
    if title:
        display(HTML(f"<h3>{title}</h3>"))
    
    if isinstance(content, pd.DataFrame):
        display(HTML(content.to_html(index=False)))
    elif isinstance(content, str):
        # Format strings containing HTML properly
        if "<" in content and ">" in content:
            display(HTML(content))
        else:
            display(HTML(f"<pre style='white-space: pre-wrap;'>{content}</pre>"))
    else:
        print(content)
