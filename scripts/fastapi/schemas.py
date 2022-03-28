from fastapi import Form
from pydantic import BaseModel
from typing import List


class SearchForm(BaseModel):
    search_query: str
    category: str
    facultad_name: List[str]

    @classmethod
    def as_form(
        cls,
        search_query: str = Form(""),
        category: str = Form(""), 
        facultad_name: List[str] = Form([""])
    ):
        return cls(
            search_query = search_query,
            category = category,
            facultad_name = facultad_name
        )
