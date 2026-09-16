from sqlalchemy import MetaData, inspect
from src.database.database import engine
from langchain.tools import tool

@tool
def get_schema():
    """Get the database schema, including table names, columns, data types, and foreign-key relationships."""
    inspector = inspect(engine)

    table_names = inspector.get_table_names()

    table_schema = []

    for table_name in table_names:

        if table_name == "alembic_version":
            continue

        columns = inspector.get_columns(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)

        table_schema.append({
            "table_name": table_name,
 
            "columns": [
                {
                    "name": column["name"],
                    "type": str(column["type"])
                }
                for column in columns
            ],

            "foreign_keys": [
                {
                    "column": fk["constrained_columns"][0],
                    "referred_table": fk["referred_table"],
                    "referred_column": fk["referred_columns"][0]
                }
                for fk in foreign_keys
            ]
        })
    return table_schema