import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import time

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Social Media Expert AI", page_icon="📸", layout="wide")

# 2. INICIALIZAÇÃO DE CLIENTES E SEGREDOS
# Certifique-se de cadastrar OPENAI_API_KEY, GEMINI_API_KEY, ASSISTANT_ID e DNA_FIXO nos Secrets
try:
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]
except Exception as e:
    st.error("Erro de Configuração: Verifique as chaves nos Secrets do Streamlit.")

# 3. LÓGICA DE PERSISTÊNCIA DO DNA
# Ele busca o DNA gravado nos Secrets. Se você alterar na tela, ele muda apenas para a sessão atual.
if "dna_registrado" not in st.session_state:
    st.session_state.dna_registrado = st.secrets.get("DNA_FIXO", "DNA não configurado nos Secrets.")

# --- INTERFACE PRINCIPAL ---
st.title("🚀 Social Media Content Master")

with st.expander("🧬 DNA da Empresa (Gravado Permanente)", expanded=False):
    dna_input = st.text_area(
        "Edite o DNA abaixo se precisar de uma alteração temporária:", 
        value=st.session_state.dna_registrado,
        height=100
    )
    if dna_input != st.session_state.dna_registrado:
        st.session_state.dna_registrado = dna_input
        st.toast("DNA atualizado para esta geração!", icon="🔄")

st.markdown("---")

# --- FUNÇÃO DO SUPER AGENTE (OPENAI) ---
def executar_agente(comando):
    thread = client_openai.beta.threads.create()
    client_openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Contexto DNA: {st.session_state.dna_registrado}. Tarefa: {comando}"
    )
    run = client_openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    
    with st.spinner("O Super Agente está processando seu conteúdo..."):
        while run.status != "completed":
            time.sleep(0.5)
            run = client_openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    msgs = client_openai.beta.threads.messages.list(thread_id=thread.id)
    return msgs.data[0].content[0].text.value

# --- ESTRUTURA DE ABAS ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Prompts Gemini"])

# ABA 1: LEGENDAS
with tab1:
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        formato = st.selectbox("Tipo de Postagem:", ["Post Simples", "Carrossel", "Reels", "Vídeo Curto", "Anúncio (Ads)"])
        tema = st.text_area("Sobre o que é a postagem?", placeholder="Ex: Benefícios do produto X para a pele...")
        precisa_prompt = st.checkbox("Gerar prompt de imagem para este post?")
        btn_legenda = st.button("Gerar Legenda ✨")

    if btn_legenda:
        comando = f"Crie uma legenda detalhada para {formato} sobre {tema}. Use emojis, hashtags e uma CTA forte."
        resultado = executar_agente(comando)
        
        with col_r:
            st.subheader("📝 Conteúdo Gerado")
            st.code(resultado, language=None) # Botão de copiar automático
            st.caption("☝️ Clique no ícone no canto superior direito do bloco acima para copiar.")
            
            if precisa_prompt:
                st.divider()
                st.subheader("🎨 Prompt para Imagem (Gemini)")
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt_gemini = model.generate_content(f"Crie um prompt visual rico para: {tema}. Estilo: {st.session_state.dna_registrado}")
                st.code(prompt_gemini.text, language=None)

# ABA 2: STORIES
with tab2:
    tipo_s = st.selectbox("Objetivo dos Stories:", ["Bastidores", "Venda/Oferta", "Educativo", "Engajamento/Enquetes"])
    tema_s = st.text_input("Tema da sequência de Stories:")
    
    if st.button("Criar Roteiro de Stories 🤳"):
        comando_s = f"Crie um roteiro de 5 stories estilo {tipo_s} sobre {tema_s}. Inclua sugestão de texto para tela e emojis."
        roteiro = executar_agente(comando_s)
        st.subheader("🎬 Roteiro Sugerido")
        st.code(roteiro, language=None)

# ABA 3: PROMPTS GEMINI (CRIAÇÃO DE IMAGEM)
with tab3:
    st.info("Crie prompts detalhados para o Gemini ou Midjourney.")
    ideia_img = st.text_input("Descreva a ideia da imagem que deseja criar:")
    
    if st.button("Gerar Prompt de Imagem 🎨"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res_img = model.generate_content(f"Crie um prompt profissional de imagem para IA: {ideia_img}. DNA: {st.session_state.dna_registrado}")
        st.subheader("🖼️ Prompt Gerado")
        st.code(res_img.text, language=None)
