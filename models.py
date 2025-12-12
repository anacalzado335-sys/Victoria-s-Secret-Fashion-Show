import json
import os
import events
import clothes
import resources

class Event : #encargado de leerlos eventos
     def __init__(self,name : list, begin, end, assigned_events= None ):
         self.name = name
         self.begin = begin
         self.end = end
         self.assigned_events = assigned_events #puede estar vacío o no estarlo
         
     def duration(self):
         return self.end - self.begin #toma el inicio y el fin y dice cuanto duro
     
class Resource: #maneja los recursos 
     def __init__(self,name, type):
         self.name = name 
         self.type = type 
         
class Planner  :
    def __init__(self, resource_inventory : list, events_calendary : list):
        self.resource_inventory = resource_inventory #lista de los recursos disponibles
        self.events_calendary = events_calendary #lista  de eventos planificados   
      
def Events(events):
    with open(events) as json_file:
        json_data = json.load(json_file)
        return list(json_data.values())    
         
         
