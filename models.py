import json
from datetime import datetime, timedelta

class Event : # representa un evento planificado
     def __init__(self,id:int ,name : str, begin:str, end : str, assigned_events= None ):
         self.id = id
         self.name = name
         self.begin = datetime.strptime(begin.strip(), "%Y-%m-%d %H:%M:%S") #aquí esas cosas solo reperesentan el dia , mes y año , lo mismo en los de abajo , eso solo es para que sean bjetos de datetime y sea mas facil trabajar con 6
         self.end = datetime.strptime(end.strip(), "%Y-%m-%d %H:%M:%S")
         self.assigned_events = assigned_events #puede estar vacío o no estarlo
         
     def duration(self) -> timedelta: #duración del evento
         return self.end - self.begin 
    
     def __repr__(self):
         return f"Evento(nombre : '{self.name}',\n comienza: {self.begin.strftime("%Y-%m-%d %H:%M:%S")}, \n termina: {self.end.strftime("%Y-%m-%d %H:%M:%S")})"


def load_events_from_json(file_path = "events.json") -> list['Event'] :
         try:
             with open(file_path, 'r') as file :
                 data = json.load(file)
         except FileNotFoundError:
             print(f"ERROR: El archivo {file_path} no fue encontrado. Verifique la ubicación")
             return[]
         event_list = []
         #el archivo json es una lista de diccionarios
         for item in data:
             #instancia de la clase Event
             event_obj = Event (
                   id = item["id"],
                   name = item["name"],   
                   begin = item["begin"],
                   end = item["end"]
             )
             event_list.append(event_obj)
         return event_list        
     
     
  
