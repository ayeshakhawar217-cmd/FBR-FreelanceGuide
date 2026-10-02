from utils.calculator import calculate_export_tax


result = calculate_export_tax(
    annual_income=4_800_000,
    tax_rate=0.25,
)

print("\nCALCULATION")
print("=" * 80)

for key, value in result.items():
    print(f"{key}: {value}")