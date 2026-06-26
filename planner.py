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
    def save_to_json(self, file_path= "database.json"):
        events_data = []
        for event in self.events_calendary:
            events_data.append({
                "id": event.id,
                "name" : event.name,
                "begin": event.begin.strftime("%Y-%m-%d %H:%M:%S"),
                "end": event.end.strftime("%Y-%m-%d %H:%M:%S"),
                #name de los res asignados
                "assigned_resources": [res.name for res in event.assigned_resources]
            })
         #estructurar los recursos   
        resources_data = {}
        for r in self.resource_inventory:
            r_type = r.type.strip()
            if r_type not in resources_data:
                resources_data[r_type] = []
            if r.name.strip() not in resources_data[r_type]:
                resources_data[r_type].append(r.name.strip())  
                
         #estructurar la Ropa
        clothes_data = {}   
        for c in self.events_clothes:
            c_cat = c.category.strip()
            if c_cat not in clothes_data:
                clothes_data[c_cat] = []
            if c.name.strip() not in clothes_data[c_cat]:
                clothes_data[c_cat].append(c.name.strip())   
                
        single_database = {
            "events": events_data,
            "resources": resources_data,
            "clothes": clothes_data
        } 
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(single_database,file, indent=4, ensure_ascii=False)        
            
                    
    
    def is_available(self, resource, new_event):
        #Verifica si hay conflicto  de horario 
        for exist_event in self.events_calendary:
            #verificar si el recurso está asignado
            resource_name = [r.name for r in exist_event.assigned_resources]
            
            if resource.name in resource_name:
                
                if new_event.begin < exist_event.end and exist_event.begin < new_event.end:
                   return False #Existe un choque de horario entre las modelos
        return True     #no hay choque de horario y están libres      

     
    def validate_co_requisite(self, resources_to_assign):
        resources_types = [r.type.strip() for r in resources_to_assign]
        
        #rule: si hay modelo => hay lugar
        if "Models" in resources_types:
            if "places" not in resources_types:
                return False , "ERROR DE CO-REQUISITO :No puedes asiganr modelos sin lugares"
            
        return True , "Validación Exitosa" 
    
    def validate_inclusion(self, resources_to_assign):
        
        resources_names = [r.name.strip() for r in resources_to_assign]
        
        if "Grand Palais" in resources_names and "Naomi Cambell" in resources_names:
            return False, "ERROR DE EXCLUSION: La modelo Naomi Cambell tiene exclusividad y no puede desfilar en Grand Palais"
      
        return True, "Validación exitosa"   
            
    def assign_models_automatically(self):
        #asigna modelos si no violan restricciones
        for event in self.events_calendary:
            for resource in self.resource_inventory:
                if resource.type.strip() == 'Models':
                    simulated_resources = event.assigned_resources + [resource]
                    #validar la inclusión de accesorios
                    is_exclusion_valid, _ = self.validate_inclusion(simulated_resources)
                    
                    #verificar disponibilidad antes de asignar
                    if is_exclusion_valid  and self.is_available(resource, event):
                        if resource not in event.assigned_resources:
                                event.assigned_resources.append(resource)      
                       
    
    def find_next_gap(self, duration_hours, resources_to_assign):
        search_time = datetime.now()
        gap_needed = timedelta(hours= duration_hours)
        
        temp_list = []
        for event in self.events_calendary:
            temp_list.append((event.begin, event)) 
        #ordenar por fecha de inicio
        temp_list.sort()
        
        for star_time , event in temp_list:
            #ignorar eventis finalizados
            if event.end < search_time:
                continue
            
            inicio_str = search_time.strftime("%Y-%m-%d %H:%M:%S")
            fin_str = (search_time + gap_needed).strftime("%Y-%m-%d %H:%M:%S")
            
            simulated_event = Event(
                0,
                "Simulado",
                search_time.strftime("%Y-%m-%d %H:%M:%S"), 
                (search_time + gap_needed).strftime("%Y-%m-%d %H:%M:%S")
                )
            
            resources_available = True
            for res in resources_to_assign:
                if not self.is_available(res, simulated_event):
                    resources_available = False
                    break
                
            if resources_available and (event.begin - search_time) >= gap_needed:
                return search_time 
            
            if not resources_available:
                search_time = search_time + gap_needed + timedelta(days=1)
            else: 
                if event.end > search_time:
                 search_time =  event.end
                  
             
        return search_time       
             
                               