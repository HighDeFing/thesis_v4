from fastapi import Form
from pydantic import BaseModel
from typing import List


class SearchForm(BaseModel):
    search_query: str
    query: str
    category: str
    facultad_name: List[str]
    
    @classmethod
    def as_form(
        cls,
        search_query: str = Form(""),
        query: str = Form(""),
        category: str = Form(""), 
        facultad_name: List[str] = Form([""])

    ):
        return cls(
            search_query = search_query,
            query = query,
            category = category,
            facultad_name = facultad_name
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
