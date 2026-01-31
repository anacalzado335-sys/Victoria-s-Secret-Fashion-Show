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
    my_planner.assign_models_automatically()
    
    print("\n--- Verificando Restricción de Exclusión ---")
    # Simulamos una lista de ropa prohibida
    ropa_prohibida = [c for c in clothes if c.name == "tenis" or c.category == "Ropa Interior "]
    valid, message = my_planner.validate_inclusion(resources, clothes)
    if not valid:
        print(f"Alerta de lógica: {message}")
                         
if __name__ == "__main__":
    Main()