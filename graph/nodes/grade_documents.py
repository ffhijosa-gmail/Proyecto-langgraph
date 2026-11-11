"""Nodo del grafo RAG encargado de filtrar documentos por relevancia.

Este script:
- Recibe del estado una pregunta y una lista de documentos recuperados.
- Usa `retrieval_grader` para evaluar si cada documento es relevante para la pregunta.
- Devuelve solo los documentos relevantes y una bandera `web_search` que indica si hace falta buscar más.
"""

from typing import Any, Dict  # Tipos genéricos para anotar la estructura del diccionario devuelto

from graph.chains.retrieval_grader import retrieval_grader  # Cadena LLM que puntúa la relevancia de un documento
from graph.state import GraphState  # Tipo que define la estructura del estado compartido del grafo


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """Evalúa la relevancia de cada documento respecto a la pregunta y filtra los irrelevantes."""

    print("---CHEQUEO DE RELEVANCIA CON LA PREGUNTA---")  # Traza para indicar que se está comprobando la relevancia
    question = state["question"]  # Extrae la pregunta del estado
    documents = state["documents"]  # Extrae la lista de documentos recuperados

    filtered_docs = []  # Lista donde se acumularán solo los documentos relevantes
    web_search = False  # Bandera que marcará si es necesario lanzar una búsqueda web adicional
    for d in documents:  # Recorre cada documento recuperado
        score = retrieval_grader.invoke(  # Invoca la cadena de evaluación con la pregunta y el contenido del documento
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score  # Extrae la puntuación binaria ('sí' o 'no') de relevancia
        if grade.lower() in ("yes", "sí"):  # Si el documento se considera relevante
            print("---EVALUACIÓN: DOCUMENTO RELEVANTE---")  # Mensaje de traza indicando relevancia
            filtered_docs.append(d)  # Añade el documento a la lista filtrada
        else:  # Si el documento no es relevante
            print("---EVALUACIÓN: DOCUMENTO NO RELEVANTE---")  # Mensaje de traza indicando irrelevancia
            web_search = True  # Activa la bandera para indicar que quizá haga falta una nueva búsqueda
            continue  # Pasa al siguiente documento
    return {  # Devuelve el nuevo fragmento de estado con documentos filtrados, pregunta y la bandera de búsqueda web
        "documents": filtered_docs,
        "question": question,
        "web_search": web_search,
    }
