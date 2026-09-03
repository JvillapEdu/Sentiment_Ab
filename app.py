import json
from PIL import Image
import pandas as pd
import streamlit as st
from googletrans import Translator
from streamlit_lottie import st_lottie
from textblob import TextBlob

# Función para cargar archivos JSON Lottie de forma segura
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Carga de animaciones Lottie (asegúrate de tener estos archivos .json en tu repositorio)
lottie_happy = load_lottiefile("happy.json")
lottie_sad = load_lottiefile("sad.json")
lottie_neutral = load_lottiefile("neutral.json")

st.title("Análisis de Sentimiento")

# Carga de la imagen principal
try:
    image = Image.open("emoticones.jpg")
    st.image(image)
except FileNotFoundError:
    st.warning("No se encontró la imagen 'emoticones.jpg' en el directorio.")

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

translator = Translator()

with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.write(
        """
        Polaridad: Indica si el sentimiento expresado en el texto es positivo, negativo o neutral. 
        Su valor oscila entre -1 (muy negativo) y 1 (muy positivo), con 0 representando un sentimiento neutral.
        
        Subjetividad: Mide cuánto del contenido es subjetivo (opiniones, emociones, creencias) frente a objetivo
        (hechos). Va de 0 a 1, donde 0 es completamente objetivo y 1 es completamente subjetivo.
        """
    )

with st.expander("Analizar texto"):
    text = st.text_input("Escribe por favor: ")
    if text:
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)

        st.write("Polarity: ", round(blob.sentiment.polarity, 2))
        st.write("Subjectivity: ", round(blob.sentiment.subjectivity, 2))

        x = round(blob.sentiment.polarity, 2)

        if x > 0:
            st.write("Es un sentimiento Positivo 😊")
            if lottie_happy:
                st_lottie(lottie_happy, width=350, key="happy")
        elif x < 0:
            st.write("Es un sentimiento Negativo 😔")
            if lottie_sad:
                st_lottie(lottie_sad, width=350, key="sad")
        else:
            st.write("Es un sentimiento Neutral 😐")
            if lottie_neutral:
                st_lottie(lottie_neutral, width=350, key="neutral")