from agents.intake import extract_freelancer_facts
from agents.retrieval import retrieve_rules
from agents.rule_selection import select_tax_rule


user_text = """
I'm a Pakistani software developer. I earn around PKR 4.8 million
annually from US clients through Upwork. I get paid into my Pakistani
bank account. I'm registered with PSEB and I filed my return last year.
"""


print("\n1. INTAKE")
print("=" * 80)

profile = extract_freelancer_facts(user_text)

print(profile.model_dump_json(indent=2))


print("\n2. RETRIEVAL")
print("=" * 80)

rules = retrieve_rules(
    profile,
    n_results=3,
)

print(f"Retrieved {len(rules)} unique evidence chunks.")


print("\n3. RULE SELECTION")
print("=" * 80)

selected_rule = select_tax_rule(
    profile,
    rules,
)

print(selected_rule)