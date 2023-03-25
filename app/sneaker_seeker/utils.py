import json

class JsonReader:

    def __init__(self, fname: str = "config.json"):
        try:
            with open(fname) as json_file:
                data = json.load(json_file)
                for k, v in data.items():
                    setattr(self, k, v)
        except Exception as e:
            print(type(e), e, sep='\n')
            exit(-1)


def read_json(fname: str = 'config.json'):
    try:
        with open(fname) as json_file:
            return json.load(json_file)
    except Exception as e:
        print(type(e), e, sep='\n')



