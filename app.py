import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="Social Media Master AI", page_icon="📈", layout="wide")

st.title("🚀 Social Media Content Master")

# --- 🧬 CONFIGURAÇÃO DO DNA DA MARCA (VISÍVEL) ---
if "dna_marca" not in st.session_state:
    st.session_state.dna_marca = ""

# Expander para não ocupar espaço desnecessário após configurar
with st.expander("⚙️ Configurar Identidade da Marca (DNA)", expanded=True):
    # REMOVIDO O PASSWORD - Agora ela vê o que escreve
    dna_input = st.text_area(
        "Descreva o nicho, tom de voz e público-alvo:", 
        placeholder="Ex: Loja de sapatos femininos, tom descontraído e moderno, público 20-35 anos...",
        help="Essas informações guiarão a inteligência de todas as gerações."
    )
    if dna_input:
        st.session_state.dna_marca = dna_input
    
    if st.session_state.dna_marca:
        # Mensagem discreta confirmando que o DNA está ativo
        st.info(f"📍 DNA ativo: {st.session_state.dna_marca[:70]}...")

st.markdown("---")

# --- 🧠 LÓGICA DE GERAÇÃO (OPENAI & GEMINI) ---
def chamar_ia_completa(tema, formato, precisa_imagem):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    sys_prompt = f"""
    Você é um especialista em marketing digital e copywriter.
    ESTILO DA MARCA: {st.session_state.dna_marca}
    
    INSTRUÇÕES:
    - Use emojis em abundância para engajamento.
    - Crie ganchos fortes no início.
    - Finalize com uma CTA (Chamada para Ação).
    - Inclua hashtags relevantes.
    """
    
    user_prompt = f"Gere conteúdo para um {formato} sobre o tema: {tema}."
    if formato == "Carrossel":
        user_prompt += " Sugira o que escrever em cada slide (mínimo 5 slides)."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}]
    )
    
    texto_final = response.choices[0].message.content
    prompt_img = ""
    
    if precisa_imagem:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_refinado = f"Crie um prompt visual rico para IA baseado no tema '{tema}' e no estilo de marca: {st.session_state.dna_marca}. Foco em qualidade fotográfica para Instagram."
        img_res = model.generate_content(prompt_refinado)
        prompt_img = img_res.text
        
    return texto_final, prompt_img

# --- ABAS ---
tab1, tab2, tab3 = st.tabs(["✍️ Legendas", "📱 Stories", "🎨 Prompts Gemini"])

with tab1:
    col_in, col_out = st.columns([1, 1.2])
    with col_in:
        formato = st.selectbox("Formato do Post:", ["Post Simples", "Carrossel", "Reels", "Anúncio"])
        tema = st.text_area("Sobre o que vamos falar hoje?", placeholder="Ex: Promoção de queima de estoque")
        check_img = st.checkbox("Gerar prompt de imagem para este post?")
        btn_gerar = st.button("Gerar Conteúdo ✨")

    if btn_gerar:
        if st.session_state.dna_marca:
            txt, img = chamar_ia_completa(tema, formato, check_img)
            with col_out:
                st.subheader("📝 Legenda Gerada")
                st.write(txt)
                if check_img:
                    st.divider()
                    st.subheader("🎨 Prompt de Imagem")
                    st.code(img)
        else:
            st.error("Por favor, preencha o DNA da Marca antes.")

with tab2:
    tipo_s = st.selectbox("Estilo do Story:", ["Educativo", "Venda/Oferta", "Bastidores", "Caixinha de Perguntas"])
    tema_s = st.text_input("Contexto do Story:")
    if st.button("Criar Sequência de Stories 🤳"):
        # Reaproveita a lógica da IA com ajuste de formato
        txt, _ = chamar_ia_completa(tema_s, f"Sequência de 5 Stories estilo {tipo_s}", False)
        st.markdown(txt)

with tab3:
    tema_livre = st.text_input("Ideia para imagem isolada:")
    if st.button("Gerar Prompt Detalhado"):
        _, img_solo = chamar_ia_completa(tema_livre, "Prompt de Imagem", True)
        st.code(img_solo)
