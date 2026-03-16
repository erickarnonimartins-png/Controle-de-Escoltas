import streamlit as st
from db import get_connection

st.set_page_config(page_title="Rotas", page_icon="🛣️")
st.title("🛣️ Cadastro de Rotas")


def carregar_rotas():
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT id, nome_rota, origem, destino, valor_fixo_receber,
               valor_fixo_pagar, observacao, ativa
        FROM rotas
        ORDER BY nome_rota
    """).fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "nome_rota": row["nome_rota"],
            "origem": row["origem"] or "",
            "destino": row["destino"] or "",
            "valor_fixo_receber": float(row["valor_fixo_receber"] or 0),
            "valor_fixo_pagar": float(row["valor_fixo_pagar"] or 0),
            "observacao": row["observacao"] or "",
            "ativa": row["ativa"],
        }
        for row in rows
    ]


def contar_servicos_da_rota(rota_id):
    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute(
        "SELECT COUNT(*) AS total FROM servicos WHERE rota_id = ?",
        (rota_id,)
    ).fetchone()
    conn.close()
    return int(row["total"] or 0)


rotas = carregar_rotas()
mapa_rotas = {r["id"]: r for r in rotas}

ativas = sum(1 for r in rotas if r["ativa"] == 1)
inativas = sum(1 for r in rotas if r["ativa"] == 0)

m1, m2, m3 = st.columns(3)
m1.metric("Total de rotas", len(rotas))
m2.metric("Ativas", ativas)
m3.metric("Inativas", inativas)

st.divider()

# =========================================================
# NOVA ROTA
# =========================================================
st.subheader("Nova rota")

with st.form("form_nova_rota", clear_on_submit=True):
    nome_rota = st.text_input("Nome da rota")
    origem = st.text_input("Origem")
    destino = st.text_input("Destino")
    valor_fixo_receber = st.number_input(
        "Valor fixo a receber",
        min_value=0.0,
        step=10.0,
        format="%.2f"
    )
    valor_fixo_pagar = st.number_input(
        "Valor fixo a pagar",
        min_value=0.0,
        step=10.0,
        format="%.2f"
    )
    observacao = st.text_area("Observação")
    ativa = st.checkbox("Rota ativa", value=True)

    salvar = st.form_submit_button("Salvar rota")

    if salvar:
        if not nome_rota.strip():
            st.error("Digite o nome da rota.")
        else:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO rotas (
                    nome_rota, origem, destino, valor_fixo_receber,
                    valor_fixo_pagar, observacao, ativa
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    nome_rota.strip(),
                    origem.strip(),
                    destino.strip(),
                    float(valor_fixo_receber),
                    float(valor_fixo_pagar),
                    observacao.strip(),
                    1 if ativa else 0
                )
            )
            conn.commit()
            conn.close()
            st.success("Rota salva com sucesso.")
            st.rerun()

st.divider()

# =========================================================
# EDITAR / EXCLUIR
# =========================================================
st.subheader("Gerenciar rota")

if rotas:
    ids_rotas = [r["id"] for r in rotas]

    rota_id_sel = st.selectbox(
        "Escolha uma rota",
        options=ids_rotas,
        format_func=lambda rid: (
            f'#{mapa_rotas[rid]["id"]} | '
            f'{mapa_rotas[rid]["nome_rota"]} | '
            f'Recebo: R$ {mapa_rotas[rid]["valor_fixo_receber"]:.2f} | '
            f'Pago: R$ {mapa_rotas[rid]["valor_fixo_pagar"]:.2f}'
        )
    )

    rota_sel = mapa_rotas[rota_id_sel]

    aba1, aba2 = st.tabs(["✏️ Editar", "🗑️ Excluir"])

    # -------------------------
    # EDITAR
    # -------------------------
    with aba1:
        with st.form(f"form_editar_rota_{rota_sel['id']}"):
            nome_rota_edit = st.text_input("Nome da rota", value=rota_sel["nome_rota"])
            origem_edit = st.text_input("Origem", value=rota_sel["origem"])
            destino_edit = st.text_input("Destino", value=rota_sel["destino"])
            valor_fixo_receber_edit = st.number_input(
                "Valor fixo a receber",
                min_value=0.0,
                step=10.0,
                format="%.2f",
                value=float(rota_sel["valor_fixo_receber"])
            )
            valor_fixo_pagar_edit = st.number_input(
                "Valor fixo a pagar",
                min_value=0.0,
                step=10.0,
                format="%.2f",
                value=float(rota_sel["valor_fixo_pagar"])
            )
            observacao_edit = st.text_area("Observação", value=rota_sel["observacao"])
            ativa_edit = st.checkbox("Rota ativa", value=(rota_sel["ativa"] == 1))

            salvar_edicao = st.form_submit_button("Salvar alterações")

            if salvar_edicao:
                if not nome_rota_edit.strip():
                    st.error("Digite o nome da rota.")
                else:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute(
                        """
                        UPDATE rotas
                        SET nome_rota = ?, origem = ?, destino = ?,
                            valor_fixo_receber = ?, valor_fixo_pagar = ?,
                            observacao = ?, ativa = ?
                        WHERE id = ?
                        """,
                        (
                            nome_rota_edit.strip(),
                            origem_edit.strip(),
                            destino_edit.strip(),
                            float(valor_fixo_receber_edit),
                            float(valor_fixo_pagar_edit),
                            observacao_edit.strip(),
                            1 if ativa_edit else 0,
                            rota_sel["id"]
                        )
                    )
                    conn.commit()
                    conn.close()
                    st.success("Rota atualizada com sucesso.")
                    st.rerun()

    # -------------------------
    # EXCLUIR
    # -------------------------
    with aba2:
        qtd_servicos = contar_servicos_da_rota(rota_sel["id"])

        if qtd_servicos > 0:
            st.warning(
                f'Essa rota possui {qtd_servicos} serviço(s) vinculado(s). '
                'Por segurança, não exclua. O ideal é marcar como inativa.'
            )

            if st.button("Marcar como inativa", key=f"inativar_rota_{rota_sel['id']}"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "UPDATE rotas SET ativa = 0 WHERE id = ?",
                    (rota_sel["id"],)
                )
                conn.commit()
                conn.close()
                st.success("Rota marcada como inativa.")
                st.rerun()
        else:
            st.warning("A exclusão apaga essa rota do banco de dados.")

            with st.form(f"form_excluir_rota_{rota_sel['id']}"):
                confirmar = st.checkbox(
                    f'Confirmo excluir a rota "{rota_sel["nome_rota"]}"'
                )
                excluir = st.form_submit_button("Excluir rota")

                if excluir:
                    if not confirmar:
                        st.error("Marque a confirmação antes de excluir.")
                    else:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("DELETE FROM rotas WHERE id = ?", (rota_sel["id"],))
                        conn.commit()
                        conn.close()
                        st.success("Rota excluída com sucesso.")
                        st.rerun()
else:
    st.info("Nenhuma rota cadastrada ainda.")

st.divider()

# =========================================================
# LISTAGEM
# =========================================================
st.subheader("Rotas cadastradas")

rotas = carregar_rotas()

if rotas:
    dados = []
    for rota in rotas:
        dados.append({
            "ID": rota["id"],
            "Rota": rota["nome_rota"],
            "Origem": rota["origem"],
            "Destino": rota["destino"],
            "Recebo Fixo": f'R$ {rota["valor_fixo_receber"]:.2f}',
            "Pago Fixo": f'R$ {rota["valor_fixo_pagar"]:.2f}',
            "Observação": rota["observacao"],
            "Status": "Ativa" if rota["ativa"] == 1 else "Inativa"
        })

    st.dataframe(dados, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma rota cadastrada ainda.")