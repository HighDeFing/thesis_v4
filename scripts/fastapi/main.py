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
from datetime import datetime, date
from elasticsearch import Elasticsearch
import json
import unidecode


es = Elasticsearch('http://localhost:9200')



f = open('web/static/data/escuelas.json')
data = json.load(f)

model_path = "../../notebooks/models/model_big"

model_9 = '../../notebooks/models/model_9'
model_10 = '../../notebooks/models/model_10'

model_4 = '../../notebooks/models/model_4'
model_6 = '../../notebooks/models/model_6'

# Dense retriever

#hyperparameters
# haystack = Haystack_module(option="Dense", pipe_line_op = "document", dense_model_path=model_9)
# haystack = Haystack_module(option="Dense", pipe_line_op = "document", dense_model_path=model_10)
# haystack = Haystack_module(option="Dense", pipe_line_op = "document", dense_model_path=model_4)
# haystack = Haystack_module(option="Dense", pipe_line_op = "document", dense_model_path=model_6)

#barebones

haystack = Haystack_module(option="Dense", pipe_line_op = "document")


#Elastic search retriever
#haystack = Haystack_module(option="ES", pipe_line_op = "document")


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

def get_list_elastic(option, name, start_date, end_date):
    if option == "author":
        search_author = name
        search_author = unidecode.unidecode(search_author)
        search_author = search_author.lower()
        value = search_author

        resp = es.search(index="document", size=10000, query={
            "bool": {
                "must": {
                    "wildcard": {
                    "author_uncased": {
                        "value": "*" + value + "*"
                            }
                        }
                    },
                    "filter":{
                        "range": {
                        "year" : {"gt": start_date, "lt": end_date}
                        }
                    }
                }
            },
            _source =  [
                    "author",
                    "author_uncased",
                    "content",
                    "path",
                    "school",
                    "size",
                    "title",
                    "year"
                ]
        )
        #this is the author list that searches in elastic search.
        author_list = []
        for hit in resp['hits']['hits']:
            #print("%(author_uncased)s" % hit["_source"])
            #print(len(hit))
            #print(hit)
            #count += 1
            author_list.append(hit["_source"]['author_uncased'])
        author_list = [*set(author_list)]
        return author_list
    if option == "tutor":
        search_tutor = name
        search_tutor = unidecode.unidecode(search_tutor)
        search_tutor = search_tutor.lower()
        value = search_tutor

        resp = es.search(index="document", size=10000, query={
            "bool": {
                "must": {
                    "wildcard": {
                    "tutor_uncased": {
                        "value": "*" + value + "*"
                            }
                        }
                    },
                    "filter":{
                        "range": {
                        "year" : {"gt": start_date, "lt": end_date}
                        }
                    }
                }
            },
            _source =  [
                    "tutor",
                    "tutor_uncased",
                    "content",
                    "path",
                    "school",
                    "size",
                    "title",
                    "year"
                ]
        )
        #this is the author list that searches in elastic search.
        tutor_list = []
        for hit in resp['hits']['hits']:
            #print("%(author_uncased)s" % hit["_source"])
            #print(len(hit))
            #print(hit)
            #count += 1
            tutor_list.append(hit["_source"]['tutor_uncased'])
        tutor_list = [*set(tutor_list)]
        return tutor_list



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

@app.get("/results.html//{unique_res}////{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html//{unique_res}/{search_tutor}/{search_author}/{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html//{unique_res}/{search_tutor}//{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html/{search_query}/{unique_res}/{search_tutor}/{search_author}/{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html/{search_query}/{unique_res}//{search_author}/{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html/{search_query}/{unique_res}/{search_tutor}//{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html/{search_query}/{unique_res}///{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html/{search_query}?/{unique_res}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html/{search_query}/{unique_res}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html//{unique_res}///{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html//{unique_res}//{search_author}/{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.get("/results.html//{unique_res}/{facultad_name}", response_class=HTMLResponse)
async def read_item(request: Request, search_query: Optional[str] = Query(None), unique_res: Optional[bool] = Query(None), search_author: Optional[str] = Query(None), search_tutor: Optional[str] = Query(None), start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None), facultad_name: Optional[str] = Query(None)):
    #print(search_query)
    #print(facultad_name) , #"filters": {"school":facultad_name}
    #print("in result", search_author)
    #print("in result", search_tutor)

    if facultad_name:
        schools = parse_schools(facultad_name)
    else:
        schools = []
        for facultad in data:
            for sch in facultad['escuelas']:
                schools.append(sch)
    #print(schools)
    query = search_query
    #print(facultad_name[1])
    #result = document_pipe.run(query, params={"Retriever": {"top_k": 100}})
    #print_documents(result, max_text_len=500, print_name=True, print_meta=True)
    #result = elastic_pipe.run(query=query, params={"Retriever": {"top_k": 10, "filters": {"school": schools}}, "Reader": {"top_k": 3}})
    print(start_date)
    if(start_date == None):
        start_date = "2000-01-01"
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = datetime.strftime(start_date, "%Y-%m-%d")

    if(end_date == None):
       end_date = date.today()
       end_date = datetime.strftime(end_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    end_date = datetime.strftime(end_date, "%Y-%m-%d")

    #print("in result", start_date)
    #print("in result", end_date)

    filter_tap = { 
        "$and": {
           "school": schools,
           "year": {"$gt": start_date, "$lt": end_date}
        }
    }

    if query == None:
        query = "Universidad"

        
    if search_author != None and search_tutor==None:
        author_list = get_list_elastic(option="author", name=search_author, start_date=start_date, end_date=end_date)
        filter_tap = { 
        "$and": {
           "school": schools,
           "year": {"$gt": start_date, "$lt": end_date},
           "author_uncased" : {"$in": author_list}
            }
        }

    if search_tutor != None and search_author == None:
        tutor_list = get_list_elastic(option="tutor", name=search_tutor, start_date=start_date, end_date=end_date)
        filter_tap = { 
        "$and": {
           "school": schools,
           "year": {"$gt": start_date, "$lt": end_date},
           "tutor_uncased" : {"$in": tutor_list}
            }
        }

    if search_tutor != None and search_author != None:
        author_list = get_list_elastic(option="author", name=search_author, start_date=start_date, end_date=end_date)
        tutor_list = get_list_elastic(option="tutor", name=search_tutor, start_date=start_date, end_date=end_date)
        filter_tap = { 
        "$and": {
           "school": schools,
           "year": {"$gt": start_date, "$lt": end_date},
           "tutor_uncased" : {"$in": tutor_list},
           "author_uncased" : {"$in": author_list}
            }
        }
        

        #print("author_list", author_list)


    # result = document_pipe.run(query=query, params={"Retriever": {"top_k": 15}, "filters": {"school": schools}}
    result = document_pipe.run(query=query, params={"Retriever": {"top_k": 15}, "filters": filter_tap})

    #print_answers(result, details="all", max_text_len=200)
    #print_documents(result, max_text_len=100, print_name=True, print_meta=True)
    #ansObj = Answer_result(result)
    #ansObj = ansObj.json_object()
    #print(result)
    ansObj = Document_result(result)
    if(unique_res):
        ansObj.make_unique_results()
    ansObj = ansObj.json_object()
    #print(ansObj)
    #ansObj = "something"

    #print("data:", type(ansObj))

    # for res in ansObj:
    #     print("res:", res)

    return templates.TemplateResponse("results.html", {"request": request, "respuestas": ansObj})

@app.post("/results.html//{unique_res}////{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html//{unique_res}/{search_tutor}/{search_author}/{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html//{unique_res}/{search_tutor}//{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html/{search_query}/{unique_res}/{search_tutor}/{search_author}/{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html/{search_query}/{unique_res}//{search_author}/{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html/{search_query}/{unique_res}/{search_tutor}//{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html/{search_query}/{unique_res}///{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html/{search_query}?/{unique_res}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html/{search_query}/{unique_res}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html//{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html//{unique_res}///{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html//{unique_res}//{search_author}/{start_date}/{end_date}/{facultad_name}", response_class=HTMLResponse)
@app.post("/results.html//{unique_res}/{facultad_name}", response_class=HTMLResponse)
async def handle_form(request: Request, form_data:  SearchSimpleForm = Depends(SearchSimpleForm.as_form)):
    #print(form_data)
    search_query = form_data.query
    schools = []
    for facultad in data:
        for sch in facultad['escuela']:
            schools.append(sch)
    facultad_name = schools
    unique_res = True
    if search_query == "":
        search_query = "Universidad"
        #search in all schools if none is giving
    #headers={"form_data": form_data}
    return RedirectResponse(f"/results.html/{search_query}/{unique_res}/{facultad_name}",  status_code=303)

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
    #print(query)
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

    search_tutor = form_data.search_tutor
    search_author = form_data.search_author
    start_date = form_data.start_date
    end_date = form_data.end_date
    unique_res = form_data.unique_res
    #print(unique_res)
    if start_date == "":
        start_date = "2000-01-01"
    if end_date == "":
        end_date = date.today()
        end_date = datetime.strftime(end_date, "%Y-%m-%d")

        #search in all schools if none is giving
    #headers={"form_data": form_data}
    return RedirectResponse(f"/results.html/{search_query}/{unique_res}/{search_tutor}/{search_author}/{start_date}/{end_date}/{facultad_name}",  status_code=303)

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