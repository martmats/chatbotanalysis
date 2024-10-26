import streamlit as st
import pandas as pd
from openai import OpenAI

# Mostrar el título y la descripción de la aplicación.
st.title("💬 Chatbot con Análisis de CSV")
st.write(
    "Este es un chatbot simple que usa el modelo GPT-3.5 de OpenAI para generar respuestas. "
    "Para usar esta app, necesitas proporcionar una clave de API de OpenAI, que puedes obtener [aquí](https://platform.openai.com/account/api-keys). "
)

# Pedir al usuario su clave de API de OpenAI.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Por favor, añade tu clave de API de OpenAI para continuar.", icon="🗝️")
else:
    # Crear un cliente de OpenAI.
    client = OpenAI(api_key=openai_api_key)

    # Cargar archivo CSV
    uploaded_file = st.file_uploader("Sube un archivo CSV para análisis", type="csv")
    if uploaded_file:
        # Leer y mostrar el CSV
        df = pd.read_csv(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(df)

        # Convertir el contenido del CSV a un formato de texto para el modelo
        csv_text = df.to_string()

    # Crear una variable de estado de sesión para almacenar los mensajes.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar los mensajes de chat existentes.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Crear un campo de entrada de chat para el usuario.
    if prompt := st.chat_input("¿Cuál es tu pregunta?"):

        # Almacenar y mostrar la pregunta del usuario.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar una respuesta usando la API de OpenAI, incluyendo los datos del CSV si están cargados.
        context = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        # Agregar contexto del CSV si existe
        if uploaded_file:
            context.append({"role": "system", "content": f"Aquí están los datos del CSV para referencia: {csv_text}"})

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context,
            stream=True,
        )

        # Mostrar la respuesta del modelo
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

