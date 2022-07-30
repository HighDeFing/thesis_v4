from datetime import date, datetime
from fastapi import Body, Form
from pydantic import BaseModel
from typing import List
from datetime import datetime, time, timedelta
from typing import Union


class SearchForm(BaseModel):
    search_query: str
    query: str
    unique_res: bool
    search_author: str
    search_tutor: str
    start_date: str
    end_date: str
    facultad_name: List[str]
    
    @classmethod
    def as_form(
        cls,
        search_query: str = Form(""),
        query: str = Form(""),
        unique_res: bool = Form(False),
        search_author: str = Form(""),
        search_tutor: str = Form(""),
        facultad_name: List[str] = Form([""]),
        start_date: str = Form(""),
        end_date: str = Form("")


    ):
        return cls(
            search_query = search_query,
            query = query,
            unique_res = unique_res,
            search_author = search_author,
            search_tutor = search_tutor,
            facultad_name = facultad_name,
            start_date = start_date,
            end_date = end_date
        )

class SearchSimpleForm(BaseModel):
    query: str
    
    @classmethod
    def as_form(
        cls,
        query: str = Form("")

    ):
        return cls(
            query = query
        )
