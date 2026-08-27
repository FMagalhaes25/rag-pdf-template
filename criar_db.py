import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

PASTA_BASE = "base"

def criar_db():
    # carregar documentos
    documentos = carregar_documentos()
    # dividir os documentos em pedaçõs de texto (chunks)
    chunks = dividir_chunks(documentos)
    # vetorizar os chunks com o processo de embedding
    vetorizar_chunks(chunks)

def carregar_documentos():
    carregador_docs = PyPDFDirectoryLoader(PASTA_BASE, glob="*.pdf") #Por padrão lê pdf, porém declarei
    documentos = carregador_docs.load()
    return documentos

def dividir_chunks(documentos):
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500, #Sobreposição de um chunk para preservar o contexto
        length_function=len,
        add_start_index=True #caractere inicial de cada chunk
    )
    chunks = separador_documentos.split_documents(documentos)
    #print(len(chunks))
    return chunks

def vetorizar_chunks(chunks):
    db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="db")
    #print("Banco de dados criado")

criar_db()