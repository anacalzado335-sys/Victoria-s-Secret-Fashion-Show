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
    models_name = [r.name for r in planner.resource_inventory if r.type.strip() == "Models"]
    places_name = [r.name  for r in planner.resource_inventory if r.type.strip() == "places" ]
     
    selected_models = st.multiselect("Seleccionar Modelos", models_name)
    selected_places = st.multiselect("Seleccionar Lugar", places_name)
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
        actual_resource_objects = [
            r for r in planner.resource_inventory
            if r.name in selected_models or r.name in  selected_places    
        ]
        actual_clothes_objects = [clothes_items[n] for n in selected_clothes_names] + \
                                 [shoes_items[n] for n in selected_shoes_names] + \
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
        is_valid_inc , msg_inc = planner.validate_inclusion(actual_resource_objects, actual_clothes_objects)
        conflicts = [res.name for res in actual_resource_objects if not planner.is_available(res, new_event)]   
        
        if not is_valid_co:
            st.error(msg_co)
        elif not is_valid_inc:
            st.error(msg_inc) 
        elif conflicts:
             st.error(f"Conflicto de horario: Los siguientes recursos ya están ocupados: {conflicts}")
        else:        
            
             new_event.assigned_resources = actual_resource_objects
             planner.add_event(new_event)
             planner.save_to_json()
             st.success(f"Evento '{event_name}' añadido exitosamente.")
             st.rerun()

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
    st.subheader("💎 Agenda y  Estado de Recursos")
    if not planner.resource_inventory:
        st.info("No hay recursos registrados en el sistema.")
    else: 
        resource_names = [res.name for res in planner.resource_inventory]
        #selector para el usuario
        selected_resource_name = st.selectbox(
            "Selecciona una Modelo o Lugar para ver su agenda detallada:", options=resource_names
            )
        
        selected_resource_obj = next(
            (r for r in planner.resource_inventory if r.name == selected_resource_name),
            None
        )
        
        if selected_resource_obj:
            st.write(f"### Agenda para : **{selected_resource_obj.name}** ({selected_resource_obj.type})")
            
            resource_agenda =[]
            for event in planner.events_calendary:
                if any(res.name == selected_resource_obj.name for res in event.assigned_resources):
                    resource_agenda.append(event)
            
            if not resource_agenda:
                st.warning(f"Actualmente **{selected_resource_obj.name}** no tiene ningún desfile asignado")
            else:
                st.success(f"Se encontraron {len(resource_agenda)} evento(s) asignado(s):")
                
                for idx, ev in enumerate(resource_agenda, 1):
                    with st.container(border=True):
                        st.markdown(f"**{idx}. {ev.name}**")
                        st.write(f"📅 **Inicio:** {ev.begin.strftime('%d %b %Y - %H:%M')}")
                        st.write(f"🏁 **Fin:** {ev.end.strftime('%d %b %Y - %H:%M')}")
                        
                        #mostar con quien comparte pasarela
                        companions = [r.name for r in ev.assigned_resources if r.name != selected_resource_obj.name]
                        if companions:
                            st.write(f"🔗 **Otros recursos en este evento:** {', '.join(companions)}")
                             
                        
                              
                     
  