"""
Tamil Nadu Road Safety Analysis (real government data)
--------------------------------------------------------
Source: Tamil Nadu Police / Government of Tamil Nadu, published via
        data.opencity.in (OpenCity civic data portal)

Demonstrates: data cleaning (handling a missing value), pandas
aggregation, an SQL query (via sqlite3), and chart generation.

Run:
    pip install pandas matplotlib seaborn
    python road_safety_analysis.py
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
district = pd.read_csv("tn_district_accidents_2021_2023.csv")
trend = pd.read_csv("tn_statewide_trend_1993_2025.csv")

print("District data shape:", district.shape)
print(district.head())
print("\nTrend data shape:", trend.shape)
print(trend.tail())

# ---------------------------------------------------------
# 2. CLEANING
# ---------------------------------------------------------
# Myiladuthurai district was carved out of Nagapattinam in 2020,
# so its 2021 figures are reported as "NA" in the source data.
# We convert to numeric and leave those two cells as NaN rather
# than guessing a value — this is worth calling out in your report.
for col in district.columns[2:]:
    district[col] = pd.to_numeric(district[col], errors="coerce")

district["District"] = district["District"].str.title()

# ---------------------------------------------------------
# 3. DERIVED METRICS
# ---------------------------------------------------------
district["fatality_rate_2023"] = (
    district["Total Deaths 2023"] / district["Total Accidents 2023"] * 100
).round(2)

district["accident_growth_21_23_pct"] = (
    (district["Total Accidents 2023"] - district["Total Accidents 2021"])
    / district["Total Accidents 2021"] * 100
).round(1)

trend["fatality_rate"] = (trend["Persons_Killed"] / trend["Total_Accidents"] * 100).round(2)

# ---------------------------------------------------------
# 4. PANDAS AGGREGATIONS
# ---------------------------------------------------------
print("\n=== Top 10 districts by 2023 accident count ===")
print(
    district.sort_values("Total Accidents 2023", ascending=False)
    .head(10)[["District", "Total Accidents 2023", "Total Deaths 2023", "fatality_rate_2023"]]
)

print("\n=== Top 10 districts by fatality rate (deaths per 100 accidents), 2023 ===")
print(
    district.sort_values("fatality_rate_2023", ascending=False)
    .head(10)[["District", "Total Accidents 2023", "fatality_rate_2023"]]
)

print("\n=== Districts with fastest-growing accident counts (2021 -> 2023) ===")
print(
    district.dropna(subset=["accident_growth_21_23_pct"])
    .sort_values("accident_growth_21_23_pct", ascending=False)
    .head(10)[["District", "Total Accidents 2021", "Total Accidents 2023", "accident_growth_21_23_pct"]]
)

# ---------------------------------------------------------
# 5. SQL-STYLE QUERY (via in-memory SQLite)
# ---------------------------------------------------------
conn = sqlite3.connect(":memory:")
district.to_sql("district_accidents", conn, index=False, if_exists="replace")

query = """
SELECT District,
       "Total Accidents 2023" AS accidents_2023,
       "Total Deaths 2023"    AS deaths_2023,
       fatality_rate_2023
FROM district_accidents
WHERE "Total Accidents 2023" > 2000
ORDER BY fatality_rate_2023 DESC;
"""
high_volume_high_risk = pd.read_sql_query(query, conn)
print("\n=== SQL: High-volume districts (>2000 accidents) ranked by fatality rate ===")
print(high_volume_high_risk)

# ---------------------------------------------------------
# 6. VISUALIZATIONS
# ---------------------------------------------------------
sns.set_theme(style="darkgrid")

# 6a. Top 15 districts by accident count, 2023
top15 = district.sort_values("Total Accidents 2023", ascending=False).head(15)
plt.figure(figsize=(9, 6))
sns.barplot(x="Total Accidents 2023", y="District", data=top15, palette="flare")
plt.title("Top 15 Tamil Nadu Districts by Road Accidents (2023)")
plt.xlabel("Total Accidents")
plt.ylabel("")
plt.tight_layout()
plt.savefig("chart_top_districts_2023.png", dpi=150)
plt.close()

# 6b. Statewide trend, 1993-2025
plt.figure(figsize=(10, 5))
ax1 = plt.gca()
sns.barplot(x="Year", y="Total_Accidents", data=trend, color="#F5A623", alpha=0.6, ax=ax1)
ax2 = ax1.twinx()
sns.lineplot(x=range(len(trend)), y="Persons_Killed", data=trend, color="#E8543E", marker="o", ax=ax2)
ax1.set_xticklabels(trend["Year"], rotation=90, fontsize=8)
ax1.set_title("Tamil Nadu: Total Accidents (bars) vs Persons Killed (line), 1993-2025")
plt.tight_layout()
plt.savefig("chart_statewide_trend.png", dpi=150)
plt.close()

# 6c. Fatality rate vs accident volume scatter (2023)
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x="Total Accidents 2023", y="fatality_rate_2023", data=district, s=70, color="#E8543E"
)
for _, row in district.iterrows():
    if row["Total Accidents 2023"] > 2500 or row["fatality_rate_2023"] > 30:
        plt.text(row["Total Accidents 2023"] + 20, row["fatality_rate_2023"], row["District"], fontsize=8)
plt.title("Accident Volume vs Fatality Rate by District (2023)")
plt.xlabel("Total Accidents")
plt.ylabel("Fatality Rate (%)")
plt.tight_layout()
plt.savefig("chart_volume_vs_fatality.png", dpi=150)
plt.close()

print("\nCharts saved: chart_top_districts_2023.png, chart_statewide_trend.png, chart_volume_vs_fatality.png")
