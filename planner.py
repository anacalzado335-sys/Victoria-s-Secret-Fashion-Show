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
    
    def is_available(self, resource, new_event):
        #Verifica si hay conflicto  de horario tanto para lugares como para las modelos
        for exist_event in self.events_calendary:
            #verificar si el recurso está asignado a un evento existente
            resource_name = [r.name for r in exist_event.assigned_resources]
            
            if resource.name in resource_name:
                
                if new_event.begin < exist_event.end and exist_event.begin < new_event.end:
                   return False #Existe un choque de horario entre las modelos
        return True     #no hay choque de horario y están libres      
    
    def validate_inclusion(self, resource_to_assign, clothes_to_assign):
        clothes_name = [c.name.lower().strip() for c in clothes_to_assign]
        resources_name = [r.name.strip() for r in resource_to_assign]
        
        if "Grand Palais" in resources_name and "tenis " in clothes_name:
            return False, "ERROR DE EXCLUSION: No se permiten tenis en el Grand Palais"
        
        #si es ropa interior no puedo usarla en la línea Pink por ejemplo
        clothes_category = [c.category.strip() for c in clothes_to_assign]
        if "Ropa Interior" in clothes_category and "juvenil" in clothes_name:
            return False, "ERROR DE EXCLUSION: No mezcclar Ropa Interior con la Linea Pink"
        
        return True, "Validación exitosa"
        
        
    def assign_models_automatically(self):
        for event in self.events_calendary:
            for resource in self.resource_inventory:
                if resource.type.strip() == 'Models':
                    #validar la inclusión de accesorios
                    is_valid, message = self.validate_inclusion([resource], self.events_clothes)
                    
                    #verificar disponibilidad antes de asignar
                    if is_valid  and self.is_available:
                            #evitar las duplicaciones
                        if resource not in event.assigned_resources:
                                event.assigned_resources.append(resource)      
                       
                            
    
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