"""Punto de entrada del paquete `nodes` con los nodos principales del grafo RAG.

Este archivo:
- Importa las funciones de cada nodo (`generate`, `grade_documents`, `retrieve`, `web_search`).
- Expone explícitamente esos nombres en `__all__` para facilitar su importación desde otros módulos.
"""

from graph.nodes.generate import generate  # Nodo que genera la respuesta final del LLM
from graph.nodes.grade_documents import grade_documents  # Nodo que filtra documentos por relevancia
from graph.nodes.retrieve import retrieve  # Nodo que recupera documentos desde el vector store
from graph.nodes.web_search import web_search  # Nodo que amplía el contexto con búsqueda web

__all__ = ["generate", "grade_documents", "retrieve", "web_search"]  # Exporta públicamente los nodos disponibles en el paquete
