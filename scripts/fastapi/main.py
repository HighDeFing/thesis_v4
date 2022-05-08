from email import header
from wsgiref import headers
from typing import Optional, List
import json
from fastapi import FastAPI, Query, Header, Request, File, Form, UploadFile, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from scripts.haystack_files.haystack_upload_files import Haystack_module
from haystack.utils import print_answers, print_documents
from schemas import SearchForm, SearchSimpleForm
from parser import Answer_result, Document_result

import json

f = open('web/static/data/escuelas.json')
data = json.load(f)

model_path = "../../notebooks/models/model_big"

# Dense retriever
#haystack = Haystack_module(option="Dense", pipe_line_op = "document", dense_model_path=model_path)

#Elastic search retriever
haystack = Haystack_module(option="ES", pipe_line_op = "document")

#haystack.init_QAPipeline()
#elastic_pipe = haystack.get_QAPipeline()
#etriever = haystack.get_Dense_retriever()
document_pipe = haystack.get_DocumentSearchPipeline()


def parse_schools(school_strings):
    #print(school_strings[1])
    #delete []
    disallowed_characters = "[']'"
    for character in disallowed_characters:
        school_strings = school_strings.replace(character, "")
    #tokenizer
    school_strings = school_strings.split(',')
    new_schools = []
    # delete blanks
    for schools in school_strings:
        new_schools.append(schools.strip())

    #print(new_schools)
    return(new_schools)


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

@app.get("/results.html/{search_query}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html/{search_query}?/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html//{facultad_name}", response_class=HTMLResponse)
async def read_item(request: Request, search_query: Optional[str] = Query(None), facultad_name: Optional[str] = Query(None)):
    #print(search_query)
    #print(facultad_name) , #"filters": {"school":facultad_name}
    if facultad_name:
        schools = parse_schools(facultad_name)
    else:
        schools = []
        for facultad in data:
            for sch in facultad['escuelas']:
                schools.append(sch)
    print(schools)
    query = search_query
    #print(facultad_name[1])
    #result = document_pipe.run(query, params={"Retriever": {"top_k": 100}})
    #print_documents(result, max_text_len=500, print_name=True, print_meta=True)
    #result = elastic_pipe.run(query=query, params={"Retriever": {"top_k": 10, "filters": {"school": schools}}, "Reader": {"top_k": 3}})
    result = document_pipe.run(query=query, params={"Retriever": {"top_k": 10}})
    #print_answers(result, details="all", max_text_len=200)
    #print_documents(result, max_text_len=100, print_name=True, print_meta=True)
    #ansObj = Answer_result(result)
    #ansObj = ansObj.json_object()
    ansObj = Document_result(result)
    ansObj = ansObj.json_object()
    #ansObj = "something"

    #print("data:", type(ansObj))

    # for res in ansObj:
    #     print("res:", res)

    return templates.TemplateResponse("results.html", {"request": request, "respuestas": ansObj})

@app.post("/results.html/{search_query}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html//{facultad_name}", response_class=HTMLResponse)
async def handle_form(request: Request, form_data:  SearchSimpleForm = Depends(SearchSimpleForm.as_form)):
    #print(form_data)
    search_query = form_data.query

    schools = []
    for facultad in data:
        for sch in facultad['escuela']:
            schools.append(sch)
    facultad_name = schools

        #search in all schools if none is giving
    #headers={"form_data": form_data}
    return RedirectResponse(f"/results.html/{search_query}/{facultad_name}",  status_code=303)

@app.get("/search", response_class=HTMLResponse)
@app.get("/search.html", response_class=HTMLResponse)
async def read_item(request: Request):
    #print("data:", type(data))
    return templates.TemplateResponse("search.html", {"request": request, "escuelas": data})

@app.post("/search", response_class=HTMLResponse)
@app.post("/search.html", response_class=HTMLResponse)
async def handle_form(request: Request, form_data:  SearchForm = Depends(SearchForm.as_form)):
    #print(form_data)
    search_query = form_data.search_query
    query = form_data.query
    if search_query:
        pass
    else:
        search_query = query
    if query:
        search_query = query
    facultad_name = form_data.facultad_name
    if facultad_name != [""]:
        pass
    else:
        schools = []
        for facultad in data:
            for sch in facultad['escuela']:
                schools.append(sch)
        facultad_name = schools

        #search in all schools if none is giving
    #headers={"form_data": form_data}
    return RedirectResponse(f"/results.html/{search_query}/{facultad_name}",  status_code=303)

@app.get("/test.html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

# @app.post("/submitform")
# async def handle_form(search_query: str = Form(None), category: str = Form(None), facultad_name: List[str] = Form(None) ):
#     print(search_query, category, facultad_name)
#     #query = '¿Qué es un adolescente?'
#     #result = elastic_pipe.run(query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 3}})
#     #print(result)
#     #return result