from haystack_upload_files import Haystack_module

if __name__ == "__main__":
    elastic = Haystack_module()
    elastic.init_QAPipeline()
    elastic_pipe = elastic.get_QAPipeline()

    # documents = elastic.get_document_store()

    # document = documents.get_document_by_id('c518397269a6f3b6cda96c10284aeb31')
    # print(document.content)

    query = '¿Qué es un adolescente?'
    result = elastic_pipe.run(query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 3}})
    print(result)