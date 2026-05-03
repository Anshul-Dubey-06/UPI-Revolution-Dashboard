-- ============================================================
--  PROJECT 4: India's UPI Revolution
--  Database: upi_analysis
--  Tables: upi_monthly, upi_annual
-- ============================================================

USE upi_analysis;

-- ────────────────────────────────────────────────────────────
--  Q1: Year-wise growth story
-- ────────────────────────────────────────────────────────────
SELECT
    txn_year,
    ROUND(total_volume_crore, 0)   AS crore_transactions,
    ROUND(total_value_crore/100000, 2) AS lakh_crore_value,
    ROUND(avg_value_rs, 0)         AS avg_txn_value_rs,
    ROUND(yoy_growth_pct, 1)       AS yoy_growth_pct
FROM upi_annual
ORDER BY txn_year;


-- ────────────────────────────────────────────────────────────
--  Q2: Monthly growth trend (last 24 months)
-- ────────────────────────────────────────────────────────────
SELECT
    period,
    ROUND(volume_lakh, 0)       AS volume_lakh,
    ROUND(value_crore, 0)       AS value_crore,
    ROUND(avg_value_rs, 0)      AS avg_txn_value_rs,
    ROUND(mom_growth_pct, 1)    AS mom_growth_pct
FROM upi_monthly
ORDER BY period DESC
LIMIT 24;


-- ────────────────────────────────────────────────────────────
--  Q3: Era-wise performance comparison
-- ────────────────────────────────────────────────────────────
SELECT
    era,
    COUNT(*)                            AS months,
    ROUND(AVG(volume_lakh), 0)          AS avg_monthly_volume_lakh,
    ROUND(MAX(volume_lakh), 0)          AS peak_volume_lakh,
    ROUND(AVG(avg_value_rs), 0)         AS avg_txn_value_rs,
    ROUND(AVG(mom_growth_pct), 1)       AS avg_mom_growth_pct
FROM upi_monthly
WHERE mom_growth_pct IS NOT NULL
GROUP BY era
ORDER BY MIN(txn_date);


-- ────────────────────────────────────────────────────────────
--  Q4: Covid impact analysis
--  Compare 6 months before vs 6 months after lockdown
-- ────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN period BETWEEN '2019-09' AND '2020-02' THEN 'Pre-Covid (Sep19-Feb20)'
        WHEN period BETWEEN '2020-03' AND '2020-08' THEN 'Covid Lockdown (Mar20-Aug20)'
        WHEN period BETWEEN '2020-09' AND '2021-02' THEN 'Post-Lockdown (Sep20-Feb21)'
    END AS period_label,
    COUNT(*) AS months,
    ROUND(AVG(volume_lakh), 0) AS avg_monthly_volume_lakh,
    ROUND(AVG(value_crore), 0) AS avg_monthly_value_crore,
    ROUND(AVG(avg_value_rs), 0) AS avg_txn_value_rs
FROM upi_monthly
WHERE period BETWEEN '2019-09' AND '2021-02'
GROUP BY period_label
ORDER BY MIN(period);


-- ────────────────────────────────────────────────────────────
--  Q5: The falling average transaction value story
--  This is the KEY insight — UPI became small-ticket
-- ────────────────────────────────────────────────────────────
SELECT
    txn_year,
    ROUND(avg_value_rs, 0) AS avg_txn_value_rs,
    CASE
        WHEN avg_value_rs > 2000 THEN 'High ticket (transfers)'
        WHEN avg_value_rs > 1500 THEN 'Medium ticket (bills)'
        WHEN avg_value_rs > 1200 THEN 'Low ticket (daily use)'
        ELSE 'Micro payments (chai/auto)'
    END AS usage_pattern
FROM upi_annual
ORDER BY txn_year;


-- ────────────────────────────────────────────────────────────
--  Q6: Demonetization impact (Nov 2016 spike)
-- ────────────────────────────────────────────────────────────
SELECT
    period,
    month_name,
    txn_year,
    ROUND(volume_lakh, 2) AS volume_lakh,
    ROUND(mom_growth_pct, 1) AS mom_growth_pct
FROM upi_monthly
WHERE txn_year IN (2016, 2017)
ORDER BY period;


-- ────────────────────────────────────────────────────────────
--  Q7: Key milestones — when did UPI cross major thresholds?
-- ────────────────────────────────────────────────────────────
-- Q7: Key milestones
SELECT '100 Lakh milestone' AS milestone, period, ROUND(volume_lakh, 0) AS volume_lakh, era
FROM upi_monthly WHERE volume_lakh >= 100 ORDER BY period LIMIT 1;

SELECT '1,000 Lakh milestone' AS milestone, period, ROUND(volume_lakh, 0) AS volume_lakh, era
FROM upi_monthly WHERE volume_lakh >= 1000 ORDER BY period LIMIT 1;

SELECT '10,000 Lakh milestone' AS milestone, period, ROUND(volume_lakh, 0) AS volume_lakh, era
FROM upi_monthly WHERE volume_lakh >= 10000 ORDER BY period LIMIT 1;

SELECT '1,00,000 Lakh milestone' AS milestone, period, ROUND(volume_lakh, 0) AS volume_lakh, era
FROM upi_monthly WHERE volume_lakh >= 100000 ORDER BY period LIMIT 1;


-- ────────────────────────────────────────────────────────────
--  Q8: Monthly seasonality — which months are busiest?
-- ────────────────────────────────────────────────────────────
SELECT
    month_name,
    ROUND(AVG(volume_lakh), 0)      AS avg_volume_lakh,
    ROUND(AVG(mom_growth_pct), 1)   AS avg_growth_pct,
    COUNT(*)                         AS years_of_data
FROM upi_monthly
WHERE txn_year >= 2021
GROUP BY month_name
ORDER BY avg_volume_lakh DESC;


-- ────────────────────────────────────────────────────────────
--  Q9: Growth rate slowdown — is UPI maturing?
-- ────────────────────────────────────────────────────────────
SELECT
    txn_year,
    ROUND(yoy_growth_pct, 1) AS yoy_growth_pct,
    CASE
        WHEN yoy_growth_pct > 200 THEN 'Hypergrowth'
        WHEN yoy_growth_pct > 80  THEN 'High Growth'
        WHEN yoy_growth_pct > 40  THEN 'Moderate Growth'
        ELSE 'Maturing'
    END AS growth_stage
FROM upi_annual
WHERE yoy_growth_pct IS NOT NULL
ORDER BY txn_year;


-- ────────────────────────────────────────────────────────────
--  Q10: Value vs Volume divergence
--  Shows when UPI became small-ticket dominant
-- ────────────────────────────────────────────────────────────
SELECT
    period,
    txn_year,
    ROUND(volume_lakh, 0)      AS volume_lakh,
    ROUND(value_crore, 0)      AS value_crore,
    ROUND(avg_value_rs, 0)     AS avg_txn_rs,
    ROUND(yoy_growth_pct, 1)   AS vol_yoy_growth
FROM upi_monthly
WHERE period IN (
    '2019-01','2019-06','2019-12',
    '2020-06','2020-12',
    '2021-06','2021-12',
    '2022-06','2022-12',
    '2023-06','2023-12',
    '2024-06','2024-12',
    '2025-06'
)
ORDER BY period;
