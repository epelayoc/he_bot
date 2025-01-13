import streamlit as st
import google.generativeai as genai
import httpx
import base64

# Configure the API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro-latest")

idioma = 'español'

titulo = "HE - Guía rápida del participante"
pdf_url = "https://www.horizonteeuropa.es/sites/default/files/noticias/GUIA%20RAPIDA.pdf"
resumen = """
Esta guía ha sido elaborada por CDTI, E.P.E, en colaboración con la Fundación Española
para la Ciencia y la Tecnología (FECYT) y el Ministerio de Ciencia e Innovación (MCIN).
El objeto de esta guía rápida es proporcionar información general de Horizonte Europa, el
Programa Marco de Investigación e Innovación de la Unión Europea para el periodo 2021-
2027, así como sobre el proceso de participación en el Programa.
Este documento tiene carácter informativo y en ningún caso sustituye o reemplaza la documen
tación oficial publicada por la Comisión Europea.
"""



@st.cache_resource
def load_document(pdf_url):
  if pdf_url:
    try:
      doc_data = base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")
      return doc_data
    except Exception as e:
      st.error(f"Error loading document: {e}")
      return None
  else:
    return None

def generate_response(document_data, user_question):
    try:
        user_question = user_question + ".Responde en " + idioma
        response = model.generate_content([{'mime_type':'application/pdf', 'data': document_data}, user_question])
        return response.text
    except Exception as e:
      st.error(f"Error generating response: {e}")
      return "Sorry, I couldn't process your request."

def generate_summary(document_data):
    try:
        prompt = "Proporciona un resumen de 4/5 lineas de este documento. Responde en español"
        response = model.generate_content([{'mime_type':'application/pdf', 'data': document_data}, prompt])
        return response.text
    except Exception as e:
      st.error(f"Error generating summary: {e}")
      return "Sorry, I couldn't generate a summary."


#st.image('https://www.cdti.es/sites/default/files/logo_cdti_2024_con_banderas_soportes_digitales.jpg')
st.image(https://www.horizonteeuropa.es/sites/default/files/2023-01/horizon-europe_0.jpg)
st.title("Asistente conversacional HE")
instrucciones = """
Puedes usar el chat para 
hacer preguntas específicas sobre la guía y el asistente te dará respuestas basadas en el documento.
"""
st.info(instrucciones, icon="ℹ️")
idioma = st.radio(
    "Selecciona tu idioma",
    ["Español", "Inglés", "Catalan"],
)



if "messages" not in st.session_state:
    st.session_state.messages = []

# Only proceed if an option has been selected
if True:
    #titulo, pdf_url, resumen = convocatorias[option]
    document_data = load_document(pdf_url)

    if document_data:
            st.subheader(titulo)
            st.markdown(f'<a href="{pdf_url}">Enlace al documento</a>', unsafe_allow_html=True)
            st.write(resumen)
            st.markdown('Plantea tus cuestiones a continuacion')

            for message in st.session_state.messages:
                  with st.chat_message(message["role"]):
                      st.write(message["content"])

            if prompt := st.chat_input("Pregunta al documento"):
              st.session_state.messages.append({"role": "user", "content": prompt})
              with st.chat_message("user"):
                    st.write(prompt)

              with st.chat_message("assistant"):
                    with st.spinner("Pensando..."):
                        response = generate_response(document_data, prompt)
                        st.write(response)
              st.session_state.messages.append({"role": "assistant", "content": response})

    else:
      st.warning("Please enter a PDF URL")
