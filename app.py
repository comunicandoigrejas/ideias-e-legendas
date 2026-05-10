import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import time
import requests
import json

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Social Media Expert AI", page_icon="📸", layout="wide")

# 2. INICIALIZAÇÃO E VALIDAÇÃO DOS SEGREDOS
try:
    # O código DEVE buscar pelo nome da chave, NÃO pelo link direto
    if "URL_PLANILHA_SCRIPT" in st.secrets:
        SCRIPT_URL = st.secrets["https://script.google.com/macros/s/AKfycbxBA4CduznYTrW2hK-ULLhMKvutqjg6DSMTgp0YbHBqKmRPz1l5i9Mc1ILxo8tGFDVfVg/exec"]
    else:
        st.error("⚠️ Erro: A chave 'URL_PLANILHA_SCRIPT' não foi encontrada no painel Secrets.")
        st.stop()

    # Inicialização das IAs
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]
    
except Exception as e:
    st.error(f"Erro de Configuração: {e}")
    st.stop()
    
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]
except Exception as e:
    st.error(f"⚠️ Erro de Configuração: {e}")
    st.stop()

# --- CONTINUAÇÃO DO CÓDIGO (LOGIN) ---
if "logado" not in st.session_state:
    st.session_state.logado = False

# ... (restante do seu código de login e abas)

# 2. FUNÇÃO DE AUTENTICAÇÃO (Apps Script)
def autenticar_usuario(username, password):
    payload = {"username": username, "password": password}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 3. TELA DE LOGIN
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🙏 Login - Social Media Master")
    with st.container(border=True):
        u_input = st.text_input("Usuário")
        p_input = st.text_input("Senha", type="password")
        if st.button("Entrar no Sistema", use_container_width=True):
            with st.spinner("Validando credenciais..."):
                res = autenticar_usuario(u_input, p_input)
                if res.get("status") == "success":
                    st.session_state.logado = True
                    st.session_state.user_data = res
                    # Prioriza a API Key do usuário se estiver preenchida (Coluna F)
                    st.session_state.api_key_atual = res["api_key_user"] if res["api_key_user"] else st.secrets["OPENAI_API_KEY"]
                    st.rerun()
                else:
                    st.error("Credenciais inválidas, varão! Verifique os dados.")
    st.stop()

# --- SE CHEGOU AQUI, O USUÁRIO ESTÁ LOGADO ---
user = st.session_state.user_data

# 4. INICIALIZAÇÃO DE CLIENTES COM DADOS DO USUÁRIO
try:
    client_openai = OpenAI(api_key=st.session_state.api_key_atual)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]
except Exception as e:
    st.error("Erro de conexão com as APIs. Verifique as chaves.")

# Sidebar com informações do perfil
st.sidebar.title(f"Bem-vindo, {user['nome_exibicao']}")
st.sidebar.info(f"Nicho: {user['nicho']}")
if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()

# --- INTERFACE PRINCIPAL ---
st.title("🚀 Social Media Content Master")

# O DNA é carregado da planilha, mas permite edição temporária
with st.expander("🧬 DNA Personalizado (Carregado do Perfil)", expanded=False):
    dna_texto = st.text_area(
        "Contexto atual para as IAs:", 
        value=user['dna'],
        height=150
    )

# --- FUNÇÃO DO AGENTE ---
def executar_agente(comando):
    thread = client_openai.beta.threads.create()
    client_openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Contexto DNA: {dna_texto}. Tarefa: {comando}"
    )
    run = client_openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    
    with st.spinner("O Super Agente está processando..."):
        while run.status not in ["completed", "failed"]:
            time.sleep(0.5)
            run = client_openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    if run.status == "completed":
        msgs = client_openai.beta.threads.messages.list(thread_id=thread.id)
        return msgs.data[0].content[0].text.value
    return "Ocorreu um erro no processamento."

# --- ABAS ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Prompts Gemini"])

with tab1:
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        formato = st.selectbox("Formato:", ["Post Simples", "Carrossel", "Reels", "Vídeo Curto"])
        tema = st.text_area("Tema da postagem:")
        btn_legenda = st.button("Gerar Conteúdo ✨", use_container_width=True)

    if btn_legenda:
        resultado = executar_agente(f"Crie uma legenda para {formato} sobre {tema}. Se for para igreja, use Bíblia ARA.")
        with col_r:
            st.subheader("📝 Conteúdo Gerado")
            st.code(resultado, language=None)

with tab3:
    st.info("Prompts otimizados para Instagram (Ratio 1:1)")
    ideia_img = st.text_input("O que deseja visualizar?")
    if st.button("Gerar Prompt Visual 🎨"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Instrução reforçando as cores e o ratio 1:1 salvos anteriormente
        instrucao = f"Crie um prompt para IA (1:1 ratio). Cores: azul, roxo, verde, laranja e amarelo. Ideia: {ideia_img}. Contexto: {dna_texto}"
        res_img = model.generate_content(instrucao)
        st.code(res_img.text, language=None)
