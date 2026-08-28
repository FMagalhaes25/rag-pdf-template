import streamlit as st

from main import responder


st.set_page_config(
    page_title="Pergunte à sua base de dados!",
    page_icon="📂",
    layout="centered",
)

st.title("Pergunte aos seus documentos")
st.caption("Faça uma pergunta e receba uma resposta baseada nos PDFs da pasta base.")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for mensagem in st.session_state.mensagens:
    avatar = "🤖" if mensagem["role"] == "assistant" else None
    with st.chat_message(mensagem["role"], avatar=avatar):
        st.write(mensagem["resposta"])

        if mensagem["role"] == "assistant" and mensagem.get("fontes"):
            with st.expander("Ver fontes consultadas"):
                for fonte in mensagem["fontes"]:
                    pagina = fonte["pagina"]
                    pagina_texto = f", página {pagina + 1}" if pagina is not None else ""
                    st.write(
                        f"- `{fonte['arquivo']}`{pagina_texto} "
                        f"(relevância: {fonte['relevancia']:.2f})"
                    )

pergunta = st.chat_input("Ex.: Quais são os principais pontos do documento?")

if pergunta and pergunta.strip():
    pergunta = pergunta.strip()
    st.session_state.mensagens.append({"role": "user", "resposta": pergunta})

    with st.chat_message("user"):
        st.write(pergunta)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Consultando a base e gerando a resposta..."):
            try:
                resultado = responder(pergunta)
            except Exception as erro:
                resposta = f"Não foi possível consultar a base: {erro}"
                st.error(resposta)
                resultado = {"resposta": resposta, "fontes": []}
            else:
                st.write(resultado["resposta"])

                if resultado["fontes"]:
                    with st.expander("Ver fontes consultadas"):
                        for fonte in resultado["fontes"]:
                            pagina = fonte["pagina"]
                            pagina_texto = f", página {pagina + 1}" if pagina is not None else ""
                            st.write(
                                f"- `{fonte['arquivo']}`{pagina_texto} "
                                f"(relevância: {fonte['relevancia']:.2f})"
                            )

    st.session_state.mensagens.append(
        {
            "role": "assistant",
            "resposta": resultado["resposta"],
            "fontes": resultado["fontes"],
        }
    )