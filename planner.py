import json 
import os
from models import Event, load_events_from_json
from resources_manager import Resource, load_resources_from_json
from clothing import Clothes, load_clothes_from_json
from datetime import datetime, timedelta

class Planner  :
    def __init__(self, resource_inventory : list, events_calendary : list, events_clothes : list):
        self.resource_inventory = resource_inventory #lista de los recursos disponibles
        self.events_calendary = events_calendary #lista  de eventos planificados 
        self.events_clothes = events_clothes   #lista de los diferentes vestuarios y accesorios
        
    def add_event(self, event):
        return self.events_calendary.append(event)
    def add_resource(self, resource):
        return self.resource_inventory.append(resource)
    def add_clothes(self, clothes):
        return self.events_clothes.append(clothes)
    
    #relacionar los datos del JSON dentro del planner
    def find_event_by_Id(self, event_id):
        for event in self.events_calendary:
            if event.id == event_id:
                return event
        return None    
    
    def assign_models_automatically(self):
        for event in self.events_calendary:
            for resource in self.resource_inventory:
                if resource.type == 'Models':
                    event.assigned_resources.append(resource)
        print(f"Se han asigando las modelos a los {len(self.events_calendary)} eventos")            
    
    def show_report(self):
         print("------ CARGANDO LOS EVENTOS DE VICTORIA'S SECRET -------")
         print(f"Eventos planificados: {len(self.events_calendary)}")
         print(f"Los recursos necesarios para los eventos son : {len(self.resource_inventory)}")
    
         if not self.events_calendary:
             print("No hay eventos programados")
             return
         
         for event  in self.events_calendary:
             print(f"\nEvento : {event.name} ") #imprime el nombre del evento
             print("Modelos asignadas :")
             
             #recorrer la lista de las modelos
             if event.assigned_resources:
                 for m in event.assigned_resources:
                     print(f" - {m.name} ")
             else:
                 print("No hay modelos asignadas aún")    