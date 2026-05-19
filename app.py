import streamlit as st
import requests

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

# 1. VERIFICAÇÃO DO LINK DO SCRIPT DO GOOGLE
if "URL_PLANILHA_SCRIPT" in st.secrets:
    SCRIPT_URL = st.secrets["URL_PLANILHA_SCRIPT"]
else:
    st.error("⚠️ Erro: Chave 'URL_PLANILHA_SCRIPT' não encontrada nos Secrets do Streamlit.")
    st.stop()

# Inicializar as variáveis de sessão (gavetas de memória)
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None
if "legenda_gerada" not in st.session_state:
    st.session_state["legenda_gerada"] = ""

# --- CONTROLE DE FLUXO DE TELAS ---

if st.session_state["usuario_logado"] is not None:
    # ==========================================
    # 🚀 TELA PRINCIPAL (SISTEMA INTEGRADO VIA SCRIPT)
    # ==========================================
    dados = st.session_state["usuario_logado"]
    
    # Exibe o Nome do Cliente ACIMA do título do sistema
    st.write(f"✨ Cliente Ativo: **{dados.get('nome_exibicao', 'Varão')}**")
    st.title("📸 Social Media Content Master")
    
    # Botão para Sair do Aplicativo
    if st.button("🚪 Sair do Aplicativo"):
        st.session_state["usuario_logado"] = None
        st.session_state["legenda_gerada"] = ""
        st.rerun()
        
    st.divider()
    
    # CRIAÇÃO DAS JANELAS SEPARADAS (ABAS)
    janela_legenda, janela_arte = st.tabs(["📝 Criar Legenda", "🎨 Criar Arte"])
    
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
                with st.spinner("O servidor está processando sua legenda..."):
                    try:
                        # Enviamos a ação 'gerar_legenda' direto para o seu script do Google
                        payload = {
                            "action": "gerar_legenda",
                            "username": dados.get("username"),
                            "prompt": tema_legenda.strip()
                        }
                        resposta = requests.post(SCRIPT_URL, json=payload)
                        
                        if resposta.status_code == 200:
                            resultado = resposta.json()
                            if resultado.get("status") == "success":
                                st.session_state["legenda_gerada"] = resultado.get("texto")
                            else:
                                st.error(f"Erro no Script: {resultado.get('message')}")
                        else:
                            st.error(f"Erro de conexão com a planilha (Status: {resposta.status_code})")
                    except Exception as e:
                        st.error(f"Erro ao processar a legenda: {e}")
            else:
                st.warning("Por favor, digite o assunto da legenda antes de gerar.")
                
        if st.session_state["legenda_gerada"]:
            st.success("Legenda pronta! Para copiar, basta clicar no ícone de duas folhas no canto superior direito do bloco abaixo:")
            st.code(st.session_state["legenda_gerada"], language="text")
            
    # ------------------------------------------
    # JANELA 2: CRIAÇÃO DA ARTE PRONTA
    # ------------------------------------------
    with janela_arte:
        st.write("### Gerador de Imagens Integrado (Pronto para o Feed)")
        st.caption("As imagens são geradas automaticamente no formato quadrado (1:1) para o Instagram.")
        
        ideia_arte = st.text_input(
            "Digite a ideia da imagem que você quer entregar pronta:",
            key="input_ideia_arte"
        )
        
        if st.button("Gerar Imagem Pronta 📸", key="btn_gerar_arte"):
            if ideia_arte.strip():
                with st.spinner("O servidor está desenhando a sua arte real agora, aguarde..."):
                    try:
                        # Enviamos a ação 'gerar_arte' direto para o seu script do Google
                        payload = {
                            "action": "gerar_arte",
                            "username": dados.get("username"),
                            "prompt": ideia_arte.strip()
                        }
                        resposta = requests.post(SCRIPT_URL, json=payload)
                        
                        if resposta.status_code == 200:
                            resultado = resposta.json()
                            if resultado.get("status") == "success":
                                url_imagem = resultado.get("url_imagem")
                                
                                # Puxa os bytes da imagem final gerada pelo link do script
                                img_data = requests.get(url_imagem).content
                                
                                st.success("Glória a Deus! Arte criada com sucesso:")
                                st.image(img_data, caption="Sua arte gerada (Proporção 1:1)", use_container_width=True)
                                
                                st.download_button(
                                    label="📥 Baixar Imagem Pronta",
                                    data=img_data,
                                    file_name="arte_social_media.png",
                                    mime="image/png",
                                    key="btn_download_arte"
                        )
                            else:
                                st.error(f"Erro no Script de Arte: {resultado.get('message')}")
                        else:
                            st.error(f"Erro de conexão com a planilha (Status: {resposta.status_code})")
                    except Exception as e:
                        st.error(f"Erro ao processar ou gerar a imagem: {e}")
            else:
                st.warning("Por favor, digite qual é a ideia da imagem.")

else:
    # ==========================================
    # 🔑 TELA DE LOGIN
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
                            "action": "login",
                            "username": usuario_input.strip(),
                            "password": senha_input.strip()
                        }
                        resposta = requests.post(SCRIPT_URL, json=payload)
                        
                        if resposta.status_code == 200:
                            resultado_servidor = resposta.json()
                            
                            if resultado_servidor.get("status") == "success":
                                # Salva os dados retornados e insere o 'username' para controle posterior
                                resultado_servidor["username"] = usuario_input.strip()
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
