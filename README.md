# 🇮🇳 India's UPI Revolution — Power BI Dashboard (2016–2026)

> *"Volume grew 38,000x. But the average transaction fell 65%. UPI didn't replace bank transfers — it replaced cash for chai, autos, and street food."*

---

## 📌 Project Overview

This project analyzes **10 years of UPI transaction data** sourced directly from the **Reserve Bank of India** — 115 months of real payment data from April 2016 to January 2026.

Built as a 3-page Power BI dashboard that tells the story of how a single payment system transformed how 1.4 billion people move money.

---

## 🔍 The Insight Nobody Talks About

Everyone celebrates UPI's volume growth. Nobody asks **why the average transaction size keeps falling**.

| Metric | 2016 | 2026 |
|--------|------|------|
| Monthly Volume | 0.05 Cr | 2,170 Cr |
| Avg Transaction Value | ₹3,800 | ₹1,311 |
| Growth | — | **38,000x** |
| Avg Value Change | — | **−65%** |

**The answer:** UPI won India's streets — not its banks. It became the payment rail for ₹50 chai, ₹200 auto rides, and ₹500 grocery runs. Not EMIs. Not rent.

---

## 📊 Dashboard Pages

### Page 1 — UPI Transaction Dashboard (2016–2026)
- 5 KPI cards: Total Transactions, Peak Month, Growth, Years Active, Latest Avg Txn
- Full decade line chart with milestone annotations
- Milestones: Demonetisation (2016), WhatsApp Pay launch (2019), COVID lockdown boost (2020)

### Page 2 — Three Moments That Defined UPI
- **01 — Demonetisation Shock** (Nov 2016 – Mar 2017): +566% in one month
- **02 — COVID Contactless Boom** (Apr 2020 – Dec 2020): +105% YoY in 2021
- **03 — The Scale Milestone** (2023 – Present): 2,170 Cr/month peak
- Before vs After comparison chart (log scale)
- 3 sparkline trajectory charts per moment

### Page 3 — The Insight Nobody Talks About
- Dual axis divergence chart: Volume (↑) vs Avg Transaction Value (↓)
- 3 insight KPI cards
- The story behind India's everyday payment revolution

---

## 🛠️ Tools & Tech Stack

| Tool | Usage |
|------|-------|
| **Python** | Data extraction from RBI Excel files, cleaning |
| **MySQL** | Data storage, 10 analytical SQL queries |
| **Power BI** | 3-page interactive dashboard, DAX measures |
| **DAX** | Custom measures for KPI cards and calculations |

---

## 📁 Repository Structure

```
UPI-Revolution-Dashboard/
│
├── data/
│   ├── upi_monthly_complete.csv       # 115 months of monthly UPI data
│   ├── upi_annual.csv                 # Annual aggregated data
│   ├── sparkline_demonetisation.csv   # Nov 2016 – Mar 2017 sparkline
│   ├── sparkline_covid.csv            # Apr 2020 – Dec 2020 sparkline
│   └── sparkline_scale.csv            # Jan 2023 – Jan 2026 sparkline
│
├── dashboard/
│   └── UPI_ANALYSIS.pdf              # Exported dashboard (all 3 pages)
│
└── README.md
```

---

## 📈 Key Facts

- 🏦 **Data Source:** Reserve Bank of India (RBI) — official payment system data
- 📅 **Time Period:** April 2016 – January 2026 (115 months)
- 💰 **₹29.97 Lakh Crore** moved through UPI in 2025 alone
- 🌍 Visa took **50 years** to reach 1 billion transactions/day — India did it in **7**
- 📱 Peak: **2,170 Crore transactions** in January 2026

---

## 🎨 Design

- **Theme:** India Digital — Dark Navy `#0A1628` + Saffron `#FF6B35`
- **Style:** Narrative dashboard — tells a story across 3 pages
- **Inspiration:** The tricolor of India's digital payment revolution

---

## 💡 SQL Queries Performed

1. Monthly transaction volume trend
2. Year-over-year growth rate
3. Month-over-month growth rate
4. Peak month identification
5. Average transaction value trend
6. Pre/Post Demonetisation comparison
7. COVID period analysis
8. Annual aggregation
9. Cumulative transaction volume
10. Rolling 3-month average

---

## 🚀 How to Use

1. Clone this repository
2. Open `dashboard/UPI_ANALYSIS.pdf` to view the complete dashboard
3. Load CSV files from `data/` folder into Power BI for interactive version
4. Connect to MySQL if you want to run SQL queries

---

## 👤 Author

**Anshul Dubey**
Data Analyst Portfolio → [anshul-dubey-06.github.io](https://Anshul-Dubey-06.github.io)

---

## 📂 Other Projects

| Project | Description | Score |
|---------|-------------|-------|
| [Job Market India](https://github.com/Anshul-Dubey-06/data-analyst-job-market-india) | 1000+ job postings scraped from Naukri | 8/10 |
| [Zomato Delhi](https://github.com/Anshul-Dubey-06/zomato-delhi-food-desert-analysis) | Food desert analysis across 15 Delhi localities | 8.5/10 |
| [IPL Intelligence](https://github.com/Anshul-Dubey-06/ipl-intelligence-dashboard) | Custom MVP scoring from 260K ball-by-ball deliveries | 8.5/10 |
| **UPI Revolution** | **10 years of RBI payment data — this project** | **9/10** |

---

*Data Source: Reserve Bank of India | 2016–2026*
