import os
from fastapi import FastAPI
from dotenv import load_dotenv
from src.routers.analyst import analyst_router
load_dotenv()

app = FastAPI(debug=os.getenv("DEBUG", "False").lower() == "true")
app.include_router(analyst_router)

        