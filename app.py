import streamlit as st
from openai import OpenAI
import time

# --- CONFIGURAÇÃO ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"] # Salve o ID do assistente nos secrets também

def conversar_com_agente(tema, formato, dna):
    # 1. Cria uma conversa (Thread)
    thread = client.beta.threads.create()
    
    # 2. Envia a mensagem com o DNA e o Tema
    mensagem = f"DNA da Marca: {dna}. Formato: {formato}. Tema: {tema}."
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=mensagem
    )
    
    # 3. Executa o Agente (Run)
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )
    
    # 4. Aguarda a resposta
    while run.status != "completed":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    # 5. Pega a resposta final
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

# --- INTERFACE STREAMLIT (Resumida) ---
st.title("🚀 Super Agente de Social Media")

# DNA visível conforme solicitado
dna = st.text_area("🧬 DNA da Marca:", value=st.session_state.get('dna_temp', ""))
if dna: st.session_state['dna_temp'] = dna

tab1, tab2 = st.tabs(["✍️ Legendas", "📱 Stories"])

with tab1:
    tipo = st.selectbox("Tipo:", ["Post Simples", "Carrossel", "Reels"])
    tema = st.text_input("Tema do post:")
    if st.button("Gerar com Super Agente"):
        with st.spinner("O Agente está pensando..."):
            resposta = conversar_com_agente(tema, tipo, dna)
            st.markdown(resultado)
