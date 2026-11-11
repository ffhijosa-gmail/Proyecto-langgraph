"""Definición del grafo RAG completo usando LangGraph.

Este script:
- Define funciones de enrutado y decisión (router, chequeo de alucinaciones, etc.).
- Declara los nodos del grafo y cómo se conectan entre sí.
- Compila el workflow a una app ejecutable y genera un diagrama (`graph.png`) del flujo.
"""

from dotenv import load_dotenv  # Carga variables de entorno necesarias (por ejemplo, claves de APIs)
from langgraph.graph import END, StateGraph  # Primitivas principales para definir el grafo de estado

from graph.chains.answer_grader import answer_grader  # Cadena que evalúa si la respuesta atiende la pregunta
from graph.chains.hallucination_grader import (  # Cadena que evalúa si la respuesta está apoyada en los documentos
    hallucination_grader,
)
from graph.chains.router import RouteQuery, question_router  # Cadena que decide a qué fuente enviar la pregunta
from graph.consts import GENERATE, GRADE_DOCUMENTS, RETRIEVE, WEBSEARCH  # Constantes con nombres de nodos
from graph.nodes import generate, grade_documents, retrieve, web_search  # Funciones que implementan cada nodo
from graph.state import GraphState  # Tipo que representa el estado compartido entre nodos

load_dotenv()  # Carga las variables de entorno desde el archivo .env


def decide_to_generate(state: GraphState) -> str:
    """Decide si, tras filtrar documentos, se debe generar ya o lanzar búsqueda web adicional."""
    print("---VALORANDO DOCUMENTOS FILTRADOS---")  # Traza para indicar el punto de decisión

    if state["web_search"]:  # Si el nodo de grading marcó que hace falta más búsqueda
        print(
            "---DECISIÓN: NO TODOS LOS DOCUMENTOS SON RELEVANTES, ACTIVAR BÚSQUEDA WEB---"
        )
        return WEBSEARCH  # Dirige el flujo al nodo de búsqueda web
    else:  # Si los documentos actuales se consideran suficientes
        print("---DECISIÓN: GENERAR---")
        return GENERATE  # Dirige el flujo al nodo de generación


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    """Evalúa si la generación está anclada en los documentos y si responde bien a la pregunta."""
    print("---CHEQUEO ALUCINACIONES---")  # Traza para indicar que se comprueban alucinaciones
    question = state["question"]  # Pregunta original
    documents = state["documents"]  # Documentos de contexto usados
    generation = state["generation"]  # Respuesta generada por el LLM

    score = hallucination_grader.invoke(  # Evalúa si la respuesta está apoyada en los documentos
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:  # Si se considera que la respuesta está bien fundada
        print("---DECISIÓN: GENERACIÓN FUNDAMENTADA EN DOCUMENTOS---")
        print("---VALORACIÓN GENERACIÓN vs PREGUNTA---")  # Ahora se evalúa si responde a la pregunta
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:  # Si atiende bien la pregunta
            print("---DECISIÓN: GENERACIÓN RESPONDE CORRECTAMENTE A LA PREGUNTA---")
            return "útil"  # Marca la generación como útil
        else:  # Si no responde adecuadamente a la pregunta
            print("---DECISIÓN: GENERACIÓN NO RESPONDE CORRECTAMENTE A LA PREGUNTA---")
            return "inútil"  # Indica que no es útil y se deberá buscar más
    else:  # Si la respuesta no está bien anclada en los documentos (potencial alucinación)
        print("---DECISIÓN: GENERACIÓN NO FUNDAMENTADA EN DOCUMENTOS, REINTENTANDO---")
        return "sin soporte"  # Indica que debe reintentarse la generación


def route_question(state: GraphState) -> str:
    """Decide la ruta inicial de la pregunta: vector store (RAG) o búsqueda web directa."""
    print("---ENRUTANDO PREGUNTA---")  # Traza para indicar el enrutado de la pregunta
    question = state["question"]  # Extrae la pregunta del estado
    source: RouteQuery = question_router.invoke({"question": question})  # Llama al router para decidir la fuente
    if source.datasource == WEBSEARCH:  # Si la fuente recomendada es web search
        print("---ENRUTANDO A BÚSQUEDA WEB---")
        return WEBSEARCH  # Ruta de entrada: nodo de búsqueda web
    elif source.datasource == "vectorstore":  # Si se debe usar el vector store (RAG clásico)
        print("---ENRUTANDO A RAG---")
        return RETRIEVE  # Ruta de entrada: nodo de recuperación de documentos


workflow = StateGraph(GraphState)  # Crea el grafo de estado parametrizado por GraphState

workflow.add_node(RETRIEVE, retrieve)  # Registra el nodo de recuperación con su identificador
workflow.add_node(GRADE_DOCUMENTS, grade_documents)  # Nodo de filtrado de documentos
workflow.add_node(GENERATE, generate)  # Nodo de generación de respuesta
workflow.add_node(WEBSEARCH, web_search)  # Nodo de búsqueda web

workflow.set_conditional_entry_point(  # Define cómo se entra al grafo dependiendo de la pregunta
    route_question,  # Función que decide la ruta inicial
    {
        WEBSEARCH: WEBSEARCH,  # Si route_question devuelve WEBSEARCH, entra por el nodo de web search
        RETRIEVE: RETRIEVE,  # Si devuelve RETRIEVE, entra por el nodo de recuperación
    },
)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)  # Tras recuperar documentos, se pasan al nodo de grading
workflow.add_conditional_edges(  # Desde el nodo de grading se decide si ir a generar o a web search
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEBSEARCH: WEBSEARCH,  # Si decide buscar en web, va al nodo de web search
        GENERATE: GENERATE,  # Si decide generar, va al nodo de generación
    },
)

workflow.add_conditional_edges(  # Desde generación se revisa si la respuesta es válida o hay que reintentar
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "sin soporte": GENERATE,  # Si no está bien anclada, se reintenta generación
        "útil": END,  # Si es útil, se termina el flujo
        "inútil": WEBSEARCH,  # Si no responde bien, se amplía contexto con búsqueda web
    },
)
workflow.add_edge(WEBSEARCH, GENERATE)  # Tras búsqueda web, se vuelve a generar
workflow.add_edge(GENERATE, END)  # Camino directo de generación a fin (cuando no se revisa/reenruta)

app = workflow.compile()  # Compila la definición del workflow en una aplicación ejecutable

app.get_graph().draw_mermaid_png(output_file_path="graph.png")  # Dibuja y guarda el grafo en formato imagen
