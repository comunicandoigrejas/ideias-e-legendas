import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import time
import requests
import json

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Social Media Expert AI", page_icon="📸", layout="wide")

# 2. INICIALIZAÇÃO DE SEGREDOS
try:
    SCRIPT_URL = st.secrets["URL_PLANILHA_SCRIPT"]
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]
except Exception as e:
    st.error(f"Erro de Configuração: {e}")
    st.stop()

# 3. FUNÇÃO DE AUTENTICAÇÃO
def autenticar_usuario(username, password):
    payload = {"username": username, "password": password}
    try:
        response = requests.post(SCRIPT_URL, json=payload, allow_redirects=True, timeout=10)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 4. LÓGICA DE LOGIN
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🙏 Login - Social Media Master")
    with st.container(border=True):
        u_input = st.text_input("Usuário")
        p_input = st.text_input("Senha", type="password")
        if st.button("Entrar no Sistema", use_container_width=True):
            res = autenticar_usuario(u_input, p_input)
            if res.get("status") == "success":
                st.session_state.logado = True
                st.session_state.user_data = res
                st.rerun()
            else:
                st.error("Credenciais inválidas, varão! Verifique a planilha.")
    st.stop()

# --- INTERFACE PÓS-LOGIN ---
user = st.session_state.user_data

# Cabeçalho com Nome do Cliente e Botão de Sair
col_nome, col_sair = st.columns([0.8, 0.2])
with col_nome:
    st.markdown(f"### 👤 {user['nome_exibicao']}")
with col_sair:
    if st.button("Sair do Aplicativo 🚪", use_container_width=True):
        st.session_state.logado = False
        st.session_state.user_data = None
        st.rerun()

st.title("🚀 Social Media Content Master")

# DNA Personalizado
with st.expander("🧬 DNA Personalizado", expanded=False):
    dna_atual = st.text_area("Contexto da IA:", value=user['dna'], height=150)

# FUNÇÃO DO AGENTE (OPENAI)
def executar_agente(comando):
    thread = client_openai.beta.threads.create()
    client_openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Contexto DNA: {dna_atual}. Regra: Se for igreja, use Bíblia ARA. Tarefa: {comando}"
    )
    run = client_openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    with st.spinner("Processando..."):
        while run.status != "completed":
            time.sleep(0.5)
            run = client_openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    msgs = client_openai.beta.threads.messages.list(thread_id=thread.id)
    return msgs.data[0].content[0].text.value

# ABAS DE CONTEÚDO
tab1, tab2 = st.tabs(["✍️ Legendas", "🎨 Visual"])

with tab1:
    tema = st.text_input("Tema do Post:")
    if st.button("Gerar Legenda ✨"):
        legenda_gerada = executar_agente(f"Crie uma legenda para Instagram sobre {tema}")
        st.text_area("Legenda Gerada:", value=legenda_gerada, height=300)
        # O Streamlit já tem um ícone de "copiar" nativo no canto superior direito do text_area
        st.success("Legenda gerada com sucesso!")

with tab2:
    ideia = st.text_input("Ideia para Imagem:")
    if st.button("Gerar Prompt 🎨"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_input = f"Crie um prompt 1:1. Cores: azul, roxo, verde, laranja e amarelo. Tema: {ideia}"
        prompt_resultado = model.generate_content(prompt_input)
        st.text_area("Prompt para IA:", value=prompt_resultado.text, height=150)
        st.info("Prompt gerado! Use as cores da marca: azul, roxo, verde, laranja e amarelo.")

# CSS para remover a barra lateral
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)
