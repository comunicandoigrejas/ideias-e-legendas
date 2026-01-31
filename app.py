import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="Social Media AI Gen", page_icon="📸", layout="centered")

# --- ESTILIZAÇÃO E DNA ---
st.title("📸 AI Social Media Assistant")
st.markdown("---")

# Campo de DNA (conforme sua ideia de sumir após digitar)
if 'dna_input' not in st.session_state:
    st.session_state.dna_input = ""

dna_text = st.text_input("🧬 Configure o DNA Ministerial (Pressione Enter)", 
                         type="password", 
                         placeholder="Cole aqui o DNA da igreja...")

if dna_text:
    st.session_state.dna_input = dna_text
    st.success("DNA configurado com sucesso!")
    st.caption(f"📍 **DNA atual:** {dna_text[:30]}...")

# --- CONFIGURAÇÃO DAS APIS ---
# No Streamlit Cloud, use st.secrets para segurança
try:
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Configure as chaves OPENAI_API_KEY e GEMINI_API_KEY nos Secrets do Streamlit.")

# --- ABAS DO APLICATIVO ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Prompts Gemini"])

# 1. ABA DE LEGENDAS
with tab1:
    tema_legenda = st.text_area("Sobre o que é a postagem?", placeholder="Ex: Culto de domingo sobre gratidão")
    if st.button("Gerar Legenda ✨"):
        prompt_sistema = f"Você é um social media expert. Use o DNA: {st.session_state.dna_input}. Crie uma legenda com muitos emojis, hashtags e CTA."
        
        response = client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Gere uma legenda para: {tema_legenda}"}
            ]
        )
        st.subheader("Sua Legenda:")
        st.write(response.choices[0].message.content)

# 2. ABA DE STORIES
with tab2:
    tema_story = st.text_input("Qual o tema dos Stories?")
    if st.button("Gerar Roteiro 🤳"):
        prompt_sistema = f"Crie um roteiro de 5 stories com emojis, sugestões de enquetes e textos de tela. DNA: {st.session_state.dna_input}"
        
        response = client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Roteiro para: {tema_story}"}
            ]
        )
        st.subheader("Roteiro Sugerido:")
        st.write(response.choices[0].message.content)

# 3. ABA DE PROMPTS (GEMINI)
with tab3:
    tema_imagem = st.text_input("Descreva a imagem que deseja criar:")
    if st.button("Criar Prompt Profissional 🎨"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_request = f"Transforme isso em um prompt detalhado de imagem para IA (estilo fotorealista, luz suave, 4k): {tema_imagem}"
        
        response = model.generate_content(prompt_request)
        st.subheader("Prompt Gerado para o Gemini:")
        st.code(response.text)
