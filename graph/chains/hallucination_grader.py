"""
Nodo evaluador de alucinaciones en un flujo RAG.

Este script define:
- Un modelo estructurado (`GradeHallucinations`) para evaluar si una respuesta
  generada por un LLM está fundamentada en documentos recuperados.
- Un prompt que instruye al modelo para actuar como evaluador.
- Una secuencia ejecutable (`hallucination_grader`) que combina prompt + LLM
  con salida estructurada para producir una evaluación binaria.
"""

from langchain_core.prompts import ChatPromptTemplate  # Permite construir prompts estructurados tipo chat (system/human)
from langchain_core.runnables import RunnableSequence  # Permite encadenar componentes ejecutables en una secuencia
from langchain_openai import ChatOpenAI  # Wrapper de LangChain para utilizar modelos de OpenAI en formato chat
from pydantic import BaseModel, Field  # Librería para definir modelos de datos estructurados y validados


# Instancia del modelo LLM con temperatura 0 para respuestas deterministas
# (se busca consistencia en la evaluación, no creatividad)
llm = ChatOpenAI(model="gpt-5-mini",temperature=0)


class GradeHallucinations(BaseModel):
    """
    Modelo de salida estructurada para evaluar alucinaciones.

    Representa un resultado binario que indica si la respuesta generada
    por el LLM está fundamentada en los hechos proporcionados.
    """

    binary_score: bool = Field(
        description="Indica si la respuesta está fundamentada en los hechos: 'sí' o 'no'"
    )
    # Campo booleano que indica:
    # - True → La respuesta está fundamentada en los documentos.
    # - False → La respuesta contiene alucinaciones o no está soportada.


# Se transforma el LLM para que obligue a devolver una salida estructurada
# que cumpla el esquema definido en GradeHallucinations
structured_llm_grader = llm.with_structured_output(GradeHallucinations)


# Prompt de sistema que define el rol del modelo como evaluador
system = """Eres un evaluador que determina si una respuesta generada por un LLM
está fundamentada o respaldada por un conjunto de hechos recuperados.

Debes devolver una puntuación binaria: 'sí' o 'no'.
'Sí' significa que la respuesta está fundamentada o respaldada por el conjunto de hechos."""


# Construcción del prompt en formato chat
# Incluye:
# - Mensaje de sistema (rol del modelo)
# - Mensaje humano con los documentos recuperados y la respuesta generada
hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Conjunto de hechos:\n\n {documents} \n\n Respuesta generada por el LLM: {generation}"),
    ]
)
# {documents} → Placeholder donde se insertarán los documentos recuperados
# {generation} → Placeholder donde se insertará la respuesta generada por el LLM


# Se construye la secuencia ejecutable:
# 1️⃣ Se formatea el prompt con los datos reales
# 2️⃣ Se pasa el prompt al LLM estructurado
# 3️⃣ Se obtiene una salida validada según el modelo Pydantic
hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader