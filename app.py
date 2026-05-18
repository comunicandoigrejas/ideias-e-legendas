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

# --- SUA TELA DE CRIAÇÃO DE IMAGEM ---
st.title("📸 Gerador de Imagens Integrado")
st.write(f"Bem-vindo, abençoado **{st.session_state.usuario_logado.get('nome_exibicao', 'Varão')}**!")

# Input onde o usuário digita a ideia simples
ideia = st.text_input("Qual ideia de imagem você quer que o Gemini crie hoje?")

if st.button("Gerar Imagem Pronta ✨"):
    if ideia:
        with st.spinner("Aguarde, irmão... O Gemini está processando e gerando sua imagem pronta..."):
            # Puxa a configuração do chat pronto (coluna D da sua planilha)
            dna_do_usuario = st.session_state.usuario_logado.get("dna", "Estilo profissional e moderno")
            
            # Executa a função
            imagem_bytes = gerar_imagem_com_gemini(ideia, dna_do_usuario)
            
            if imagem_bytes:
                st.success("Bênção pura! Imagem gerada com sucesso:")
                
                # Exibe a imagem gerada direto na tela do App
                st.image(imagem_bytes, caption="Sua imagem gerada (Proporção 1:1)", use_container_width=True)
                
                # Cria o botão para o cliente baixar o arquivo PNG pronto
                st.download_button(
                    label="📥 Baixar Imagem Pronta",
                    data=imagem_bytes,
                    file_name="post_instagram_pronto.png",
                    mime="image/png"
                )
    else:
        st.warning("Por favor, digite a ideia da imagem para que o sistema possa trabalhar.")
