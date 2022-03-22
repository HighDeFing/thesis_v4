from fastapi import FastAPI, Request, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from scripts.haystack_files.haystack_upload_files import Haystack_module

import json

f = open('web/static/data/escuelas.json')
data = json.load(f)

haystack = Haystack_module()
haystack.init_QAPipeline()
elastic_pipe = haystack.get_QAPipeline()

app = FastAPI()

app.mount("/web/static", StaticFiles(directory="web/static"), name="static")

templates = Jinja2Templates(directory="web/templates")

@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/elements.html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("elements.html", {"request": request})

@app.get("/generic.html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("generic.html", {"request": request})

@app.get("/search.html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("search.html", {"request": request, "escuelas": data}) 

@app.get("/test.html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.post("/submitform")
async def handle_form(search_query: str = Form(None), category: str = Form(None), facultad_name: List[str] = Form(None) ):
    print(search_query, category, facultad_name)
    query = '¿Qué es un adolescente?'
    result = elastic_pipe.run(query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 3}})
    print(result)
    return result