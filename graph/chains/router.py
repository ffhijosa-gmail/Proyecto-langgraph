from typing import Literal  # Importa Literal para restringir valores posibles a un conjunto cerrado

from langchain_core.prompts import ChatPromptTemplate  # Importa la clase para construir prompts estructurados para modelos de chat
from langchain_openai import ChatOpenAI  # Importa el wrapper del modelo de OpenAI para usarlo dentro de LangChain
from pydantic import BaseModel, Field  # Importa BaseModel para definir esquemas estructurados y Field para añadir metadatos


class RouteQuery(BaseModel):  # Define un modelo estructurado que representa la decisión de enrutamiento
    """Enruta una consulta del usuario hacia la fuente de datos más relevante."""  # Docstring traducido al castellano

    datasource: Literal["vectorstore", "websearch"] = Field(  # Define el campo datasource limitado a dos valores posibles
        ...,  # Indica que este campo es obligatorio
        description="Dada una pregunta del usuario, elige si debe enviarse a búsqueda web o a una base de datos vectorial.",  # Descripción traducida
    )


llm = ChatOpenAI(model="gpt-5-mini", temperature=0)  # Inicializa el modelo con temperatura 0 para hacerlo determinista
structured_llm_router = llm.with_structured_output(RouteQuery)  # Configura el modelo para que devuelva una salida estructurada según el esquema RouteQuery


system = """Eres un experto en decidir si una pregunta debe enviarse a una base de datos vectorial o a una búsqueda web.
La base de datos vectorial contiene documentos relacionados con documentación técnica de cargadores de vehículos eléctricos (EV).
Utiliza la base de datos vectorial para preguntas sobre estos temas. Para cualquier otro caso, utiliza búsqueda web."""  # Prompt del sistema traducido al castellano

route_prompt = ChatPromptTemplate.from_messages(  # Crea una plantilla de prompt basada en mensajes tipo chat
    [
        ("system", system),  # Mensaje de sistema que define el comportamiento del modelo
        ("human", "{question}"),  # Mensaje del usuario donde {question} será reemplazado dinámicamente
    ]
)

question_router = route_prompt | structured_llm_router  # Encadena el prompt con el modelo estructurado usando LCEL