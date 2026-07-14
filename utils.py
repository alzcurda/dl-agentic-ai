# Utility helpers used across notebooks.

"""Utility helpers used across notebooks.

This file consolidates the `print_html` function (and related helpers) that were previously defined in
`01_reflection/utils.py` and `02_improving_reflection/utils.py`. The implementation mirrors the original
behaviour: it prints a title separator and either displays an image or plain content in a Jupyter
environment.
"""

from __future__ import annotations

try:
    from IPython.display import display, HTML, Image
except ImportError:
    # Fallback stubs for environments without IPython
    def display(obj):
        print(obj)
    def HTML(s):
        return s
    class Image:
        def __init__(self, filename=None):
            self.filename = filename
    # End of fallback

import base64
import os
import sqlite3
import pandas as pd
from datetime import datetime


def print_html(content, title: str | None = None, is_image: bool = False) -> None:
    """Print formatted HTML (or an image) inside a notebook.

    Args:
        content: The text/HTML to display or a path to an image file when ``is_image`` is True.
        title: Optional title printed as a separator before the content.
        is_image: If True, ``content`` is interpreted as a file path to an image.
    """
    if title:
        print(f"\n--- {title} ---")
    if is_image:
        # Display an image file directly.
        display(Image(filename=content))
    else:
        # ``content`` may be a string, a DataFrame, or any object with a ``__str__``.
        if hasattr(content, "to_html"):
            # Pandas DataFrames have a nice HTML representation.
            display(HTML(content.to_html(index=False)))
        else:
            print(content)
    print("-" * 40)


def encode_image_b64(path: str) -> tuple[str, str]:
    """Encode an image file as a base64 data URI.

    Returns a ``(media_type, b64_string)`` tuple suitable for sending to LLM image‑generation
    endpoints.
    """
    with open(path, "rb") as image_file:
        b64_string = base64.b64encode(image_file.read()).decode("utf-8")
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    media_type = f"image/{ext}" if ext in {"png", "jpg", "jpeg", "gif", "webp"} else "image/png"
    return media_type, b64_string


def ensure_execute_python_tags(code: str) -> str:
    """Wrap raw Python code in ``<execute_python>`` tags when missing.

    The notebook execution environment expects code blocks to be wrapped. This helper guarantees
    the required markup.
    """
    if "<execute_python>" not in code:
        return f"<execute_python>\n{code}\n</execute_python>"
    return code

# ----------------------------------------------------------------------
# Database utilities (originally from 02_improving_reflection/utils.py)
# ----------------------------------------------------------------------
def create_transactions_db(db_path: str = "products.db") -> None:
    """Create an SQLite DB with dummy transaction data."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute(
        """
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
        """
    )
    dummy_data = [
        (1, "Running Shoe", "Nike", "Shoes", "Red", "insert", 100, None, "Initial stock", "2023-01-01 10:00:00"),
        (2, "T-Shirt", "Adidas", "Clothing", "Blue", "insert", 50, None, "Initial stock", "2023-01-01 10:05:00"),
        (1, "Running Shoe", "Nike", "Shoes", "Red", "sale", -10, 120.00, "Online sale", "2023-01-02 14:30:00"),
        (2, "T-Shirt", "Adidas", "Clothing", "Blue", "sale", -5, 25.00, "In-store sale", "2023-01-03 09:15:00"),
        (3, "Yoga Mat", "Lululemon", "Accessories", "Green", "insert", 200, None, "Initial stock", "2023-01-04 11:00:00"),
        (3, "Yoga Mat", "Lululemon", "Accessories", "Green", "sale", -1, 190571.46, "Bulk sale", "2023-01-05 16:45:00"),
        (1, "Running Shoe", "Nike", "Shoes", "Red", "sale", -20, 120.00, "Online sale", "2023-01-06 12:00:00"),
    ]
    cur.executemany(
        """
        INSERT INTO transactions
        (product_id, product_name, brand, category, color, action, qty_delta,
         unit_price, notes, ts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        dummy_data,
    )
    conn.commit()
    conn.close()
    print(f"Database '{db_path}' created and populated with sample data.")


def get_schema(db_path: str = "products.db") -> str:
    """Return a textual representation of the SQLite schema."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    schema = ""
    for (table_name,) in tables:
        schema += f"Table name: {table_name}\n"
        cur.execute(f"PRAGMA table_info({table_name})")
        for col in cur.fetchall():
            col_name, col_type = col[1], col[2]
            schema += f"{col_name} ({col_type})\n"
        schema += "\n"
    conn.close()
    return schema.strip()


def execute_sql(sql_query: str, db_path: str = "products.db") -> pd.DataFrame:
    """Run a SQL query and return the result as a pandas DataFrame."""
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(sql_query, conn)
    except Exception as e:  # pragma: no cover
        df = pd.DataFrame({"Error": [str(e)]})
    finally:
        conn.close()
    return df
