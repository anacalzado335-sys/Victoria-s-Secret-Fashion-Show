import streamlit as st
from datetime import datetime
from planner import Planner
from clothing import load_clothes_from_json
from models import load_events_from_json, Event
from resources_manager import load_resources_from_json

# Configuración de la página
st.set_page_config(page_title="VS Fashion Show Planner", layout="wide")

# Carga de datos inicial (usamos cache para no recargar cada vez)
@st.cache_data
def get_initial_data():
    events = load_events_from_json("events.json")
    clothes = load_clothes_from_json("clothes.json")
    resources = load_resources_from_json("resources.json")
    return events, clothes, resources

events, clothes, resources = get_initial_data()

# Inicializar el planificador en el estado de la sesión
if 'planner' not in st.session_state:
    st.session_state.planner = Planner(resources, events, clothes)

planner = st.session_state.planner

st.title("👠 Victoria's Secret Event Planner")

# --- BARRA LATERAL: AGREGAR EVENTO ---
st.sidebar.header("Nuevo Evento")
with st.sidebar.form("form_evento"):
    nombre = st.text_input("Nombre del Desfile")
    fecha_inicio = st.date_input("Fecha de Inicio", datetime.now())
    hora_inicio = st.time_input("Hora de Inicio")
    fecha_fin = st.date_input("Fecha de Fin", datetime.now())
    hora_fin = st.time_input("Hora de Fin")
    
    # Selección de recursos
    res_nombres = [r.name for r in resources]
    seleccionados = st.multiselect("Asignar Modelos y Lugares", res_nombres)
    
    enviar = st.form_submit_button("Verificar y Planificar")

if enviar:
    # Construir datetimes
    dt_inicio = datetime.combine(fecha_inicio, hora_inicio)
    dt_fin = datetime.combine(fecha_fin, hora_fin)
    
    if dt_inicio >= dt_fin:
        st.error("La fecha de fin debe ser posterior a la de inicio.")
    else:
        # Buscar objetos recurso reales
        objetos_res = [r for r in resources if r.name in seleccionados]
        nuevo_ev = Event(len(planner.events_calendary) + 1, nombre, 
                         dt_inicio.strftime("%Y-%m-%d %H:%M:%S"), 
                         dt_fin.strftime("%Y-%m-%d %H:%M:%S"))
        
        # VALIDACIÓN DE CONFLICTOS
        conflictos = []
        for r in objetos_res:
            if not planner.is_available(r, nuevo_ev):
                conflictos.append(r.name)
        
        if conflictos:
            st.error(f"Conflicto de horario: Los recursos {conflictos} ya están ocupados.")
        else:
            # VALIDACIÓN DE REGLAS (Inclusión/Exclusión)
            valido, msj = planner.validate_inclusion(objetos_res, clothes)
            if not valido:
                st.warning(msj)
            else:
                nuevo_ev.assigned_resources = objetos_res
                planner.add_event(nuevo_ev)
                st.success(f"Evento '{nombre}' añadido con éxito.")

# --- CUERPO PRINCIPAL ---
tabs = st.tabs(["📅 Calendario de Eventos", "🔍 Buscar Hueco", "💎 Recursos"])

with tabs[0]:
    st.subheader("Eventos Planificados")
    if not planner.events_calendary:
        st.info("No hay eventos registrados.")
    else:
        for ev in planner.events_calendary:
            with st.expander(f"{ev.name} | {ev.begin.strftime('%d %b, %H:%M')}"):
                st.write(f"**Fin:** {ev.end}")
                st.write("**Recursos:**")
                for r in ev.assigned_resources:
                    st.write(f"- {r.name} ({r.type})")
                if st.button(f"Eliminar ID: {ev.id}", key=f"del_{ev.id}"):
                    planner.events_calendary.remove(ev)
                    st.rerun()

with tabs[1]:
    st.subheader("Asistente Inteligente")
    st.write("Esta herramienta busca el próximo espacio libre según tus restricciones.")
    duracion_h = st.number_input("Duración estimada (horas)", 1, 48)
    if st.button("Buscar primer hueco disponible"):
        # Aquí llamarías a la función find_next_gap que definimos antes
        st.info("Buscando el mejor horario sin conflictos...")

with tabs[2]:
    st.subheader("Estado de Recursos")
    tipo_res = st.selectbox("Filtrar por tipo", ["Models", "places"])
    for r in resources:
        if r.type.strip() == tipo_res:
            st.write(f"📍 **{r.name}**")