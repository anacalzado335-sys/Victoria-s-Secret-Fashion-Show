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
        first_event = my_planner.events_calendary[0]
        print(f"\nModelos en {first_event.name}:")
        for m in first_event.assigned_resources:
            print(f"- {m.name}")

if __name__ == "__main__":
    Main()