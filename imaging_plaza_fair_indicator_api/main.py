from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import requests

from .fairindicator import *

app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the Imaging Plaza Fair Level Indicator v0.0.9"}

@app.get("/indicate/")
async def indicate(uri:str, graph: str):

    # Take shapesfile from environment variable
    shapesfile = "/app/imaging_plaza_fair_indicator_api/ImagingOntologyCombined.ttl"
    
    suggestions = indicate_fair(uri, graph, shapesfile)

    return suggestions



