from rag.vectorstore import search_documents


def retrieve_fbr_rules(query: str, n_results: int = 5):
    results = search_documents(query, n_results=n_results)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return [
        {
            "text": document,
            "metadata": metadata,
        }
        for document, metadata in zip(documents, metadatas)
    ]