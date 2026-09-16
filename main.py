import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from src.routers.analyst import analyst_router

app = FastAPI(debug=os.getenv("DEBUG", "False").lower() == "true")
app.include_router(analyst_router)

        