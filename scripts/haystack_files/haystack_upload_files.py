from haystack.nodes import PDFToTextConverter
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import FARMReader, ElasticsearchRetriever
from haystack.pipelines import ExtractiveQAPipeline, DocumentSearchPipeline
from haystack.nodes import PreProcessor
from haystack import Document
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

        # self.initBM25_retriver()
        self.initDense__retriver()

        #self.retriever = self.get_BM25()
        self.retriever = self.get_DPR(self)
        self.reader = FARMReader("mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es", use_gpu=False)
        self.qa_pipe = ExtractiveQAPipeline(reader=self.reader, retriever=self.retriever)

    def initDense__retriver(self):
        self.dp_retriver = DensePassageRetriever(
        document_store=self.document_store,
        query_embedding_model="voidful/dpr-question_encoder-bert-base-multilingual",
        passage_embedding_model="sadakmed/dpr-passage_encoder-spanish",
        use_gpu=False
        )

    def get_DPR(self):
        return self.dp_retriver

    def initBM25_retriver(self):
        self.bm25_retriver = ElasticsearchRetriever(self.document_store)

    def get_BM25(self):
        return self.bm25_retriver

    def write_file_in_elastic(self, file_source, school, title, author, year, size, path, resumen):
        meta_data = { "school": str(school), "title": str(title), "author": str(author), "year": str(year), "size": str(size), "path": str(path), "resumen": str(resumen) }
        # print(meta_data)
        converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["es"])
        docs = converter.convert(file_path=file_source, meta=meta_data)


        # text = """d A cu m u lad a (% )\n\n\n\n\n\n\n\n\n\n\nV alor m xim o de tensin fase-tierra (en p.u)\n\nValor m xim o de tensin fas e-tierra (e n p.u)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nP ro b ab ilid ad A cu m u lad a ( % )\n\n\x0cProbabilida d Acum ulada\n(Ba rra 115kV fa se "C" - S/E Te m bla dor)\n\nProbabilidad Acumulada\n(Barra 34,5kV fase "C" - S/E Tucupita)\n\n\n\nPro b ab ilid ad Acu m u lad a (% )\n\nProbabilidad Acumulada (%)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nProba bilidad Acumulada\n(Barra 13,8kV fase "C" - S/E Barra ncas)\n\nProba bilidad Acumulada\n(Ba rra 13,8kV fa se "B" - S/E Tucupita)\n\n\nProbabilidad Acumulada (%)\n\nProbabilidad Acumulada (%)\n\n\nV alor m xim o de te ns in fase -tier ra (en p.u)\n\nValor m xim o de te ns in fas e -tie rra (e n p.u)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nV alor m xim o de te ns in fas e -tie rra (e n p.u)\n\n\n\nValor m xim o de te ns in fas e -tie rra (e n p.u)\n\nA.26.3 Distribucin estadstica de probabilidad de ocurrencia de sobretensiones para\nenergizacin de lneas de transmisin (CASO 1)\n\nHistogram a S/E Ba rranca s Barra 115kV\n\n\n\nProbabilidad Ocurrencia (%)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nProbabilidad Ocurrencia (%)\n\nHistogra ma S/E Palital Ba rra 115kV\n\nInte rvalo de s obre te ns in fas e -tie rr a "Fas e A" (p.u)\n\nInte r valo de s obr e te ns in fas e -tie rr a "Fas e B" (p.u)\n\n\x0cHistograma S/E Temblador Barra 115kV\n\n\n\nP ro b a b ilida d O c ur re n c ia (% )\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nProbabilidad Ocurrencia (% )\n\nHistograma S/E Tucupita Barra 115kV\n\n\nIntervalo de s obretensin fas e-tie rra "Fas e C" (p.u)\n\nHistogra ma S/E Tucupita Ba rra 34,5kV\n\nProbabilidad Ocurrencia (%)\n\n\nProbabilidad Ocurrencia (%)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nInte r valo de s obr e te ns in fas e -tie r ra "Fas e C" (p.u)\n\nHistogra ma S/E Ba rra nca s Ba rra 13,8kV\n\n\n\nInte rvalo de s obre te ns in fas e -tie r ra "Fas e B" (p.u)\n\n\nProbabilidad Ocurrencia (%)\n\n\nHistogra ma S/E Tucupita Ba rra 13,8kV\n\n\n\nInte rvalo de s obre"""
        # print(text.replace('\n',""))

        new_docs = self.clean_break_line(docs)
        pre_docs = new_docs

        #file_text = pre_docs.strip()
        #print(file_text)
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

    def clean_break_line(self, docs):
        aux_content = []
        new_docs = []
        for pre_docs in docs:
            #print(pre_docs["content"].replace('\n',""))
            aux_meta = pre_docs["meta"]
            aux_content = pre_docs["content"].replace('\n',"")
            new_docs.append(Document(aux_content, aux_meta))
        return new_docs


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

    def write_files_from_csv(self, csv_source):
        df = pd.read_csv(csv_source)
        df_head = df.copy()

        write_vec = np.vectorize(self.write_file_in_elastic)

        write_vec(df_head['path'], df_head["school_complex"],
        df_head["thesis_title"], df_head["thesis_author"], df_head["thesis_year"],
        df_head["size"], df_head["path"], df_head["resumen"])


if __name__ == "__main__":
    elastic = Haystack_module()
    csv_source = "scripts/haystack_files/data/thesis_200_with_resumen_school_complex.csv"
    elastic.write_files_from_csv(csv_source)

    #df = pd.read_csv(csv_source)
    #df_head = df.copy()
    #df_head = df_head.head(2)

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





