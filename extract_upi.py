import pandas as pd
import numpy as np

# ─────────────────────────────────────────
#  LOAD RAW EXCEL
# ─────────────────────────────────────────
FILE = "RBIB Table No. 45 _ Payment System Indicators.xlsx"
raw = pd.read_excel(FILE, header=None)
print(f"Raw shape: {raw.shape}")

# ─────────────────────────────────────────
#  EXTRACT UPI DATA
#  UPI found at row 5, col 36
#  Volume = col 36, Value = col 37
#  Month/Year = col 1
#  Data starts at row 7
# ─────────────────────────────────────────

# Print around UPI column to confirm
print("\nUPI columns check (rows 3-8, cols 34-40):")
print(raw.iloc[3:9, 34:41].to_string())

# Extract month, UPI volume and value
upi_data = []

for i in range(7, 84):  # rows 7 to 83 (data rows)
    row = raw.iloc[i]
    month = row[1]
    upi_vol = row[36]   # Volume (Lakh)
    upi_val = row[37]   # Value (Rupees Crores)

    if pd.isna(month):
        continue

    upi_data.append({
        "month":          str(month).strip(),
        "upi_volume_lakh": upi_vol,
        "upi_value_crore": upi_val,
    })

df = pd.DataFrame(upi_data)
print(f"\nExtracted {len(df)} rows")
print(df.head(10).to_string())

# ─────────────────────────────────────────
#  CLEAN & ENRICH
# ─────────────────────────────────────────

# Convert to numeric
df["upi_volume_lakh"] = pd.to_numeric(df["upi_volume_lakh"], errors="coerce")
df["upi_value_crore"] = pd.to_numeric(df["upi_value_crore"], errors="coerce")

# Parse date
df["date"] = pd.to_datetime(df["month"], format="%b-%Y", errors="coerce")
df = df.dropna(subset=["date", "upi_volume_lakh"])
df = df.sort_values("date").reset_index(drop=True)

# Add derived columns
df["year"]              = df["date"].dt.year
df["month_name"]        = df["date"].dt.strftime("%b")
df["year_month"]        = df["date"].dt.strftime("%Y-%m")

# Convert to more readable units
df["upi_volume_crore"]  = (df["upi_volume_lakh"] / 100).round(3)  # Lakh → Crore transactions
df["upi_value_lakh_cr"] = (df["upi_value_crore"] / 100000).round(4)  # Crore → Lakh Crore

# Avg transaction value (in Rupees)
df["avg_txn_value_rs"]  = (
    (df["upi_value_crore"] * 1e7) / (df["upi_volume_lakh"] * 1e5)
).round(2)

# Month-over-month growth
df["vol_mom_growth_pct"] = df["upi_volume_lakh"].pct_change() * 100
df["val_mom_growth_pct"] = df["upi_value_crore"].pct_change() * 100

# Year-over-year growth
df["vol_yoy_growth_pct"] = df["upi_volume_lakh"].pct_change(12) * 100
df["val_yoy_growth_pct"] = df["upi_value_crore"].pct_change(12) * 100

# Era classification
def classify_era(date):
    if date < pd.Timestamp("2017-01-01"):
        return "Launch (2016)"
    elif date < pd.Timestamp("2020-03-01"):
        return "Growth (2017-2019)"
    elif date < pd.Timestamp("2021-06-01"):
        return "Covid Surge (2020-2021)"
    elif date < pd.Timestamp("2023-01-01"):
        return "Mainstream (2022)"
    else:
        return "Scale (2023+)"

df["era"] = df["date"].apply(classify_era)

# ─────────────────────────────────────────
#  SAVE
# ─────────────────────────────────────────
df.to_csv("upi_monthly.csv", index=False, encoding="utf-8-sig")
print(f"\nSaved upi_monthly.csv — {len(df)} months")

# ─────────────────────────────────────────
#  KEY INSIGHTS REPORT
# ─────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  UPI Growth Story — Key Numbers")
print(f"{'='*60}")

first = df.iloc[0]
last  = df.iloc[-1]

print(f"\n  First month: {first['year_month']} — {first['upi_volume_lakh']:.2f} Lakh transactions")
print(f"  Latest month: {last['year_month']} — {last['upi_volume_lakh']:.2f} Lakh transactions")
print(f"\n  Total growth: {((last['upi_volume_lakh']/first['upi_volume_lakh'])-1)*100:.0f}x increase in volume")

print(f"\n  Peak month by volume:")
peak_vol = df.nlargest(1, "upi_volume_lakh").iloc[0]
print(f"  {peak_vol['year_month']} — {peak_vol['upi_volume_lakh']:.0f} Lakh transactions")

print(f"\n  Avg transaction value over time:")
print(df.groupby("year")["avg_txn_value_rs"].mean().round(0).to_string())

print(f"\n  Volume by era:")
print(df.groupby("era")["upi_volume_lakh"].mean().round(0).to_string())

print(f"\n  Year-wise total volume (Lakh transactions):")
print(df.groupby("year")["upi_volume_lakh"].sum().round(0).to_string())

print(f"\n  Columns saved:")
print(df.columns.tolist())
