"""
Nodo evaluador de calidad de respuesta en un flujo RAG.

Este script define:
- Un modelo estructurado (`GradeAnswer`) para evaluar si una respuesta
  generada por un LLM resuelve correctamente una pregunta.
- Un prompt que instruye al modelo para actuar como evaluador.
- Una secuencia ejecutable (`answer_grader`) que combina prompt + LLM
  con salida estructurada para producir una evaluación binaria.
"""

from langchain_core.prompts import ChatPromptTemplate  # Permite construir prompts estructurados tipo chat (system/human)
from langchain_core.runnables import RunnableSequence  # Permite encadenar componentes ejecutables en una secuencia
from langchain_openai import ChatOpenAI  # Wrapper de LangChain para utilizar modelos de OpenAI en formato chat
from pydantic import BaseModel, Field  # Librería para definir modelos de datos estructurados y validados


class GradeAnswer(BaseModel):
    """
    Modelo de salida estructurada para evaluar si una respuesta
    resuelve correctamente una pregunta.
    """

    binary_score: bool = Field(
        description="Indica si la respuesta aborda y resuelve la pregunta: 'sí' o 'no'"
    )
    # Campo booleano que indica:
    # - True → La respuesta resuelve la pregunta.
    # - False → La respuesta no responde adecuadamente.


# Instancia del modelo LLM con temperatura 0 para garantizar evaluación determinista
llm = ChatOpenAI(model="gpt-5-mini",temperature=0)


# Se transforma el LLM para que obligue a devolver una salida estructurada
# que cumpla el esquema definido en GradeAnswer
structured_llm_grader = llm.with_structured_output(GradeAnswer)


# Prompt de sistema que define el rol del modelo como evaluador
system = """Eres un evaluador que determina si una respuesta
aborda y resuelve correctamente una pregunta.

Debes devolver una puntuación binaria: 'sí' o 'no'.
'Sí' significa que la respuesta resuelve la pregunta."""


# Construcción del prompt en formato chat
# Incluye:
# - Mensaje de sistema (rol del modelo)
# - Mensaje humano con la pregunta del usuario y la respuesta generada
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Pregunta del usuario:\n\n {question} \n\n Respuesta generada por el LLM: {generation}"),
    ]
)
# {question} → Placeholder donde se insertará la pregunta original
# {generation} → Placeholder donde se insertará la respuesta generada por el modelo


# Se construye la secuencia ejecutable:
# 1️⃣ Se formatea el prompt con la pregunta y la respuesta real
# 2️⃣ Se pasa el prompt al LLM estructurado
# 3️⃣ Se obtiene una salida validada según el modelo Pydantic
answer_grader: RunnableSequence = answer_prompt | structured_llm_grader