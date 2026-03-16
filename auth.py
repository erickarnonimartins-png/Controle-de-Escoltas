import streamlit as st

SENHA_APP = "1234"  # troque pela senha que você quiser


def iniciar_auth():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False


def tela_login():
    st.title("🔐 Acesso ao Sistema")

    with st.form("form_login"):
        senha = st.text_input("Digite a senha", type="password")
        entrar = st.form_submit_button("Entrar")

        if entrar:
            if senha == SENHA_APP:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Senha incorreta.")

    st.stop()


def exigir_login():
    iniciar_auth()

    if not st.session_state.autenticado:
        tela_login()


def botao_sair():
    if st.sidebar.button("🚪 Sair"):
        st.session_state.autenticado = False
        st.rerun()