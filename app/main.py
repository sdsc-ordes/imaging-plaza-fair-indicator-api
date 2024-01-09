from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import requests

from .fairindicator import *

app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the Imaging Plaza Fair Level Indicator"}

@app.get("/indicate/")
async def validate(uri:str, graph: str):

    if graph == "temporary":
        graphURL = "https://epfl.ch/example/temporaryGraph"
    elif graph == "final":
        graphURL = "https://epfl.ch/example/finalGraph"
    else:
        raise "ERROR GRAPH NOT FOUND"
    
    suggestions = indicate_fair(uri, graphURL)

    return suggestions



