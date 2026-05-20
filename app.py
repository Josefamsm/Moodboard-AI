import streamlit as st
import requests
import colorgram
import random

from PIL import Image
from io import BytesIO

# =====================================================
# API KEY
# =====================================================

UNSPLASH_ACCESS_KEY = "4Xup6SFwh0QWOi9d8ChrLMQ9tLMGItpufkRxepDK4EQ"
# =====================================================
# CONFIG PAGE
# =====================================================

st.set_page_config(
    page_title="Moodboard AI",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: white;
}

h1, h2, h3, p, label {
    color: black;
}

.stButton > button {
    border-radius: 10px;
    background-color: #f3f3f3;
    color: black;
    border: 1px solid #dcdcdc;
    padding: 10px 18px;
}

.stButton > button:hover {
    background-color: #e9e9e9;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("Moodboard AI ✨")
st.write("Generador inteligente de moodboards")

# =====================================================
# PROMPT
# =====================================================

prompt = st.text_input(
    "Describe tu vibe",
    placeholder="Ej: cinematic rainy tokyo workspace"
)

# =====================================================
# SEARCH IMAGES (FIXED)
# =====================================================

def buscar_imagenes(query, cantidad=4):

    try:

        st.write("🔎 QUERY:", query)

        url = "https://api.unsplash.com/search/photos"

        headers = {
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }

        response = requests.get(
            url,
            headers=headers,
            params={
                "query": query,
                "per_page": cantidad
            }
        )

        data = response.json()

        st.write("STATUS:", response.status_code)
        st.write("RAW RESPONSE:", data)

        imagenes = []

        for item in data.get("results", []):

            url_img = item.get("urls", {}).get("regular")

            if url_img:
                imagenes.append(url_img)

        return imagenes

    except Exception as e:

        st.error(f"Error buscando imágenes: {e}")
        return []

# =====================================================
# EXTRAER COLORES
# =====================================================

def extraer_colores(url_imagen):

    try:

        response = requests.get(url_imagen)

        img = Image.open(BytesIO(response.content)).convert("RGB")

        colores = colorgram.extract(img, 5)

        resultado = []

        for color in colores:

            rgb = color.rgb

            hex_color = '#%02x%02x%02x' % (rgb.r, rgb.g, rgb.b)

            resultado.append(hex_color)

        return resultado

    except Exception as e:

        st.error(f"Error extrayendo colores: {e}")
        return []

# =====================================================
# TEXTOS
# =====================================================

def generar_textos(prompt):

    adjetivos = ["Cinematic","Nordic","Cozy","Editorial","Minimal","Dreamy","Moody","Luxury","Creative","Modern"]
    sustantivos = ["Escape","Studio","Retreat","Workspace","Atmosphere","Vision","Mood","Aesthetic"]

    keywords_base = [
        "soft lighting","neutral tones","editorial","cinematic",
        "warm shadows","minimal","modern","cozy","textured",
        "atmospheric","luxury","visual storytelling"
    ]

    fuentes = ["Inter","Poppins","Playfair Display","Montserrat","Cormorant","Space Grotesk","Lora","DM Sans"]

    titulo = random.choice(adjetivos) + " " + random.choice(sustantivos)

    descripcion = f"A visual atmosphere inspired by {prompt}, combining aesthetic composition and emotional storytelling."

    keywords = random.sample(keywords_base, 5)
    fonts = random.sample(fuentes, 2)

    return f"""
# {titulo}

### Description
{descripcion}

### Keywords
{" • ".join(keywords)}

### Typography
{fonts[0]} + {fonts[1]}
"""

# =====================================================
# BUTTON
# =====================================================

if st.button("Generar Moodboard"):

    if prompt:

        with st.spinner("Creando moodboard..."):

            textos = generar_textos(prompt)
            st.markdown(textos)

            imagenes = buscar_imagenes(prompt)

            st.write(f"🖼️ Imágenes encontradas: {len(imagenes)}")

            if len(imagenes) == 0:

                st.warning("No se encontraron imágenes.")

            else:

                st.subheader("Moodboard")

                cols = st.columns(2)

                for i, img_url in enumerate(imagenes):

                    with cols[i % 2]:

                        st.image(img_url, use_container_width=True)

                        colores = extraer_colores(img_url)

                        if colores:

                            st.write("🎨 Paleta")

                            palette_cols = st.columns(len(colores))

                            for idx, color in enumerate(colores):

                                palette_cols[idx].markdown(
                                    f"""
                                    <div style="
                                        width:60px;
                                        height:60px;
                                        background-color:{color};
                                        border-radius:12px;
                                        border:1px solid #ddd;
                                    "></div>
                                    <p style="font-size:11px;text-align:center;">
                                        {color}
                                    </p>
                                    """,
                                    unsafe_allow_html=True
                                )

    else:

        st.warning("Escribe una descripción primero.")