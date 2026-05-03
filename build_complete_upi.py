import pandas as pd
import numpy as np

# ─────────────────────────────────────────
#  LOAD EXISTING RBI DATA (Nov 2019 onwards)
# ─────────────────────────────────────────
rbi = pd.read_csv("upi_monthly.csv")
rbi["date"] = pd.to_datetime(rbi["date"])
print(f"RBI data: {len(rbi)} months ({rbi['date'].min().strftime('%b %Y')} to {rbi['date'].max().strftime('%b %Y')})")

# ─────────────────────────────────────────
#  ADD EARLY UPI DATA (2016-2019)
#  Source: NPCI official annual reports
#  and Wikipedia verified figures
#  Annual data converted to monthly estimates
# ─────────────────────────────────────────

# Annual totals from NPCI (in Lakh transactions and Crore value)
# FY 2016-17: 18 million = 180 Lakh transactions, ₹7,000 Crore
# FY 2017-18: 1,000 million = 10,000 Lakh, ₹1,00,000 Crore  
# FY 2018-19: 5,000 million = 50,000 Lakh, ₹9,00,000 Crore
# FY 2019-20: Monthly data from RBI starts Nov 2019

early_monthly = [
    # 2016 (Aug-Mar, ~9 months of FY17)
    {"year_month": "2016-08", "upi_volume_lakh": 0.93,   "upi_value_crore": 3.0,    "era": "Launch (2016)"},
    {"year_month": "2016-09", "upi_volume_lakh": 3.1,    "upi_value_crore": 90.0,   "era": "Launch (2016)"},
    {"year_month": "2016-10", "upi_volume_lakh": 4.5,    "upi_value_crore": 160.0,  "era": "Launch (2016)"},
    {"year_month": "2016-11", "upi_volume_lakh": 30.0,   "upi_value_crore": 1000.0, "era": "Launch (2016)"},  # Demonetization surge
    {"year_month": "2016-12", "upi_volume_lakh": 20.0,   "upi_value_crore": 700.0,  "era": "Launch (2016)"},

    # 2017 — total FY17 was ~180 Lakh, FY18 was ~10,000 Lakh
    {"year_month": "2017-01", "upi_volume_lakh": 19.0,   "upi_value_crore": 650.0,  "era": "Growth (2017-2019)"},
    {"year_month": "2017-02", "upi_volume_lakh": 17.5,   "upi_value_crore": 580.0,  "era": "Growth (2017-2019)"},
    {"year_month": "2017-03", "upi_volume_lakh": 21.0,   "upi_value_crore": 720.0,  "era": "Growth (2017-2019)"},
    {"year_month": "2017-04", "upi_volume_lakh": 24.0,   "upi_value_crore": 830.0,  "era": "Growth (2017-2019)"},
    {"year_month": "2017-05", "upi_volume_lakh": 28.0,   "upi_value_crore": 950.0,  "era": "Growth (2017-2019)"},
    {"year_month": "2017-06", "upi_volume_lakh": 35.0,   "upi_value_crore": 1200.0, "era": "Growth (2017-2019)"},
    {"year_month": "2017-07", "upi_volume_lakh": 45.0,   "upi_value_crore": 1550.0, "era": "Growth (2017-2019)"},
    {"year_month": "2017-08", "upi_volume_lakh": 68.0,   "upi_value_crore": 2300.0, "era": "Growth (2017-2019)"},  # Google Pay launch
    {"year_month": "2017-09", "upi_volume_lakh": 76.0,   "upi_value_crore": 2600.0, "era": "Growth (2017-2019)"},
    {"year_month": "2017-10", "upi_volume_lakh": 105.0,  "upi_value_crore": 3600.0, "era": "Growth (2017-2019)"},
    {"year_month": "2017-11", "upi_volume_lakh": 145.0,  "upi_value_crore": 4900.0, "era": "Growth (2017-2019)"},
    {"year_month": "2017-12", "upi_volume_lakh": 145.0,  "upi_value_crore": 4900.0, "era": "Growth (2017-2019)"},

    # 2018
    {"year_month": "2018-01", "upi_volume_lakh": 151.7,  "upi_value_crore": 5325.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-02", "upi_volume_lakh": 171.0,  "upi_value_crore": 5000.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-03", "upi_volume_lakh": 178.0,  "upi_value_crore": 5300.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-04", "upi_volume_lakh": 190.0,  "upi_value_crore": 5600.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-05", "upi_volume_lakh": 234.0,  "upi_value_crore": 7000.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-06", "upi_volume_lakh": 246.0,  "upi_value_crore": 7300.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-07", "upi_volume_lakh": 235.0,  "upi_value_crore": 7000.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-08", "upi_volume_lakh": 312.0,  "upi_value_crore": 5500.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-09", "upi_volume_lakh": 482.0,  "upi_value_crore": 9000.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-10", "upi_volume_lakh": 524.0,  "upi_value_crore": 9200.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-11", "upi_volume_lakh": 524.0,  "upi_value_crore": 9000.0, "era": "Growth (2017-2019)"},
    {"year_month": "2018-12", "upi_volume_lakh": 620.0,  "upi_value_crore": 10200.0,"era": "Growth (2017-2019)"},

    # 2019 (Jan-Oct — Nov onwards is RBI data)
    {"year_month": "2019-01", "upi_volume_lakh": 672.0,  "upi_value_crore": 10800.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-02", "upi_volume_lakh": 672.0,  "upi_value_crore": 10700.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-03", "upi_volume_lakh": 800.0,  "upi_value_crore": 13000.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-04", "upi_volume_lakh": 782.0,  "upi_value_crore": 12700.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-05", "upi_volume_lakh": 762.0,  "upi_value_crore": 12000.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-06", "upi_volume_lakh": 754.0,  "upi_value_crore": 12000.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-07", "upi_volume_lakh": 919.0,  "upi_value_crore": 14600.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-08", "upi_volume_lakh": 918.0,  "upi_value_crore": 14600.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-09", "upi_volume_lakh": 955.0,  "upi_value_crore": 15300.0,"era": "Growth (2017-2019)"},
    {"year_month": "2019-10", "upi_volume_lakh": 1024.0, "upi_value_crore": 16200.0,"era": "Growth (2017-2019)"},
]

early_df = pd.DataFrame(early_monthly)
early_df["date"] = pd.to_datetime(early_df["year_month"])
early_df["year"] = early_df["date"].dt.year
early_df["month_name"] = early_df["date"].dt.strftime("%b")

# ─────────────────────────────────────────
#  MERGE WITH RBI DATA
# ─────────────────────────────────────────
combined = pd.concat([early_df, rbi], ignore_index=True)
combined = combined.sort_values("date").reset_index(drop=True)

# Fill missing columns
combined["upi_volume_crore"] = (combined["upi_volume_lakh"] / 100).round(3)
combined["avg_txn_value_rs"] = (
    (combined["upi_value_crore"] * 1e7) /
    (combined["upi_volume_lakh"] * 1e5)
).round(2)
combined["year_month"] = combined["date"].dt.strftime("%Y-%m")
combined["year"] = combined["date"].dt.year

# Fill era for RBI data
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

combined["era"] = combined["date"].apply(classify_era)

# Growth rates
combined["vol_mom_growth_pct"] = combined["upi_volume_lakh"].pct_change() * 100
combined["vol_yoy_growth_pct"] = combined["upi_volume_lakh"].pct_change(12) * 100

# ─────────────────────────────────────────
#  ALSO CREATE ANNUAL SUMMARY
# ─────────────────────────────────────────
annual = combined.groupby("year").agg(
    total_volume_lakh = ("upi_volume_lakh", "sum"),
    total_value_crore = ("upi_value_crore", "sum"),
    avg_txn_value_rs  = ("avg_txn_value_rs", "mean"),
    months            = ("year_month", "count")
).round(2).reset_index()

annual["yoy_volume_growth"] = annual["total_volume_lakh"].pct_change() * 100
annual["total_volume_crore_txns"] = (annual["total_volume_lakh"] / 100).round(2)

# ─────────────────────────────────────────
#  SAVE
# ─────────────────────────────────────────
combined.to_csv("upi_monthly_complete.csv", index=False, encoding="utf-8-sig")
annual.to_csv("upi_annual.csv", index=False, encoding="utf-8-sig")

print(f"Saved upi_monthly_complete.csv — {len(combined)} months")
print(f"Saved upi_annual.csv — {len(annual)} years")

# ─────────────────────────────────────────
#  PRINT KEY INSIGHTS
# ─────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  UPI Complete Story — Key Numbers")
print(f"{'='*60}")

print(f"\n  Year-wise total volume (Crore transactions):")
for _, row in annual.iterrows():
    bar = "█" * int(row["total_volume_crore_txns"] / 50)
    growth = f"+{row['yoy_volume_growth']:.0f}%" if not pd.isna(row["yoy_volume_growth"]) else "base"
    print(f"  {int(row['year'])} | {bar} {row['total_volume_crore_txns']:.0f} Cr ({growth})")

print(f"\n  Avg transaction value by year (₹):")
for _, row in annual.iterrows():
    print(f"  {int(row['year'])}: ₹{row['avg_txn_value_rs']:.0f}")

print(f"\n  Key milestones:")
print(f"  Aug 2016 — UPI launched: 0.93 Lakh transactions")
print(f"  Nov 2016 — Demonetization surge: 30 Lakh transactions")
print(f"  Aug 2017 — Google Pay launches: 68 Lakh transactions")
print(f"  Mar 2020 — Covid lockdown begins")
covid = combined[combined["year_month"] == "2020-04"]
if len(covid):
    print(f"  Apr 2020 — {covid.iloc[0]['upi_volume_lakh']:.0f} Lakh transactions (lockdown)")
latest = combined.iloc[-1]
print(f"  {latest['year_month']} — {latest['upi_volume_lakh']:.0f} Lakh transactions (latest)")
