"""Nodo de recuperación de documentos del grafo RAG.

Este script define la función `retrieve`, responsable de:
- Leer la pregunta actual del estado del grafo.
- Invocar al `retriever` definido en `ingestion.py` para obtener documentos relevantes.
- Devolver un nuevo fragmento de estado con la pregunta y los documentos recuperados.
"""

from typing import Any, Dict  # Tipos genéricos para el diccionario de salida

from graph.state import GraphState  # Tipo que representa el estado compartido del grafo
from ingestion import retriever  # Objeto retriever construido a partir del vector store de Chroma


def retrieve(state: GraphState) -> Dict[str, Any]:
    """Recupera documentos relevantes para la pregunta presente en el estado."""
    print("---RECUPERACIÓN---")  # Mensaje de traza para identificar cuándo se ejecuta este nodo
    question = state["question"]  # Extrae la pregunta del estado de entrada

    documents = retriever.invoke(question)  # Llama al retriever para obtener documentos relevantes a la pregunta
    return {"documents": documents, "question": question}  # Devuelve un diccionario parcial de estado con pregunta y documentos

