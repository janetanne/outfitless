import requests

image_batch = requests.get('http://localhost:5000/upload.json')

batch = image_batch.json()

# to get the first three concepts in the JSON:

# first_concept = batch['outputs'][0]['data']['concepts'][0]['name']

# second_concept = batch['outputs'][0]['data']['concepts'][1]['name']

# third_concept = batch['outputs'][0]['data']['concepts'][2]['name']

# print("HARDCODED PULLS: {}, {}, {}".format(first_concept, second_concept, third_concept))

def get_concepts(_dict):
    """gets first three concepts for each item in batch upload"""
    counter = 0
    list_of_concepts = []

    while counter <= 2:
        concept = _dict['data']['concepts'][counter]['name']
        list_of_concepts.append(concept)
        counter +=1

    return list_of_concepts


for item in batch['outputs']:
    print("FUNCTION PULLS: {}".format(get_concepts(item)))
