from dotenv import load_dotenv

load_dotenv()

#from graph.graph_v1 import app #Importación de grafo RAG sencillo
from graph.graph_v2 import app #Importación de grafo RAG complejo

if __name__ == "__main__":
    print("Hola Agente RAG")
    print(app.invoke(input={"question": "¿Qué potencia máxima DC tiene el cargador?"}))
