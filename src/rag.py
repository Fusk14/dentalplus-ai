
from pathlib import Path
import faiss

from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings



BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "data" / "documentos"

MODELO_EMBEDDINGS = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def cargar_documentos():
    loader = DirectoryLoader(
        str(DOCS_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=False,
    )

    documentos = loader.load()

    if not documentos:
        raise ValueError("No se encontraron documentos de DentalPlus.")

    return documentos


def dividir_documentos(documentos):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return splitter.split_documents(documentos)


def crear_vectorstore():
    documentos = cargar_documentos()
    fragmentos = dividir_documentos(documentos)

    embeddings = HuggingFaceEmbeddings(
        model_name=MODELO_EMBEDDINGS,
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    dimension = len(
        embeddings.embed_query("texto de prueba")
    )

    vectorstore = FAISS(
        embedding_function=embeddings,
        index=faiss.IndexFlatIP(dimension),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
        distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT,
    )

    vectorstore.add_documents(fragmentos)

    return vectorstore



def buscar_informacion(
    vectorstore,
    consulta,
    k=3,
    umbral=0.30
):
    resultados = (
        vectorstore.similarity_search_with_score(
            consulta,
            k=k
        )
    )

    documentos_relevantes = []

    for doc, score in resultados:

        similitud = float(score)

        if similitud >= umbral:
            documentos_relevantes.append({
                "fuente": Path(
                    doc.metadata["source"]
                ).name,
                "contenido": doc.page_content,
                "similitud": round(similitud, 3)
            })

    return documentos_relevantes
