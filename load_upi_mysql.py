import pandas as pd
import mysql.connector
from mysql.connector import Error
import math

# ─────────────────────────────────────────
#  CONFIG — add your password
# ─────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "Anshul@2106",  # ← replace this
}
DB_NAME = "upi_analysis"

# ─────────────────────────────────────────
#  CONNECT
# ─────────────────────────────────────────
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Connected to MySQL!")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    print(f"Database '{DB_NAME}' ready.")
except Error as e:
    print(f"[!] Connection failed: {e}")
    exit()

def clean_val(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return v

# ─────────────────────────────────────────
#  LOAD MONTHLY DATA
# ─────────────────────────────────────────
print("\nLoading monthly data...")
df = pd.read_csv("upi_monthly_complete.csv")
df = df.where(pd.notnull(df), None)
print(f"Rows: {len(df)}")

cursor.execute("DROP TABLE IF EXISTS upi_monthly")
cursor.execute("""
CREATE TABLE upi_monthly (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    period              VARCHAR(10),
    txn_date            VARCHAR(20),
    txn_year            INT,
    month_name          VARCHAR(10),
    era                 VARCHAR(30),
    volume_lakh         FLOAT,
    value_crore         FLOAT,
    volume_crore        FLOAT,
    avg_value_rs        FLOAT,
    mom_growth_pct      FLOAT,
    yoy_growth_pct      FLOAT
)
""")

cols_map = {
    "year_month":         "period",
    "date":               "txn_date",
    "year":               "txn_year",
    "month_name":         "month_name",
    "era":                "era",
    "upi_volume_lakh":    "volume_lakh",
    "upi_value_crore":    "value_crore",
    "upi_volume_crore":   "volume_crore",
    "avg_txn_value_rs":   "avg_value_rs",
    "vol_mom_growth_pct": "mom_growth_pct",
    "vol_yoy_growth_pct": "yoy_growth_pct",
}

db_cols = list(cols_map.values())
csv_cols = list(cols_map.keys())

placeholders = ", ".join(["%s"] * len(db_cols))
col_names    = ", ".join(db_cols)
insert_sql   = f"INSERT INTO upi_monthly ({col_names}) VALUES ({placeholders})"

rows = [tuple(clean_val(row[c]) for c in csv_cols)
        for _, row in df.iterrows()]

cursor.executemany(insert_sql, rows)
conn.commit()
print(f"Loaded {cursor.rowcount} rows into upi_monthly")

# ─────────────────────────────────────────
#  LOAD ANNUAL DATA
# ─────────────────────────────────────────
print("\nLoading annual data...")
annual = pd.read_csv("upi_annual.csv")
annual = annual.where(pd.notnull(annual), None)

cursor.execute("DROP TABLE IF EXISTS upi_annual")
cursor.execute("""
CREATE TABLE upi_annual (
    txn_year            INT PRIMARY KEY,
    total_volume_lakh   FLOAT,
    total_value_crore   FLOAT,
    avg_value_rs        FLOAT,
    months              INT,
    yoy_growth_pct      FLOAT,
    total_volume_crore  FLOAT
)
""")

annual_cols = ["year", "total_volume_lakh", "total_value_crore",
               "avg_txn_value_rs", "months", "yoy_volume_growth",
               "total_volume_crore_txns"]

rows2 = [tuple(clean_val(row[c]) for c in annual_cols)
         for _, row in annual.iterrows()]

cursor.executemany(
    "INSERT INTO upi_annual VALUES (%s,%s,%s,%s,%s,%s,%s)",
    rows2
)
conn.commit()
print(f"Loaded {cursor.rowcount} rows into upi_annual")

# ─────────────────────────────────────────
#  VERIFY
# ─────────────────────────────────────────
cursor.execute("SELECT COUNT(*) FROM upi_monthly")
print(f"\nVerified: {cursor.fetchone()[0]} rows in upi_monthly")

cursor.execute("SELECT txn_year, ROUND(total_volume_crore,0) AS crore_txns FROM upi_annual ORDER BY txn_year")
print("\nAnnual summary in MySQL:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} Crore transactions")

cursor.close()
conn.close()
print(f"\nDone! Open MySQL Workbench → {DB_NAME}")
