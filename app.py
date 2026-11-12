from google import genai
import streamlit as st

st.set_page_config(page_title="Mi Asistente Géminis", page_icon="🐺")

# Inicializar el cliente aquí arriba para que esté disponible en todo el script
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("Mi Chat IA Sencillo")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "👦" if message["role"] == "user" else "🐺"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👦"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🐺"):
        with st.spinner("Pensando..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                st.markdown(response.text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )
            except Exception as e:
                st.error(f"Error: {e}")
