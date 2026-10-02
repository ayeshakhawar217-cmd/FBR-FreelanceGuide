from rag.retriever import retrieve_fbr_rules


query = """
Pakistani software developer earning income from foreign clients.
The person provides IT services, receives payment from abroad,
is registered with PSEB, and wants to know the applicable tax treatment.
"""

results = retrieve_fbr_rules(query, n_results=5)

for i, result in enumerate(results, 1):
    print("\n" + "=" * 80)
    print(f"RESULT {i}")
    print("=" * 80)

    print("\nSOURCE:")
    print(result["metadata"])

    print("\nTEXT:")
    print(result["text"])