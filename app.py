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
if "resultado_final" not in st.session_state:
    st.session_state["resultado_final"] = ""

# --- CONTROLE DE FLUXO DE TELAS ---

if st.session_state["usuario_logado"] is not None:
    # ==========================================
    # 🚀 TELA PRINCIPAL (TELA ÚNICA INTEGRADA)
    # ==========================================
    dados = st.session_state["usuario_logado"]
    
    # Exibe o Nome do Cliente ACIMA do título do sistema
    st.write(f"✨ Cliente Ativo: **{dados.get('nome_exibicao', 'Varão')}**")
    st.title("📸 Social Media Content Master")
    
    # Botão para Sair do Aplicativo
    if st.button("🚪 Sair do Aplicativo"):
        st.session_state["usuario_logado"] = None
        st.session_state["resultado_final"] = ""
        st.rerun()
        
    st.divider()
    
    st.write(f"### Gerador de Conteúdo Profissional")
    st.caption(f"Nicho configurado para este perfil: **{dados.get('nicho', 'Geral')}**")
    
    # Campo de entrada para o tema do post
    tema_post = st.text_area(
        "Sobre qual assunto ou tema você deseja criar o seu post hoje, irmão?", 
        placeholder="Ex: Aviso sobre o culto de jovens deste sábado ou promoção de doces gourmet...",
        key="input_tema_post"
    )
    
    if st.button("Gerar Conteúdo Completo ✨", key="btn_gerar_tudo"):
        if tema_post.strip():
            with st.spinner("A OpenAI está redigindo sua legenda e selecionando as hashtags..."):
                try:
                    dna_do_chat = dados.get("dna", "Escreva de forma engajadora")
                    
                    # Chamada única para o GPT criar o texto e as tags juntos de forma harmoniosa
                    resposta = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system", 
                                "content": (
                                    f"Você é um redator e especialista em SEO profissional. "
                                    f"Use estritamente o seguinte estilo/DNA de escrita: {dna_do_chat}. "
                                    f"Foque no nicho: {dados.get('nicho')}. "
                                    f"Instrução de formato: Escreva a legenda completa para o Instagram e, logo ao final dela, "
                                    f"adicione uma seleção de 15 a 20 hashtags estratégicas (virais e nichadas) separadas por espaços."
                                )
                            },
                            {
                                "role": "user", 
                                "content": f"Crie uma legenda e hashtags para um post sobre: {tema_post}"
                            }
                        ]
                    )
                    st.session_state["resultado_final"] = resposta.choices[0].message.content
                except Exception as e:
                    st.error(f"Erro ao processar na OpenAI: {e}")
        else:
            st.warning("Por favor, digite o assunto do post antes de gerar.")
            
    st.divider()
    
    # Se já houver conteúdo gerado, exibe na caixa de texto para edição/cópia
    if st.session_state["resultado_final"]:
        st.write("### 📝 Legenda e Hashtags Prontas")
        st.caption("Você pode editar ou ajustar o texto diretamente na caixa abaixo antes de copiar:")
        
        # Caixa de texto editável com o conteúdo gerado
        conteudo_editado = st.text_area(
            label="Conteúdo final do post",
            value=st.session_state["resultado_final"],
            height=350,
            key="caixa_resultado_final"
        )
        
        # Atualiza a memória caso o usuário digite algo na caixa de texto
        st.session_state["resultado_final"] = conteudo_editado
        st.success("Glória a Deus! Tudo pronto. Basta selecionar o texto acima e copiar para o seu Instagram.")

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
                            resultado_servidor = response_json = resposta.json()
                            
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
