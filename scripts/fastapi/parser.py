import json
from numpy import size


class Answer_result():
    def __init__(self, results):
        self.a = [x.to_dict() for x in results["answers"]]
        self.a_json = [x.to_json() for x in results["answers"]]

        self.a_json = [json.loads(x) for x in self.a_json]

        self.size_arr = len(self.a)

        self.answers = []
        self.context = []
        self.school = []
        self.offsets_in_context = []
        self.score = []
        for ans in self.a:
            self.answers.append(ans["answer"])
            self.context.append(ans["context"])
            self.school.append(ans["meta"])
            self.offsets_in_context.append(ans["offsets_in_context"])
            self.score.append(ans["score"])

    def get_school(self, index):
        #print(self.school[index]["school"])
        return self.school[index]["school"]

    def get_answer(self, index):
        return self.answers[index]

    def get_context(self, index):
        return self.context[index]

    def get_offsets_in_context(self, index):
        return self.offsets_in_context[index]

    def get_score(self, index):
        return self.score[index]

    def get_size(self):
        return self.size_arr

    def dict_object(self):
        return self.a

    def json_object(self):
        new_json = []
        for x in self.a_json:
            start = x['offsets_in_context'][0]['start']
            end = x['offsets_in_context'][0]['end']
            #print("start", start, "end:", end)
            new_word = x['context'][:start] + "<mark>" + x['context'][start:end] + "</mark>" + x['context'][end:]
            #print(new_word)
            x['context'] = new_word
            new_json.append(x)
        return new_json

class Document_result():
    def __init__(self, results):
        self.a = [x.to_dict() for x in results["documents"]]
        self.a_json = [x.to_json() for x in results["documents"]]

        self.a_json = [json.loads(x) for x in self.a_json]

        self.size_arr = len(self.a)
        #print(self.a_json)
        self.a_json = self.round_json()
    
    def round_json(self, round_by = 4):
        new_json = []
        for x in self.a_json:
            new_number = round(x['score'], round_by)
            x['score'] = new_number
            new_json.append(x)
        return new_json

    def json_object(self):
        return self.a_json


