import streamlit as st

# Inicializa a memória se ela não existir
if "dna_registrado" not in st.session_state:
    st.session_state.dna_registrado = ""

st.title("🚀 Social Media Manager")

# Área de texto que carrega o que já está salvo na memória
dna_atualizado = st.text_area(
    "🧬 DNA da Empresa (Gravado automaticamente):", 
    value=st.session_state.dna_registrado,
    placeholder="Digite o DNA aqui uma única vez...",
    height=150
)

# Se o que foi digitado for diferente do que está salvo, ele atualiza a "gravação"
if dna_atualizado != st.session_state.dna_registrado:
    st.session_state.dna_registrado = dna_atualizado
    st.success("✅ DNA atualizado com sucesso!")

# Exibição discreta para confirmar que está gravado
if st.session_state.dna_registrado:
    st.info(f"📍 Memória ativa para: {st.session_state.dna_registrado[:50]}...")
