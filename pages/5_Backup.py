import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Backup", page_icon="💾")
st.title("💾 Backup do Banco de Dados")

DB_PATH = Path("data") / "escolta.db"

st.write("Aqui você pode baixar uma cópia completa do banco de dados do sistema.")

if DB_PATH.exists():
    tamanho_bytes = DB_PATH.stat().st_size
    ultima_modificacao = datetime.fromtimestamp(DB_PATH.stat().st_mtime)

    tamanho_kb = round(tamanho_bytes / 1024, 2)
    tamanho_mb = round(tamanho_bytes / (1024 * 1024), 2)

    c1, c2, c3 = st.columns(3)
    c1.metric("Arquivo", DB_PATH.name)
    c2.metric("Tamanho", f"{tamanho_kb} KB")
    c3.metric("Última atualização", ultima_modificacao.strftime("%d/%m/%Y %H:%M:%S"))

    st.divider()

    with open(DB_PATH, "rb") as f:
        db_bytes = f.read()

    nome_backup = f'escolta_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'

    st.download_button(
        label="📥 Baixar backup do banco",
        data=db_bytes,
        file_name=nome_backup,
        mime="application/octet-stream",
        use_container_width=True
    )

    st.divider()

    st.subheader("Informações importantes")
    st.write("- Esse arquivo contém todos os agentes, rotas e lançamentos.")
    st.write("- Guarde esse backup em local seguro.")
    st.write("- Faça backup sempre antes de alterações importantes no sistema.")
else:
    st.error("O arquivo do banco de dados não foi encontrado em data\\escolta.db")