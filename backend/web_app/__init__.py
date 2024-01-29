from .database import DATABASE_URL, Base
from fastapi import FastAPI

app = FastAPI(title='Drom')