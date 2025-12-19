from planner import Planner
from clothing import load_clothes_from_json
from models import  load_events_from_json


def Main() :
    #cargar datos de los json 
    events = load_events_from_json("events.json")
    clothes = load_clothes_from_json("clothes.json")
    
    #instanciar el planificador
    my_planner = Planner(events,clothes)
    
    print("------ CARGANDO LOS EVENTOS DE VICTORIA'S SECRET -------")
    print(f"Eventos planificados: {len(my_planner.events_calendary)}")
    
    if my_planner.events_calendary:
        ev = my_planner.events_calendary[1]
        print(f"\nDuración del evento '{ev.name}': {ev.duration()}")

if __name__ == "__main__":
    Main()