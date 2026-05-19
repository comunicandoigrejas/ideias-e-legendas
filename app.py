import streamlit as st
import requests
from openai import OpenAI

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Social Media Content Master",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# ESCONDER SIDEBAR
# ==========================================

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="collapsedSidebarNoContent"] {
            display: none !important;
        }
        .stCodeBlock {
            white-space: pre-wrap;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# VERIFICAÇÃO DOS SECRETS
# ==========================================

if "URL_PLANILHA_SCRIPT" not in st.secrets:
    st.error("⚠️ URL_PLANILHA_SCRIPT não encontrada nos secrets.")
    st.stop()

if "OPENAI_API_KEY" not in st.secrets:
    st.error("⚠️ OPENAI_API_KEY não encontrada nos secrets.")
    st.stop()

SCRIPT_URL = st.secrets["URL_PLANILHA_SCRIPT"]

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==========================================
# SESSION STATE
# ==========================================

if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

if "resultado_final" not in st.session_state:
    st.session_state["resultado_final"] = ""

# ==========================================
# FUNÇÃO GERAR CONTEÚDO (APROVADA)
# ==========================================

def gerar_conteudo(dados_usuario, tema_post):
    if not tema_post or not tema_post.strip():
        return "❌ Por favor, insira um tema para gerar a legenda."

    dna = dados_usuario.get("dna", "Escreva de forma envolvente e estratégica")
    nicho = dados_usuario.get("nicho", "Marketing")
    tom = dados_usuario.get("tom", "Profissional")
    objetivo = dados_usuario.get("objetivo", "Gerar engajamento")
    publico = dados_usuario.get("publico", "Público geral")
    cta = dados_usuario.get("cta", "Clique no link da bio")

    system_prompt = f"""
    Você é um especialista em copywriting para Instagram, focado em legenda persuasivas e de alto engajamento.

    NICHO: {nicho}
    DNA DA MARCA: {dna}
    TOM DE VOZ: {tom}
    OBJETIVO: {objetivo}
    PÚBLICO-ALVO: {publico}
    CTA PADRÃO: {cta}

    REGRAS OBRIGATÓRIAS:
    - Escreva em português brasileiro natural e fluido
    - Crie conexão emocional com o público
    - Use no máximo 3-4 emojis relevantes
    - Utilize gatilhos mentais quando fizer sentido
    - Seja fiel ao tema informado pelo usuário
    - Nunca invente ingredientes, preços, nomes ou informações
    - Finalize sempre com um CTA forte
    - Insira exatamente 5 hashtags relevantes no final
    - Mantenha a legenda atrativa, escaneável e persuasiva
    """

    user_prompt = f"""
    Crie uma legenda para Instagram exatamente sobre o seguinte tema:

    {tema_post}
    """

    try:
        resposta = client.responses.create(
            model="gpt-4.1-mini",
            instructions=system_prompt,
            input=user_prompt,
            temperature=0.75,
            max_output_tokens=800
        )
        return resposta.output_text.strip()

    except Exception as e:
        raise Exception(f"Erro na API OpenAI: {str(e)}")


# ==========================================
# ÁREA LOGADA
# ==========================================

if st.session_state["usuario_logado"] is not None:

    dados = st.session_state["usuario_logado"]

    st.title("📸 Social Media Content Master")
    st.success(f"✅ Cliente ativo: **{dados.get('nome_exibicao', 'Cliente')}**")
    st.caption(f"📌 Nicho: **{dados.get('nicho', 'Não configurado')}**")

    # Botão Sair
    if st.button("🚪 Sair do Aplicativo"):
        st.session_state["usuario_logado"] = None
        st.session_state["resultado_final"] = ""
        st.rerun()

    st.divider()

    # Input do Tema
    tema_post = st.text_area(
        "Sobre qual assunto deseja criar a legenda?",
        placeholder="Ex: Marmita fit de frango grelhado com batata doce e brócolis (300g)",
        height=140,
        max_chars=600
    )

    # Botão Gerar
    if st.button("✨ Gerar Legenda", type="primary", use_container_width=True):
        if tema_post.strip():
            with st.spinner("Gerando legenda com IA..."):
                try:
                    resultado = gerar_conteudo(dados, tema_post)
                    st.session_state["resultado_final"] = resultado
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao gerar conteúdo: {str(e)}")
        else:
            st.warning("⚠️ Digite o tema da legenda antes de gerar.")

    st.divider()

    # Resultado
    if st.session_state["resultado_final"]:
        col1, col2 = st.columns([1, 3])

        with col1:
            if st.button("🗑️ Limpar"):
                st.session_state["resultado_final"] = ""
                st.rerun()

        with col2:
            st.caption("📋 Clique no botão de copiar no canto superior direito da caixa")

        st.subheader("📝 Legenda Gerada")
        st.code(st.session_state["resultado_final"], language=None)

        st.success("✅ Legenda gerada com sucesso!")

# ==========================================
# ÁREA DE LOGIN
# ==========================================

else:
    st.title("🔑 Social Media Content Master")
    st.markdown("### Faça login para continuar")

    with st.form("formulario_login"):
        usuario_input = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
        senha_input = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")

        botao_entrar = st.form_submit_button("Entrar no Sistema", use_container_width=True)

        if botao_entrar:
            if usuario_input.strip() and senha_input.strip():
                with st.spinner("Autenticando..."):
                    try:
                        payload = {
                            "username": usuario_input.strip(),
                            "password": senha_input.strip()
                        }

                        resposta = requests.post(
                            SCRIPT_URL,
                            json=payload,
                            timeout=12
                        )

                        if resposta.status_code == 200:
                            resultado_servidor = resposta.json()

                            if resultado_servidor.get("status") == "success":
                                st.session_state["usuario_logado"] = resultado_servidor
                                st.success("Login realizado com sucesso!")
                                st.rerun()
                            else:
                                st.error(resultado_servidor.get("message", "Usuário ou senha inválidos"))
                        else:
                            st.error(f"Erro no servidor ({resposta.status_code})")

                    except requests.exceptions.Timeout:
                        st.error("⏳ Tempo de resposta esgotado. Tente novamente.")
                    except Exception as e:
                        st.error(f"Erro de conexão: {str(e)}")
            else:
                st.warning("Preencha usuário e senha")

    st.caption("Desenvolvido por Comunicando Igrejas")
