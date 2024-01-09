from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import requests

from .fairindicator import *

app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the Imaging Plaza Fair Level Indicator"}

@app.get("/indicate/")
async def indicate(uri:str, graph: str):

    shapesfile = "app/shapes.ttl"
    
    suggestions = indicate_fair(uri, graph, shapesfile)

    return suggestions



