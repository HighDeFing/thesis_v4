from elasticsearch import Elasticsearch
import unidecode



es = Elasticsearch('http://localhost:9200')

value = "Manuel Enrique"
value = "veronica"
start_date = "2017-01-01"
end_date = "2022-12-31"

accented_string = 'Verónica'
# accented_string is of type 'unicode'

unaccented_string = unidecode.unidecode(accented_string)

print(unaccented_string.lower())

value = "antonio"

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

#print(resp)
#print(resp['hits'])
print("Got %d Hits:" % resp['hits']['total']['value'])
print(len(resp['hits']))
author_list = []
count = 0
for hit in resp['hits']['hits']:
    print("%(author_uncased)s" % hit["_source"])
    #print(len(hit))
    #print(hit)
    count += 1
    author_list.append(hit["_source"]['author_uncased'])

print([*set(author_list)])

print(count) 
#     print("%(author)s:" % hit["_source"])