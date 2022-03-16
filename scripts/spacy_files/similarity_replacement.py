#!/bin/env python
from black import main
import spacy
import json
from spacy import displacy
import unidecode
import pandas as pd
import numpy as np
import os


csv_source = "scripts/spacy_files/data/thesis_200_with_school.csv"
df = pd.read_csv(csv_source)
df = df[df['isScan']==False]
df = df.sort_values('isScan', ascending=False)

text1= "Escuela de Enfermería"

text2 = "ESCUELA DE ENFERMERIA"

file = open("scripts/spacy_files/data/escuelas.json", "r")
file = json.load(file)
temp_list = []
for facultad in file:
    temp_list.append(facultad['escuela'])
#print(facultad['escuela'])
escuelas = [item for sublist in temp_list for item in sublist] # make the list flat

#print(escuelas)

text1_u = unidecode.unidecode(text1)
text1_l_u = text1_u.lower()
text2_l_u = unidecode.unidecode(text2).lower()
print(text1_l_u, "<-->", text2_l_u)
if text1_l_u == text2_l_u:
    print(text1, "  is correct.")

def unaccent_list(accent_list):
        unaccented_schools = []
        for sch in accent_list:
            unaccented_schools.append(unidecode.unidecode(sch).lower())
        return unaccented_schools

def set_school_to_unaccent(escuelas):
        escuelas = unaccent_list(escuelas)
        return escuelas

def create_dictionary(schools):
    myDict = dict((e,i) for i,e in enumerate(schools))
    return myDict

def set_schools_accents(row, dict, dict_c):
    index = dict.get(row.lower())
    key_list = list(dict_c.keys())
    val_list = list(dict_c.values())

    try:
        position = val_list.index(index)
        key_list[position]
    except:
        return None

if __name__ == "__main__":
    u_escuelas = set_school_to_unaccent(escuelas)
    u_escuelas_dict = create_dictionary(u_escuelas)
    escuelas_dict = create_dictionary(escuelas)
    print(u_escuelas_dict)
    print(escuelas_dict)
    print(set_schools_accents("No school", u_escuelas_dict, escuelas_dict))




