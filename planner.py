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
    
    def is_available(self, model, new_event):
        #Verifica si hay conflicto con las modelos y el horario
        for exist_event in self.events_calendary:
            if model in exist_event.assigned_resources:
                if new_event.begin < exist_event.end and exist_event.begin < new_event.end:
                   return False #Existe un choque de horario entre las modelos
        return True     #no hay choque de horario y están libres      
    
    def validate_inclusion(self, resource_to_assign, clothes_to_assign):
        model = False
        accesories = False 
        
        #busco si hay modelo
        for r in resource_to_assign:
            if r.type.strip() == 'Models':
                model = True
                break #ya encontre la modelo y paro
            
        #busco si hay un accesorio en la ropa
        for c in clothes_to_assign:
            if c.category.strip() == 'Accesorios':
                accesories = True
                break #ya encontre la ropa
            
        if model and not accesories:
            return False, "Error : Si asignas una modelo debes incluir accesorios"        
        return True , "Validación exitosa"
    
    
    def assign_models_automatically(self):
        for event in self.events_calendary:
            for resource in self.resource_inventory:
                if resource.type.strip() == 'Models':
                    #validar la inclusión de accesorios
                    is_valid, message = self.validate_inclusion([resource], self.events_clothes)
                    
                    #verificar disponibilidad antes de asignar
                    if is_valid :
                        if  not is_valid :
                            print(f"No se pudo asignar a {event.name} : {message}")
                            continue
                        
                        #verificar disponibilidad de horarios
                        if self.is_available(resource,event):
                            #evitar las duplicaciones
                            if resource not in event.assigned_resources:
                                event.assigned_resources.append(resource)      
                        else:   
                              print(f"Conflicto de horario para {resource.name} en el evento {event.name}")     
                            
    
    def show_report(self):
         print("------ CARGANDO LOS EVENTOS DE VICTORIA'S SECRET -------")
         print(f"Eventos planificados: {len(self.events_calendary)}")
         print(f"Los recursos necesarios para los eventos son : {len(self.resource_inventory)}")
    
         if not self.events_calendary:
             print("No hay eventos programados")
             return
         
         for event  in self.events_calendary:
             print(f"\nEvento : {event.name} ") #imprime el nombre del evento
             print(f"Horario : {event.begin} - {event.end}")
             print("Modelos asignadas :")
             
             #recorrer la lista de las modelos
             if event.assigned_resources:
                 for m in event.assigned_resources:
                     print(f" - {m.name} ")
             else:
                 print("No hay modelos asignadas aún")    