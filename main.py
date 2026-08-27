from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

CAMINHO_DB = str(Path(__file__).parent / "db")

prompt_template = """
Responda a pergunta do usuário: 
{pergunta}

com base nessas informações abaixo:
{base_conhecimento}"""

def responder(pergunta):
    """Busca contexto relevante e gera uma resposta baseada nele."""
    # carregar o banco de dados
    funcao_embedding = OpenAIEmbeddings()
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)

    # comparar pergunta do usuario (embedding) com o meu banco de dados
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)

    if len(resultados) == 0 or resultados[0][1] < 0.7:
        return {
            "resposta": "Não encontrei informação relevante na base de conhecimento.",
            "fontes": [],
        }
    
    texts_resultado = []
    for resultado in resultados:
        texto = resultado[0].page_content
        texts_resultado.append(texto)
        
    base_conhecimento = "\n\n-----\n\n".join(texts_resultado)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt.invoke({"pergunta": pergunta, "base_conhecimento": base_conhecimento})
    #print(prompt)
    
    modelo = ChatOpenAI()
    texto_resposta = modelo.invoke(prompt).content
    fontes = [
        {
            "arquivo": Path(resultado[0].metadata.get("source", "desconhecido")).name,
            "pagina": resultado[0].metadata.get("page"),
            "relevancia": resultado[1],
        }
        for resultado in resultados
    ]
    return {"resposta": texto_resposta, "fontes": fontes}


def perguntar():
    pergunta = input("Escreva sua pergunta: ")
    resultado = responder(pergunta)
    print("Resposta da IA:", resultado["resposta"])
    

if __name__ == "__main__":
    perguntar()