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
    # 🚀 TELA PRINCIPAL (APÓS LOGIN COM SUCESSO)
    # ==========================================
    dados = st.session_state["usuario_logado"]
    
    # Inicializa o cliente da OpenAI usando a chave vinda da planilha (Coluna F)
    # Certifique-se de que a chave na planilha comece com "sk-..."
    if dados.get("api_key_user"):
        client = OpenAI(api_key=dados.get("api_key_user"))
    else:
        st.error("⚠️ Chave de API da OpenAI não encontrada para este usuário na planilha.")
        st.stop()
    
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
    # JANELA 1: CRIAÇÃO DE LEGENDA (OPENAI)
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
                        
                        # Chamada oficial do modelo gpt-4o-mini (rápido e econômico)
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
    # JANELA 2: CRIAÇÃO DA ARTE PRONTA (OPENAI DALL-E 3)
    # ------------------------------------------
    with janela_arte:
        st.write("### Gerador de Imagens Integrado (Pronto para o Feed)")
        st.caption("As imagens são geradas automaticamente no formato quadrado (1:1) para o Instagram.")
        
        ideia_arte = st.text_input(
            "Digite a ideia da imagem que você quer que a Inteligência Artificial entregue pronta:",
            key="input_ideia_arte"
        )
        
        if st.button("Gerar Imagem Pronta 📸", key="btn_gerar_arte"):
            if id_arte := ideia_arte.strip():
                with st.spinner("A OpenAI está gerando a sua arte real agora através do DALL-E 3, aguarde..."):
                    try:
                        dna_do_chat = dados.get("dna", "Estilo moderno")
                        
                        # Construção do prompt injetando a identidade de cores e formato
                        prompt_completo = (
                            f"Crie uma imagem de alta qualidade baseada no estilo: '{dna_do_chat}'. "
                            f"Ideia central: {id_arte}. "
                            f"DIRETRIZ VISUAL OBRIGATÓRIA: A imagem deve focar fortemente nas tonalidades de azul, roxo, verde, laranja e amarelo. "
                            f"Importante: Não adicione nenhum tipo de texto, letras, frases ou palavras escritas dentro da imagem."
                        )
                        
                        # Chamada oficial do DALL-E 3 da OpenAI
                        resposta_imagem = client.images.generate(
                            model="dall-e-3",
                            prompt=prompt_completo,
                            size="1024x1024",  # Força a proporção 1:1 perfeita para o Instagram
                            quality="standard",
                            n=1,
                        )
                        
                        url_imagem = resposta_imagem.data[0].url
                        
                        # Baixa os bytes da imagem gerada pela URL para permitir o download no botão do Streamlit
                        img_bytes = requests.get(url_imagem).content
                        
                        st.success("Glória a Deus! Arte criada com sucesso:")
                        st.image(img_bytes, caption="Sua arte gerada pela OpenAI (Proporção 1:1)", use_container_width=True)
                        
                        st.download_button(
                            label="📥 Baixar Imagem Pronta",
                            data=img_bytes,
                            file_name="arte_openai_social_media.png",
                            mime="image/png",
                            key="btn_download_arte"
                        )
                    except Exception as e:
                        st.error(f"Erro ao gerar a imagem na OpenAI: {e}")
            else:
                st.warning("Por favor, digite qual é a ideia da imagem.")

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
