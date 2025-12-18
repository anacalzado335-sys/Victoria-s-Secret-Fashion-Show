import json
import os

class Resource: # maneja los recursos 
     def __init__(self,name, type):
         self.name = name 
         self.type = type 
     def __repr__(self):
         return f"Recursos necesarios: {self.name}, {self.type}"  
     
     #función para cargar datos del json
     def load_from_json(file_path=  "resources.json") -> list['Resource']:
         #lee el json y devuelve una lista de objetos resource
         try:
             with open(file_path, 'r') as file:
                 data = json.load(file) 
         except FileNotFoundError:
             print(f"El archivo {file_path} no ha sido encontrado")
             return[]
         
         resource_list  = []
         #iterara sobre las categorias 
         for category, items in data.items():
             if isinstance(items, list):
                 #iterar sobre cada elemento de la lista de categorias 
                 for item_name in items:
                     #instanciar Resource con el nombre del item ybla categoria
                     resource_obj = Resource(
                         name = item_name.strip(),
                         type = category 
                     ) 
                     resource_list.append*resource_obj
         return resource_list                