from sqlglot import parse
from sqlglot.expressions import Select


def validate_sql(query):
    try:
        statements = parse(query)

        if len(statements) != 1:
            return {
                "valid": False,
                "reason": "Only one SQL statement is allowed"
            }

        statement = statements[0]

        if statement.find(Select) is None:
            return {
                "valid": False,
                "reason": "Only SELECT queries are allowed"
            }

        return {
            "valid": True,
            "reason": None
        }

    except Exception as e:
        return {
            "valid": False,
            "reason": f"Invalid SQL: {str(e)}"
        }