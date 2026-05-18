import streamlit as st
import google.generativeai as genai

# Garanta que o Gemini está configurado com a API Key do usuário que fez o login
if "usuario_logado" in st.session_state:
    genai.configure(api_key=st.session_state.usuario_logado["api_key_user"])

def gerar_imagem_com_gemini(ideia_usuario, dna_chat_pronto):
    """
    Usa o DNA do chat pronto do usuário para criar o prompt 
    e depois gera a imagem real no formato 1:1.
    """
    try:
        # PASSO 1: Usar o modelo de texto para processar a ideia baseada no "Chat Pronto" (DNA)
        # Aqui passamos a instrução personalizada de cada usuário que vem da planilha
        modelo_texto = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                f"Você é um especialista em criar prompts artísticos. Baseando-se rigorosamente neste "
                f"estilo/DNA de chat pronto do usuário: '{dna_chat_pronto}', transforme a ideia enviada em um "
                f"prompt de imagem detalhado e profissional. "
                f"EXIGÊNCIA VISUAL: A imagem DEVE usar tons de azul, roxo, verde, laranja e amarelo. "
                f"Não use texto escrito dentro da imagem."
            )
        )
        
        # O Gemini gera o prompt perfeito focado nas suas cores
        resposta_prompt = modelo_texto.generate_content(f"Crie um prompt detalhado para a ideia: {ideia_usuario}")
        prompt_final = resposta_prompt.text

        # PASSO 2: Chamar o Imagen 3 para desenhar a imagem real
        modelo_imagem = genai.ImageGenerationModel("imagen-3.0-generate-002")
        resultado = modelo_imagem.generate_images(
            prompt=prompt_final,
            number_of_images=1,
            aspect_ratio="1:1"  # Força o formato perfeito para o feed do Instagram
        )
        
        # Retorna os bytes da imagem gerada
        return resultado.images[0].image.bytes

    except Exception as e:
        st.error(f"Erro ao operar a geração da imagem: {e}")
        return None

# --- CONTROLE DE TELA SEGURO ---

# Verificamos primeiro se o usuário já passou pelo login com sucesso
if "usuario_logado" in st.session_state and st.session_state["usuario_logado"] is not None:
    
    # 1. Se ele estiver logado, pegamos os dados dele com segurança
    dados_usuario = st.session_state["usuario_logado"]
    nome = dados_usuario.get("nome_exibicao", "Varão")
    
    # 2. Exibe o topo da tela personalizado (sem a barra lateral)
    st.write(f"✨ Cliente: **{nome}**")
    st.title("📸 Social Media Content Master")
    
    # --- AQUI CONTINUA O SEU CÓDIGO DA ÁREA LOGADA ---
    # Onde gera as ideias, imagens 1:1, cores da marca e o botão de copiar a legenda...

else:
    # 3. Se NÃO estiver logado, exibe estritamente a tela de login
    st.title("🔑 Social Media Content Master - Login")
    
    with st.form("formulario_login"):
        usuario_input = st.text_input("Usuário")
        senha_input = st.text_input("Senha", type="password")
        botao_entrar = _=st.form_submit_button("Entrar no Sistema")
        
        if botao_entrar:
            # Aqui roda a sua função doPost(e) que você já configurou.
            # Quando o login funcionar, você salva os dados assim:
            # st.session_state["usuario_logado"] = resultado_do_google_sheets
            # st.rerun()
            pass
