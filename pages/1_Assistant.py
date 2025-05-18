from openai import OpenAI
import streamlit as st

with open("data/context.txt", "r") as f:
    context = f.read()

st.title("Assistente de Compra de Carros")
client = OpenAI(api_key=st.secrets["api_key"], base_url="https://api.deepseek.com")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": context}  # context inicial
    ]
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Qual carro você quer comparar ou conhecer?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
