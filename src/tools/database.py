
from src.database.database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import  text

def execute_sql( query ):

    session = SessionLocal()
    result =[]
    try:
        rows = session.execute(text(query))
        for row in rows :
            result.append(row)
    finally:
        session.close()
    print(result)
    return result
