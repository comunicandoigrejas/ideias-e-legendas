import streamlit as st
import requests
from openai import OpenAI

# Configuração inicial da página (Força a tela limpa e sem barra lateral)
st.set_page_config(
    page_title="Social Media Content Master", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Estilização CSS para garantir que a barra lateral suma completamente em qualquer situação
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="collapsedSidebarNoContent"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# 1. VERIFICAÇÃO DAS CHAVES NOS SECRETS DO STREAMLIT
if "URL_PLANILHA_SCRIPT" in st.secrets:
    SCRIPT_URL = st.secrets["URL_PLANILHA_SCRIPT"]
else:
    st.error("⚠️ Erro: Chave 'URL_PLANILHA_SCRIPT' não encontrada nos Secrets do Streamlit.")
    st.stop()

if "OPENAI_API_KEY" in st.secrets:
    # Inicializa o cliente da OpenAI pegando a chave fixa e segura dos Secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ Erro: Chave 'OPENAI_API_KEY' não encontrada nos Secrets do Streamlit.")
    st.stop()

# Inicializar as variáveis de sessão (gavetas de memória)
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None
if "legenda_gerada" not in st.session_state:
    st.session_state["legenda_gerada"] = ""
if "hashtags_geradas" not in st.session_state:
    st.session_state["hashtags_geradas"] = ""

# --- CONTROLE DE FLUXO DE TELAS ---

if st.session_state["usuario_logado"] is not None:
    # ==========================================
    # 🚀 TELA PRINCIPAL (APÓS LOGIN COM SUCESSO)
    # ==========================================
    dados = st.session_state["usuario_logado"]
    
    # Exibe o Nome do Cliente ACIMA do título do sistema
    st.write(f"✨ Cliente Ativo: **{dados.get('nome_exibicao', 'Varão')}**")
    st.title("📸 Social Media Content Master")
    
    # Botão para Sair do Aplicativo
    if st.button("🚪 Sair do Aplicativo"):
        st.session_state["usuario_logado"] = None
        st.session_state["legenda_gerada"] = ""
        st.session_state["hashtags_geradas"] = ""
        st.rerun()
        
    st.divider()
    
    # CRIAÇÃO DAS JANELAS SEPARADAS (ABAS ATUALIZADAS)
    janela_legenda, janela_hashtags = st.tabs(["📝 Criar Legenda", "#️⃣ Gerar Hashtags"])
    
    # ------------------------------------------
    # JANELA 1: CRIAÇÃO DE LEGENDA
    # ------------------------------------------
    with janela_legenda:
        st.write(f"### Gerador de Legendas Profissionais")
        st.caption(f"Nicho configurado para este perfil: **{dados.get('nicho', 'Geral')}**")
        
        tema_legenda = st.text_area(
            "Sobre qual assunto ou tema você deseja criar a sua legenda hoje, irmão?", 
            placeholder="Ex: Aviso sobre o culto de jovens deste sábado ou promoção de doces gourmet...",
            key="input_tema_legenda"
        )
        
        if st.button("Gerar Legenda Abençoada ✨", key="btn_gerar_legenda"):
            if tema_legenda.strip():
                with st.spinner("A OpenAI está redigindo a sua legenda personalizada..."):
                    try:
                        dna_do_chat = dados.get("dna", "Escreva de forma engajadora")
                        
                        resposta = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {
                                    "role": "system", 
                                    "content": f"Você é um redator profissional. Use estritamente o seguinte estilo/DNA de escrita: {dna_do_chat}. Foque no nicho: {dados.get('nicho')}."
                                },
                                {
                                    "role": "user", 
                                    "content": f"Escreva uma legenda completa para post de Instagram sobre: {tema_legenda}"
                                }
                            ]
                        )
                        st.session_state["legenda_gerada"] = resposta.choices[0].message.content
                    except Exception as e:
                        st.error(f"Erro ao gerar a legenda na OpenAI: {e}")
            else:
                st.warning("Por favor, digite o assunto da legenda antes de gerar.")
                
        if st.session_state["legenda_gerada"]:
            st.success("Legenda pronta! Para copiar, basta clicar no ícone de duas folhas no canto superior direito do bloco abaixo:")
            st.code(st.session_state["legenda_gerada"], language="text")
            
    # ------------------------------------------
    # JANELA 2: CRIAÇÃO DE HASHTAGS
    # ------------------------------------------
    with janela_hashtags:
        st.write("### Gerador de Hashtags Estratégicas")
        st.caption(f"Nicho ativo: **{dados.get('nicho', 'Geral')}**")
        
        tema_hashtags = st.text_input(
            "Insira o tema ou palavras-chave do post para criar as melhores hashtags:",
            placeholder="Ex: culto de libertação, confeitaria artesanal, bolo de festa...",
            key="input_tema_hashtags"
        )
        
        if st.button("Gerar Hashtags 🚀", key="btn_gerar_hashtags"):
            if tema_hashtags.strip():
                with st.spinner("Selecionando as melhores tags para o seu engajamento..."):
                    try:
                        resposta_tags = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {
                                    "role": "system", 
                                    "content": (
                                        f"Você é um especialista em SEO e redes sociais. "
                                        f"Gere uma seleção com as 15 a 20 melhores hashtags estratégicas (divididas entre virais, médias e nichadas) "
                                        f"completamente focadas no nicho '{dados.get('nicho')}'. "
                                        f"Entregue apenas as hashtags prontas, separadas por espaços, sem textos explicativos."
                                    )
                                },
                                {
                                    "role": "user", 
                                    "content": f"Gere hashtags para o seguinte tema de post: {tema_hashtags}"
                                }
                            ]
                        )
                        st.session_state["hashtags_geradas"] = resposta_tags.choices[0].message.content
                    except Exception as e:
                        st.error(f"Erro ao gerar hashtags na OpenAI: {e}")
            else:
                st.warning("Por favor, informe o tema das hashtags.")
                
        if st.session_state["hashtags_geradas"]:
            st.success("Hashtags geradas com sucesso! Copie no bloco abaixo:")
            st.code(st.session_state["hashtags_geradas"], language="text")

else:
    # ==========================================
    # 🔑 TELA DE LOGIN (SÓ APARECE SE NÃO ESTIVER LOGADO)
    # ==========================================
    st.title("🔑 Social Media Content Master - Login")
    
    with st.form("formulario_login"):
        usuario_input = st.text_input("Usuário")
        senha_input = st.text_input("Senha", type="password")
        botao_entrar = st.form_submit_button("Entrar no Sistema")
        
        if botao_entrar:
            if usuario_input.strip() and senha_input.strip():
                with st.spinner("Autenticando credenciais na base de dados..."):
                    try:
                        payload = {
                            "username": usuario_input.strip(),
                            "password": senha_input.strip()
                        }
                        resposta = requests.post(SCRIPT_URL, json=payload)
                        
                        if resposta.status_code == 200:
                            resultado_servidor = resposta.json()
                            
                            if resultado_servidor.get("status") == "success":
                                st.session_state["usuario_logado"] = resultado_servidor
                                st.success("Bênção! Acesso liberado.")
                                st.rerun()
                            else:
                                erro_msg = resultado_servidor.get("message", "Credenciais inválidas")
                                st.error(f"❌ Erro: {erro_msg}")
                        else:
                            st.error(f"Erro de comunicação com o servidor Google (Código: {resposta.status_code})")
                    except Exception as e:
                        st.error(f"Erro ao processar login: {e}")
            else:
                st.warning("Por favor, preencha todos os campos de login.")
                st.warning("Desenvolvido pr Comunicando Igrejas")
