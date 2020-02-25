import twitter2
import json

path = 'twitter_result.json'
class_you_need = input('Enter a class you want to search:')
js = set()
with open(path, encoding='utf-8') as f:
    data = json.load(f)

def reading_json(data1, class_you_need1):
    """
    (str) -> (dict)
    this function creates a dictionary that contains information
    about group, division and section of a class that user gives us 
    as an input
    """
    if type(data1) is dict:
        for key in data1:
            if key == class_you_need1:
                js.add(data1[key])
            reading_json(data1[key], class_you_need1)
    if type(data1) is list:
        for i in data1:
            reading_json(i, class_you_need1)
    return js
print(reading_json(data, class_you_need))