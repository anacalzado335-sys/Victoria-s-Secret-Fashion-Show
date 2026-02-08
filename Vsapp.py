import streamlit as st
from datetime import datetime
from planner import Planner
from clothing import load_clothes_from_json
from models import load_events_from_json, Event
from resources_manager import load_resources_from_json

# Configuarción de la Página
st.set_page_config(page_title="VS Fashion Show Planner", layout="wide")

if 'planner' not in st.session_state:
    events = load_events_from_json("events.json")
    clothes = load_clothes_from_json("clothes.json")
    resources = load_resources_from_json("resources.json")
    
    res_map = {r.name.strip(): r for r in resources}
    for ev in events : 
        ev.assigned_resources = [res_map[name.strip()] for name in ev.assigned_resources if name.strip() in res_map]   
        
    st.session_state.planner = Planner(resources, events, clothes)
    
planner = st.session_state.planner

st.title("👠 Planificador de Eventos Victoria's Secret")

# --- SIDEBAR: ADD NEW EVENT ---
st.sidebar.header("Nuevo Evento")
with st.sidebar.form("event_form"):
    event_name = st.text_input("Nombre del Desfile")
    start_date = st.date_input("Fecha de Inicio", datetime.now())
    start_time = st.time_input("Hora de Inicio")
    end_date = st.date_input("Fecha de Fin", datetime.now())
    end_time = st.time_input("Hora de Fin")
    
    # Selección de Recursos (Modelos y Lugares)
    resource_names = [r.name for r in planner.resource_inventory]
    selected_resources = st.multiselect("Asignar Modelos y Lugares", resource_names)
    
    # ---- Selector de ropa ----
    clothes_items = {
        c.name: c for c in planner.events_clothes
        if c.category.strip().lower() not in ["accesorios", "calzado"]
    }
    
    shoes_items = {
        c.name: c for c in planner.events_clothes
        if c.category.strip().lower() == "calzado"
    }
    
    accesories_items = {
        c.name : c for c in planner.events_clothes
        if c.category.strip().lower() == "accesorios"
    }
    
    selected_clothes_names = st.multiselect("Seleccionar Ropa (Interior/Pink)", list(clothes_items.keys()))
    selected_shoes_names = st.multiselect("Seleccionar Calzado", list(shoes_items.keys()))
    selected_accesory_names = st.multiselect("Seleccionar accesorios", list(accesories_items.keys()))
    
    
    submit_button = st.form_submit_button("Verificar y Planear")

if submit_button:
    # Construcción de objetos datetime
    dt_start = datetime.combine(start_date, start_time)
    dt_end = datetime.combine(end_date, end_time)
    
    if dt_start >= dt_end:
        st.error("La fecha de fin debe ser posterior a la de inicio.")
    else:
        # Buscar objetos recurso reales
        actual_resource_objects = [r for r in planner.resource_inventory if r.name in selected_resources]
        actual_clothes_objects = [clothes_items[n] for n in selected_clothes_names] + [shoes_items[n] for n in selected_shoes_names] +\
                                 [accesories_items[n] for n in selected_accesory_names]
        
        if planner.events_calendary:
            new_id = max([ev.id for ev in planner.events_calendary]) + 1
        else :
            new_id = 1    
        new_event = Event(
                         new_id, 
                         event_name,
                         dt_start.strftime("%Y-%m-%d %H:%M:%S"), 
                         dt_end.strftime("%Y-%m-%d %H:%M:%S"))
        
        
        # Validación de Conflictos de horarios
        is_valid_co ,msg_co = planner.validate_co_requisite(actual_resource_objects)
        if not is_valid_co:
            st.error(msg_co)
            
        conflicts = []
        for resource in actual_resource_objects:
            if not planner.is_available(resource, new_event):
                conflicts.append(resource.name)
        
        if conflicts:
            st.error(f"Conflicto de horario: Los siguientes recursos ya están ocupados: {conflicts}")
        else:
            # VALIDACIÓN DE REGLAS (Inclusion/Exclusion)
            is_valid, message = planner.validate_inclusion(actual_resource_objects, actual_clothes_objects)
            if not is_valid:
                st.warning(message)
            else:
                new_event.assigned_resources = actual_resource_objects
                planner.add_event(new_event)
                planner.save_to_json()
                st.success(f"Evento '{event_name}' añadido exitosamente.")

# --- CUERPO PRINCIPAL ---
tabs = st.tabs(["📅 Calendario de Eventos", "🔍 Encontrar Disponibilidad", "💎 Recursos"])

with tabs[0]:
    st.subheader("Eventos Programados")
    if not planner.events_calendary:
        st.info("No hay eventos regristrados actualmente.")
    else:
        for event in planner.events_calendary:
            with st.expander(f"{event.name} | {event.begin.strftime('%d %b, %H:%M')}"):
                st.write(f"**Finaliza:** {event.end}")
                st.write("**Recursos Asignados:**")
                for res in event.assigned_resources:
                    st.write(f"- {res.name} ({res.type})")
                
                # Using unique key for the delete button
                if st.button(f"Eliminar ID: {event.id}", key=f"del_{event.id}"):
                    planner.events_calendary.remove(event)
                    planner.save_to_json()
                    st.rerun()
                    

with tabs[1]:
    st.subheader("Asistente Inteligente")
    
    #user elige la hora
    hours = st.number_input("Horas necesarias para el desfile", 1, 24, 2)
    
    if st.button("Buscar próximo espacio"):
        gap = planner.find_next_gap(hours)
        
        st.success(f"📍 Próximo hueco disponible:")
        st.info(f"Fecha: {gap.strftime('%d de %B, %Y')}")
        st.info(f"Hora: {gap.strftime('%H:%M %p')}")
        
        
with tabs[2]:
    st.subheader("Estado de Recursos")
    resource_filter = st.selectbox("Filtrar por tipo", ["Models", "places"])
    for res in planner.resource_inventory:
        if res.type.strip() == resource_filter:
            st.write(f"📍 **{res.name}**")