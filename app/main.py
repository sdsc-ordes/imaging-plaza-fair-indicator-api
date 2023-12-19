from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import requests

from fairindicator import *

app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the Imaging Plaza Fair Level Indicator"}

@app.get("/indicate/{uri}")
async def validate(uri:str):
    # 1. Retrieve information from GraphDB
    # 2. Provide it to the indicator function
    # 3. Return it 

    pass



