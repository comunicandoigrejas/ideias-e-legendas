import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="Gerador de Conteúdo AI", page_icon="📈")

st.title("🚀 Social Media Business Generator")
st.subheader("Crie conteúdos profissionais para qualquer nicho")

# --- LÓGICA DO DNA DA MARCA (MULTI-NICHO) ---
if "dna_marca" not in st.session_state:
    st.session_state.dna_marca = ""

# O campo limpa ao dar enter, mas o resumo aparece embaixo
dna_input = st.text_input(
    "🎯 Defina o DNA do Negócio (Nicho, tom de voz, público-alvo)", 
    type="password", 
    placeholder="Ex: Clínica de estética, tom elegante, público feminino classe A..."
)

if dna_input:
    st.session_state.dna_marca = dna_input
    st.success("Configuração de marca salva!")

# Exibição discreta do resumo
if st.session_state.dna_marca:
    st.info(f"📌 **DNA atual:** {st.session_state.dna_marca[:50]}...")

st.markdown("---")

# --- FUNÇÃO DO SUPER AGENTE ---
def gerar_conteudo_openai(tema, tipo):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    system_prompt = f"""
    Você é um estrategista de marketing digital de alto nível.
    O perfil do cliente que você está atendendo é: {st.session_state.dna_marca}.
    
    Regras:
    1. Use emojis para aumentar a retenção e o engajamento.
    2. Garanta que o tom de voz combine exatamente com o DNA fornecido.
    3. Inclua sempre uma CTA (Chamada para Ação) persuasiva.
    4. Adicione um bloco de hashtags estratégicas ao final.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Gere {tipo} sobre o tema: {tema}"}
        ]
    )
    return response.choices[0].message.content

# --- ABAS DO APP ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Prompts Gemini"])

with tab1:
    tema_post = st.text_area("Sobre o que será o post?")
    if st.button("Gerar Legenda Completa"):
        if st.session_state.dna_marca:
            res = gerar_conteudo_openai(tema_post, "uma legenda de alta conversão")
            st.write(res)
        else:
            st.warning("Defina o DNA da marca primeiro.")

with tab2:
    tema_story = st.text_input("Objetivo dos Stories (Ex: Venda de produto X)")
    if st.button("Gerar Sequência de Stories"):
        if st.session_state.dna_marca:
            res = gerar_conteudo_openai(tema_story, "um roteiro de 5 stories (texto e ideia visual)")
            st.write(res)
        else:
            st.warning("Defina o DNA da marca primeiro.")

with tab3:
    tema_img = st.text_input("O que a imagem deve mostrar?")
    if st.button("Gerar Prompt para Gemini"):
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt_refinado = f"Crie um prompt detalhado de imagem para IA baseado no DNA {st.session_state.dna_marca}. O tema é: {tema_img}"
        response = model.generate_content(prompt_refinado)
        st.code(response.text)
