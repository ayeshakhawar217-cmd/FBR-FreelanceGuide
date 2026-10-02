from pathlib import Path
import os

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_PATH = PROJECT_ROOT / "chroma_db"


# Use the existing D: drive cache locally.
# On Render/Linux, use a project-local cache directory.
if os.name == "nt":
    MODEL_PATH = Path(
        r"D:\FBR-FreelanceGuide-Cache\models"
    ) / "all-MiniLM-L6-v2"
else:
    MODEL_PATH = PROJECT_ROOT / ".cache" / "models" / "all-MiniLM-L6-v2"


class LocalEmbeddingFunction:
    """
    Generates embeddings locally using Sentence Transformers.

    On Windows development:
        D:\\FBR-FreelanceGuide-Cache\\models

    On Render/Linux:
        project/.cache/models
    """

    def __init__(self):
        print("Loading embedding model...")

        MODEL_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            cache_folder=str(MODEL_PATH),
        )

        print("Embedding model loaded.")

    def __call__(self, input):
        return self.embed_documents(input)

    def embed_documents(self, input):
        embeddings = self.model.encode(
            input,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_query(self, input):
        embeddings = self.model.encode(
            input,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    @staticmethod
    def name():
        return "local_all-MiniLM-L6-v2"


# Create embedding function
embedding_function = LocalEmbeddingFunction()


# Create persistent Chroma client
client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


# Load existing collection or create it
collection = client.get_or_create_collection(
    name="fbr_freelanceguide",
    embedding_function=embedding_function,
    metadata={
        "description": (
            "FBR tax rules relevant to Pakistani freelancers"
        )
    },
)


def add_documents(
    documents: list[str],
    metadatas: list[dict],
    ids: list[str],
):
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )


def search_documents(
    query: str,
    n_results: int = 5,
):
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    return results