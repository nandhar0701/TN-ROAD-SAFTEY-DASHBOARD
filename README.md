# 🚦 Tamil Nadu Road Safety Dashboard

An interactive dashboard analyzing road accidents and fatalities across
Tamil Nadu, built on **real government data** — district-wise accidents
(2021–2023) and a 32-year statewide trend (1993–2025). Built with plain
HTML, CSS, and JavaScript (Chart.js) — no frameworks, no build step.

🔗 **Live demo:** https://YOUR-USERNAME.github.io/REPO-NAME/

*(Replace `YOUR-USERNAME` and `REPO-NAME` above with your actual GitHub
username and repo name once GitHub Pages is enabled — see
[Setup](#-setup) below.)*

---

## ✨ Features

- **District Leaderboard** — all 38 districts ranked by accidents or
  deaths, switch between 2021 / 2022 / 2023
- **32-Year Statewide Trend** — total accidents vs. persons killed,
  1993–2025 (2024/25 marked provisional)
- **Accident Severity Mix** — stacked chart of fatal / grievous / minor /
  non-injury accidents over time
- **2025 Severity Breakdown** (pie) — proportion of each severity type in
  the latest year
- **Top Districts by Share** (pie) — top 8 districts vs. the rest of the
  state, by accident volume
- **District Risk Tiers** (pie) — all 38 districts grouped into
  low/medium/high fatality-rate bands, with district names on hover
- **All Years table** — every year from 1993–2025 in one scrollable,
  sortable-by-eye table with color-coded fatality rate
- KPI row: total 2023 accidents/deaths statewide, fatality rate, and the
  highest-risk district

## 📊 Data Sources

- **Publisher:** Tamil Nadu Police / Government of Tamil Nadu
- **Hosted by:** [data.opencity.in](https://data.opencity.in) — a
  civic-tech open data portal republishing Indian government datasets
- **Datasets:**
  1. District-wise road accidents & deaths, all 38 districts, 2021–2023
  2. Statewide accident severity breakdown, 1993–2025

This is real, published government data — not simulated.

## 🗂️ Files in this repo

| File | What it is |
|---|---|
| `index.html` (or `tn_road_safety_dashboard.html`) | The interactive dashboard — open directly in any browser |
| `tn_district_accidents_2021_2023.csv` | Raw district-wise dataset |
| `tn_statewide_trend_1993_2025.csv` | Raw statewide historical dataset |
| `road_safety_analysis.py` | Python script: pandas cleaning, an SQL query (sqlite3), and matplotlib/seaborn charts |
| `README.md` | This file |

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data source | Real government CSVs (data.opencity.in) |
| Cleaning / analysis | Python (pandas) |
| Querying | SQL (sqlite3) |
| Static charts | matplotlib + seaborn |
| Interactive dashboard | HTML/CSS/JS + Chart.js, no dependencies |

## ▶️ Running the Python analysis

```bash
pip install pandas matplotlib seaborn
python road_safety_analysis.py
```

Prints top districts by accident count and fatality rate, fastest-growing
districts, a SQL query on high-volume/high-risk districts, and saves 3
PNG charts.

## 📈 Key findings

- **Coimbatore and Chennai City** had the most accidents in 2023, but
  very different fatality rates (28.6% vs 13.8%) — likely reflecting
  slower, denser city traffic vs. faster suburban/highway roads
- **Chengalpattu and Thiruvallur** (Chennai's metro periphery) saw
  accidents more than double from 2021→2023
- **Statewide fatality rate has held around 27–28%** for the last three
  years — roughly 1 in 4 recorded accidents is fatal
- 2023 accident totals (67,213) had nearly returned to the pre-pandemic
  2019 peak (62,685), after a sharp COVID-era dip in 2020 (49,844)

**Data-quality note:** Myiladuthurai district's 2021 figures are missing
("NA") in the source — it was only carved out as a separate district
from Nagapattinam in late 2020, so 2021 reporting was inconsistent. The
analysis script leaves this as a genuine `NaN` rather than guessing a
value.

## 🚀 Setup

1. Clone or download this repo
2. Open `index.html` directly in any browser — no server needed

### Enabling GitHub Pages (to get a live link)

1. Go to **Settings → Pages** in your repo
2. Under "Build and deployment," set **Source** to `Deploy from a branch`
3. Pick the `main` branch and `/ (root)` folder → **Save**
4. Live at `https://YOUR-USERNAME.github.io/REPO-NAME/` within a minute
   or two

## 📄 License / Attribution

Personal/academic project. All statistics are compiled from public
government data sources cited above (data.opencity.in, originally
published by Tamil Nadu Police).

---

*Built as a data analyst portfolio project.*
