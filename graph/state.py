"""Definición del estado compartido que usa el grafo RAG para pasar información entre nodos."""

from typing import List, TypedDict  # Importa tipos para anotar listas y diccionarios tipados


class GraphState(TypedDict):  # Declara un tipo de diccionario tipado que representa el estado del grafo
    """
    Representa el estado de nuestro grafo de RAG.

    Atributos:
        question: pregunta original del usuario.
        generation: respuesta generada por el LLM.
        web_search: indica si se debe realizar o se ha realizado búsqueda web adicional.
        documents: lista de documentos (o fragmentos) relevantes recuperados.
    """

    question: str  # Texto de la pregunta que hace el usuario
    generation: str  # Texto de la respuesta generada por el modelo
    web_search: bool  # Bandera booleana para activar o reflejar uso de búsqueda web
    documents: List[str]  # Lista de documentos o chunks de texto que alimentan la respuesta
