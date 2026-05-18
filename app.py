import streamlit as st
import requests
import json

# 1. ASSEGURAR A CONFIGURAÇÃO DO SCRIPT URL
if "URL_PLANILHA_SCRIPT" in st.secrets:
    SCRIPT_URL = st.secrets["URL_PLANILHA_SCRIPT"]
else:
    st.error("⚠️ Erro: Chave 'URL_PLANILHA_SCRIPT' em falta nos Secrets.")
    st.stop()

# 2. INICIALIZAR O ESTADO DE SESSÃO DO UTILIZADOR
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

# --- CONTROLO DE ACESSO AO ECRÃ ---

if st.session_state["usuario_logado"] is not None:
    # ==========================================
    # ECRÃ PRINCIPAL (APÓS LOGIN EFETUADO)
    # ==========================================
    dados = st.session_state["usuario_logado"]
    
    # Coloca o nome do cliente ACIMA do título do sistema, como solicitado
    st.write(f"✨ Cliente Activo: **{dados.get('nome_exibicao', 'Varão')}**")
    st.title("📸 Social Media Content Master")
    
    # Botão para Sair do Aplicativo
    if st.button("🚪 Sair do Aplicativo"):
        st.session_state["usuario_logado"] = None
        st.rerun() # Atualiza o ecrã para voltar ao login imediatamente
        
    st.divider()
    
    # --- AQUI SEGUE A SUA ÁREA DE GERAÇÃO DE IMAGENS E LEGENDAS ---
    st.write("### 🚀 Painel de Criação")
    st.write(f"Nicho de Atuação: {dados.get('nicho')}")
    
    # O DNA (Coluna D) e a API Key (Coluna F) já estão guardados em:
    # dados.get('dna') e dados.get('api_key_user') prontos para usar no Gemini!

else:
    # ==========================================
    # ECRÃ DE LOGIN (SE NÃO ESTIVER LOGADO)
    # ==========================================
    st.title("🔑 Social Media Content Master - Login")
    
    with st.form("formulario_login"):
        usuario_input = st.text_input("Usuário / E-mail")
        senha_input = st.text_input("Senha", type="password")
        botao_entrar = st.form_submit_button("Entrar no Sistema")
        
        if botao_entrar:
            if usuario_input.strip() and senha_input.strip():
                with st.spinner("A validar credenciais na base de dados..."):
                    try:
                        # Monta o pacote com o formato exato que o seu doPost(e) espera
                        payload = {
                            "username": usuario_input.strip(),
                            "password": senha_input.strip()
                        }
                        
                        # Faz a chamada HTTP POST para a Web App do Google Apps Script
                        resposta = requests.post(SCRIPT_URL, json=payload)
                        
                        if resposta.status_code == 200:
                            resultado_servidor = resposta.json()
                            
                            # Valida o status retornado pelo seu script da planilha
                            if resultado_servidor.get("status") == "success":
                                # Salva o dicionário completo retornado (Nome, DNA, Chave API) na sessão
                                st.session_state["usuario_logado"] = resultado_servidor
                                st.success("Bênção! Login efetuado com sucesso!")
                                st.rerun() # Força o Streamlit a redesenhar o ecrã já autenticado
                            else:
                                # Mostra a mensagem de erro da planilha ("Credenciais inválidas")
                                mensagem_erro = resultado_servidor.get("message", "Acesso negado.")
                                st.error(f"❌ Erro: {mensagem_erro}")
                        else:
                            st.error(f"Falha de comunicação com o servidor Google (Código: {resposta.status_code})")
                            
                    except Exception as e:
                        st.error(f"Erro crítico ao processar o login: {e}")
            else:
                st.warning("Por favor, preencha os campos de Usuário e Senha.")
