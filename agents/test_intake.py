from agents.intake import extract_freelancer_facts


text = """
I'm a Pakistani software developer. I earn around PKR 4.8 million
annually from US clients through Upwork. I get paid into my Pakistani
bank account. I'm registered with PSEB and I filed my return last year.
"""


profile = extract_freelancer_facts(text)

print("\nExtracted profile:")
print(profile.model_dump_json(indent=2))