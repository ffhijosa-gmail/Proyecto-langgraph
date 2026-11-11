"""Cadena de generación RAG que combina un prompt con un LLM de OpenAI.

Este script:
- Configura un modelo de chat de OpenAI.
- Define `generation_chain`, que toma contexto/pregunta, aplica el prompt, llama al LLM y devuelve solo el texto.
"""

from langchain_core.prompts import ChatPromptTemplate  # en lugar de usar langchain.hub
from langchain_core.output_parsers import StrOutputParser #StrOutputParser() transforma la salida estructurada del modelo en solo el texto con el content de la respuesta del AI message (str).
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5-mini",temperature=0)  # Instancia del LLM de chat, configurado de forma determinista (temperature=0)
prompt = ChatPromptTemplate.from_template(
    """Eres un asistente experto que responde preguntas basándote en los siguientes documentos de contexto.

Contexto:
{context}

Pregunta del usuario:
{question}

Responde de forma clara y concisa en castellano. Si la información no está en el contexto, dilo explícitamente."""
)

generation_chain = prompt | llm | StrOutputParser()  # Pipeline: aplica el prompt, llama al LLM y parsea la salida a string
