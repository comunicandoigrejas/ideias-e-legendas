import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import time

# 1. Configurações Iniciais e Memória
st.set_page_config(page_title="Social Media Expert", page_icon="📸", layout="wide")

# Inicializa o DNA na memória se ainda não existir
if "dna_registrado" not in st.session_state:
    st.session_state.dna_registrado = ""

# 2. Configuração das APIs (Lendo dos Secrets)
try:
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]
except:
    st.error("Erro: Verifique as chaves nos Secrets do Streamlit.")

# --- TÍTULO E DNA ---
st.title("🚀 Social Media AI Assistant")

# Campo de DNA com persistência automática
with st.expander("🧬 Configuração de DNA (Gravação Automática)", expanded=True):
    dna_input = st.text_area(
        "Insira o DNA da Marca/Negócio aqui:", 
        value=st.session_state.dna_registrado,
        placeholder="Ex: Consultoria jurídica, tom sério, foco em empresas...",
        height=100
    )
    # Atualiza a memória sempre que o texto mudar
    if dna_input != st.session_state.dna_registrado:
        st.session_state.dna_registrado = dna_input
        st.toast("DNA atualizado com sucesso!", icon="✅")

if st.session_state.dna_registrado:
    st.caption(f"📍 **DNA Ativo:** {st.session_state.dna_registrado[:60]}...")

st.divider()

# --- FUNÇÃO DE GERAÇÃO (OPENAI ASSISTANT) ---
def gerar_com_agente(comando):
    thread = client_openai.beta.threads.create()
    client_openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Contexto DNA: {st.session_state.dna_registrado}. Tarefa: {comando}"
    )
    run = client_openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    
    with st.spinner("O Super Agente está escrevendo..."):
        while run.status != "completed":
            time.sleep(1)
            run = client_openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    msgs = client_openai.beta.threads.messages.list(thread_id=thread.id)
    return msgs.data[0].content[0].text.value

# --- ESTRUTURA DE ABAS ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Prompts Gemini"])

# 1. ABA DE LEGENDAS
with tab1:
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        formato = st.selectbox("Formato:", ["Post Simples", "Carrossel", "Reels", "Anúncio"])
        tema = st.text_area("Tema do post:", placeholder="Sobre o que vamos postar?")
        add_img = st.checkbox("Gerar prompt de imagem?")
        btn_legenda = st.button("Gerar Conteúdo ✨")

    if btn_legenda:
        if st.session_state.dna_registrado:
            resposta = gerar_com_agente(f"Crie uma legenda para {formato} sobre {tema}. Com emojis e CTA.")
            with col_r:
                st.subheader("Resultado:")
                # O componente code permite copiar com um clique no ícone lateral
                st.code(resposta, language=None)
                st.info("💡 Clique no ícone no canto superior direito do texto acima para copiar.")
                
                if add_img:
                    st.divider()
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt_img = model.generate_content(f"Prompt visual para {tema}. Estilo: {st.session_state.dna_registrado}")
                    st.subheader("🎨 Prompt de Imagem:")
                    st.code(prompt_img.text, language=None)
        else:
            st.warning("Preencha o DNA da marca primeiro!")

# 2. ABA DE STORIES
with tab2:
    tipo_s = st.selectbox("Estilo do Story:", ["Educativo", "Venda", "Bastidores", "Enquete"])
    tema_s = st.text_input("Contexto:")
    if st.button("Criar Roteiro 🤳"):
        roteiro = gerar_com_agente(f"Roteiro de 5 stories estilo {tipo_s} sobre {tema_s}.")
        st.subheader("Roteiro:")
        st.code(roteiro, language=None)

# 3. ABA DE PROMPTS
with tab3:
    ideia = st.text_input("Ideia para imagem:")
    if st.button("Gerar Prompt 🎨"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Prompt rico para IA: {ideia}")
        st.code(res.text, language=None)
