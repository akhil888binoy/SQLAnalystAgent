import os
from fastapi import FastAPI
from dotenv import load_dotenv
from src.tools.database import execute_sql

load_dotenv()
app = FastAPI(debug=os.getenv("DEBUG", "False").lower() == "true")
execute_sql('SELECT COUNT(*) FROM products')