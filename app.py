# app.py COMPLETO CORRIGIDO
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

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# ==========================================
# SESSION STATE
# ==========================================

if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

if "resultado_final" not in st.session_state:
    st.session_state["resultado_final"] = ""

# ==========================================
# FUNÇÃO GERAR CONTEÚDO
# ==========================================


def gerar_conteudo(dados_usuario, tema_post):

    dna = dados_usuario.get(
        "dna",
        "Escreva de forma envolvente e estratégica"
    )

    nicho = dados_usuario.get(
        "nicho",
        "Marketing"
    )

    tom = dados_usuario.get(
        "tom",
        "Profissional"
    )

    objetivo = dados_usuario.get(
        "objetivo",
        "Gerar engajamento"
    )

    publico = dados_usuario.get(
        "publico",
        "Público geral"
    )

    cta = dados_usuario.get(
        "cta",
        "Clique no link da bio"
    )

    system_prompt = f"""
    Você é especialista em criação de legendas para redes sociais.

    NICHO:
    {nicho}

    DNA:
    {dna}

    TOM:
    {tom}

    OBJETIVO:
    {objetivo}

    PÚBLICO:
    {publico}

    CTA:
    {cta}

    REGRAS:
    - Criar conexão emocional
    - Gerar retenção
    - Gerar engajamento
    - Adaptar a linguagem ao nicho
    - Criar a legenda com emojis relacionados ao tema
    - Utilizar copy persuasiva
    - Utilizar gatilhos mentais quando fizer sentido
    - Finalizar com CTA forte, recomendando o pedido quando convenienete exemplo peça já a sua ou nos envie seu cardapio para um orçamento
    - Inserir exatamente 5 hashtags no final da legenda
    - Utilizar hashtags relevantes para o nicho
    - Nunca inventar ingredientes, produtos ou informações não citadas pelo usuário
    - Ser totalmente fiel ao pedido informado
    - Não adicionar acompanhamentos que não foram mencionados
    - Não modificar nomes de produtos
    - Não criar informações fictícias
    """


    user_prompt = f"""
    Crie uma legenda para Instagram exatamente sobre:

    {tema_post}
    """

    resposta = client.responses.create(
        model="gpt-4.1-mini",
        instructions=system_prompt,
        input=user_prompt
    )

    return resposta.output_text


# ==========================================
# ÁREA LOGADA
# ==========================================

if st.session_state["usuario_logado"] is not None:

    dados = st.session_state["usuario_logado"]

    st.title("📸 Social Media Content Master")

    st.success(
        f"Cliente ativo: {dados.get('nome_exibicao', 'Cliente')}"
    )

    st.caption(
        f"Nicho configurado: {dados.get('nicho', 'Geral')}"
    )

    # ==========================================
    # BOTÃO SAIR
    # ==========================================

    if st.button("🚪 Sair do Aplicativo"):

        st.session_state["usuario_logado"] = None
        st.session_state["resultado_final"] = ""

        st.rerun()

    st.divider()

    # ==========================================
    # INPUT TEMA
    # ==========================================

    tema_post = st.text_area(
        "Sobre qual assunto deseja criar a legenda?",
        placeholder="Ex: Marmita de frango com batata doce",
        height=120
    )

    # ==========================================
    # BOTÃO GERAR
    # ==========================================

    if st.button("✨ Gerar Conteúdo"):

        if tema_post.strip():

            with st.spinner("Gerando legenda..."):

                try:

                    resultado = gerar_conteudo(
                        dados,
                        tema_post
                    )

                    st.session_state["resultado_final"] = resultado

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Erro ao gerar conteúdo: {e}"
                    )

        else:

            st.warning(
                "Digite um tema antes de gerar."
            )

    st.divider()

    # ==========================================
    # RESULTADO
    # ==========================================

    if st.session_state["resultado_final"]:

        col1, col2 = st.columns(2)

        with col1:

            if st.button("🗑️ Limpar Conteúdo"):

                st.session_state["resultado_final"] = ""

                st.rerun()

        with col2:

            st.caption(
                "📋 Use o botão copy no canto superior da caixa"
            )

        st.write("### 📝 Conteúdo Gerado")

        st.code(
            st.session_state["resultado_final"],
            language=None
        )

        st.success(
            "✅ Conteúdo gerado com sucesso"
        )

# ==========================================
# ÁREA LOGIN
# ==========================================

else:

    st.title("🔑 Social Media Content Master")

    with st.form("formulario_login"):

        usuario_input = st.text_input("Usuário")

        senha_input = st.text_input(
            "Senha",
            type="password"
        )

        botao_entrar = st.form_submit_button(
            "Entrar no Sistema"
        )

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
                            json=payload
                        )

                        if resposta.status_code == 200:

                            resultado_servidor = resposta.json()

                            if resultado_servidor.get("status") == "success":

                                st.session_state["usuario_logado"] = resultado_servidor

                                st.rerun()

                            else:

                                st.error(
                                    resultado_servidor.get(
                                        "message",
                                        "Usuário ou senha inválidos"
                                    )
                                )

                        else:

                            st.error(
                                f"Erro servidor ({resposta.status_code})"
                            )

                    except Exception as e:

                        st.error(
                            f"Erro no login: {e}"
                        )

            else:

                st.warning(
                    "Preencha usuário e senha"
                )

    st.caption("Desenvolvido por Comunicando Igrejas")
