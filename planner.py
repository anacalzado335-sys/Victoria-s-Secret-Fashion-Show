import json 
import os
from models import Event, load_events_from_json
from resource import Resource, load_resources_from_json
from datetime import datetime, timedelta

class Planner  :
    def __init__(self, resource_inventory : list, events_calendary : list):
        self.resource_inventory = resource_inventory #lista de los recursos disponibles
        self.events_calendary = events_calendary #lista  de eventos planificados   
        
    def add_event(self, event):
        return self.events_calendary.append(event)
    def add_resource(self, resource):
        return self.resource_inventory.append(resource)