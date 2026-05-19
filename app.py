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

# Remove sidebar completamente
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="collapsedSidebarNoContent"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# VERIFICAÇÃO DOS SECRETS
# ==========================================

if "URL_PLANILHA_SCRIPT" in st.secrets:
    SCRIPT_URL = st.secrets["URL_PLANILHA_SCRIPT"]
else:
    st.error("⚠️ Chave URL_PLANILHA_SCRIPT não encontrada.")
    st.stop()

if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )
else:
    st.error("⚠️ Chave OPENAI_API_KEY não encontrada.")
    st.stop()

# ==========================================
# SESSION STATE
# ==========================================

if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

if "resultado_final" not in st.session_state:
    st.session_state["resultado_final"] = ""

# ==========================================
# FUNÇÃO DE GERAÇÃO COM RESPONSES API
# ==========================================

def gerar_conteudo(dados_usuario, tema_post):

    dna = dados_usuario.get(
        "dna",
        "Escreva de forma moderna e envolvente"
    )

    nicho = dados_usuario.get(
        "nicho",
        "Marketing Digital"
    )

    nome_cliente = dados_usuario.get(
        "nome_exibicao",
        "Cliente"
    )

    # Campos futuros já preparados
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
        "Comente sua opinião."
    )

    # ==========================================
    # PROMPT DO AGENTE
    # ==========================================

    system_prompt = f"""
    Você é um especialista profissional em:
    - copywriting
    - marketing digital
    - SEO para redes sociais
    - criação de legendas virais

    CLIENTE:
    {nome_cliente}

    NICHO:
    {nicho}

    DNA DE ESCRITA:
    {dna}

    TOM:
    {tom}

    OBJETIVO:
    {objetivo}

    PÚBLICO:
    {publico}

    CTA PADRÃO:
    {cta}

    SUA MISSÃO:
    Criar legendas altamente profissionais para Instagram.

    REGRAS:
    - Criar conexão emocional
    - Gerar retenção
    - Gerar engajamento
    - Adaptar a linguagem ao nicho
    - Utilizar copy persuasiva
    - Utilizar gatilhos mentais quando fizer sentido
    - Finalizar com CTA forte
    - Inserir exatamente 5 hashtags no final da legenda
    - Utilizar hashtags relevantes para o nicho
    - Nunca inventar ingredientes, produtos ou informações não citadas pelo usuário
    - Ser totalmente fiel ao pedido informado
    - Não adicionar acompanhamentos que não foram mencionados
    - Não modificar nomes de produtos
    - Não criar informações fictícias
    """

    user_prompt = f"""
    Crie uma legenda para Instagram sobre:

{tema_post}

    {tema_post}
    """

    # ==========================================
    # CHAMADA OPENAI - RESPONSES API
    # ==========================================

    resposta = client.responses.create(
        model="gpt-5-mini",
        instructions=system_prompt,
        input=user_prompt
    )

    return resposta.output_text

# ==========================================
# ÁREA LOGADA
# ==========================================

if st.session_state["usuario_logado"] is not None:

    dados = st.session_state["usuario_logado"]

    st.write(
        f"✨ Cliente Ativo: **{dados.get('nome_exibicao', 'Cliente')}**"
    )

    st.title("📸 Social Media Content Master")

    # ==========================================
    # BOTÃO SAIR
    # ==========================================

    if st.button("🚪 Sair do Aplicativo"):

        st.session_state["usuario_logado"] = None
        st.session_state["resultado_final"] = ""

        st.rerun()

    st.divider()

    st.write("### Gerador de Conteúdo Profissional")

    st.caption(
        f"Nicho configurado: **{dados.get('nicho', 'Geral')}**"
    )

    # ==========================================
    # INPUT TEMA
    # ==========================================

    tema_post = st.text_area(
        "Sobre qual assunto você deseja criar conteúdo hoje?",
        placeholder="Ex: culto de jovens, promoção de roupas, hamburguer artesanal...",
        key="input_tema_post"
    )

    # ==========================================
    # GERAR CONTEÚDO
    # ==========================================

    if st.button("Gerar Conteúdo Completo ✨"):

        if tema_post.strip():

            with st.spinner("A IA está criando seu conteúdo..."):

                try:

                    resultado = gerar_conteudo(
                        dados,
                        tema_post
                    )

                    st.session_state["resultado_final"] = resultado

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

    # BOTÃO LIMPAR
    if st.button("🗑️ Limpar Conteúdo"):

        st.session_state["resultado_final"] = ""

        st.rerun()

    st.write("### 📝 Conteúdo Gerado")

    st.caption(
        "Você pode editar o conteúdo abaixo antes de copiar."
    )

    conteudo_editado = st.text_area(
        label="Legenda final",
        value=st.session_state["resultado_final"],
        height=350,
        key="caixa_resultado_final"
    )

    st.session_state["resultado_final"] = conteudo_editado

    st.success(
        "✅ Conteúdo gerado com sucesso."
    )

# ==========================================
# ÁREA DE LOGIN
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

                with st.spinner(
                    "Autenticando..."
                ):

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

                                st.success(
                                    "✅ Login realizado com sucesso."
                                )

                                st.rerun()

                            else:

                                erro_msg = resultado_servidor.get(
                                    "message",
                                    "Credenciais inválidas"
                                )

                                st.error(
                                    f"❌ {erro_msg}"
                                )

                        else:

                            st.error(
                                f"Erro servidor Google Sheets ({resposta.status_code})"
                            )

                    except Exception as e:

                        st.error(
                            f"Erro no login: {e}"
                        )

            else:

                st.warning(
                    "Preencha usuário e senha."
                )

    st.caption("Desenvolvido por Comunicando Igrejas")
