from haystack.nodes import PDFToTextConverter
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import FARMReader, ElasticsearchRetriever
from haystack.pipelines import ExtractiveQAPipeline, DocumentSearchPipeline
from haystack.nodes import PreProcessor
from haystack.nodes import ElasticsearchRetriever, BM25Retriever
from haystack import Document
import json
import pdfplumber
#import spacy
import pandas as pd
import numpy as np
import os
import unidecode
from scripts.progress_bar.progress_bar import printProgressBar

model_path = './notebooks/models/model_big'
model_9 = './notebooks/models/model_9'
model_10 = './notebooks/models/model_10'

model_4 = './notebooks/models/model_4'
model_6 = './notebooks/models/model_6'

class Haystack_module():
    def __init__(self, option = "ES", pipe_line_op = "document", dense_model_path = ""):
        self.document_store = ElasticsearchDocumentStore(similarity="dot_product")

        #select an option for retriever
        if option == "Dense":
            self.init_Dense_retriever(document_store=self.document_store, save_dir=dense_model_path)
            retriever = self.get_Dense_retriever()
        if option == "ES":
            self.init_ES_retriever(self.document_store)
            retriever = self.get_ES_retriever()
        
        # get the reader
        #self.init_FARMReader()
        #reader =  self.get_FARMReader()
        
        #set preprocess files
        self.init_preProcessor()

        #Establish pipeline
        if pipe_line_op == "document":
            self.init_DocumentSearchPipeline(retriever)
        if pipe_line_op == "qa":
            # get the reader
            self.init_FARMReader()
            reader =  self.get_FARMReader()
            self.init_QAPipeline(retriever = retriever, reader = reader)

        #self.qa_pipe = ExtractiveQAPipeline(reader=reader, retriever=retriever)

    # Document Store
    def get_document_store(self):
        return self.document_store

    #Retrivers
    #Elastic Search retriever
    def init_ES_retriever(self, document_store):
        self.es_retriever = BM25Retriever(document_store=document_store)

    def get_ES_retriever(self):
        return self.es_retriever

    #Dense retriever
    def init_Dense_retriever(self, document_store, save_dir=""):

        if not save_dir:
            self.dp_retriever = DensePassageRetriever(
            document_store=document_store,
            query_embedding_model="IIC/dpr-spanish-question_encoder-allqa-base",  #IIC/dpr-spanish-question_encoder-allqa-base #voidful/dpr-question_encoder-bert-base-multilingual
            passage_embedding_model="IIC/dpr-spanish-passage_encoder-allqa-base", #IIC/dpr-spanish-passage_encoder-allqa-base #voidful/dpr-ctx_encoder-bert-base-multilingual
            use_gpu=True,
            batch_size = 64
            )
        else:
            #load fine tuned model
            #print("THIS IS THE MODEL")
            print(save_dir)
            self.dp_retriever = DensePassageRetriever.load(load_dir=save_dir, document_store=document_store, use_gpu=True)


    def get_Dense_retriever(self):
        return self.dp_retriever

    #Readers
    def init_FARMReader(self):
        self.FARM_reader = FARMReader("mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es", use_gpu=True)

    def get_FARMReader(self):
        return self.FARM_reader


    def write_file_in_elastic(self, document_store, retriever, option, file_source, school, title, author, year, size, path):
        meta_data = { "school": str(school), "title": str(title), "author": str(author), "year": str(year), "size": str(size), "path": str(path) }
        # print(meta_data)
        converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["es"])
        docs = converter.convert(file_path=file_source, meta=meta_data)


        # text = """d A cu m u lad a (% )\n\n\n\n\n\n\n\n\n\n\nV alor m xim o de tensin fase-tierra (en p.u)\n\nValor m xim o de tensin fas e-tierra (e n p.u)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nP ro b ab ilid ad A cu m u lad a ( % )\n\n\x0cProbabilida d Acum ulada\n(Ba rra 115kV fa se "C" - S/E Te m bla dor)\n\nProbabilidad Acumulada\n(Barra 34,5kV fase "C" - S/E Tucupita)\n\n\n\nPro b ab ilid ad Acu m u lad a (% )\n\nProbabilidad Acumulada (%)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nProba bilidad Acumulada\n(Barra 13,8kV fase "C" - S/E Barra ncas)\n\nProba bilidad Acumulada\n(Ba rra 13,8kV fa se "B" - S/E Tucupita)\n\n\nProbabilidad Acumulada (%)\n\nProbabilidad Acumulada (%)\n\n\nV alor m xim o de te ns in fase -tier ra (en p.u)\n\nValor m xim o de te ns in fas e -tie rra (e n p.u)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nV alor m xim o de te ns in fas e -tie rra (e n p.u)\n\n\n\nValor m xim o de te ns in fas e -tie rra (e n p.u)\n\nA.26.3 Distribucin estadstica de probabilidad de ocurrencia de sobretensiones para\nenergizacin de lneas de transmisin (CASO 1)\n\nHistogram a S/E Ba rranca s Barra 115kV\n\n\n\nProbabilidad Ocurrencia (%)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nProbabilidad Ocurrencia (%)\n\nHistogra ma S/E Palital Ba rra 115kV\n\nInte rvalo de s obre te ns in fas e -tie rr a "Fas e A" (p.u)\n\nInte r valo de s obr e te ns in fas e -tie rr a "Fas e B" (p.u)\n\n\x0cHistograma S/E Temblador Barra 115kV\n\n\n\nP ro b a b ilida d O c ur re n c ia (% )\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nProbabilidad Ocurrencia (% )\n\nHistograma S/E Tucupita Barra 115kV\n\n\nIntervalo de s obretensin fas e-tie rra "Fas e C" (p.u)\n\nHistogra ma S/E Tucupita Ba rra 34,5kV\n\nProbabilidad Ocurrencia (%)\n\n\nProbabilidad Ocurrencia (%)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nInte r valo de s obr e te ns in fas e -tie r ra "Fas e C" (p.u)\n\nHistogra ma S/E Ba rra nca s Ba rra 13,8kV\n\n\n\nInte rvalo de s obre te ns in fas e -tie r ra "Fas e B" (p.u)\n\n\nProbabilidad Ocurrencia (%)\n\n\nHistogra ma S/E Tucupita Ba rra 13,8kV\n\n\n\nInte rvalo de s obre"""
        # print(text.replace('\n',""))

        #print(docs[0].meta)
        #new_docs = self.clean_break_line(docs)
        preProcessor = self.get_preProcessor()
        new_docs = preProcessor.process(docs)
        #print(new_docs)
        #print(new_docs[1]["meta"])
        new_docs = self.clean_break_line(new_docs)
        pre_docs = new_docs

        #print(new_docs)

        #file_text = pre_docs.strip()
        #print(file_text)
        #self.init_preProcessor()
        #processor = self.get_preProcessor()
        #pre_docs = processor.process(docs)

        document_store.write_documents(pre_docs)
        if option == "dense":
            document_store.update_embeddings(retriever)
        

    #PipeLines
    #QA Pipeline
    def init_QAPipeline(self, reader, retriever):
        self.qa_pipe = ExtractiveQAPipeline(reader=reader, retriever=retriever)

    def get_QAPipeline(self):
        return self.qa_pipe

    #Document PipeLine
    def init_DocumentSearchPipeline(self, retriever):
        self.document_search_pipe = DocumentSearchPipeline(retriever=retriever)

    def get_DocumentSearchPipeline(self):
        return self.document_search_pipe

    def clean_break_line(self, docs):
        aux_content = []
        new_docs = []
        for pre_docs in docs:
            #print(pre_docs["content"].replace('\n',""))
            aux_meta = pre_docs.meta
            aux_content = pre_docs.content.replace('\n',"")
            new_docs.append(Document(content=aux_content, meta=aux_meta))
        #print(new_docs)
        return new_docs

    def init_preProcessor(self):
        self.processor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            split_by="word",
            split_length=400,
            split_respect_sentence_boundary=True,
            split_overlap=0,
            language="es"
        )

    def get_preProcessor(self):
        return self.processor

    def write_files_from_csv_Dense(self, csv_source):
        df = pd.read_csv(csv_source)
        df_head = df.copy()

        write_vec = np.vectorize(self.write_file_in_elastic)

        document_store = self.get_document_store()
        #self.init_Dense_retriever(document_store)
        retriever = self.get_Dense_retriever()
        option = "dense" 
        
        write_vec(document_store = document_store, retriever = retriever, option = option, 
        file_source = df_head['path'], school = df_head["school_complex"], title = df_head["thesis_title"],
        author = df_head["thesis_author"], year = df_head["thesis_year"], size = df_head["size"], path = df_head["path"])

    def write_files_from_csv_Sparse(self, csv_source):
        df = pd.read_csv(csv_source)
        df_head = df.copy()

        write_vec = np.vectorize(self.write_file_in_elastic)

        document_store = self.get_document_store()
        retriever = self.get_ES_retriever()
        option = "sparse" 

        write_vec(document_store = document_store, retriever = retriever, option = option, 
        file_source = df_head['path'], school = df_head["school_complex"], title = df_head["thesis_title"],
        author = df_head["thesis_author"], year = df_head["thesis_year"], size = df_head["size"], path = df_head["path"])


if __name__ == "__main__":

    csv_source = "scripts/haystack_files/data/thesis_comp_ingelec_quimica.csv"

    ## BM25 
    # elastic = Haystack_module(option="ES")
    # elastic.write_files_from_csv_Sparse(csv_source)

    ## Bare bones
    # elastic = Haystack_module(option="Dense")
    # elastic.write_files_from_csv_Dense(csv_source)

    ## model_4
    #elastic = Haystack_module(option="Dense", dense_model_path=model_4)
    #elastic.write_files_from_csv_Dense(csv_source)

    ## model_6
    #elastic = Haystack_module(option="Dense", dense_model_path=model_6)
    #elastic.write_files_from_csv_Dense(csv_source)

    ## model_9
    # elastic = Haystack_module(option="Dense", dense_model_path=model_9)
    # elastic.write_files_from_csv_Dense(csv_source)

    ## model_10
    elastic = Haystack_module(option="Dense", dense_model_path=model_10)
    elastic.write_files_from_csv_Dense(csv_source)

    #model_9
    # model_path = model_9
    # elastic = Haystack_module(option="Dense", dense_model_path=model_path)
    # elastic = Haystack_module(option="Dense")
    # #csv_source = "scripts/haystack_files/data/thesis_30_computacion.csv"
    # csv_source = "scripts/haystack_files/data/thesis_comp_ingelec_quimica.csv"
    # elastic.write_files_from_csv_Dense(csv_source)

    # df = pd.read_csv(csv_source)
    # df_head = df.copy()
    # df_head = df_head.head(2)

    #print(df_head['path'].values[1])

    # write_vec = np.vectorize(elastic.write_file_in_elastic)

    # write_vec(df_head['path'], df_head["school_complex"],
    # df_head["thesis_title"], df_head["thesis_author"], df_head["thesis_year"],
    # df_head["size"], df_head["path"], df_head["resumen"])

    # elastic.write_file_in_elastic(df_head['path'].values[0], df_head["school_complex"].values[0],
    # df_head["thesis_title"].values[0], df_head["thesis_author"].values[0], df_head["thesis_year"]
    # .values[0], df_head["size"].values[0], df_head["path"].values[0], df_head["resumen"].values[0])

    # elastic.init_QAPipeline()
    # elastic.init_DocumentSearchPipeline()

    # elastic_pipe = elastic.get_QAPipeline()
    # elastic_search_pipe = elastic.get_DocumentSearchPipeline()

    # query = '¿Qué es un adolescente?'
    # result = elastic_pipe.run(query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 3}})
    # ##result_2 = elastic_search_pipe.run(query=query)
    # #elastic_pipe.draw()
    # print(result)
    ##print(result_2)





