# Script para ingesta de documentos en la base de datos vectorial y consulta posterior (retrieval)

# 1. Importaciones
#--------------------------------------------------------------------------------
from dotenv import load_dotenv  # Importa la función para cargar variables de entorno desde un archivo .env
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter  # Importa el divisor de texto que trocea documentos en chunks
from langchain_chroma import Chroma  # Importa la clase Chroma, el vector store basado en ChromaDB

from langchain_openai import OpenAIEmbeddings  # Importa la clase que genera embeddings usando modelos de OpenAI

load_dotenv()  # Carga en memoria las variables definidas en el archivo .env (por ejemplo, la API key de OpenAI)

# 2. Lectura del fichero de datos 
#--------------------------------------------------------------------------
# Construye la ruta hacia el archivo Markdown dentro de la carpeta "Datasets RAG"
md_path = Path("Datasets RAG") / "EV_documentación_técnica.md"  

# Lee el contenido completo del archivo Markdown como texto UTF-8
md_text = md_path.read_text(encoding="utf-8")  


# 3. SPLIT SEMÁNTICO POR ENCABEZADOS MARKDOWN
# -------------------------------------------------------

# Crea el splitter que divide el documento según niveles de encabezado
# Cada nivel se almacenará como metadata (h1, h2, h3)
header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "h1"),    # Divide por encabezados principales
        ("##", "h2"),   # Divide por secciones
        ("###", "h3"),  # Divide por subsecciones
    ]
)

# Aplica el split semántico al texto Markdown. Devuelve una lista de Document con metadata estructurada
docs_by_header = header_splitter.split_text(md_text)


# 4. CHUNKING ADICIONAL POR TAMAÑO (OPTIMIZADO PARA EMBEDDINGS)
# -------------------------------------------------------

# Crea un splitter basado en tokens usando el encoder de tiktoken
# chunk_size define el tamaño máximo por fragmento
# chunk_overlap mantiene continuidad semántica entre fragmentos
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=400,     # Tamaño recomendado para documentación técnica
    chunk_overlap=50,   # Solapamiento para mejorar coherencia en retrieval
)

# Aplica el chunking adicional sobre los documentos ya divididos por encabezado
doc_splits = text_splitter.split_documents(docs_by_header)


# 5. CREACIÓN DEL VECTOR STORE PERSISTENTE (EJECUTAR UNA SOLA VEZ)
# -------------------------------------------------------
vectorstore = Chroma.from_documents(
    documents=doc_splits,                # Lista final de chunks listos para embedding
    collection_name="rag-chroma",        # Nombre lógico de la colección
    embedding=OpenAIEmbeddings(),        # Modelo de embeddings de OpenAI
    persist_directory="./.chroma",       # Carpeta donde se guarda la base vectorial
)


# 6. Recuperación de datos desde la base de datos vectorial cuando se realicen consultas
# # Convierte el vector store en un retriever de alto nivel para búsqueda semántica
#-----------------------------------------------------------------
retriever = Chroma(  # Inicializa un vector store Chroma existente para poder recuperar documentos
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(),
).as_retriever(search_kwargs={"k": 3})   # Máximo número de documentos a devolver = 3 (defecto 4)
 
