from planner import Planner
from clothing import load_clothes_from_json
from models import  load_events_from_json
from resources_manager import load_resources_from_json

def Main() :
    #cargar datos de los json 
    events = load_events_from_json("events.json")
    clothes = load_clothes_from_json("clothes.json")
    resources = load_resources_from_json("resources.json")
    
    #instanciar el planificador
    my_planner = Planner(resources,events,clothes)
    
    #llamado a la automatizacion
    my_planner.assign_models_automatically()
    
    print("------ CARGANDO LOS EVENTOS DE VICTORIA'S SECRET -------")
    print(f"Eventos planificados: {len(my_planner.events_calendary)}")
    print(f"Los recursos necesarios para los eventos son : {len(my_planner.resource_inventory)}")
    
    if my_planner.events_calendary:
         for event  in my_planner.events_calendary:
             print(f"\nEvento : {event.name} ") #imprime el nombre del evento
             print("Modelos asignadas :")
             
             #recorrer la lista de las 
             if event.assigned_resources:
                 for m in event.assigned_resources:
                     print(f" - {m.name} ")
             else:
                 print("No hay modelos asignadas aún")
                         
if __name__ == "__main__":
    Main()