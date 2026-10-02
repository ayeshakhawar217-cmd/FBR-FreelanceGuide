from agents.intake import extract_freelancer_facts
from agents.retrieval import retrieve_rules


user_text = """
I'm a Pakistani software developer. I earn around PKR 4.8 million
annually from US clients through Upwork. I get paid into my Pakistani
bank account. I'm registered with PSEB and I filed my return last year.
"""


profile = extract_freelancer_facts(user_text)

print("\nPROFILE")
print("=" * 80)
print(profile.model_dump_json(indent=2))


print("\nRETRIEVED FBR RULES")
print("=" * 80)

results = retrieve_rules(profile, n_results=3)

for i, result in enumerate(results, 1):
    print(f"\nRESULT {i}")
    print("-" * 80)
    print("SOURCE:", result["metadata"])
    print("TEXT:")
    print(result["text"][:1500])