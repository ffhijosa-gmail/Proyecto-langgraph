"""Nodo del grafo RAG que enriquece el contexto con resultados de búsqueda web.

Este script:
- Configura una herramienta de búsqueda (Tavily) para recuperar información de la web.
- Recibe una pregunta (y opcionalmente documentos previos) desde el estado del grafo.
- Ejecuta una búsqueda, junta los resultados en un único `Document` y lo añade a la lista de documentos.
"""

from typing import Any, Dict  # Tipos genéricos para anotar la estructura del diccionario devuelto

from dotenv import load_dotenv  # Para cargar variables de entorno (por ejemplo, claves de Tavily)
from langchain_core.documents import Document  # Tipo de documento estándar de LangChain (ruta actual en langchain-core)
from langchain_tavily import TavilySearch  # Herramienta de búsqueda web Tavily

from graph.state import GraphState  # Tipo que representa el estado compartido del grafo

load_dotenv()  # Carga las variables de entorno definidas en el archivo .env
web_search_tool = TavilySearch(max_results=3)  # Crea la herramienta de búsqueda, limitada a 3 resultados


def web_search(state: GraphState) -> Dict[str, Any]:
    """Realiza una búsqueda web sobre la pregunta y añade los resultados como documentos al estado."""
    print("---BÚSQUEDA WEB---")  # Traza para indicar que se está ejecutando el nodo de búsqueda web
    question = state["question"]  # Extrae la pregunta del estado
    if "documents" in state:  # Si ya existe una lista de documentos en el estado
        documents = state["documents"]  # Recupera esos documentos para añadir los nuevos resultados
    else:  # En caso contrario (por ejemplo, primera vez que se llama a la búsqueda web)
        documents = None  # Indica que todavía no hay documentos previos

    tavily_results = web_search_tool.invoke({"query": question})["results"]  # Llama a Tavily con la pregunta y recoge los resultados crudos
    joined_tavily_result = "\n".join(  # Une el contenido de todos los resultados en un solo texto
        [tavily_result["content"] for tavily_result in tavily_results]
    )
    web_results = Document(page_content=joined_tavily_result)  # Crea un `Document` de LangChain con el texto combinado
    if documents is not None:  # Si ya había documentos
        documents.append(web_results)  # Añade el nuevo documento con resultados web
    else:  # Si no había documentos previos
        documents = [web_results]  # Inicializa la lista de documentos con el resultado web
    return {"documents": documents, "question": question}  # Devuelve el nuevo fragmento de estado
