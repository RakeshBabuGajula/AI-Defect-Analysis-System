from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# =========================================================
# PROJECT CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

VECTOR_DB_DIR = (
    BASE_DIR
    / "data"
    / "vector_db"
)

COLLECTION_NAME = "historical_defects_balanced"

MODEL_NAME = "all-MiniLM-L6-v2"


# =========================================================
# INITIALIZE MODEL
# =========================================================

_model = SentenceTransformer(
    MODEL_NAME
)


# =========================================================
# INITIALIZE CHROMADB
# =========================================================

_client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)


_collection = _client.get_collection(
    name=COLLECTION_NAME
)


# =========================================================
# RETRIEVE SIMILAR DEFECTS
# =========================================================

def retrieve_similar_bugs(
    query,
    top_k=5
):

    """
    Retrieve historically similar software defects.

    Parameters
    ----------
    query : str
        New bug description.

    top_k : int
        Number of historical defects to retrieve.

    Returns
    -------
    list
        Structured historical defect results.
    """


    if not query or not query.strip():

        return []


    # -----------------------------------------------------
    # Generate query embedding
    # -----------------------------------------------------

    query_embedding = _model.encode(
        query,
        normalize_embeddings=True
    )


    # -----------------------------------------------------
    # Semantic search
    # -----------------------------------------------------

    results = _collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=top_k

    )


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    # -----------------------------------------------------
    # Structure results
    # -----------------------------------------------------

    retrieved_bugs = []


    for rank, (
        document,
        metadata,
        distance
    ) in enumerate(
        zip(
            documents,
            metadatas,
            distances
        ),
        start=1
    ):

        similarity = 1 - distance


        retrieved_bugs.append({

            "rank": rank,

            "bug_id":
                metadata.get(
                    "bug_id"
                ),

            "source":
                metadata.get(
                    "source"
                ),

            "title":
                metadata.get(
                    "title"
                ),

            "product":
                metadata.get(
                    "product"
                ),

            "component":
                metadata.get(
                    "component"
                ),

            "severity":
                metadata.get(
                    "severity"
                ),

            "priority":
                metadata.get(
                    "priority"
                ),

            "status":
                metadata.get(
                    "status"
                ),

            "resolution":
                metadata.get(
                    "resolution"
                ),

            "similarity":
                round(
                    similarity,
                    4
                ),

            "text":
                document

        })


    return retrieved_bugs