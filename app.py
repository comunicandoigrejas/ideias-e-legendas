import streamlit as st
from openai import OpenAI

# Configuração da Página
st.set_page_config(page_title="Gerador Ministerial Pro", page_icon="⛪")

st.title("⛪ Social Media Ministerial")
st.markdown("---")

# --- LÓGICA DO DNA MINISTERIAL ---
# Usamos session_state para garantir que o DNA fique salvo "na memória" do app durante o uso
if "dna_ministerial" not in st.session_state:
    st.session_state.dna_ministerial = ""

# Campo de entrada que "limpa" visualmente após o Enter
dna_input = st.text_input(
    "🧬 Configure o DNA Ministerial da Igreja", 
    type="password", 
    placeholder="Ex: Igreja jovem, foco em missões, linguagem contemporânea..."
)

if dna_input:
    st.session_state.dna_ministerial = dna_input
    st.success("DNA Ministerial atualizado e aplicado à lógica da IA!")

# Exibição discreta conforme solicitado anteriormente
if st.session_state.dna_ministerial:
    resumo_dna = st.session_state.dna_ministerial[:40] + "..."
    st.caption(f"✨ **DNA atual:** {resumo_dna}")

st.markdown("---")

# --- FUNÇÃO DO SUPER AGENTE ---
def gerar_conteudo(tema, tipo_conteudo):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Aqui é onde o DNA Ministerial entra na lógica profunda
    system_message = f"""
    Você é um Super Agente de Comunicação Cristã. 
    Sua missão é criar conteúdo baseado RIGOROSAMENTE no seguinte DNA MINISTERIAL:
    ---
    {st.session_state.dna_ministerial}
    ---
    Regras de Ouro:
    1. Adapte o vocabulário, as gírias (ou falta delas) e a profundidade teológica ao DNA acima.
    2. Use MUITOS emojis relevantes para aumentar o engajamento.
    3. Sempre inclua uma CTA (Chamada para Ação) e Hashtags estratégicas.
    """
    
    prompt_usuario = f"Gere {tipo_conteudo} sobre o tema: {tema}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt_usuario}
        ]
    )
    return response.choices[0].message.content

# --- INTERFACE DE ABAS ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Prompts Gemini"])

with tab1:
    tema_post = st.text_area("Tema da Postagem:")
    if st.button("Gerar Legenda com DNA"):
        if st.session_state.dna_ministerial:
            with st.spinner("A IA está processando o DNA ministerial..."):
                resultado = gerar_conteudo(tema_post, "uma legenda para Instagram")
                st.markdown(resultado)
        else:
            st.warning("⚠️ Por favor, insira o DNA Ministerial antes de gerar.")

with tab2:
    tema_story = st.text_input("Tema dos Stories:")
    if st.button("Gerar Roteiro com DNA"):
        if st.session_state.dna_ministerial:
            with st.spinner("Criando sequência de stories..."):
                resultado = gerar_conteudo(tema_story, "um roteiro de 5 stories (texto e ação)")
                st.markdown(resultado)
        else:
            st.warning("⚠️ Insira o DNA Ministerial primeiro.")

with tab3:
    # Lógica similar para o prompt de imagem
    st.info("O DNA Ministerial também será usado para ditar o estilo visual dos prompts.")
    # ... (mesma lógica de chamada de API)
