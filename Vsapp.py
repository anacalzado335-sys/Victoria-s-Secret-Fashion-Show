import streamlit as st
from datetime import datetime
from planner import Planner
from clothing import load_clothes_from_json
from models import load_events_from_json, Event
from resources_manager import load_resources_from_json

# Page configuration
st.set_page_config(page_title="VS Fashion Show Planner", layout="wide")

# Initial data loading (cached to prevent reloading on every interaction)
@st.cache_data
def get_initial_data():
    events = load_events_from_json("events.json")
    clothes = load_clothes_from_json("clothes.json")
    resources = load_resources_from_json("resources.json")
    return events, clothes, resources

events, clothes, resources = get_initial_data()

# Initialize the planner in the session state
if 'planner' not in st.session_state:
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
    
    # Selección de Recursos
    resource_names = [r.name for r in resources]
    selected_resources = st.multiselect("Asignar Modelos y Lugares", resource_names)
    
    submit_button = st.form_submit_button("Verificar y Planear")

if submit_button:
    # Construcción de objetos datetime
    dt_start = datetime.combine(start_date, start_time)
    dt_end = datetime.combine(end_date, end_time)
    
    if dt_start >= dt_end:
        st.error("La fecha de fin debe ser posterior a la de inicio.")
    else:
        # Buscar objetos recurso reales
        actual_resource_objects = [r for r in resources if r.name in selected_resources]
        new_event = Event(len(planner.events_calendary) + 1, event_name, 
                         dt_start.strftime("%Y-%m-%d %H:%M:%S"), 
                         dt_end.strftime("%Y-%m-%d %H:%M:%S"))
        
        # Validación de Conflictos de horarios
        conflicts = []
        for resource in actual_resource_objects:
            if not planner.is_available(resource, new_event):
                conflicts.append(resource.name)
        
        if conflicts:
            st.error(f"Conflicto de horario: Los siguientes recursos ya están ocupados: {conflicts}")
        else:
            # VALIDACIÓN DE REGLAS (Inclusion/Exclusion)
            is_valid, message = planner.validate_inclusion(actual_resource_objects, clothes)
            if not is_valid:
                st.warning(message)
            else:
                new_event.assigned_resources = actual_resource_objects
                planner.add_event(new_event)
                st.success(f"Event '{event_name}' successfully added.")

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
                    st.rerun()

with tabs[1]:
    st.subheader("Asistente Inteligente")
    st.write("Esta herramienta busca el próximo espacio libre según tus restricciones.")
    duration_hours = st.number_input("Duración estimada (horas)", 1, 48)
    if st.button("Buscar ell primer hueco disponible"):
        # Placeholder for the find_next_gap logic
        st.info("Buscando el mejor horario sin conflictos...")

with tabs[2]:
    st.subheader("Estado de Recursos")
    resource_filter = st.selectbox("Filtrar por tipo", ["Models", "places"])
    for res in resources:
        if res.type.strip() == resource_filter:
            st.write(f"📍 **{res.name}**")