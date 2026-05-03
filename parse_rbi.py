import pandas as pd
import numpy as np

# ─────────────────────────────────────────
#  LOAD RAW EXCEL
# ─────────────────────────────────────────
FILE = "RBIB Table No. 45 _ Payment System Indicators.xlsx"

print("Loading raw Excel...")
raw = pd.read_excel(FILE, header=None)
print(f"Raw shape: {raw.shape}")

# Print first 15 rows to understand structure
print("\nFirst 15 rows (first 20 columns):")
print(raw.iloc[:15, :20].to_string())

# ─────────────────────────────────────────
#  FIND UPI ROW
# ─────────────────────────────────────────
print("\n\nSearching for UPI in the file...")
for i, row in raw.iterrows():
    for j, val in enumerate(row):
        if isinstance(val, str) and 'UPI' in val.upper():
            print(f"  Found 'UPI' at row {i}, col {j}: '{val}'")

# ─────────────────────────────────────────
#  FIND MONTH/YEAR COLUMN
# ─────────────────────────────────────────
print("\nSearching for Month/Year column...")
for i, row in raw.iterrows():
    for j, val in enumerate(row):
        if isinstance(val, str) and 'month' in val.lower():
            print(f"  Found 'Month' at row {i}, col {j}: '{val}'")
