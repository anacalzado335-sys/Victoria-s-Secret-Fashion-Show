# Título Principal: Planificador de Eventos Victoria's Secret

## 1. Qué hace mi programa
El propósito fundamental de este software es automatizar y optimizar la gestión  de la  planificación de desfiles de moda  para la marca *Victoria's Secret*. En él se gestionan múltiples recursos entre los que se encuentran: las modelos, los lugares en los que ocurrirán los desfiles ,  prendas íntimas , líneas juveniles, calzado exclusivo y accesorios de alta joyería.

Este programa  unifica todos estos recursos a través una interfaz gráfica construida sobre el framework Streamlit. Los requisitos funcionales con que cuenta  el programa son los siguientes:

* **Creación de Eventos:** Permite crear desfiles con su su fecha y hora de inicio, así como su fecha y hora de culminación, a través de la utilización de ficheros json previamente creados(Ver 2.2).
* **Validación de una misma asignación de modelos o lugares a más de un desfile en la misma línea de tiempo** Al crear un desfile se comprueba que no exista  una misma modelo o un mismo lugar en dos desfiles en la línea de tiempo.
* **Validación de campos obligatorios:** Al confirmar un desfile se verifica que el campo lugar no se encuentren vacío. 
* **Encontrar disponibilidad de nuevos eventos:** Existe una funcionalidad que permite encontrar la disponibilidad de modelos  para cubrir un desfile de una duración de horas específica.
* **Disponibilidad de modelos o lugares especificos:** Permite  filtrar el calendario global para inspeccionar detalladamente la agenda de una sola modelo o lugar, revelando con qué otras compañeras compartirá pasarela.

---

## 2. Cómo lo diseñaste y por qué tomaste las decisiones que tomaste

### 2.1 Enfoque de Arquitectura Orientada a Objetos (POO)
El programa ha sido diseñado siguiendo los principios de la Programación Orientada a Objetos para segmentar responsabilidades, encapsular la lógica y garantizar la extensibilidad del sistema a largo plazo. Se definieron clases independientes para cada entidad del dominio del problema real, distribuidas en módulos especializados:

#### A. La Clase `Resource` (`resources_manager.py`)
Modela los recursos físicos e individuales que participan en las pasarelas. Recibe en su constructor los atributos `name` (nombre) y `type` (tipo, por ejemplo `"Models"` o `"places"`). 


#### B. La Clase `Clothes` (`clothing.py`)
Encapsula el vestuario y los accesorio que se utilizarán en los desfiles, conteniendo las propiedades de nombre de la pieza (`name`) y su categoría de pertenencia (`category`). 


#### C. La Clase `Event` (`models.py`)
Representa formalmente los desfiles programados en el calendario. Posee un identificador único numérico (`id`), un nombre descriptivo (`name`), un marcador de inicio (`begin`), un marcador de fin (`end`), y un listado dinámico de referencias denominado `assigned_resources`.En esta clase se utilizó la conversión explícita e inmediata de las cadenas de texto planas de fechas provenientes de la capa de almacenamiento en objetos nativos `datetime` de Python a través de máscaras de formateo estrictas (`"%Y-%m-%d %H:%M:%S"`). Esto permite que operaciones de cálculo complejas (como la determinación de la duración de un show mediante el método `duration()` que devuelve un objeto de tipo `timedelta`) o comparaciones de precedencia temporal se resuelvan de forma matemática directa en el procesador, en lugar de recurrir a complejas manipulaciones de strings de texto.

#### D. La Clase Central `Planner` (`planner.py`)
Funciona como el núcleo integrador (el Controlador del sistema). Mantiene en memoria el estado operativo global mediante tres listas maestras: `resource_inventory`, `events_calendary` y `events_clothes`. El `Planner` no se encarga directamente de abrir o parsear archivos sueltos de manera interna al crearse; recibe las colecciones ya pre-procesadas e instanciadas en su constructor. Esto dota al motor de una modularidad excepcional, permitiendo realizar pruebas automatizadas aisladas en entornos de desarrollo de forma muy simple y asegurando que la lógica pura de negocio esté desacoplada de la interfaz de usuario web.

### 2.2 Utilización de json
El proyecto define estructuras importantes divididas en tres archivos físicos independientes: `resources.json`, `clothes.json` y `events.json`. Sin embargo, para entornos de ejecución continua, depender de múltiples archivos separados para mantener la consistencia temporal introduce problemas de concurrencia y desincronización de referencias cruzadas.

Por este motivo, se diseñó un mecanismo de consolidación en un archivo unificado llamado `database.json`. Al arrancar, si el archivo unificado existe, el sistema carga una única estructura monolítica que asocia eventos, recursos y ropa en un solo bloque atómico. Al guardar cambios a través del método `save_to_json()`, se reconstruye este mapa integral y se vuelca de golpe al disco empleando codificación UTF-8 y desactivando el escape de caracteres ASCII (`ensure_ascii=False`). Esto garantiza que los caracteres especiales en español (como tildes o eñes) se almacenen perfectamente legibles.

---

## 3. Qué aprendiste durante el desarrollo
El ciclo de vida del desarrollo de este proyecto me proporcionó aprendizajes  en ingeniería de software, conocer acerca del framework streamlit , así como profundizar en Python. Además aprendí sobre:

1. Trabajar con fechas y horas reales me ayudó a comprender que las operaciones cronológicas no pueden tratarse como simples datos numéricos o cadenas de texto. El aprendizaje del uso defensivo de las clases `datetime` y `timedelta` de Python fue crucial para dominar el cálculo preciso de duraciones de eventos, intervalos de descanso y algoritmos de prevención de solapamientos lógicos.
2.  Diseñar las funciones de validación de co-requisitos y exclusiones dentro del `Planner` como métodos puros e independientes que devuelven tuplas de estado (`bool, str`) me enseñó sobre los beneficios de una arquitectura limpia. Este enfoque facilitó la incorporación futura de nuevas reglas contractuales o restricciones operacionales complejas sin necesidad de alterar en absoluto la interfaz visual de Streamlit ni los formularios de captura de datos.
3. Aprendí la necesidad  de manejar errores mediante el uso `try-except` al interactuar con sistemas de archivos externos. 
---

## 4. Cómo se usa el programa (con ejemplos)

### 4.1 Requisitos de Ejecución e Inicio del Sistema
El programa se ejecuta directamente desde la terminal del sistema invocando el intérprete de streamlit sobre el archivo principal de control del proyecto:

```bash
streamlit run main.py


---

---

## 5. Dificultades que encontraste y cómo las resolviste

### 5.1 Gestión de almacenamiento, control de versiones e interfaz gráfica
Durante el ciclo de desarrollo del proyecto se presentaron diversos obstáculos técnicos que requirieron investigación y adaptación para asegurar la correcta ejecución del sistema:

* **Creación y estructuración de archivos JSON:** En los inicios del proyecto, una de las mayores dificultades fue la generación y correcta configuración de los archivos JSON para la persistencia de datos. Esto se resolvió mediante una investigación profunda y autónoma a través de videos tutoriales en YouTube, logrando comprender la estructura de estos ficheros.
* **Autenticación y subida de commits en GitHub:** Igualmente, enfrenté dificultades para poder subir los commits debido a un error de permisos en mi cuenta local. La solución se halló nuevamente mediante videos de YouTube, los cuales mostraron el procedimiento exacto para generar y asignarle un token de acceso personal (PAT) temporal a mi cuenta de GitHub, restableciendo la conexión con el repositorio.
* **Migración de arquitectura (Consola a Entorno Web):** El proyecto inicialmente iba a ser desarrollado para ejecutarse exclusivamente en la consola de comandos. Sin embargo, luego de consultar detalladamente la documentación oficial del framework Streamlit, pude resolver este reto y lograr que mi proyecto contara con una interfaz gráfica interactiva y mucho más amigable para el usuario.



