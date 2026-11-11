"""Cadena LLM que actúa como “juez” de relevancia de documentos recuperados.

Este script construye un pequeño pipeline que:
- Define un modelo Pydantic `GradeDocuments` para representar una evaluación binaria.
- Configura un LLM de chat de OpenAI.
- Crea un prompt de sistema/humano que describe la tarea de evaluar relevancia.
- Encapsula todo en `retrieval_grader`, que recibe documento y pregunta, y devuelve 'yes' o 'no'.
"""

from langchain_core.prompts import ChatPromptTemplate  # Para definir plantillas de prompts de chat
from langchain_openai import ChatOpenAI  # Cliente de modelo de chat de OpenAI
from pydantic import BaseModel, Field  # Base para modelos de datos tipados y metadatos de campos

llm = ChatOpenAI(model="gpt-5-mini",temperature=0)  # Instancia del LLM de chat, determinista (temperature=0)


class GradeDocuments(BaseModel):  # Modelo que define la estructura de la salida del evaluador
    """Puntúa binariamente si un documento es relevante para la pregunta."""

    binary_score: str = Field(  # Campo que contendrá 'sí' o 'no'
        description="Decide si los documentos son relevantes para la pregunta: 'sí' o 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)  # Envuelve el LLM para que devuelva instancias de GradeDocuments

system = """Eres un evaluador que analiza la relevancia de un documento recuperado respecto a la pregunta de un usuario. \n 
    Si el documento contiene palabra(s) clave o significado semántico relacionado con la pregunta, márcalo como relevante. \n
    Devuelve una puntuación binaria 'sí' o 'no' para indicar si el documento es relevante para la pregunta."""  # Instrucciones al modelo sobre cómo evaluar
grade_prompt = ChatPromptTemplate.from_messages(  # Construye el prompt de chat a partir de mensajes de sistema y humano
    [
        ("human", "Documento recuperado: \n\n {document} \n\n Pregunta del usuario: {question}"),  # Mensaje humano con el documento y la pregunta
        ("system", system),  # Mensaje de sistema con las reglas de evaluación
    ]
)  # Cierra la definición de la plantilla de prompt

retrieval_grader = grade_prompt | structured_llm_grader  # Pipeline: primero se formatea el prompt y luego se pasa al LLM estructurado
