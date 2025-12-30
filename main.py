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
    #imprimir la lógica 
    my_planner.show_report()
                         
if __name__ == "__main__":
    Main()