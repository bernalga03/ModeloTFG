#Librerias
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import matplotlib.pyplot as plt
from io import BytesIO
import pdfkit
import os

# Configuración de la página
st.set_page_config(page_title="Modelo de Inclusión Laboral", layout="wide")


# Menú lateral de navegación
opcion = st.sidebar.selectbox(
    "Selecciona módulo",
    ["Perfil funcional", "Gestión de ofertas", "Matching", "Itinerario personalizado", "Seguimiento y evaluación"],
    key="Selecciona módulo"
)

if opcion == "Perfil funcional":

    # Título y descripción
    st.title("Perfil funcional del candidato")
    st.markdown(
        "Este formulario recoge la información clave del perfil funcional de una persona con discapacidad "
        "(intelectual reconocida o límite) para evaluar su encaje en diferentes puestos de trabajo. "
        "Por favor, completa cada campo con base en la observación directa o información compartida con la persona y su entorno."
    )

    # Datos generales
    st.subheader("Datos generales")

    edad = st.number_input(
        "Edad",
        min_value=14,
        max_value=99,
        value=25,
        help="Introduce la edad de la persona candidata."
    )

    formacion = st.selectbox(
        "Nivel educativo o formación técnica",
        options=["Ninguna", "ESO", "Bachillerato", "FP básica", "FP media", "FP superior", "Universidad"],
        help="Selecciona el nivel más alto de formación completado."
    )

    experiencia_laboral = st.selectbox(
        "Experiencia laboral previa",
        options=["Ninguna", "Puntual (menos de 3 meses)", "Prolongada (más de 3 meses)"],
        help="Indica si tiene experiencia laboral previa. Si quieres, añade algún ejemplo."
    )

    experiencia_texto = st.text_input(
        "Ejemplo de experiencia (opcional)",
        placeholder="Ej. prácticas en almacén, trabajo puntual en limpieza técnica..."
    )

    # Sección: Capacidades funcionales
    st.subheader("Capacidades funcionales")

    autonomia_personal = st.slider(
        "Nivel de autonomía personal",
        min_value=1,
        max_value=5,
        value=3,
        help="Evalúa el grado de autonomía en tareas diarias sin supervisión constante. 1 significa muy dependiente, 5 completamente autónomo."
    )

    autonomia_laboral = st.slider(
        "Nivel de autonomía laboral",
        min_value=1,
        max_value=5,
        value=3,
        help="¿Con qué facilidad sigue instrucciones, trabaja y mantiene el ritmo laboral?"
    )

    comprension_verbal = st.selectbox(
        "Comprensión verbal",
        options=["Baja", "Media", "Alta"],
        help="¿Qué nivel tiene para entender instrucciones orales?"
    )

    comprension_lectora = st.selectbox(
        "Comprensión lectora",
        options=["Baja", "Media", "Alta"],
        help="¿Qué nivel tiene para leer y entender instrucciones escritas?"
    )

    atencion = st.slider(
        "Atención sostenida",
        min_value=1,
        max_value=5,
        value=3,
        help="¿Durante cuánto tiempo puede concentrarse sin distraerse? 1 = muy poco tiempo, 5 = muy prolongado."
    )

    motricidad_fina = st.selectbox(
        "Motricidad fina",
        options=["Baja", "Media", "Alta"],
        help="¿Con qué habilidad realiza tareas que requieren precisión manual?"
    )

    movilidad = st.selectbox(
        "Movilidad física general",
        options=["Baja", "Media", "Alta"],
        help="¿Puede moverse fácilmente por espacios de trabajo?"
    )

    apoyos_externos = st.selectbox(
        "Necesidad de apoyos externos",
        options=["Alta", "Media", "Baja"],
        help="¿Cuánta ayuda externa necesita para mantener un empleo?"
    )

    trabajo_equipo = st.selectbox(
        "Trabajo en equipo",
        options=["Escasa", "Aceptable", "Buena"],
        help="¿Qué nivel de habilidad tiene para colaborar con otras personas?"
    )

    estilo_aprendizaje = st.multiselect(
        "Estilo de aprendizaje preferente",
        options=["Visual", "Oral", "Repetición", "Demostración práctica"],
        help="¿Cómo aprende mejor esta persona? Puedes marcar varias opciones."
    )

    iniciativa = st.slider(
        "Iniciativa y proactividad",
        min_value=1,
        max_value=5,
        value=3,
        help="¿Con qué frecuencia toma decisiones o actúa sin necesidad de instrucciones?"
    )

    tolerancia_estres = st.selectbox(
        "Tolerancia al estrés y a los cambios",
        options=["Baja", "Media", "Alta"],
        help="¿Cómo responde ante cambios, presión o situaciones inesperadas?"
    )

    habilidades_sociales = st.selectbox(
        "Habilidades sociales",
        options=["Escasa", "Media", "Buena"],
        help="¿Qué nivel de habilidades sociales muestra?"
    )

    intereses_laborales = st.multiselect(
        "Intereses laborales",
        options=["Montaje", "Almacén", "Limpieza técnica", "Verificación", "Logística interna", "Otro"],
        help="Selecciona los sectores o tareas que más le interesan. Puedes añadir uno manual abajo."
    )

    intereses_otro = st.text_input(
        "Otro interés (especificar)",
        placeholder="Ej. jardinería, atención al cliente..."
    )

    certificado_discapacidad = st.checkbox(
        "¿Tiene certificado de discapacidad ≥33%?",
        help="¿Cuenta con un certificado oficial de discapacidad igual o superior al 33%?"
    )

    # Resultados en un diccionario
    perfil_funcional = {
        "edad": edad,
        "formacion": formacion,
        "experiencia_laboral": experiencia_laboral,
        "experiencia_texto": experiencia_texto,
        "autonomia_personal": autonomia_personal,
        "autonomia_laboral": autonomia_laboral,
        "comprension_verbal": comprension_verbal,
        "comprension_lectora": comprension_lectora,
        "atencion": atencion,
        "motricidad_fina": motricidad_fina,
        "movilidad": movilidad,
        "apoyos_externos": apoyos_externos,
        "trabajo_equipo": trabajo_equipo,
        "estilo_aprendizaje": estilo_aprendizaje,
        "iniciativa": iniciativa,
        "tolerancia_estres": tolerancia_estres,
        "habilidades_sociales": habilidades_sociales,
        "intereses_laborales": intereses_laborales,
        "intereses_otro": intereses_otro,
        "certificado_discapacidad": certificado_discapacidad
    }

    # Mostrar resumen del perfil en pantalla
    st.subheader("Resumen del perfil ingresado")
    st.json(perfil_funcional)

    # Validaciones de campos obligatorios no rellenados

    # Edad limitada
    if edad is None or edad < 16:
        st.error("La edad debe ser igual o mayor a 16 años.")

    # Nivel educativo
    if formacion == "":
        st.warning("Por favor, selecciona el nivel educativo alcanzado.")

    # Experiencia previa sin describirla más
    if experiencia_laboral != "Ninguna" and experiencia_texto.strip() == "":
        st.warning("Has indicado experiencia previa, pero no has añadido ningún ejemplo.")

    # Estilo de aprendizaje vacío
    if not estilo_aprendizaje:
        st.warning("Selecciona al menos un estilo de aprendizaje preferente.")

    # Intereses laborales vacíos
    if not intereses_laborales:
        st.warning("Selecciona al menos un interés laboral.")


    # Relaciones incoherentes entre campos

    if movilidad == "Baja" and any(interes in intereses_laborales for interes in ["Almacén", "Logística interna", "Montaje"]):
        st.error("Cuidado: el interés seleccionado puede no ser compatible con una movilidad física baja.")

    if comprension_verbal == "Baja" and "Oral" in estilo_aprendizaje:
        st.warning("Has seleccionado 'Oral' como estilo de aprendizaje, pero el nivel de comprensión verbal es bajo.")

    if comprension_lectora == "Baja" and any(estilo in estilo_aprendizaje for estilo in ["Repetición", "Visual"]):
        st.warning("Has seleccionado 'Visual' o 'Repetición' como estilo de aprendizaje, pero la comprensión lectora es baja.")

    if iniciativa <= 2 and any(interes in intereses_laborales for interes in ["Verificación", "Montaje"]):
        st.warning("Las tareas seleccionadas requieren cierta autonomía, pero la iniciativa aparece como muy baja.")

    if tolerancia_estres == "Baja" and any(interes in intereses_laborales for interes in ["Logística interna", "Limpieza técnica"]):
        st.warning("Estas tareas pueden implicar presión o cambios, y has indicado una baja tolerancia al estrés.")


    # Valores extremos que requieren atención

    if autonomia_personal <= 2 and iniciativa <= 2 and atencion <= 2:
        st.info("Este perfil podría requerir un entorno laboral altamente estructurado y apoyos intensivos.")


    # Confirmación general

    if st.button("Validar y continuar"):
        st.session_state.perfil_funcional = perfil_funcional
        st.success("Perfil guardado correctamente. Puedes continuar a la sección de matching.")

elif opcion == "Gestión de ofertas":

    # Lista temporal para almacenar las ofertas creadas durante la sesión

    if "ofertas_guardadas" not in st.session_state:
        st.session_state.ofertas_guardadas = [
            {
                "id": "E001",
                "nombre": "Operario de ensamblaje manual",
                "departamento": "Ensamblaje",
                "descripcion": "Montaje de piezas con herramientas básicas en entorno estructurado y con apoyos.",
                "autonomia_laboral": "Media",
                "comprension": "Media",
                "atencion": 3,
                "motricidad": "Alta",
                "interaccion_social": "Baja",
                "tolerancia_cambio": "Media",
                "formacion_tecnica": "FP básica",
                "apoyos_puesto": "Medio",
                "estilo_aprendizaje": ["Demostración", "Repetición"],
                "iniciativa": "Media",
                "adaptabilidad": "Sí",
                "tareas": ["Montaje", "Verificación"]
            },
            {
                "id": "E002",
                "nombre": "Auxiliar de logística interna",
                "departamento": "Almacén",
                "descripcion": "Recepción, clasificación y traslado de materiales con apoyo visual y tareas repetitivas.",
                "autonomia_laboral": "Alta",
                "comprension": "Alta",
                "atencion": 4,
                "motricidad": "Media",
                "interaccion_social": "Media",
                "tolerancia_cambio": "Alta",
                "formacion_tecnica": "FP media",
                "apoyos_puesto": "Bajo",
                "estilo_aprendizaje": ["Visual", "Repetición"],
                "iniciativa": "Alta",
                "adaptabilidad": "Sí",
                "tareas": ["Almacén", "Logística interna"]
            },
            {
                "id": "E003",
                "nombre": "Operario de limpieza técnica",
                "departamento": "Mantenimiento",
                "descripcion": "Limpieza especializada de maquinaria e instalaciones en entornos controlados.",
                "autonomia_laboral": "Baja",
                "comprension": "Baja",
                "atencion": 2,
                "motricidad": "Alta",
                "interaccion_social": "Baja",
                "tolerancia_cambio": "Baja",
                "formacion_tecnica": "Ninguna",
                "apoyos_puesto": "Alto",
                "estilo_aprendizaje": ["Demostración", "Oral"],
                "iniciativa": "Baja",
                "adaptabilidad": "Sí",
                "tareas": ["Limpieza técnica"]
            }
        ]

    st.title("Gestión de ofertas")

    subopcion = st.selectbox(
        "Selecciona una acción",
        ["Añadir nueva oferta de trabajo", "Ver o modificar ofertas existentes"]
    )

    if subopcion == "Añadir nueva oferta de trabajo":
        oferta_en_edicion = st.session_state.get("oferta_en_edicion", None)

        if oferta_en_edicion:
            st.markdown(f"**Editando oferta existente:** `{oferta_en_edicion['id']}`")
            nuevo_id = oferta_en_edicion['id']
            nombre_puesto_default = oferta_en_edicion['nombre']
            departamento_default = oferta_en_edicion['departamento']
            descripcion_default = oferta_en_edicion['descripcion']
            autonomia_laboral_default = oferta_en_edicion['autonomia_laboral']
            comprension_default = oferta_en_edicion['comprension']
            atencion_default = oferta_en_edicion['atencion']
            motricidad_default = oferta_en_edicion['motricidad']
            interaccion_social_default = oferta_en_edicion['interaccion_social']
            tolerancia_cambio_default = oferta_en_edicion['tolerancia_cambio']
            formacion_tecnica_default = oferta_en_edicion['formacion_tecnica']
            apoyos_puesto_default = oferta_en_edicion['apoyos_puesto']
            estilo_aprendizaje_default = oferta_en_edicion['estilo_aprendizaje']
            iniciativa_default = oferta_en_edicion['iniciativa']
            adaptabilidad_default = oferta_en_edicion['adaptabilidad']
            tareas_default = oferta_en_edicion['tareas']
            # Cargar requisitos indispensables si existen
            requisitos_default = oferta_en_edicion.get("requisitos", {})
            autonomia_requisito_default = requisitos_default.get("autonomia_laboral", False)
            comprension_requisito_default = requisitos_default.get("comprension", False)
            atencion_requisito_default = requisitos_default.get("atencion", False)
            motricidad_requisito_default = requisitos_default.get("motricidad", False)
            interaccion_social_requisito_default = requisitos_default.get("interaccion_social", False)
            tolerancia_requisito_default = requisitos_default.get("tolerancia_cambio", False)
            formacion_requisito_default = requisitos_default.get("formacion_tecnica", False)
            iniciativa_requisito_default = requisitos_default.get("iniciativa", False)
        else:
            nuevo_id = f"E{len(st.session_state.ofertas_guardadas)+1:03d}"
            nombre_puesto_default = ""
            departamento_default = "Producción"
            descripcion_default = ""
            autonomia_laboral_default = "Media"
            comprension_default = "Media"
            atencion_default = 3
            motricidad_default = "Media"
            interaccion_social_default = "Media"
            tolerancia_cambio_default = "Media"
            formacion_tecnica_default = "Ninguna"
            apoyos_puesto_default = "Medio"
            estilo_aprendizaje_default = []
            iniciativa_default = "Media"
            adaptabilidad_default = "Sí"
            tareas_default = []
            autonomia_requisito_default = False
            comprension_requisito_default = False
            atencion_requisito_default = False
            motricidad_requisito_default = False
            interaccion_social_requisito_default = False
            tolerancia_requisito_default = False
            formacion_requisito_default = False
            iniciativa_requisito_default = False

        st.markdown(f"**ID asignado automáticamente:** `{nuevo_id}`")

        st.subheader("Añadir nueva oferta de trabajo")

        with st.form("form_nueva_oferta"):

            st.markdown("### Información general del puesto")
            nombre_puesto = st.text_input("Nombre del puesto", value=nombre_puesto_default, help="Título del puesto de trabajo")
            departamento = st.selectbox(
                "Departamento / área",
                options=["Producción", "Ensamblaje", "Almacén", "Mantenimiento", "Calidad", "Otros"],
                index=["Producción", "Ensamblaje", "Almacén", "Mantenimiento", "Calidad", "Otros"].index(departamento_default),
                help="Área funcional o sector donde se realiza el trabajo"
            )
            descripcion_general = st.text_area("Descripción general", value=descripcion_default, help="Breve resumen de las tareas y funciones del puesto")

            st.markdown("### Requisitos funcionales")

            atributo_clave = st.selectbox(
                "Atributo clave del puesto (peso extra en el matching)",
                ["Ninguno", "Autonomía laboral", "Comprensión", "Atención", "Motricidad", "Interacción social", "Tolerancia al cambio", "Formación técnica", "Estilo de aprendizaje", "Iniciativa", "Apoyos disponibles"],
                help="Este atributo recibirá un peso adicional al calcular la compatibilidad del candidato."
            )

            autonomia_laboral = st.selectbox("Nivel de autonomía requerido", ["Baja", "Media", "Alta"], index=["Baja", "Media", "Alta"].index(autonomia_laboral_default))
            autonomia_requisito = st.checkbox("¿Es un requisito indispensable?", key="req_autonomia", value=autonomia_requisito_default)
            comprension = st.selectbox("Nivel de comprensión necesario", ["Baja", "Media", "Alta"], index=["Baja", "Media", "Alta"].index(comprension_default))
            comprension_requisito = st.checkbox("¿Es un requisito indispensable?", key="req_comprension", value=comprension_requisito_default)
            atencion = st.slider("Nivel de atención requerido", 1, 5, value=atencion_default)
            atencion_requisito = st.checkbox("¿Es un requisito indispensable?", key="req_atencion", value=atencion_requisito_default)
            motricidad = st.selectbox("Habilidad motriz necesaria", ["Baja", "Media", "Alta"], index=["Baja", "Media", "Alta"].index(motricidad_default))
            motricidad_requisito = st.checkbox("¿Es un requisito indispensable?", key="req_motricidad", value=motricidad_requisito_default)
            interaccion_social = st.selectbox("Necesidad de interacción social", ["Baja", "Media", "Alta"], index=["Baja", "Media", "Alta"].index(interaccion_social_default))
            interaccion_social_requisito = st.checkbox("¿Es un requisito indispensable?", key="req_interaccion_social", value=interaccion_social_requisito_default)
            tolerancia_cambio = st.selectbox("Tolerancia al cambio", ["Baja", "Media", "Alta"], index=["Baja", "Media", "Alta"].index(tolerancia_cambio_default))
            tolerancia_requisito = st.checkbox("¿Es un requisito indispensable?", key="req_tolerancia", value=tolerancia_requisito_default)
            formacion_tecnica = st.selectbox("Formación técnica deseada", ["Ninguna", "FP básica", "FP media", "FP superior"], index=["Ninguna", "FP básica", "FP media", "FP superior"].index(formacion_tecnica_default))
            formacion_requisito = st.checkbox("¿Es un requisito indispensable?", key="req_formacion", value=formacion_requisito_default)
            apoyos_puesto = st.selectbox("Apoyos disponibles en el puesto", ["Alto", "Medio", "Bajo"], index=["Alto", "Medio", "Bajo"].index(apoyos_puesto_default))
            estilo_aprendizaje = st.multiselect(
                "Estilo de aprendizaje deseado",
                ["Visual", "Oral", "Repetición", "Demostración"],
                default=estilo_aprendizaje_default,
                help="Selecciona uno o varios estilos preferentes para transmitir las tareas"
            )
            iniciativa = st.selectbox("Nivel de iniciativa requerido", ["Baja", "Media", "Alta"], index=["Baja", "Media", "Alta"].index(iniciativa_default))
            iniciativa_requisito = st.checkbox("¿Es un requisito indispensable?", key="req_iniciativa", value=iniciativa_requisito_default)
            adaptabilidad = st.radio("¿Posibilidades de adaptación del entorno?", ["Sí", "No"], index=["Sí", "No"].index(adaptabilidad_default))

            st.markdown("### Tareas principales asociadas al puesto")
            tareas = st.multiselect(
                "Selecciona tareas asociadas",
                ["Montaje", "Almacén", "Limpieza técnica", "Verificación", "Logística interna", "Otro"],
                default=tareas_default,
                help="Selecciona las principales tareas del puesto"
            )

            # Botón de envío

            enviado = st.form_submit_button("Guardar oferta")

            if enviado:
                nueva_oferta = {
                    "id": nuevo_id,
                    "nombre": nombre_puesto,
                    "departamento": departamento,
                    "descripcion": descripcion_general,
                    "autonomia_laboral": autonomia_laboral,
                    "comprension": comprension,
                    "atencion": atencion,
                    "motricidad": motricidad,
                    "interaccion_social": interaccion_social,
                    "tolerancia_cambio": tolerancia_cambio,
                    "formacion_tecnica": formacion_tecnica,
                    "apoyos_puesto": apoyos_puesto,
                    "estilo_aprendizaje": estilo_aprendizaje,
                    "iniciativa": iniciativa,
                    "adaptabilidad": adaptabilidad,
                    "tareas": tareas,
                    "atributo_clave": atributo_clave,
                    "requisitos": {
                        "autonomia_laboral": autonomia_requisito,
                        "comprension": comprension_requisito,
                        "atencion": atencion_requisito,
                        "motricidad": motricidad_requisito,
                        "interaccion_social": interaccion_social_requisito,
                        "tolerancia_cambio": tolerancia_requisito,
                        "formacion_tecnica": formacion_requisito,
                        "iniciativa": iniciativa_requisito
                    }
                }

                if oferta_en_edicion:
                    idx = next((i for i, o in enumerate(st.session_state.ofertas_guardadas) if o["id"] == nuevo_id), None)
                    if idx is not None:
                        st.session_state.ofertas_guardadas[idx] = nueva_oferta
                    st.session_state.oferta_en_edicion = None
                else:
                    st.session_state.ofertas_guardadas.append(nueva_oferta)
                st.success(f"Oferta {nuevo_id} guardada correctamente.")

    elif subopcion == "Ver o modificar ofertas existentes":
        st.subheader("Ofertas existentes")

        if not st.session_state.ofertas_guardadas:
            st.info("No existen ofertas disponibles.")
        else:
            for oferta in st.session_state.ofertas_guardadas:
                with st.expander(f"{oferta['id']} - {oferta['nombre']}"):
                    st.write(f"**Departamento / área:** {oferta['departamento']}")
                    st.write(f"**Descripción general:** {oferta['descripcion']}")
                    st.write(f"**Nivel de autonomía requerido:** {oferta['autonomia_laboral']}")
                    st.write(f"**Nivel de comprensión necesario:** {oferta['comprension']}")
                    st.write(f"**Nivel de atención requerido:** {oferta['atencion']}")
                    st.write(f"**Habilidad motriz necesaria:** {oferta['motricidad']}")
                    st.write(f"**Interacción social necesaria:** {oferta['interaccion_social']}")
                    st.write(f"**Tolerancia al cambio:** {oferta['tolerancia_cambio']}")
                    st.write(f"**Formación técnica deseada:** {oferta['formacion_tecnica']}")
                    st.write(f"**Apoyos disponibles:** {oferta['apoyos_puesto']}")
                    st.write(f"**Estilo de aprendizaje deseado:** {', '.join(oferta['estilo_aprendizaje'])}")
                    st.write(f"**Nivel de iniciativa requerido:** {oferta['iniciativa']}")
                    st.write(f"**Posibilidad de adaptar el entorno:** {oferta['adaptabilidad']}")
                    st.write(f"**Tareas asociadas:** {', '.join(oferta['tareas'])}")

                    if st.button(f"Modificar {oferta['id']}", key=f"mod_{oferta['id']}"):
                        st.session_state.oferta_en_edicion = oferta
                        st.session_state.subopcion = "Añadir nueva oferta de trabajo"
                        st.session_state.ultima_modificada = oferta["id"]
                        st.rerun()
                    if st.session_state.get("ultima_modificada") == oferta["id"]:
                        st.info(f"La oferta {oferta['id']} se ha cargado correctamente en el editor. Selecciona 'Añadir nueva oferta de trabajo' para modificarla.")

                    if st.button(f"Eliminar {oferta['id']}", key=f"del_{oferta['id']}"):
                        st.session_state.ofertas_guardadas = [
                            o for o in st.session_state.ofertas_guardadas if o["id"] != oferta["id"]
                        ]
                        st.success(f"Oferta {oferta['id']} eliminada correctamente.")
                        st.rerun()

elif opcion == "Matching":

    st.title("Sistema de Matching")
    st.markdown("Aquí se evalúa el encaje entre el perfil funcional y las ofertas disponibles.")

    perfil = st.session_state.get("perfil_funcional", None)

    # Verificar que hay perfil funcional

    if perfil is None:
        st.warning("Primero debes completar el perfil funcional en el Módulo 1.")
    elif not st.session_state.ofertas_guardadas:
        st.warning("No hay ofertas disponibles para comparar. Añade al menos una oferta en la sección 'Gestión de ofertas'.")
    else:
        st.subheader("Resultados del matching")
        st.markdown("#### Perfil funcional utilizado")
        for clave, valor in perfil.items():
            st.markdown(f"**{clave.replace('_', ' ').capitalize()}:** {valor}")

        def evaluar_compatibilidad(perfil, oferta):

            # Filtro de requisitos

            motivos_exclusion = []
            requisitos = oferta.get("requisitos", {})

            def nivel_a_valor(valor, tipo):
                escala = {"Baja": 1, "Media": 2, "Alta": 3}
                if tipo == "formacion":
                    escala = {"Ninguna": 1, "FP básica": 2, "FP media": 3, "FP superior": 4}
                return escala.get(valor, 0)

            if requisitos.get("autonomia_laboral") and perfil["autonomia_laboral"] < nivel_a_valor(oferta["autonomia_laboral"], "general"):
                motivos_exclusion.append("Autonomía")
            if requisitos.get("comprension"):
                if perfil["comprension_verbal"] not in ["Alta", "Media"] or perfil["comprension_lectora"] not in ["Alta", "Media"]:
                    motivos_exclusion.append("Comprensión")
            if requisitos.get("atencion") and perfil["atencion"] < oferta["atencion"]:
                motivos_exclusion.append("Atención")
            if requisitos.get("motricidad") and nivel_a_valor(perfil["motricidad_fina"], "general") < nivel_a_valor(oferta["motricidad"], "general"):
                motivos_exclusion.append("Motricidad")
            if requisitos.get("interaccion_social") and nivel_a_valor(perfil["trabajo_equipo"], "general") < nivel_a_valor(oferta["interaccion_social"], "general"):
                motivos_exclusion.append("Interacción")
            if requisitos.get("tolerancia_cambio") and nivel_a_valor(perfil["tolerancia_estres"], "general") < nivel_a_valor(oferta["tolerancia_cambio"], "general"):
                motivos_exclusion.append("Tolerancia")
            if requisitos.get("formacion_tecnica") and nivel_a_valor(perfil["formacion"], "formacion") < nivel_a_valor(oferta["formacion_tecnica"], "formacion"):
                motivos_exclusion.append("Formación")
            if requisitos.get("iniciativa") and perfil["iniciativa"] < nivel_a_valor(oferta["iniciativa"], "general"):
                motivos_exclusion.append("Iniciativa")

            if motivos_exclusion:
                return {"viable": False, "motivos": motivos_exclusion}

            # Puntuación

            puntos = 0
            detalle = []
            explicaciones = []

            # Autonomía laboral

            if perfil["autonomia_laboral"] >= nivel_a_valor(oferta["autonomia_laboral"], "general"):
                puntos += 2
                detalle.append("✅ Autonomía")
                explicaciones.append(f"Nivel de autonomía del perfil ({perfil['autonomia_laboral']}) iguala o supera lo requerido ({oferta['autonomia_laboral']}).")
            else:
                detalle.append("❌ Autonomía")
                explicaciones.append(f"Nivel de autonomía del perfil ({perfil['autonomia_laboral']}) es inferior a lo requerido ({oferta['autonomia_laboral']}).")

            # Comprensión verbal y lectora: Casuísticas parciales y bajas explícitas

            cv = perfil["comprension_verbal"]
            cl = perfil["comprension_lectora"]
            cv_valida = cv in ["Media", "Alta"]
            cl_valida = cl in ["Media", "Alta"]

            # Ambos suficientes

            if cv_valida and cl_valida:
                puntos += 2
                detalle.append("✅ Comprensión verbal")
                explicaciones.append(f"Nivel de comprensión verbal del perfil ({cv}) es suficiente para lo requerido ({oferta['comprension']}).")
                detalle.append("✅ Comprensión lectora")
                explicaciones.append(f"Nivel de comprensión lectora del perfil ({cl}) es suficiente para lo requerido ({oferta['comprension']}).")
            
            # Solo verbal suficiente

            elif cv_valida and not cl_valida:
                puntos += 1
                detalle.append("✅ Comprensión verbal")
                explicaciones.append(f"Nivel de comprensión verbal del perfil ({cv}) es suficiente, pero la comprensión lectora es baja ({cl}). Puede requerir instrucciones orales o apoyos visuales adicionales.")
                detalle.append("❌ Comprensión lectora")
                explicaciones.append(f"Nivel de comprensión lectora del perfil ({cl}) es inferior a lo requerido ({oferta['comprension']}). Riesgo si el puesto requiere leer instrucciones.")
           
            # Solo lectora suficiente

            elif not cv_valida and cl_valida:
                puntos += 1
                detalle.append("❌ Comprensión verbal")
                explicaciones.append(f"Nivel de comprensión verbal del perfil ({cv}) es inferior a lo requerido ({oferta['comprension']}), pero la comprensión lectora es suficiente ({cl}). Puede funcionar si se priorizan instrucciones escritas o visuales.")
                detalle.append("✅ Comprensión lectora")
                explicaciones.append(f"Nivel de comprensión lectora del perfil ({cl}) es suficiente para lo requerido ({oferta['comprension']}).")
            
            # Ambos bajos

            else:
                detalle.append("❌ Comprensión verbal")
                explicaciones.append(f"Nivel de comprensión verbal del perfil ({cv}) es bajo.")
                detalle.append("❌ Comprensión lectora")
                explicaciones.append(f"Nivel de comprensión lectora del perfil ({cl}) es baja. Riesgo elevado de dificultad para entender instrucciones, tanto orales como escritas.")

           
            # Atención

            if perfil["atencion"] >= oferta["atencion"]:
                puntos += 1
                detalle.append("✅ Atención")
                explicaciones.append(f"Nivel de atención del perfil ({perfil['atencion']}) iguala o supera lo requerido ({oferta['atencion']}).")
            else:
                detalle.append("❌ Atención")
                explicaciones.append(f"Nivel de atención del perfil ({perfil['atencion']}) es inferior a lo requerido ({oferta['atencion']}).")

            
            # Motricidad (motricidad fina y movilidad)

            mf_val = nivel_a_valor(perfil["motricidad_fina"], "general")
            mov_val = nivel_a_valor(perfil["movilidad"], "general")
            mot_req = nivel_a_valor(oferta["motricidad"], "general")
            mf_ok = mf_val >= mot_req
            mov_ok = mov_val >= mot_req
            if mf_ok and mov_ok:
                puntos += 2
                detalle.append("✅ motricidad_fina")
                explicaciones.append(f"Nivel de motricidad fina del perfil ({perfil['motricidad_fina']}) iguala o supera lo requerido ({oferta['motricidad']}).")
                detalle.append("✅ movilidad")
                explicaciones.append(f"Nivel de movilidad del perfil ({perfil['movilidad']}) iguala o supera lo requerido ({oferta['motricidad']}).")
            elif mf_ok and not mov_ok:
                puntos += 1
                detalle.append("✅ motricidad_fina")
                explicaciones.append(f"Nivel de motricidad fina del perfil ({perfil['motricidad_fina']}) iguala o supera lo requerido ({oferta['motricidad']}), pero la movilidad es inferior ({perfil['movilidad']}). Puede requerir ajustes en desplazamientos o tareas físicas.")
                detalle.append("❌ movilidad")
                explicaciones.append(f"Nivel de movilidad del perfil ({perfil['movilidad']}) es inferior a lo requerido ({oferta['motricidad']}).")
            elif not mf_ok and mov_ok:
                puntos += 1
                detalle.append("❌ motricidad_fina")
                explicaciones.append(f"Nivel de motricidad fina del perfil ({perfil['motricidad_fina']}) es inferior a lo requerido ({oferta['motricidad']}), pero la movilidad general es suficiente ({perfil['movilidad']}). Puede funcionar si las tareas no requieren precisión manual.")
                detalle.append("✅ movilidad")
                explicaciones.append(f"Nivel de movilidad del perfil ({perfil['movilidad']}) iguala o supera lo requerido ({oferta['motricidad']}).")
            else:
                detalle.append("❌ motricidad_fina")
                explicaciones.append(f"Nivel de motricidad fina del perfil ({perfil['motricidad_fina']}) es inferior a lo requerido ({oferta['motricidad']}).")
                detalle.append("❌ movilidad")
                explicaciones.append(f"Nivel de movilidad del perfil ({perfil['movilidad']}) es inferior a lo requerido ({oferta['motricidad']}).")

            # Trabajo en equipo y habilidades sociales

            te_val = nivel_a_valor(perfil["trabajo_equipo"], "general")
            hs_val = nivel_a_valor(perfil["habilidades_sociales"], "general")
            inter_req = nivel_a_valor(oferta["interaccion_social"], "general")
            te_ok = te_val >= inter_req
            hs_ok = hs_val >= inter_req
            if te_ok and hs_ok:
                puntos += 2
                detalle.append("✅ trabajo_equipo")
                explicaciones.append(f"Nivel de trabajo en equipo del perfil ({perfil['trabajo_equipo']}) iguala o supera lo requerido ({oferta['interaccion_social']}).")
                detalle.append("✅ habilidades_sociales")
                explicaciones.append(f"Nivel de habilidades sociales del perfil ({perfil['habilidades_sociales']}) iguala o supera lo requerido ({oferta['interaccion_social']}).")
            elif te_ok and not hs_ok:
                puntos += 1
                detalle.append("✅ trabajo_equipo")
                explicaciones.append(f"Nivel de trabajo en equipo del perfil ({perfil['trabajo_equipo']}) es suficiente, pero habilidades sociales son inferiores ({perfil['habilidades_sociales']}). Puede funcionar si el entorno es estructurado o hay supervisión.")
                detalle.append("❌ habilidades_sociales")
                explicaciones.append(f"Nivel de habilidades sociales del perfil ({perfil['habilidades_sociales']}) es inferior a lo requerido ({oferta['interaccion_social']}).")
            elif not te_ok and hs_ok:
                puntos += 1
                detalle.append("❌ trabajo_equipo")
                explicaciones.append(f"Nivel de trabajo en equipo del perfil ({perfil['trabajo_equipo']}) es inferior a lo requerido ({oferta['interaccion_social']}), pero las habilidades sociales generales son suficientes ({perfil['habilidades_sociales']}). Puede adaptarse a tareas individuales o con poco trabajo grupal.")
                detalle.append("✅ habilidades_sociales")
                explicaciones.append(f"Nivel de habilidades sociales del perfil ({perfil['habilidades_sociales']}) iguala o supera lo requerido ({oferta['interaccion_social']}).")
            else:
                detalle.append("❌ trabajo_equipo")
                explicaciones.append(f"Nivel de trabajo en equipo del perfil ({perfil['trabajo_equipo']}) es inferior a lo requerido ({oferta['interaccion_social']}).")
                detalle.append("❌ habilidades_sociales")
                explicaciones.append(f"Nivel de habilidades sociales del perfil ({perfil['habilidades_sociales']}) es inferior a lo requerido ({oferta['interaccion_social']}).")

            # Tolerancia al cambio

            if nivel_a_valor(perfil["tolerancia_estres"], "general") >= nivel_a_valor(oferta["tolerancia_cambio"], "general"):
                puntos += 1
                detalle.append("✅ Tolerancia")
                explicaciones.append(f"Nivel de tolerancia al cambio/estrés del perfil ({perfil['tolerancia_estres']}) iguala o supera lo requerido ({oferta['tolerancia_cambio']}).")
            else:
                detalle.append("❌ Tolerancia")
                explicaciones.append(f"Nivel de tolerancia al cambio/estrés del perfil ({perfil['tolerancia_estres']}) es inferior a lo requerido ({oferta['tolerancia_cambio']}).")

            # Sobrecualificación explícita

            formacion_valores = {"Ninguna": 1, "FP básica": 2, "FP media": 3, "FP superior": 4, "Universidad": 5}
            f_perfil = perfil["formacion"]
            f_oferta = oferta["formacion_tecnica"]
            f_diff = formacion_valores.get(f_perfil, 0) - formacion_valores.get(f_oferta, 0)
            if f_diff == 0:
                puntos += 2
                detalle.append("✅ Formación igual")
                explicaciones.append(f"Nivel de formación del perfil ({f_perfil}) coincide con el requerido ({f_oferta}).")
            elif f_diff > 0:
                puntos += 1
                detalle.append("✅ Formación superior")

                # Sobrecualificación explícita si la diferencia es grande

                if formacion_valores.get(f_perfil, 0) >= 5 and formacion_valores.get(f_oferta, 0) <= 2:
                    explicaciones.append(f"Nivel de formación del perfil ({f_perfil}) es muy superior al requerido ({f_oferta}). Puede haber riesgo de sobrecualificación o falta de motivación en tareas muy básicas.")
                else:
                    explicaciones.append(f"Nivel de formación del perfil ({f_perfil}) es superior al requerido ({f_oferta}).")
            else:
                detalle.append("❌ Formación inferior")
                explicaciones.append(f"Nivel de formación del perfil ({f_perfil}) es inferior al requerido ({f_oferta}).")

            # Añadir explicación si el perfil es diverso

            estilos_perfil = perfil["estilo_aprendizaje"]
            estilos_oferta = oferta["estilo_aprendizaje"]
            if set(estilos_perfil).intersection(set(estilos_oferta)):
                puntos += 1
                detalle.append("✅ Estilo de aprendizaje")
                explicaciones.append(f"Al menos un estilo de aprendizaje del perfil ({', '.join(estilos_perfil)}) coincide con los deseados ({', '.join(estilos_oferta)}).")
            else:
                detalle.append("❌ Estilo de aprendizaje")

                # Perfil con varios estilos, aunque no coincidan

                if len(estilos_perfil) >= 3:
                    explicaciones.append(f"Ningún estilo de aprendizaje del perfil ({', '.join(estilos_perfil)}) coincide exactamente con los deseados ({', '.join(estilos_oferta)}), pero el perfil muestra variedad y puede adaptarse a diferentes formas de aprendizaje.")
                elif not estilos_perfil:
                    explicaciones.append("No se ha definido ningún estilo de aprendizaje en el perfil, lo que dificulta estimar el ajuste con los estilos deseados.")
                else:
                    explicaciones.append(f"Ningún estilo de aprendizaje del perfil ({', '.join(estilos_perfil)}) coincide con los deseados ({', '.join(estilos_oferta)}). Puede ser necesario adaptar la metodología de aprendizaje.")

            # Caso diferencia de un punto

            ini_perfil = perfil["iniciativa"]
            ini_oferta = nivel_a_valor(oferta["iniciativa"], "general")
            if ini_perfil >= ini_oferta:
                puntos += 1
                detalle.append("✅ Iniciativa")
                explicaciones.append(f"Nivel de iniciativa del perfil ({ini_perfil}) iguala o supera lo requerido ({oferta['iniciativa']}).")
            elif ini_perfil == ini_oferta - 1:
                detalle.append("⚠️ Iniciativa ajustada")
                explicaciones.append(f"Nivel de iniciativa del perfil ({ini_perfil}) es solo un punto inferior a lo requerido ({oferta['iniciativa']}). Podría ajustarse con apoyos o entrenamiento específico.")
            else:
                detalle.append("❌ Iniciativa")
                explicaciones.append(f"Nivel de iniciativa del perfil ({ini_perfil}) es inferior a lo requerido ({oferta['iniciativa']}).")

            # Caso de diferencia pequeña

            apoyos = {"Alta": 3, "Media": 2, "Baja": 1}
            perfil_apoyo = apoyos.get(perfil["apoyos_externos"], 0)
            oferta_apoyo = apoyos.get(oferta["apoyos_puesto"], 0)
            if perfil_apoyo <= oferta_apoyo:
                puntos += 1
                detalle.append("✅ Apoyos disponibles")
                explicaciones.append(f"La necesidad de apoyos externos del perfil ({perfil['apoyos_externos']}) es igual o menor que los apoyos disponibles en el puesto ({oferta['apoyos_puesto']}).")
            elif perfil_apoyo == oferta_apoyo + 1:
                detalle.append("⚠️ Apoyos casi suficientes")
                explicaciones.append(f"La necesidad de apoyos externos del perfil ({perfil['apoyos_externos']}) es ligeramente superior a los apoyos disponibles en el puesto ({oferta['apoyos_puesto']}). Puede adaptarse con pequeños ajustes o apoyos adicionales puntuales.")
            else:
                detalle.append("❌ Apoyos insuficientes")
                explicaciones.append(f"La necesidad de apoyos externos del perfil ({perfil['apoyos_externos']}) es superior a los apoyos disponibles en el puesto ({oferta['apoyos_puesto']}).")
                if perfil_apoyo == 3 and oferta_apoyo == 1:
                    explicaciones[-1] += " El ajuste puede ser muy difícil sin recursos adicionales."
                elif perfil_apoyo == 3 and oferta_apoyo == 2:
                    explicaciones[-1] += " Se recomienda valorar apoyos complementarios externos para facilitar el desempeño."
                elif perfil_apoyo == 2 and oferta_apoyo == 1:
                    explicaciones[-1] += " Puede ser posible con ajustes menores o acompañamiento inicial."

            # Peso extra por atributo clave

            atributo_clave = oferta.get("atributo_clave", "Ninguno")
            atributo_sumado = False
            if atributo_clave != "Ninguno":
                if atributo_clave == "Autonomía laboral" and perfil["autonomia_laboral"] >= nivel_a_valor(oferta["autonomia_laboral"], "general"):
                    puntos += 2
                    detalle.append("⭐ Atributo clave: Autonomía (peso extra)")
                    explicaciones.append("El perfil cumple el atributo clave de autonomía laboral, otorgando peso extra.")
                    atributo_sumado = True
                elif atributo_clave == "Comprensión" and perfil["comprension_verbal"] in ["Media", "Alta"] and perfil["comprension_lectora"] in ["Media", "Alta"]:
                    puntos += 2
                    detalle.append("⭐ Atributo clave: Comprensión (peso extra)")
                    explicaciones.append("El perfil cumple el atributo clave de comprensión verbal y lectora, otorgando peso extra.")
                    atributo_sumado = True
                elif atributo_clave == "Atención" and perfil["atencion"] >= oferta["atencion"]:
                    puntos += 2
                    detalle.append("⭐ Atributo clave: Atención (peso extra)")
                    explicaciones.append("El perfil cumple el atributo clave de atención, otorgando peso extra.")
                    atributo_sumado = True
                elif atributo_clave == "Motricidad" and all(nivel_a_valor(perfil[campo], "general") >= nivel_a_valor(oferta["motricidad"], "general") for campo in ["motricidad_fina", "movilidad"]):
                    puntos += 2
                    detalle.append("⭐ Atributo clave: Motricidad (peso extra)")
                    explicaciones.append("El perfil cumple el atributo clave de motricidad fina y movilidad, otorgando peso extra.")
                    atributo_sumado = True
                elif atributo_clave == "Interacción social" and all(nivel_a_valor(perfil[campo], "general") >= nivel_a_valor(oferta["interaccion_social"], "general") for campo in ["trabajo_equipo", "habilidades_sociales"]):
                    puntos += 2
                    detalle.append("⭐ Atributo clave: Interacción (peso extra)")
                    explicaciones.append("El perfil cumple el atributo clave de trabajo en equipo y habilidades sociales, otorgando peso extra.")
                    atributo_sumado = True
                elif atributo_clave == "Tolerancia al cambio" and nivel_a_valor(perfil["tolerancia_estres"], "general") >= nivel_a_valor(oferta["tolerancia_cambio"], "general"):
                    puntos += 2
                    detalle.append("⭐ Atributo clave: Tolerancia al cambio (peso extra)")
                    explicaciones.append("El perfil cumple el atributo clave de tolerancia al cambio, otorgando peso extra.")
                    atributo_sumado = True
                elif atributo_clave == "Formación técnica":
                    formacion_diff = nivel_a_valor(perfil["formacion"], "formacion") - nivel_a_valor(oferta["formacion_tecnica"], "formacion")
                    if formacion_diff >= 0:
                        puntos += 2
                        detalle.append("⭐ Atributo clave: Formación técnica (peso extra)")
                        explicaciones.append("El perfil cumple el atributo clave de formación técnica, otorgando peso extra.")
                        atributo_sumado = True
                elif atributo_clave == "Estilo de aprendizaje" and set(perfil["estilo_aprendizaje"]).intersection(set(oferta["estilo_aprendizaje"])):
                    puntos += 2
                    detalle.append("⭐ Atributo clave: Estilo de aprendizaje (peso extra)")
                    explicaciones.append("El perfil cumple el atributo clave de estilo de aprendizaje, otorgando peso extra.")
                    atributo_sumado = True
                elif atributo_clave == "Iniciativa" and perfil["iniciativa"] >= nivel_a_valor(oferta["iniciativa"], "general"):
                    puntos += 2
                    detalle.append("⭐ Atributo clave: Iniciativa (peso extra)")
                    explicaciones.append("El perfil cumple el atributo clave de iniciativa, otorgando peso extra.")
                    atributo_sumado = True
                elif atributo_clave == "Apoyos disponibles":
                    apoyos = {"Alta": 3, "Media": 2, "Baja": 1}
                    if apoyos.get(perfil["apoyos_externos"], 0) <= apoyos.get(oferta["apoyos_puesto"], 0):
                        puntos += 2
                        detalle.append("⭐ Atributo clave: Apoyos disponibles (peso extra)")
                        explicaciones.append("El perfil cumple el atributo clave de apoyos disponibles, otorgando peso extra.")
                        atributo_sumado = True
            if not atributo_sumado and atributo_clave != "Ninguno":
                detalle.append(f"❗ Atributo clave no cumplido: {atributo_clave}")
                explicaciones.append(f"El perfil no cumple el atributo clave requerido: {atributo_clave}.")

            # Compatibilidad cualitativa

            if puntos >= 13:
                nivel = "Muy alta"
            elif puntos >= 10:
                nivel = "Alta"
            elif puntos >= 7:
                nivel = "Media"
            elif puntos >= 4:
                nivel = "Baja"
            else:
                nivel = "No recomendado"

            return {
                "viable": True,
                "puntos": puntos,
                "nivel": nivel,
                "detalle": detalle,
                "explicaciones": explicaciones
            }

        # Ordenar las ofertas por compatibilidad descendente

        resultados_ofertas = []
        for oferta in st.session_state.ofertas_guardadas:
            resultado = evaluar_compatibilidad(perfil, oferta)
            resultados_ofertas.append((oferta, resultado))

        # Ordenar por puntuación (o -1 si no viable)

        resultados_ofertas.sort(key=lambda x: x[1]["puntos"] if x[1]["viable"] else -1, reverse=True)

        for oferta, resultado in resultados_ofertas:
            with st.expander(f"{oferta['id']} - {oferta['nombre']}                                                                 Puntuación: {resultado['puntos']}/15"):
                st.write(f"**Departamento:** {oferta['departamento']}")
                
                # Visualización de atributo clave

                if oferta.get("atributo_clave", "Ninguno") != "Ninguno":
                    if f"⭐ Atributo clave: {oferta['atributo_clave']} (peso extra)" in resultado["detalle"]:
                        st.success(f"Atributo clave '{oferta['atributo_clave']}' cumplido ✅")
                    else:
                        st.warning(f"Atributo clave '{oferta['atributo_clave']}' no cumplido ❌")

                if not resultado["viable"]:
                    st.error("No disponible (no cumple requisitos mínimos)")
                    st.caption("Motivos: " + ", ".join(resultado["motivos"]))
                else:
                    st.write(f"**Compatibilidad:** {resultado['nivel']}")
                    st.write(f"**Puntuación total:** {resultado['puntos']} / 15")
                    st.write("**Encaje por áreas:**")
                    for linea, justificacion in zip(resultado["detalle"], resultado["explicaciones"]):
                        st.markdown(f"- {linea} ℹ️ <span style='font-size:small; color:gray'>{justificacion}</span>", unsafe_allow_html=True)
                    if st.button(f"Seleccionar {oferta['id']}"):
                        st.session_state["puesto_seleccionado"] = oferta
                        st.success(f"Has seleccionado la oferta {oferta['id']}.")

elif opcion == "Itinerario personalizado":

    # Comprobación obligatoria de perfil funcional y oferta seleccionada

    perfil_funcional = st.session_state.get("perfil_funcional", None)
    oferta_seleccionada = st.session_state.get("puesto_seleccionado", None)
    if perfil_funcional is None or oferta_seleccionada is None:
        st.warning("Debe completar el perfil funcional (Módulo 1) y seleccionar una oferta (Módulo 2) para generar el itinerario.")
        st.stop()

    st.subheader("Itinerario personalizado")

    # Bloque de generación y visualización del itinerario personalizado

    st.success("Perfil funcional y oferta seleccionada correctamente cargados.")
    st.markdown(
        "A continuación se generará un plan estructurado de incorporación progresiva al puesto, adaptado a las características del perfil y las exigencias de la oferta."
    )

    # Resumen perfil y puesto

    st.subheader("Resumen del perfil y exigencias del puesto")
    perfil = perfil_funcional
    puesto = {
        "departamento": oferta_seleccionada.get("departamento", ""),
        "formacion_requerida": oferta_seleccionada.get("formacion_tecnica", ""),
        "tareas_manual_repetitivas": any(tarea in oferta_seleccionada.get("tareas", []) for tarea in ["Montaje", "Verificación", "Limpieza técnica"]),
        "presion_alta": oferta_seleccionada.get("tolerancia_cambio", "Media") == "Alta",
        "interaccion_externa": oferta_seleccionada.get("interaccion_social", "Media") == "Alta",
        "requiere_decisiones": oferta_seleccionada.get("iniciativa", "Media") == "Alta",
        "tareas_distintas": len(oferta_seleccionada.get("tareas", [])),
    }
    st.markdown(f"""
    **Perfil funcional:**
    - Autonomía: {perfil.get("autonomia_laboral", "")}
    - Comprensión: {perfil.get("comprension_verbal", "")}/{perfil.get("comprension_lectora", "")}
    - Atención: {perfil.get("atencion", "")}
    - Interacción: {perfil.get("interaccion", perfil.get("trabajo_equipo", ""))}
    - Iniciativa: {perfil.get("iniciativa", "")}
    - Rama: {"DI" if perfil.get("certificado_discapacidad", False) else "CIL"}

    **Puesto seleccionado:**
    - Departamento: {puesto["departamento"]}
    - Exigencia técnica: {puesto["formacion_requerida"]}, {puesto["tareas_manual_repetitivas"]}
    - Nivel de presión: {"Alta" if puesto["presion_alta"] else "Moderada/Baja"}
    - Nivel de interacción: {"Alta" if puesto["interaccion_externa"] else "Interna o limitada"}
    """)

    # --- Fase 1: Preparación y preincorporación ---

    with st.expander("Fase 1: Preparación y preincorporación", expanded=True):
        st.markdown("""
        **Objetivo general:** Organizar las acciones previas a la incorporación, centradas en la adaptación del entorno, sensibilización del equipo y apoyos iniciales para facilitar la integración de la persona candidata.
        """)
        rama = "DI" if perfil.get("certificado_discapacidad", False) else "CIL"
        
        # --- Pool de subfases posibles para Fase 1 ---

        pool_subfases_fase1 = [
            {"nombre": "Presentación del equipo y tour por la empresa", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Observación directa del entorno y rutinas básicas", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Microtareas asistidas en entorno real", "momento": "inicio", "condicion": lambda p, o: p.get("experiencia_laboral", "Ninguna") == "Ninguna"},
            {"nombre": "Familiarización con normas no escritas y cultura del taller", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Simulación de tareas clave con supervisión", "momento": "medio", "condicion": lambda p, o: p.get("autonomia_laboral", "Media") in ["Baja", "Escasa"]},
            {"nombre": "Detección de barreras físicas y adaptación ergonómica", "momento": "medio", "condicion": lambda p, o: p.get("motricidad_fina", "Media") == "Baja"},
            {"nombre": "Creación de materiales visuales o pictogramas", "momento": "medio", "condicion": lambda p, o: p.get("comprension_verbal", "Media") == "Baja"},
            {"nombre": "Ensayo con instrucciones verbales no estandarizadas", "momento": "medio", "condicion": lambda p, o: not o.get("instrucciones_estandarizadas", True)},
            {"nombre": "Rutinas de entrenamiento atencional progresivo", "momento": "final", "condicion": lambda p, o: p.get("atencion", "Media") in ["Baja", "Escasa"]},
            {"nombre": "Interacción informal con el equipo y dinámicas sociales", "momento": "final", "condicion": lambda p, o: p.get("habilidades_sociales", "Media") in ["Baja", "Escasa"]},
            {"nombre": "Simulación de jornada completa con validación técnica", "momento": "final", "condicion": lambda p, o: p.get("autonomia_laboral", "Media") in ["Baja", "Escasa"]},
        ]

        # --- Selección dinámica de subfases ---

        subfases_seleccionadas = [s for s in pool_subfases_fase1 if s["condicion"](perfil, oferta_seleccionada)]

        ordenadas_por_momento = {
            "inicio": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "inicio"],
            "medio": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "medio"],
            "final": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "final"],
        }

        # --- Visualización y cálculo de duración de la Fase 1 ---

        autonomia = perfil.get("autonomia_laboral", 3)
        comprension_v = perfil.get("comprension_verbal", "Media")
        comprension_l = perfil.get("comprension_lectora", "Media")
        iniciativa = perfil.get("iniciativa", 3)
        atencion = perfil.get("atencion", 3)
        experiencia = perfil.get("experiencia_laboral", "Ninguna")
        motricidad = perfil.get("motricidad_fina", "Media")
        movilidad = perfil.get("movilidad", "Media")
        apoyos_externos = perfil.get("apoyos_externos", "Media")
        trabajo_equipo = perfil.get("trabajo_equipo", "Aceptable")
        habilidades_sociales = perfil.get("habilidades_sociales", "Media")
        instrucciones_estandar = oferta_seleccionada.get("instrucciones_estandarizadas", True)
        duracion_fase1 = 1 if autonomia >= 4 and comprension_v == "Alta" and comprension_l == "Alta" and instrucciones_estandar and experiencia != "Ninguna" else 2 if autonomia <= 2 or comprension_v == "Baja" or comprension_l == "Baja" or not instrucciones_estandar or experiencia == "Ninguna" else 1.5
        duracion_fase1 = duracion_fase1 if isinstance(duracion_fase1, float) else float(duracion_fase1)

        # Subfases y apoyos

        subfases_fase1 = [s["nombre"] for s in subfases_seleccionadas]
        apoyos_fase1 = []

        # Apoyos recomendados según perfil y oferta

        if perfil.get("apoyos_externos", "Media") == "Alta":
            apoyos_fase1.append("Acompañamiento intensivo durante la primera semana.")
        if perfil.get("comprension_verbal", "Media") == "Baja" or perfil.get("comprension_lectora", "Media") == "Baja":
            apoyos_fase1.append("Materiales visuales, pictogramas o instrucciones adaptadas.")
        if not instrucciones_estandar:
            apoyos_fase1.append("Elaboración de rutinas e instrucciones estandarizadas para facilitar el aprendizaje.")
        if perfil.get("experiencia_laboral", "Ninguna") == "Ninguna":
            apoyos_fase1.append("Simulaciones y prácticas supervisadas antes de la incorporación real.")
        if rama == "CIL":
            apoyos_fase1.append("Coordinación con tutor interno para seguimiento diario.")
        if perfil.get("habilidades_sociales", "Media") == "Baja":
            apoyos_fase1.append("Dinámicas de integración social y apoyo en la comunicación con el equipo.")
        
        # Justificación de la fase

        justificacion_fase1 = []
        if duracion_fase1 > 1.2:
            justificacion_fase1.append("Se recomienda una fase inicial prolongada debido a la baja autonomía o comprensión.")
        if perfil.get("experiencia_laboral", "Ninguna") == "Ninguna":
            justificacion_fase1.append("La ausencia de experiencia previa motiva reforzar la preincorporación y simulaciones.")
        if not instrucciones_estandar:
            justificacion_fase1.append("La falta de instrucciones estandarizadas requiere invertir tiempo en la creación de materiales y rutinas.")

        if "nivel_formacion" not in perfil:
            formacion_map = {"Ninguna": 1, "FP básica": 2, "FP media": 3, "FP superior": 4, "Universidad": 5, "ESO": 2, "Bachillerato": 3}
            perfil["nivel_formacion"] = formacion_map.get(perfil.get("formacion", "Ninguna"), 1)

        if perfil["nivel_formacion"] <= 2 and not instrucciones_estandar:
            duracion_fase1 += 1
            subfases_fase1.append("Semana extra de formación estructurada en procedimientos no estandarizados.")
            apoyos_fase1.append("Guías visuales paso a paso y acompañamiento adicional.")
            justificacion_fase1.append("Formación baja y falta de estandarización → entrenamiento adicional.")

        if "interaccion" not in perfil:
            interaccion_map = {"Escasa": 1, "Aceptable": 2, "Buena": 3}
            perfil["interaccion"] = interaccion_map.get(perfil.get("trabajo_equipo", "Aceptable"), 2)

        if perfil["interaccion"] < 2 and puesto["interaccion_externa"]:
            duracion_fase1 += 0.5
            subfases_fase1.append("Entrenamiento en interacción social con simulaciones prácticas.")
            apoyos_fase1.append("Guía de conversación y supervisión en interacciones reales.")
            justificacion_fase1.append("Interacción baja + tareas con público → se refuerza la preparación social.")

        # Bloque texto antes del gráfico

        st.markdown(f"**Duración estimada:** {duracion_fase1} semanas")
        st.markdown("**Subfases recomendadas:**")
        for s in subfases_fase1:
            st.markdown(f"- {s}")
        st.markdown("**Apoyos propuestos en esta fase:**")
        for apoyo in apoyos_fase1:
            st.markdown(f"- {apoyo}")
        alertas_f1 = []
        if experiencia == "Ninguna":
            alertas_f1.append("La persona no tiene experiencia previa: reforzar simulaciones y acompañamiento en la primera semana.")
        if not instrucciones_estandar:
            alertas_f1.append("Las tareas no están estandarizadas: dedicar tiempo adicional a la explicación y registro de rutinas.")
        if rama == "CIL":
            alertas_f1.append("En CIL, asegurar que el tutor interno dispone de recursos y tiempo para seguimiento diario.")
        if alertas_f1:
            st.markdown("**Alertas específicas:**")
            for a in alertas_f1:
                st.markdown(f"- {a}")
        if justificacion_fase1:
            st.info("¿Por qué este itinerario?\n\n" + "\n".join(justificacion_fase1))
  
        # Visualización de la Fase 1 usando Plotly

        st.markdown("#### Representación visual de la Fase 1 (en semanas)")

        colores = {"inicio": "#B0E0E6", "medio": "#FFD700", "final": "#FFB6C1"}
        barras = []

        for idx, subfase in enumerate(subfases_seleccionadas):
            mom = subfase["momento"]
            if mom == "inicio":
                start = 0
                end = duracion_fase1 * 0.4
            elif mom == "medio":
                start = duracion_fase1 * 0.25
                end = duracion_fase1 * 0.75
            else:
                start = duracion_fase1 * 0.6
                end = duracion_fase1

            barras.append(go.Bar(
                x=[end - start],
                y=[subfase["nombre"]],
                base=start,
                orientation='h',
                marker=dict(color=colores.get(mom, "#CCCCCC")),
                hovertemplate=f"{subfase['nombre']}<br>Bloque: {mom.capitalize()}<br>Duración: {round(end - start, 2)} semanas<extra></extra>"
            ))

        layout = go.Layout(
            xaxis=dict(title="Semanas", range=[0, duracion_fase1]),
            yaxis=dict(title="Subfases", autorange="reversed"),
            height=400 + 30 * len(subfases_seleccionadas),
            margin=dict(l=150, r=40, t=40, b=40),
            barmode='stack',
            showlegend=False
        )

        fig = go.Figure(data=barras, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Recomendaciones y apoyos sugeridos")

        # Mensajes generales según rama

        if rama == "DI":
            st.info("Este perfil dispone de certificado de discapacidad, por lo que puede acceder a recursos y apoyos institucionales adicionales que deben considerarse desde esta fase.")
        else:
            st.warning("Este perfil no dispone de certificado de discapacidad, lo que limita el acceso a algunos recursos institucionales. Es recomendable reforzar apoyos internos desde el entorno laboral.")

        # Apoyos individualizados sugeridos (texto generado dinámicamente)

        apoyos_sugeridos = []
        if autonomia <= 2:
            apoyos_sugeridos.append("Asignar tutor/a de referencia durante los primeros días.")
        if comprension_v == "Baja" or comprension_l == "Baja":
            apoyos_sugeridos.append("Usar lenguaje claro, pictogramas o materiales visuales para explicar rutinas.")
        if atencion <= 2:
            apoyos_sugeridos.append("Fraccionar tareas en pasos cortos con tiempos definidos y supervisión frecuente.")
        if experiencia == "Ninguna":
            apoyos_sugeridos.append("Ofrecer un periodo de observación y familiarización progresiva antes de asumir tareas.")
        if motricidad == "Baja":
            apoyos_sugeridos.append("Valorar adaptaciones ergonómicas del puesto.")
        if movilidad == "Baja":
            apoyos_sugeridos.append("Comprobar accesibilidad de los desplazamientos internos y externos.")
        if trabajo_equipo == "Escasa" or habilidades_sociales == "Escasa":
            apoyos_sugeridos.append("Facilitar dinámicas informales o espacios estructurados para fomentar interacción social.")
        if apoyos_sugeridos:
            for apoyo in apoyos_sugeridos:
                st.markdown(f"- {apoyo}")
        else:
            st.markdown("No se identifican apoyos críticos adicionales para esta fase según el perfil ingresado.")

    # --- Fase 2: Incorporación inicial ---

    with st.expander("Fase 2: Incorporación inicial", expanded=False):
        st.markdown("""
        **Objetivo general:** Inicio de las actividades reales en el puesto, con un acompañamiento intensivo para que la persona se adapte al ritmo, tareas y dinámica del entorno. Es la fase más sensible del itinerario.
        """)

        rama = "DI" if perfil.get("certificado_discapacidad", False) else "CIL"
        instrucciones_estandar = oferta_seleccionada.get("instrucciones_estandarizadas", True)

        # --- Pool de subfases posibles para Fase 2 ---

        pool_subfases_fase2 = [
            {"nombre": "Observación del puesto y tareas reales", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Simulación práctica bajo supervisión directa", "momento": "inicio", "condicion": lambda p, o: p.get("experiencia_laboral", "Ninguna") == "Ninguna"},
            {"nombre": "Inicio de tareas con apoyo continuo", "momento": "inicio", "condicion": lambda p, o: p.get("autonomia_laboral", 3) <= 2},
            {"nombre": "Desglose de procesos en pasos visuales", "momento": "medio", "condicion": lambda p, o: p.get("comprension_verbal", "Media") == "Baja"},
            {"nombre": "Guía estructurada mediante checklist", "momento": "medio", "condicion": lambda p, o: not o.get("instrucciones_estandarizadas", True)},
            {"nombre": "Validación paralela de tareas realizadas", "momento": "medio", "condicion": lambda p, o: p.get("atencion", 3) <= 2},
            {"nombre": "Feedback diario de tareas realizadas", "momento": "medio", "condicion": lambda p, o: True},
            {"nombre": "Resolución de pequeñas incidencias con apoyo", "momento": "final", "condicion": lambda p, o: p.get("iniciativa", 3) <= 2},
            {"nombre": "Ejecución autónoma supervisada", "momento": "final", "condicion": lambda p, o: True},
            {"nombre": "Evaluación de adaptación al ritmo y tiempos", "momento": "final", "condicion": lambda p, o: True},
        ]

        subfases_seleccionadas = [s for s in pool_subfases_fase2 if s["condicion"](perfil, oferta_seleccionada)]
        ordenadas_por_momento = {
            "inicio": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "inicio"],
            "medio": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "medio"],
            "final": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "final"],
        }

        # Cálculo de duración

        duracion_fase2 = 2
        if perfil.get("autonomia_laboral", 3) <= 2 and oferta_seleccionada.get("tareas_repetitivas", False):
            duracion_fase2 = 3
        if perfil.get("comprension_verbal", "Media") == "Baja" and not instrucciones_estandar:
            duracion_fase2 = 3.5
        if perfil.get("atencion", 3) <= 2 and oferta_seleccionada.get("control_calidad", False):
            duracion_fase2 = 4
        if perfil.get("iniciativa", 3) <= 2 and oferta_seleccionada.get("requiere_decisiones", False):
            duracion_fase2 = 4
        if rama == "CIL" and not oferta_seleccionada.get("apoyo_interno_disponible", True):
            duracion_fase2 += 1
        duracion_fase2 = float(duracion_fase2)

        subfases_fase2 = [s["nombre"] for s in subfases_seleccionadas]
        apoyos_fase2 = []
        if rama == "DI":
            apoyos_fase2.append("Acompañamiento de preparador laboral externo durante toda la fase.")
        else:
            apoyos_fase2.append("Asignación de tutor interno con sesiones de seguimiento diario.")
        if perfil.get("comprension_verbal", "Media") == "Baja" or not instrucciones_estandar:
            apoyos_fase2.append("Checklist visuales, mapa de tareas y adaptación accesible del entorno.")
        if perfil.get("atencion", 3) <= 2:
            apoyos_fase2.append("Validación cruzada de entregables y revisión frecuente.")
        if perfil.get("iniciativa", 3) <= 2:
            apoyos_fase2.append("Supervisión intensiva con feedback inmediato y resolución guiada de dudas.")
        if rama == "CIL" and not oferta_seleccionada.get("apoyo_interno_disponible", True):
            apoyos_fase2.append("Asignar recurso parcial interno o reformular las condiciones de acompañamiento.")

        # Alertas

        alertas_fase2 = []
        if perfil.get("comprension_verbal", "Media") == "Baja" and not instrucciones_estandar:
            alertas_fase2.append("Instrucciones no estandarizadas y baja comprensión: riesgo de errores persistentes.")
        if perfil.get("iniciativa", 3) <= 2 and oferta_seleccionada.get("requiere_decisiones", False):
            alertas_fase2.append("El puesto requiere autonomía en toma de decisiones y el perfil no dispone de iniciativa suficiente.")
        if rama == "CIL" and not oferta_seleccionada.get("apoyo_interno_disponible", True):
            alertas_fase2.append("Sin apoyo interno definido en CIL: puede ser necesario reformular la fase o alargarla.")

        justificacion_fase2 = []
        if duracion_fase2 > 3:
            justificacion_fase2.append("Duración ampliada por combinación de baja comprensión, atención o autonomía.")
        if rama == "DI":
            justificacion_fase2.append("Se activa protocolo de empleo con apoyo mediante entidad externa acreditada.")
        else:
            justificacion_fase2.append("El itinerario se adapta a las limitaciones de apoyos institucionales en CIL.")

        # Mostramos información

        st.markdown(f"**Duración estimada:** {duracion_fase2} semanas")
        st.markdown("**Subfases recomendadas:**")
        for s in subfases_fase2:
            st.markdown(f"- {s}")
        st.markdown("**Apoyos propuestos en esta fase:**")
        for apoyo in apoyos_fase2:
            st.markdown(f"- {apoyo}")
    
        if alertas_fase2:
            st.markdown("**Alertas específicas:**")
            for a in alertas_fase2:
                st.markdown(f"- {a}")
        if justificacion_fase2:
            st.info("¿Por qué este itinerario?\n\n" + "\n".join(justificacion_fase2))

        # Representación visual de la Fase 2 (línea de tiempo)

        st.markdown("#### Representación visual de la Fase 2 (en semanas)")
        colores = {"inicio": "#B0E0E6", "medio": "#FFD700", "final": "#FFB6C1"}
        barras = []
        for idx, subfase in enumerate(subfases_seleccionadas):
            mom = subfase["momento"]
            if mom == "inicio":
                start = 0
                end = duracion_fase2 * 0.4
            elif mom == "medio":
                start = duracion_fase2 * 0.25
                end = duracion_fase2 * 0.75
            else:
                start = duracion_fase2 * 0.6
                end = duracion_fase2
            barras.append(go.Bar(
                x=[end - start],
                y=[subfase["nombre"]],
                base=start,
                orientation='h',
                marker=dict(color=colores.get(mom, "#CCCCCC")),
                hovertemplate=f"{subfase['nombre']}<br>Bloque: {mom.capitalize()}<br>Duración: {round(end - start, 2)} semanas<extra></extra>"
            ))

        layout = go.Layout(
            xaxis=dict(title="Semanas", range=[0, duracion_fase2]),
            yaxis=dict(title="Subfases", autorange="reversed"),
            height=400 + 30 * len(subfases_seleccionadas),
            margin=dict(l=150, r=40, t=40, b=40),
            barmode='stack',
            showlegend=False
        )
        fig = go.Figure(data=barras, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Recomendaciones y apoyos sugeridos")
        if rama == "DI":
            st.info("Este perfil dispone de certificado de discapacidad, por lo que puede acceder a recursos y apoyos institucionales adicionales que deben considerarse desde esta fase.")
        else:
            st.warning("Este perfil no dispone de certificado de discapacidad, lo que limita el acceso a algunos recursos institucionales. Es recomendable reforzar apoyos internos desde el entorno laboral.")

        apoyos_sugeridos_fase2 = []
        if perfil.get("autonomia_laboral", 3) <= 2:
            apoyos_sugeridos_fase2.append("Acompañamiento continuo las primeras semanas para consolidar las rutinas.")
        if perfil.get("comprension_verbal", "Media") == "Baja":
            apoyos_sugeridos_fase2.append("Descomposición de procesos en pasos visuales y repasos guiados.")
        if perfil.get("atencion", 3) <= 2:
            apoyos_sugeridos_fase2.append("Verificación frecuente del resultado de tareas, con repaso de errores.")
        if perfil.get("iniciativa", 3) <= 2:
            apoyos_sugeridos_fase2.append("Guía explícita ante incidencias, evitando múltiples alternativas hasta la semana 3.")
        if apoyos_sugeridos_fase2:
            for apoyo in apoyos_sugeridos_fase2:
                st.markdown(f"- {apoyo}")
        else:
            st.markdown("No se identifican apoyos críticos adicionales para esta fase según el perfil ingresado.")

    # --- Fase 3: Consolidación ---

    with st.expander("Fase 3: Consolidación", expanded=False):
        st.markdown("""
        **Objetivo general:** Evaluar si la persona puede sostener su desempeño con menor apoyo, promover la autonomía, resolver desajustes detectados y asegurar la viabilidad del puesto a medio plazo. Esta fase es clave para decidir si la inclusión es sostenible.
        """)
        rama = "DI" if perfil.get("certificado_discapacidad", False) else "CIL"
        autonomia = perfil.get("autonomia_laboral", 3)
        comprension = perfil.get("comprension_verbal", "Media")
        atencion = perfil.get("atencion", 3)
        interaccion = perfil.get("interaccion", 2)
        formacion = perfil.get("nivel_formacion", 3)
        puesto_estandarizado = oferta_seleccionada.get("instrucciones_estandarizadas", True)
        tiene_apoyos = perfil.get("apoyos_externos", "Media")

        # Duración fase 3

        if autonomia <= 2 and oferta_seleccionada.get("tareas_precision", False):
            duracion_fase3 = 6
        elif 2 <= atencion <= 3 and oferta_seleccionada.get("tareas_variables", False):
            duracion_fase3 = 5.5
        elif interaccion <= 2 and oferta_seleccionada.get("trabajo_equipo", False):
            duracion_fase3 = 5
        elif formacion <= 2 and not puesto_estandarizado:
            duracion_fase3 = 6
        elif rama == "CIL" and autonomia >= 3 and not oferta_seleccionada.get("estructura_apoyo", True):
            duracion_fase3 = 4
        elif rama == "DI" and tiene_apoyos == "Alta":
            duracion_fase3 = 4
        else:
            duracion_fase3 = 4.5

        pool_subfases_fase3 = [
            {"nombre": "Validación de ciclos completos de trabajo", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Observación silenciosa durante el desempeño", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Entrevista motivacional y revisión de objetivos", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Registro de progresos en tareas de precisión", "momento": "medio", "condicion": lambda p, o: p.get("autonomia_laboral", 3) <= 2},
            {"nombre": "Pruebas de desempeño autónomo sin supervisión directa", "momento": "medio", "condicion": lambda p, o: True},
            {"nombre": "Rotación de tareas bajo supervisión", "momento": "medio", "condicion": lambda p, o: o.get("tareas_variables", False)},
            {"nombre": "Simulación de conflictos sociales con feedback", "momento": "final", "condicion": lambda p, o: p.get("interaccion", 2) <= 2},
            {"nombre": "Autoevaluación estructurada semanal", "momento": "final", "condicion": lambda p, o: True},
            {"nombre": "Sesión final de revisión conjunta y cierre", "momento": "final", "condicion": lambda p, o: True},
            {"nombre": "Revisión técnica cruzada de calidad", "momento": "final", "condicion": lambda p, o: p.get("atencion", 3) <= 2},
        ]
        subfases_seleccionadas = [s for s in pool_subfases_fase3 if s["condicion"](perfil, oferta_seleccionada)]
        ordenadas_por_momento = {
            "inicio": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "inicio"],
            "medio": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "medio"],
            "final": [s["nombre"] for s in subfases_seleccionadas if s["momento"] == "final"],
        }

        subfases_fase3 = [s["nombre"] for s in subfases_seleccionadas]
        apoyos_fase3 = []
        if autonomia <= 2:
            apoyos_fase3.append("Doble validación operativa con supervisión interna permanente.")
        if interaccion <= 2:
            apoyos_fase3.append("Plan semanal de revisión emocional con mentor informal.")
        if formacion <= 2 and not puesto_estandarizado:
            apoyos_fase3.append("Itinerario formativo adaptado y revisión continua de competencias.")
        if rama == "DI" and tiene_apoyos == "Alta":
            apoyos_fase3.append("Seguimiento técnico mixto con apoyo externo institucional.")
        if rama == "CIL" and not oferta_seleccionada.get("estructura_apoyo", True):
            apoyos_fase3.append("Designación formal de un referente técnico dentro de la empresa.")

        alertas_f3 = []
        if autonomia <= 2 and oferta_seleccionada.get("tareas_precision", False):
            alertas_f3.append("Si en semana 3 no hay mejora sostenida → revisar viabilidad del puesto.")
        if interaccion <= 2:
            alertas_f3.append("Incluir test de clima social semanalmente.")
        if rama == "CIL" and not formacion > 2 and not puesto_estandarizado:
            alertas_f3.append("Recomendar inversión en formación previa antes de consolidar el puesto.")
        if rama == "DI" and tiene_apoyos != "Alta":
            alertas_f3.append("Evaluar acceso a recursos externos para sostener esta fase.")
        if not apoyos_fase3:
            alertas_f3.append("No se identifican apoyos críticos adicionales para esta fase.")

        justificacion_fase3 = []
        if duracion_fase3 > 4.5:
            justificacion_fase3.append("La complejidad del puesto o las necesidades del perfil justifican una fase de consolidación más extensa.")
        if autonomia <= 2:
            justificacion_fase3.append("Se requiere validar sostenibilidad del desempeño autónomo con tareas críticas.")
        if interaccion <= 2:
            justificacion_fase3.append("Es necesario asegurar la integración social antes de finalizar el proceso.")
        if not oferta_seleccionada.get("estructura_apoyo", True):
            justificacion_fase3.append("La falta de apoyos internos hace necesario extender la supervisión.")

        st.markdown(f"**Duración estimada:** {duracion_fase3} semanas")
        st.markdown("**Subfases recomendadas:**")
        for s in subfases_fase3:
            st.markdown(f"- {s}")
        st.markdown("**Apoyos propuestos en esta fase:**")
        for apoyo in apoyos_fase3:
            st.markdown(f"- {apoyo}")
        if alertas_f3:
            st.markdown("**Alertas específicas:**")
            for a in alertas_f3:
                st.markdown(f"- {a}")
        if justificacion_fase3:
            st.info("¿Por qué este itinerario?\n\n" + "\n".join(justificacion_fase3))

        # Visualización Fase 3

        st.markdown("#### Representación visual de la Fase 3 (en semanas)")
        colores = {"inicio": "#B0E0E6", "medio": "#FFD700", "final": "#FFB6C1"}
        barras = []
        for idx, subfase in enumerate(subfases_seleccionadas):
            mom = subfase["momento"]
            if mom == "inicio":
                start = 0
                end = duracion_fase3 * 0.4
            elif mom == "medio":
                start = duracion_fase3 * 0.25
                end = duracion_fase3 * 0.75
            else:
                start = duracion_fase3 * 0.6
                end = duracion_fase3
            barras.append(go.Bar(
                x=[end - start],
                y=[subfase["nombre"]],
                base=start,
                orientation='h',
                marker=dict(color=colores.get(mom, "#CCCCCC")),
                hovertemplate=f"{subfase['nombre']}<br>Bloque: {mom.capitalize()}<br>Duración: {round(end - start, 2)} semanas<extra></extra>"
            ))
        layout = go.Layout(
            xaxis=dict(title="Semanas", range=[0, duracion_fase3]),
            yaxis=dict(title="Subfases", autorange="reversed"),
            height=400 + 30 * len(subfases_seleccionadas),
            margin=dict(l=150, r=40, t=40, b=40),
            barmode='stack',
            showlegend=False
        )
        fig = go.Figure(data=barras, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Recomendaciones y apoyos sugeridos")
        if rama == "DI":
            st.info("Este perfil dispone de certificado de discapacidad, por lo que puede acceder a recursos y apoyos institucionales adicionales que deben considerarse desde esta fase.")
        else:
            st.warning("Este perfil no dispone de certificado de discapacidad, lo que limita el acceso a algunos recursos institucionales. Es recomendable reforzar apoyos internos desde el entorno laboral.")
        apoyos_sugeridos = []
        if autonomia <= 2:
            apoyos_sugeridos.append("Supervisión técnica frecuente y revisión cruzada de entregables.")
        if interaccion <= 2:
            apoyos_sugeridos.append("Planificar espacios de relación social e integración progresiva.")
        if formacion <= 2:
            apoyos_sugeridos.append("Ofrecer apoyo formativo adaptado al ritmo de aprendizaje del trabajador.")
        if apoyos_sugeridos:
            for apoyo in apoyos_sugeridos:
                st.markdown(f"- {apoyo}")
        else:
            st.markdown("No se identifican apoyos críticos adicionales para esta fase según el perfil ingresado.")

    # --- Fase 4: Evaluación y cierre ---

    with st.expander("Fase 4: Evaluación y cierre", expanded=False):
        st.markdown("""
        **Objetivo general:** Evaluar los resultados alcanzados durante la incorporación. Verificar si el trabajador puede mantenerse en el puesto con autonomía o con apoyos reducidos, y proponer ajustes, estabilización o transición.
        """)
        
        # Cálculo de duración personalizada

        progresion = perfil.get("progresion_global", 70)
        adaptacion_social = perfil.get("adaptacion_social", "Media")
        entorno_apoyo = oferta_seleccionada.get("estructura_apoyo", "Media")
        rama = "DI" if perfil.get("certificado_discapacidad", False) else "CIL"

        if progresion >= 70:
            duracion_fase4 = 1
        elif 50 <= progresion < 70:
            duracion_fase4 = 1.5
        elif progresion < 50:
            duracion_fase4 = 2
        elif adaptacion_social == "Baja":
            duracion_fase4 = 1.2
        else:
            duracion_fase4 = 1

        # Pool de subfases posibles

        pool_subfases_fase4 = [
            {"nombre": "Revisión final de competencias", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Entrevista de cierre estructurada", "momento": "inicio", "condicion": lambda p, o: True},
            {"nombre": "Simulación final en condiciones reales", "momento": "medio", "condicion": lambda p, o: p.get("progresion_global", 70) < 70},
            {"nombre": "Elaboración de plan de refuerzo individual", "momento": "medio", "condicion": lambda p, o: 50 <= p.get("progresion_global", 70) < 70},
            {"nombre": "Evaluación del encaje funcional", "momento": "medio", "condicion": lambda p, o: p.get("progresion_global", 70) < 50},
            {"nombre": "Sesión de devolución final", "momento": "final", "condicion": lambda p, o: True},
            {"nombre": "Diseño de plan de continuidad emocional", "momento": "final", "condicion": lambda p, o: p.get("adaptacion_social", "Media") == "Baja"},
            {"nombre": "Revisión del encaje social", "momento": "final", "condicion": lambda p, o: p.get("adaptacion_social", "Media") == "Baja"},
            {"nombre": "Informe de logros y seguimiento", "momento": "final", "condicion": lambda p, o: True},
            {"nombre": "Generación de calendario de seguimiento posterior", "momento": "final", "condicion": lambda p, o: rama == "CIL"}
        ]

        subfases_fase4 = [s for s in pool_subfases_fase4 if s["condicion"](perfil, oferta_seleccionada)]
        ordenadas_fase4 = {
            "inicio": [s["nombre"] for s in subfases_fase4 if s["momento"] == "inicio"],
            "medio": [s["nombre"] for s in subfases_fase4 if s["momento"] == "medio"],
            "final": [s["nombre"] for s in subfases_fase4 if s["momento"] == "final"],
        }

        # Visualización

        st.markdown(f"**Duración estimada:** {duracion_fase4} semanas")
        st.markdown("**Subfases recomendadas:**")
        for s in [s["nombre"] for s in subfases_fase4]:
            st.markdown(f"- {s}")

        st.markdown("**Apoyos propuestos en esta fase:**")
        apoyos_f4 = []
        if progresion >= 70:
            apoyos_f4.append("Evaluación compartida entre empresa y entidad externa" if rama == "DI" else "Evaluación interna por tutor o técnico")
        if 50 <= progresion < 70:
            apoyos_f4.append("Informe externo y plan de refuerzo" if rama == "DI" else "Fase extra de adaptación interna")
        if progresion < 50:
            apoyos_f4.append("Propuesta de reubicación o itinerario alternativo (DI)" if rama == "DI" else "Redefinición del puesto o derivación externa")
        if adaptacion_social == "Baja":
            apoyos_f4.append("Apoyo externo en habilidades sociales y plan de estabilización" if rama == "DI" else "Mentor interno y plan de coaching básico")
        if rama == "CIL":
            apoyos_f4.append("Definir calendario de seguimiento post-itinerario con tutor interno")
        for a in apoyos_f4:
            st.markdown(f"- {a}")

        alertas_f4 = []
        if progresion < 70:
            alertas_f4.append("Progresión incompleta: valorar extensión del itinerario o fase adicional")
        if rama == "CIL" and entorno_apoyo == "Baja":
            alertas_f4.append("Entorno sin estructura formal de seguimiento: riesgo de ruptura sin plan claro")
        if rama == "DI" and not perfil.get("apoyos_externos", False):
            alertas_f4.append("Faltan apoyos institucionales para una evaluación completa")
        if alertas_f4:
            st.markdown("**Alertas específicas:**")
            for a in alertas_f4:
                st.markdown(f"- {a}")

        st.markdown("#### Representación visual de la Fase 4 (en semanas)")
        colores = {"inicio": "#B0E0E6", "medio": "#FFD700", "final": "#FFB6C1"}
        barras = []

        for idx, subfase in enumerate(subfases_fase4):
            mom = subfase["momento"]
            if mom == "inicio":
                start = 0
                end = duracion_fase4 * 0.4
            elif mom == "medio":
                start = duracion_fase4 * 0.25
                end = duracion_fase4 * 0.75
            else:
                start = duracion_fase4 * 0.6
                end = duracion_fase4
            barras.append(go.Bar(
                x=[end - start],
                y=[subfase["nombre"]],
                base=start,
                orientation='h',
                marker=dict(color=colores.get(mom, "#CCCCCC")),
                hovertemplate=f"{subfase['nombre']}<br>Bloque: {mom.capitalize()}<br>Duración: {round(end - start, 2)} semanas<extra></extra>"
            ))

        layout = go.Layout(
            xaxis=dict(title="Semanas", range=[0, duracion_fase4]),
            yaxis=dict(title="Subfases", autorange="reversed"),
            height=400 + 30 * len(subfases_fase4),
            margin=dict(l=150, r=40, t=40, b=40),
            barmode='stack',
            showlegend=False
        )

        fig = go.Figure(data=barras, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Recomendaciones y apoyos sugeridos")
        if rama == "DI":
            st.info("Se recomienda convocar a la entidad de apoyo para validar la sostenibilidad del puesto.")
        else:
            st.warning("En CIL es imprescindible definir una figura interna de seguimiento para evitar rupturas laborales tempranas.")

    # --- FINAL DEL MÓDULO 3: VARIABLES PARA PASAR A 4 Y BOTÓN PARA INICIAR SEGUIMIENTO ---

    def calcular_duracion(perfil):
        autonomia = perfil.get("autonomia_laboral", 3)
        if autonomia <= 2:
            return 12
        elif autonomia == 3:
            return 8
        else:
            return 4

    def sugerir_frecuencia(perfil):
        autonomia = perfil.get("autonomia_laboral", 3)
        if autonomia <= 2:
            return "semanal"
        elif autonomia == 3:
            return "quincenal"
        else:
            return "mensual"
    
    st.markdown("---")
    st.subheader("¿Listo para iniciar el seguimiento?")
    if st.button("Iniciar seguimiento"):
        seguimiento = {
            "nombre_persona": perfil.get("nombre", "Sin nombre"),
            "rama": "DI" if perfil.get("certificado_discapacidad", False) else "CIL",
            "autonomia": perfil.get("autonomia_laboral", 3),
            "resultado_fase_4": None,
            "duracion_seguimiento": calcular_duracion(perfil),
            "frecuencia_revision": sugerir_frecuencia(perfil),
            "observaciones": []
        }
        st.session_state["seguimiento"] = seguimiento
        st.success("Seguimiento inicializado. Puedes continuar con el Módulo 4.")

elif opcion == "Seguimiento y evaluación":

    if "seguimiento" not in st.session_state:
        perfil = st.session_state.get("perfil_funcional", {})
        seguimiento = {
            "nombre_persona": perfil.get("nombre", "Sin nombre"),
            "rama": "DI" if perfil.get("certificado_discapacidad", False) else "CIL",
            "autonomia": perfil.get("autonomia_laboral", 3),
            "resultado_fase_4": None,
            "duracion_seguimiento": calcular_duracion(perfil),
            "frecuencia_revision": sugerir_frecuencia(perfil),
            "observaciones": []
        }
        st.session_state["seguimiento"] = seguimiento
        st.success("Seguimiento inicializado automáticamente. Puedes comenzar el seguimiento.")
    else:
        st.info("Seguimiento ya inicializado para: " + st.session_state["seguimiento"]["nombre_persona"])
    
    st.markdown("## Registro de observaciones semanales")

    seguimiento = st.session_state["seguimiento"]
    semanas = list(range(1, seguimiento["duracion_seguimiento"] + 1))

    st.markdown(f"**Duración del seguimiento:** {seguimiento['duracion_seguimiento']} semanas")
    st.markdown(f"**Frecuencia sugerida de revisión:** {seguimiento['frecuencia_revision'].capitalize()}")

    semana_actual = st.selectbox("Semana de seguimiento", semanas)

    indicadores = {
        "Desempeño técnico": [
            "Precisión técnica",
            "Tiempo de ejecución",
            "Adaptación a cambios menores"
        ],
        "Estabilidad emocional": [
            "Señales emocionales",
            "Motivación"
        ],
        "Interacción social y adaptación": [
            "Interacción social",
            "Aislamiento"
        ],
        "Nivel de apoyos requeridos": [
            "Apoyos requeridos",
            "Peticiones inesperadas"
        ],
        "Riesgo de ruptura del proceso": [
            "Absentismo o impuntualidad",
            "Riesgo de abandono"
        ]
    }

    descripciones_indicadores = {
        "Precisión técnica": "¿Está cumpliendo con los estándares de calidad definidos para su puesto? Fíjate si hay errores recurrentes o falta de atención.",
        "Tiempo de ejecución": "¿Tarda significativamente más (o menos) de lo previsto en completar las tareas asignadas? Observa si hay bloqueos o pausas innecesarias.",
        "Adaptación a cambios menores": "¿Cómo reacciona ante ajustes simples en el puesto (tareas, herramientas, turnos)? Evalúa si se adapta con normalidad o muestra resistencia.",
        "Señales emocionales": "¿Presenta signos de ansiedad, frustración, enfado o desánimo? Observa tanto la comunicación verbal como la no verbal.",
        "Motivación": "¿Ha cambiado su nivel de implicación o muestra falta de interés? Escucha sus comentarios y su actitud frente a las tareas.",
        "Interacción social": "¿Se relaciona con normalidad con el equipo? Evalúa si participa, colabora y responde a los intercambios sociales básicos.",
        "Aislamiento": "¿Ha disminuido su interacción voluntaria respecto a semanas anteriores? Observa si evita a los compañeros, se aísla o se muestra distante.",
        "Apoyos requeridos": "¿Sigue necesitando los apoyos previstos o han aumentado? Revisa si se está volviendo más dependiente o autónomo.",
        "Peticiones inesperadas": "¿Pide ayuda en cosas que no estaban previstas o entrenadas? Fíjate si esas peticiones indican falta de comprensión.",
        "Absentismo o impuntualidad": "¿Ha faltado o llegado tarde sin justificación? Registra si es algo puntual o si se repite en la misma semana.",
        "Riesgo de abandono": "¿Ha verbalizado intención de dejar el puesto o muestra señales claras de rechazo? Atiende a comentarios y actitudes."
    }

    dimension = st.selectbox("Dimensión observada", list(indicadores.keys()))
    indicador = st.selectbox("Indicador concreto", indicadores[dimension])
    
    # Descripción adaptativa

    st.markdown(f"*{descripciones_indicadores[indicador]}*")

    observacion = st.text_area("Observación libre del técnico", placeholder="Ejemplo: La persona mostró dificultad para adaptarse a una nueva tarea sin apoyo visual.")
    evaluacion = st.radio("Evaluación del estado actual", ["✔️ Bien", "⚠️ Cuidado", "❌ Crítico"], horizontal=True)

    if st.button("Guardar observación"):
        nueva_obs = {
            "semana": semana_actual,
            "dimension": dimension,
            "indicador": indicador,
            "observacion": observacion,
            "evaluacion": evaluacion
        }
        seguimiento["observaciones"].append(nueva_obs)
        st.success(f"Observación para la semana {semana_actual} registrada correctamente.")

    # Vista previa del histórico (últimas observaciones)

    if seguimiento["observaciones"]:
        st.markdown("### Últimas observaciones registradas")
        for obs in reversed(seguimiento["observaciones"][-5:]):
            st.markdown(f"**Semana {obs['semana']} – {obs['indicador']}**")
            st.markdown(f"- Evaluación: {obs['evaluacion']}")
            st.markdown(f"- Observación: {obs['observacion']}")
            st.markdown("---")
    
    def evaluar_alertas(observaciones):
        if not observaciones:
            return None  # No hay datos aún

        estado = {
            "riesgo_ruptura": False,
            "reactivar_fase_3": False,
            "alerta_emocional": False,
            "todo_estable": False,
            "mensaje_final": "",
            "color": "info"
        }

        criticos = ["Riesgo de abandono", "Absentismo o impuntualidad", "Señales emocionales"]
        consecutivos_positivos = 0
        semanas = sorted(list(set(obs["semana"] for obs in observaciones)))
        total_consecutivos = 0

        # Convertimos observaciones en una estructura por semana

        obs_por_semana = {}
        for obs in observaciones:
            sem = obs["semana"]
            if sem not in obs_por_semana:
                obs_por_semana[sem] = []
            obs_por_semana[sem].append(obs)

        # Análisis por semana

        for semana in semanas:
            semana_ok = True
            critico_esta_semana = False
            for obs in obs_por_semana[semana]:
                evaluacion = obs["evaluacion"]
                if obs["indicador"] in criticos and evaluacion in ["⚠️ Cuidado", "❌ Crítico"]:
                    estado["riesgo_ruptura"] = True
                    critico_esta_semana = True
                if obs["indicador"] == "Señales emocionales" and evaluacion in ["⚠️ Cuidado", "❌ Crítico"]:
                    estado["alerta_emocional"] = True
                if evaluacion == "❌ Crítico":
                    estado["reactivar_fase_3"] = True
                    semana_ok = False
                elif evaluacion == "⚠️ Cuidado":
                    semana_ok = False

            if semana_ok:
                consecutivos_positivos += 1
                total_consecutivos += 1
            else:
                consecutivos_positivos = 0

        # ¿Cierre?

        if consecutivos_positivos >= 3:
            estado["todo_estable"] = True

        # Mensaje final detallado según el análisis del seguimiento

        if estado["riesgo_ruptura"]:
            estado["mensaje_final"] = (
                "Se ha detectado un riesgo alto de ruptura en el proceso de inclusión. "
                "Recomendamos intervenir de inmediato, revisar las condiciones del puesto "
                "y valorar ajustes organizativos o apoyos adicionales."
            )
            estado["color"] = "error"

        elif estado["reactivar_fase_3"]:
            estado["mensaje_final"] = (
                "Se han observado desviaciones importantes en el desempeño o en la adaptación. "
                "Puede ser útil reformular tareas, reducir temporalmente la carga laboral o "
                "volver a entrenar algunos aspectos clave del puesto."
            )
            estado["color"] = "warning"

        elif estado["alerta_emocional"]:
            estado["mensaje_final"] = (
                "Existen señales sostenidas de malestar emocional. "
                "Se recomienda incluir acciones específicas de apoyo emocional en las próximas semanas, "
                "como espacios de escucha, tutoría o ajustes de entorno."
            )
            estado["color"] = "warning"

        elif estado["todo_estable"]:
            estado["mensaje_final"] = (
                "La evolución ha sido positiva durante las últimas semanas. "
                "Todos los indicadores clave se mantienen estables, por lo que se puede considerar cerrar "
                "el seguimiento formal y pasar a una fase de consolidación o revisión puntual."
            )
            estado["color"] = "success"

        else:
            estado["mensaje_final"] = (
                "El seguimiento continúa dentro de parámetros aceptables. "
                "No se han detectado incidencias graves, pero conviene mantener la observación regular."
            )
            estado["color"] = "info"

        return estado
    
    # Mostrar alerta actual basada en las observaciones 

    estado_alerta = evaluar_alertas(st.session_state["seguimiento"]["observaciones"])

    if estado_alerta:
        mensaje = estado_alerta["mensaje_final"]
        color = estado_alerta["color"]

        if color == "error":
            st.error(f"🚨 {mensaje}")
        elif color == "warning":
            st.warning(f"⚠️ {mensaje}")
        elif color == "success":
            st.success(f"✅ {mensaje}")
        else:
            st.info(f"ℹ️ {mensaje}")

    from collections import defaultdict

    # Procesar las observaciones para análisis gráfico

    def procesar_datos_observaciones(observaciones):
        if not observaciones:
            return {}, {}, []

        # Mapeo para convertir etiquetas completas a símbolos

        mapa_simbolos = {
            "✔️ Bien": "✔️",
            "⚠️ Cuidado": "⚠️",
            "❌ Crítico": "❌"
        }

        from collections import defaultdict
        resumen_semanal = defaultdict(lambda: {"✔️": 0, "⚠️": 0, "❌": 0})
        totales = {"✔️": 0, "⚠️": 0, "❌": 0}
        positivos_acumulados = []

        semanas_ordenadas = sorted(set(obs["semana"] for obs in observaciones))
        total_observaciones = 0
        acumulado_ok = 0

        for obs in observaciones:
            sem = obs["semana"]
            eval_completa = obs["evaluacion"]
            eval = mapa_simbolos.get(eval_completa, None)
            if not eval:
                continue

            resumen_semanal[sem][eval] += 1
            totales[eval] += 1
            total_observaciones += 1
            if eval == "✔️":
                acumulado_ok += 1

        # Crear evolución acumulada por semana

        for sem in semanas_ordenadas:
            semana_obs = sum(resumen_semanal[sem].values())
            semana_ok = resumen_semanal[sem]["✔️"]
            porcentaje_ok = round((semana_ok / semana_obs) * 100, 1) if semana_obs > 0 else 0
            positivos_acumulados.append((sem, porcentaje_ok))

        return resumen_semanal, totales, positivos_acumulados

    # Aplicar procesamiento

    resumen_semanal, totales_globales, evolucion_ok = procesar_datos_observaciones(
        st.session_state["seguimiento"]["observaciones"]
    )

    import pandas as pd
    import matplotlib.pyplot as plt
    import streamlit as st

    # Gráfico de evolución semanal

    st.markdown("### 📊 Evolución semanal de evaluaciones")

    if resumen_semanal:
        df_semanal = pd.DataFrame.from_dict(resumen_semanal, orient="index").sort_index()
        st.bar_chart(df_semanal)

        # Gráfico de porcentaje de observaciones positivas acumuladas

        st.markdown("### 📈 Porcentaje de observaciones positivas por semana")
        df_ok = pd.DataFrame(evolucion_ok, columns=["Semana", "Porcentaje ✔️"])
        df_ok = df_ok.set_index("Semana")
        st.line_chart(df_ok)
    else:
        st.info("Todavía no hay suficientes datos para mostrar gráficos.")

    def graficas_base64(resumen_semanal, evolucion_ok):
        graficas = []

        # --- 1. Barra ✔️ ⚠️ ❌ ---

        df_barras = pd.DataFrame.from_dict(resumen_semanal, orient="index").sort_index()
        fig1, ax1 = plt.subplots()
        df_barras.plot(kind='bar', stacked=True, ax=ax1)
        ax1.set_title("Evaluaciones por semana")
        ax1.set_xlabel("Semana")
        ax1.set_ylabel("Nº de observaciones")
        plt.tight_layout()

        buffer1 = BytesIO()
        plt.savefig(buffer1, format='png')
        plt.close(fig1)
        base64_img1 = base64.b64encode(buffer1.getvalue()).decode('utf-8')
        graficas.append(base64_img1)

        # --- 2. Línea ✔️ acumuladas ---

        sems = [p[0] for p in evolucion_ok]
        vals = [p[1] for p in evolucion_ok]
        fig2, ax2 = plt.subplots()
        ax2.plot(sems, vals, marker='o')
        ax2.set_title("Porcentaje ✔️ por semana")
        ax2.set_xlabel("Semana")
        ax2.set_ylabel("% ✔️")
        plt.ylim(0, 100)
        plt.grid(True)
        plt.tight_layout()

        buffer2 = BytesIO()
        plt.savefig(buffer2, format='png')
        plt.close(fig2)
        base64_img2 = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        graficas.append(base64_img2)

        return graficas

    def generar_html_informe(seguimiento, estado_alerta, resumen_semanal, totales_globales, graficas):
        from datetime import datetime

        html = f"""
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
        body {{ font-family: Arial; font-size: 14px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #999; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        </style>
        </head>
        <body>
        <h2>Informe Final de Seguimiento</h2>
        <p><strong>Nombre:</strong> {seguimiento['nombre_persona']}</p>
        <p><strong>Rama:</strong> {seguimiento['rama']}</p>
        <p><strong>Duración:</strong> {seguimiento['duracion_seguimiento']} semanas</p>
        <p><strong>Frecuencia de revisión:</strong> {seguimiento['frecuencia_revision'].capitalize()}</p>
        <p><strong>Fecha de generación:</strong> {datetime.today().strftime('%d/%m/%Y')}</p>
        <hr>

        <h3>Resumen Ejecutivo</h3>
        <p>{estado_alerta['mensaje_final']}</p>

        <h3>Totales globales</h3>
        <ul>
            <li>✔️ Positivas: {totales_globales.get('✔️', 0)}</li>
            <li>⚠️ Señales de cuidado: {totales_globales.get('⚠️', 0)}</li>
            <li>❌ Críticas: {totales_globales.get('❌', 0)}</li>
        </ul>
        """

        for i, graf in enumerate(graficas):
            html += f"<h4>Gráfico {i+1}</h4><img src='data:image/png;base64,{graf}' width='600'><br><br>"

        html += """
        <h3>Histórico de observaciones</h3>
        <table>
            <tr>
                <th>Semana</th>
                <th>Dimensión</th>
                <th>Indicador</th>
                <th>Evaluación</th>
                <th>Observación</th>
            </tr>
        """

        for obs in seguimiento["observaciones"]:
            html += f"""
            <tr>
                <td>{obs['semana']}</td>
                <td>{obs['dimension']}</td>
                <td>{obs['indicador']}</td>
                <td>{obs['evaluacion']}</td>
                <td>{obs['observacion']}</td>
            </tr>
            """

        html += """
        </table>
        <hr>
        <p><strong>Recomendaciones finales:</strong></p>
        <p>Este informe ha sido generado automáticamente por el sistema de inclusión laboral. Puede ser revisado por el técnico responsable para añadir comentarios cualitativos o validación externa.</p>
        </body>
        </html>
        """
        return html
    
    graficas = graficas_base64(resumen_semanal, evolucion_ok)
    informe_html = generar_html_informe(
        st.session_state["seguimiento"],
        estado_alerta,
        resumen_semanal,
        totales_globales,
        graficas
    )

    # HTML

    st.download_button(
        label="📥 Descargar informe HTML",
        data=informe_html.encode("utf-8"),
        file_name=f"Informe_Seguimiento_{st.session_state['seguimiento']['nombre_persona']}.html",
        mime="text/html"
    )

    # PDF 

    try:
        path_wkhtmltopdf = "/usr/local/bin/wkhtmltopdf"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        pdf_bytes = pdfkit.from_string(informe_html, False, configuration=config)

        st.download_button(
            label="📄 Descargar informe PDF",
            data=pdf_bytes,
            file_name=f"Informe_Seguimiento_{st.session_state['seguimiento']['nombre_persona']}.pdf",
            mime="application/pdf"
        )
    
    except Exception as e:
        st.warning("No se pudo generar el PDF. Asegúrate de tener wkhtmltopdf instalado correctamente.")

    # --- Paso 5: Evaluación para cierre automático del seguimiento ---
    
    def evaluar_condiciones_cierre(seguimiento):
        mensajes = []
        puede_cerrar = True

        obs = seguimiento["observaciones"]
        if len(obs) < 12:
            mensajes.append("📊 Se requieren al menos 12 observaciones para evaluar la consolidación del seguimiento.")
            puede_cerrar = False

        claves = ["Desempeño técnico", "Estabilidad emocional", "Interacción social y adaptación"]
        clave_obs = [o for o in obs if o["dimension"] in claves]

        if len(clave_obs) < 12:
            mensajes.append("🔍 Debe haber al menos 12 observaciones centradas en las dimensiones clave del modelo.")
            puede_cerrar = False

        positivas = sum(1 for o in clave_obs if o["evaluacion"] == "✔️ Bien")
        if positivas < 8:
            mensajes.append(f"✅ Solo hay {positivas} observaciones positivas ('✔️ Bien'). Se requieren al menos 8.")
            puede_cerrar = False

        recientes = list(reversed(clave_obs))[:6]
        alertas_recientes = sum(1 for o in recientes if o["evaluacion"] == "⚠️ Cuidado")
        if alertas_recientes > 1:
            mensajes.append("⚠️ Hay más de una alerta de tipo '⚠️ Cuidado' en las 6 últimas observaciones clave.")
            puede_cerrar = False

        if any(o["evaluacion"] == "❌ Crítico" for o in recientes):
            mensajes.append("❌ Se ha registrado una alerta crítica reciente. No puede cerrarse el seguimiento.")
            puede_cerrar = False

        if any("abandono" in o["observacion"].lower() or "desmotiv" in o["observacion"].lower() for o in recientes):
            mensajes.append("🚨 Se detectan señales de desmotivación o riesgo de abandono en alguna observación reciente.")
            puede_cerrar = False

        apoyos_extra = [
            o for o in obs[-6:]
            if "apoyo" in o["indicador"].lower() and "aumentado" in o["observacion"].lower()
        ]
        if apoyos_extra:
            mensajes.append("🛠️ Se han detectado solicitudes de apoyos no previstos recientemente.")
            puede_cerrar = False

        return puede_cerrar, mensajes

    # Evaluar si puede cerrarse el seguimiento

    cerrable, mensajes_cierre = evaluar_condiciones_cierre(st.session_state["seguimiento"])

    if cerrable:
        st.success("✅ Proceso de inclusión consolidado con éxito. Puedes cerrar el seguimiento formalmente.")
        if st.button("📁 Archivar seguimiento"):
            st.session_state["seguimiento_archivado"] = True
            st.success("Seguimiento archivado correctamente. El proceso se considera finalizado.")
        else:
            st.markdown("🔒 El seguimiento aún está activo. Pulsa el botón si deseas cerrarlo.")

        # Opción de seguimiento preventivo futuro
        
        st.markdown("### ⏳ ¿Deseas agendar una revisión preventiva?")
        revision = st.radio("Selecciona un plazo de revisión recomendada:", ["No agendar", "Revisión en 3 meses", "Revisión en 6 meses"])
        st.session_state["seguimiento"]["revisión_futura"] = revision
    else:
        st.info("🔁 El seguimiento aún presenta aspectos a mejorar. No se cumplen todos los criterios para un cierre automático.")
        st.markdown("#### Razones por las que no se puede cerrar el seguimiento:")
        for m in mensajes_cierre:
            st.warning(m)