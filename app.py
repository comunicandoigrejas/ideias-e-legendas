import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="Social Media Pro", page_icon="📈", layout="wide")

# Título Principal
st.title("🚀 Social Media Content Master")
st.markdown("Gerador inteligente de Legendas, Stories e Prompts.")

# --- 🧬 CONFIGURAÇÃO DO DNA DA MARCA ---
if "dna_marca" not in st.session_state:
    st.session_state.dna_marca = ""

with st.expander("⚙️ Configurar Identidade da Marca (DNA)", expanded=True):
    dna_input = st.text_input(
        "Defina o perfil do negócio e tom de voz:", 
        type="password", 
        placeholder="Ex: Consultoria financeira, tom sério e educativo..."
    )
    if dna_input:
        st.session_state.dna_marca = dna_input
    
    if st.session_state.dna_marca:
        st.caption(f"✅ **DNA atual:** {st.session_state.dna_marca[:60]}...")

st.markdown("---")

# --- 🧠 LÓGICA DO SUPER AGENTE (OPENAI) ---
def chamar_ia(prompt_sistema, prompt_usuario):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    )
    return response.choices[0].message.content

# --- 🎨 LÓGICA DO PROMPT DE IMAGEM (GEMINI) ---
def gerar_prompt_imagem(tema_base):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Crie um prompt detalhado e profissional para uma IA geradora de imagens. O tema é: {tema_base}. Considere o DNA da marca: {st.session_state.dna_marca}. O estilo deve ser focado em redes sociais de alta qualidade."
    response = model.generate_content(prompt)
    return response.text

# --- 🗂️ INTERFACE DE ABAS ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Criador de Prompts (Solo)"])

# 1. ABA DE LEGENDAS
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tipo_post = st.selectbox("Formato da Postagem:", ["Post Simples", "Carrossel", "Reels", "Vídeo Curto"])
        tema_legenda = st.text_area("Sobre o que é a postagem?", height=100)
        
        # Opção de gerar prompt de imagem junto
        precisa_imagem = st.radio("Gerar prompt de imagem para esta legenda?", ["Não", "Sim"], horizontal=True)

    if st.button("Gerar Conteúdo Completo ✨"):
        if not st.session_state.dna_marca:
            st.warning("⚠️ Configure o DNA da marca acima.")
        else:
            with st.spinner("Criando..."):
                # System Prompt customizado
                sys_prompt = f"Você é um social media expert. DNA: {st.session_state.dna_marca}. Use muitos emojis, hashtags e CTA."
                user_prompt = f"Crie uma legenda para um {tipo_post} sobre: {tema_legenda}. Se for carrossel, descreva o que vai em cada slide."
                
                legenda_final = chamar_ia(sys_prompt, user_prompt)
                
                with col2:
                    st.subheader("📝 Resultado:")
                    st.write(legenda_final)
                    
                    if precisa_imagem == "Sim":
                        st.markdown("---")
                        st.subheader("🎨 Prompt para Imagem:")
                        prompt_img = gerar_prompt_imagem(tema_legenda)
                        st.code(prompt_img)

# 2. ABA DE STORIES
with tab2:
    tipo_story = st.selectbox("Tipo de Story:", ["Bastidores", "Venda Direta (Oferta)", "Educativo/Dica", "Enquetes/Interação"])
    tema_story = st.text_area("Qual o contexto ou tema do story?")
    
    if st.button("Gerar Roteiro de Stories 🤳"):
        if st.session_state.dna_marca:
            sys_prompt = f"Especialista em Stories. DNA: {st.session_state.dna_marca}. Crie sequências dinâmicas com muitos emojis."
            user_prompt = f"Crie um roteiro de 5 stories do tipo {tipo_story} sobre: {tema_story}. Inclua indicações de texto para a tela."
            
            roteiro = chamar_ia(sys_prompt, user_prompt)
            st.markdown(roteiro)
        else:
            st.warning("⚠️ Configure o DNA da marca.")

# 3. ABA DE PROMPTS GEMINI (SOLO)
with tab3:
    st.info("Use esta aba para criar prompts de imagens que não estão necessariamente ligados a uma legenda.")
    tema_livre = st.text_input("Descreva a ideia da imagem:")
    if st.button("Gerar Prompt Detalhado 🎨"):
        if st.session_state.dna_marca:
            res_prompt = gerar_prompt_imagem(tema_livre)
            st.code(res_prompt)
        else:
            st.warning("⚠️ Configure o DNA da marca.")
