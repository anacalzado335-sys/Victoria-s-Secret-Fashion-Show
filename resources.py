import json

resources = {
    "Models" : ["Adriana Lima ", "Gigi Hadid", "Bella Hadid", "Hayley Bieber", "Naomi Cambell", "Martha Hunt"],
    "places" : ["Steiner Studio", "Mercedes-Benz Arena ", "Grand Palais","Pier 94"]
}

#de esta forma creo y leo el json 
with open("resources.json" , 'w') as outfile:
     json.dump(resources, outfile)
with open("resources,json") as file:
    data_resources = json.load(file)     