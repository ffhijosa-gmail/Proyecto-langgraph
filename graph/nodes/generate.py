"""Nodo de generación del grafo RAG que crea la respuesta final del LLM.

Este script:
- Recibe del estado la pregunta del usuario y los documentos de contexto.
- Llama a `generation_chain` (prompt + LLM + parser) para producir la respuesta.
- Devuelve en el estado la generación junto con la pregunta y los documentos.
"""

from typing import Any, Dict  # Tipos genéricos para describir el diccionario devuelto

from graph.chains.generation import generation_chain  # Cadena de generación RAG definida en el módulo de chains
from graph.state import GraphState  # Tipo que representa el estado compartido del grafo


def generate(state: GraphState) -> Dict[str, Any]:
    """Genera una respuesta del LLM usando la pregunta y los documentos del estado como contexto."""
    print("---GENERAR RESULTADO---")  # Traza para indicar que se está ejecutando el nodo de generación
    question = state["question"]  # Extrae la pregunta original del estado
    documents = state["documents"]  # Extrae los documentos que servirán de contexto para la respuesta

    generation = generation_chain.invoke(  # Ejecuta la cadena de generación con contexto y pregunta
        {"context": documents, "question": question}
    )
    return {  # Devuelve el nuevo fragmento de estado incluyendo la generación producida
        "documents": documents,
        "question": question,
        "generation": generation,
    }
