from sqlalchemy import text
from src.database.database import SessionLocal
from src.tools.sql_validator import validate_sql
from langchain.tools import tool

@tool
def execute_sql(query):
    """Execute a validated read-only SQL query against the database and return the query results."""
    validation = validate_sql(query)

    if not validation["valid"]:
        return {
            "error": validation["reason"]
        }

    session = SessionLocal()
    result = []

    try:
        rows = session.execute(text(query))

        for row in rows:
            result.append(dict(row._mapping))
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()

    return result