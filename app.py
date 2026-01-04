import json
import requests
import streamlit as st

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3.2:3b"

st.set_page_config(page_title="Asistente local (Streamlit + Ollama)", page_icon="🤖")
st.title("Asistente local — Streaming")

# Sidebar
st.sidebar.header("Config")
model = st.sidebar.text_input("Modelo", value=DEFAULT_MODEL)
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

if st.sidebar.button("🧹 Limpiar chat"):
    st.session_state.pop("messages", None)
    st.rerun()

# Init chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres un asistente útil y directo. Responde en español."}
    ]

# Render chat history (skip system message)
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input
user_text = st.chat_input("Escribe tu pregunta...")
if user_text:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Stream assistant message
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        payload = {
            "model": model,
            "messages": st.session_state.messages,
            "stream": True,
            "options": {"temperature": temperature},
        }

        try:
            with requests.post(OLLAMA_CHAT_URL, json=payload, stream=True, timeout=300) as r:
                r.raise_for_status()

                for line in r.iter_lines(decode_unicode=True):
                    if not line:
                        continue

                    chunk = json.loads(line)

                    # Ollama streams chunks like:
                    # {"message":{"role":"assistant","content":"..."},"done":false}
                    if "message" in chunk and "content" in chunk["message"]:
                        delta = chunk["message"]["content"]
                        full_text += delta
                        placeholder.markdown(full_text + "▌")

                    if chunk.get("done"):
                        break

            placeholder.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})

        except requests.exceptions.ConnectionError:
            st.error("No puedo conectar con Ollama. Asegúrate de tener `ollama serve` corriendo.")
        except requests.exceptions.HTTPError as e:
            st.error(f"Error HTTP: {e}\n\nRespuesta: {getattr(e.response, 'text', '')}")
        except Exception as e:
            st.error(f"Error: {e}")
