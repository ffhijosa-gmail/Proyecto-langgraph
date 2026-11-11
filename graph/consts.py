"""Constantes de nombres de nodos usadas en la definición del grafo RAG.

Se centralizan aquí los identificadores de cada nodo para evitar errores de escritura
y facilitar su reutilización en la construcción del grafo.
"""

RETRIEVE = "retrieve"  # Nombre canónico del nodo de recuperación de documentos
GRADE_DOCUMENTS = "grade_documents"  # Nombre canónico del nodo que filtra documentos por relevancia
GENERATE = "generate"  # Nombre canónico del nodo que genera la respuesta final
WEBSEARCH = "websearch"  # Nombre canónico del nodo que realiza búsqueda web
