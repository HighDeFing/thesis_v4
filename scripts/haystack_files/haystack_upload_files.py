from haystack.nodes import PDFToTextConverter
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline, DocumentSearchPipeline
from haystack.nodes import PreProcessor
import json
import pdfplumber
import spacy
import pandas as pd
import numpy as np
import os
import unidecode
from scripts.progress_bar.progress_bar import printProgressBar


class Haystack_module():
    def __init__(self):
        self.document_store = ElasticsearchDocumentStore(similarity="dot_product")
        self.retriever = DensePassageRetriever(
        document_store=self.document_store,
        query_embedding_model="voidful/dpr-question_encoder-bert-base-multilingual",
        passage_embedding_model="sadakmed/dpr-passage_encoder-spanish",
        use_gpu=True
    )
        self.reader = FARMReader("mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es", use_gpu=True)
        self.qa_pipe = ExtractiveQAPipeline(reader=self.reader, retriever=self.retriever)
        pass

    
    def write_file_in_elastic(self, file_source, school, title, author, year, size, path):
        meta_data = { "school": str(school), "title": str(title), "author": str(author), "year": str(year), "size": str(size), "path": str(path) }
        # print(meta_data)
        converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["es"])
        docs = converter.convert(file_path=file_source, meta=meta_data)

        pre_docs = docs
        #self.init_preProcessor()
        #processor = self.get_preProcessor()
        #pre_docs = processor.process(docs)

        self.document_store.write_documents(pre_docs)
        self.document_store.update_embeddings(self.retriever)

    def init_QAPipeline(self):
        self.qa_pipe = ExtractiveQAPipeline(reader=self.reader, retriever=self.retriever)

    def init_DocumentSearchPipeline(self):
        self.document_search_pipe = DocumentSearchPipeline(retriever=self.retriever)

    def get_DocumentSearchPipeline(self):
        return self.document_search_pipe

    def get_QAPipeline(self):
        return self.qa_pipe

    def init_preProcessor(self):
        self.processor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=True,
            split_by="passage",
            split_length=200,
            split_respect_sentence_boundary=False,
            split_overlap=0
        )

    def get_preProcessor(self):
        return self.processor


if __name__ == "__main__":
    elastic = Haystack_module()

    csv_source = "scripts/haystack_files/data/thesis_200_with_resumen_school_complex.csv"
    df = pd.read_csv(csv_source)
    df_head = df.copy()
    df_head = df_head.head(2)

    #print(df_head['path'].values[1])

    elastic.write_file_in_elastic(df_head['path'].values[0], df_head["school_complex"].values[0],
     df_head["thesis_title"].values[0], df_head["thesis_author"].values[0], df_head["thesis_year"]
     .values[0], df_head["size"].values[0], df_head["path"].values[0])

    elastic.init_QAPipeline()
    elastic.init_DocumentSearchPipeline()

    elastic_pipe = elastic.get_QAPipeline()
    elastic_search_pipe = elastic.get_DocumentSearchPipeline()

    query = '¿Qué es un adolescente?'
    result = elastic_pipe.run(query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 3}})
    ##result_2 = elastic_search_pipe.run(query=query)
    #elastic_pipe.draw()
    print(result)
    ##print(result_2)





