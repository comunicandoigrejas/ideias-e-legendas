import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import time

# Configuração da página
st.set_page_config(page_title="Social Media AI", page_icon="📈", layout="wide")

# Inicialização do Cliente OpenAI e Gemini
try:
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]
except Exception as e:
    st.error("Erro: Verifique se as chaves API estão configuradas nos Secrets do Streamlit.")

# --- INTERFACE: DNA DA MARCA ---
st.title("🚀 Social Media Super Agent")

if "dna_marca" not in st.session_state:
    st.session_state.dna_marca = ""

with st.expander("🧬 Configurar DNA da Marca", expanded=True):
    dna_input = st.text_area("Descreva o nicho e tom de voz:", placeholder="Ex: Loja de suplementos, tom motivacional...")
    if dna_input:
        st.session_state.dna_marca = dna_input
    if st.session_state.dna_marca:
        st.caption(f"✨ DNA atual: {st.session_state.dna_marca[:60]}...")

st.divider()

# --- FUNÇÃO DO AGENTE OPENAI ---
def executar_agente(comando):
    thread = client_openai.beta.threads.create()
    client_openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"DNA: {st.session_state.dna_marca}. Tarefa: {comando}"
    )
    run = client_openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    
    while run.status != "completed":
        time.sleep(1)
        run = client_openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    msgs = client_openai.beta.threads.messages.list(thread_id=thread.id)
    return msgs.data[0].content[0].text.value

# --- ABAS ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Prompts Gemini"])

# ABA 1: LEGENDAS
with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        formato = st.selectbox("Tipo de Post:", ["Post Simples", "Carrossel", "Reels", "Vídeo Curto"])
        tema = st.text_area("Tema da postagem:")
        quero_prompt = st.checkbox("Gerar também um prompt de imagem?")
        
    if st.button("Gerar Conteúdo ✨"):
        if st.session_state.dna_marca:
            resultado = executar_agente(f"Crie uma legenda para {formato} sobre {tema}. Use emojis e CTA.")
            with col_b:
                st.subheader("Resultado:")
                st.write(resultado)
                if quero_prompt:
                    st.divider()
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt_img = model.generate_content(f"Crie um prompt visual para: {tema}. DNA: {st.session_state.dna_marca}")
                    st.subheader("🎨 Prompt de Imagem:")
                    st.code(prompt_img.text)
        else:
            st.warning("Preencha o DNA primeiro!")

# ABA 2: STORIES
with tab2:
    estilo_s = st.selectbox("Estilo:", ["Bastidores", "Vendas", "Dica Útil", "Interação"])
    tema_s = st.text_input("Sobre o que são os stories?")
    if st.button("Gerar Roteiro 🤳"):
        res = executar_agente(f"Crie um roteiro de 5 stories estilo {estilo_s} sobre {tema_s}.")
        st.write(res)

# ABA 3: PROMPTS (SOLO)
with tab3:
    ideia = st.text_input("Descreva a ideia da imagem:")
    if st.button("Gerar Prompt Profissional 🎨"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Crie um prompt rico em detalhes para: {ideia}. Estilo: Redes sociais de alto padrão.")
        st.code(res.text)
