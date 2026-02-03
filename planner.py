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
    
    #guardar lo nuevo que se cree
    def save_to_json(self, file_path= "events.json"):
        data_to_save = []
        for event in self.events_calendary:
            data_to_save.append({
                "id": event.id,
                "name" : event.name,
                "begin": event.begin.strftime("%Y-%m-%d %H:%M:%S"),
                "end": event.end.strftime("%Y-%m-%d %H:%M:%S")
            })
            
        with open(file_path, 'w') as file:
            json.dump(data_to_save, file, indent=4) 
    
    def save_resources(self, file_path = "resources.json"):
         data = {}
         for res in self.resource_inventory:
             if res.type not in data:
                  data[res.type] = []
             data[res.type].append(res.name)
         with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def save_clothes(self, file_path="clothes.json"):
         data = {}
         for c in self.events_clothes:
             if c.category not in data:
                data[c.category] = []
             data[c.category].append(c.name)
         with open(file_path, 'w') as f:
             json.dump(data, f, indent=4)          
    
    def is_available(self, resource, new_event):
        #Verifica si hay conflicto  de horario 
        for exist_event in self.events_calendary:
            #verificar si el recurso está asignado
            resource_name = [r.name for r in exist_event.assigned_resources]
            
            if resource.name in resource_name:
                
                if new_event.begin < exist_event.end and exist_event.begin < new_event.end:
                   return False #Existe un choque de horario entre las modelos
        return True     #no hay choque de horario y están libres      
    
    def validate_inclusion(self, resource_to_assign, clothes_to_assign):
        clothes_name = [c.name.lower().strip() for c in clothes_to_assign]
        resources_name = [r.name.strip() for r in resource_to_assign]
        clothes_category = [c.category.strip() for c in clothes_to_assign]
        
        if "Grand Palais" in resources_name and "tenis" in clothes_name:
            return False, "ERROR DE EXCLUSION: No se permiten tenis en el Grand Palais"
        
        #si es ropa interior no puedo usarla en la línea Pink por ejemplo
        clothes_category = [c.category.strip() for c in clothes_to_assign]
        if "Ropa Interior" in clothes_category and "juvenil" in clothes_name:
            return False, "ERROR DE EXCLUSION: No mezcclar Ropa Interior con la Linea Pink"
        
        #Validación de categorías
        if "Ropa Interior" in clothes_category and "juvenil" in clothes_name:
            return False, "ERROR DE EXCLUSION: No mezclar Ropa Interior con la Linea Pink"
        return True, "Validación exitosa"
     
    def validate_co_requisite(self, resources_to_assign):
        resources_types = [r.type.strip() for r in resources_to_assign]
        resources_names = [r.name.strip() for r in resources_to_assign]
        
        #rule: si hay modelo => hay lugar
        if "Models" in resources_types:
            if "places" not in resources_types:
                return False , "ERROR :No puedes asiganr modelos sin lugares"
            
        return True , "Validación Exitosa"    
            
        
    def assign_models_automatically(self):
        for event in self.events_calendary:
            for resource in self.resource_inventory:
                if resource.type.strip() == 'Models':
                    #validar la inclusión de accesorios
                    is_valid, _ = self.validate_inclusion([resource], self.events_clothes)
                    
                    #verificar disponibilidad antes de asignar
                    if is_valid  and self.is_available(resource, event):
                            #evitar las duplicaciones
                        if resource not in event.assigned_resources:
                                event.assigned_resources.append(resource)      
                       
    
    def find_next_gap(self, duration_hours):
        search_time = datetime.now()
        
        temp_list = []
        for event in self.events_calendary:
            temp_list.append((event.begin, event))
          
        #ordenar por fecha de inicio
        temp_list.sort()
        
        gap_needed = timedelta(hours= duration_hours)
        
        for star_time , event in temp_list:
            #ignorar eventis finalizados
            if event.end < search_time:
                continue
            
            free_space = event.begin - search_time
            
            if free_space >= gap_needed:
                return search_time
            
            search_time =  event.end
            
        return search_time       
                               