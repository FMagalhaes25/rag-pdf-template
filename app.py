import streamlit as st

from main import responder


st.set_page_config(
    page_title="Pergunte à sua base de dados!",
    page_icon="📂",
    layout="centered",
)

st.title("Pergunte aos seus documentos")
st.caption("Faça uma pergunta e receba uma resposta baseada nos PDFs da pasta base.")

pergunta = st.text_area(
    "Pergunta",
    placeholder="Ex.: Quais são os principais pontos do documento?",
    height=120,
)

if st.button("Buscar resposta", type="primary", disabled=not pergunta.strip(), use_container_width=True):
    with st.spinner("Consultando a base e gerando a resposta..."):
        try:
            resultado = responder(pergunta.strip())
        except Exception as erro:
            st.error(f"Não foi possível consultar a base: {erro}")
        else:
            st.subheader("Resposta")
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