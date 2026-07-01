"""
Project 2: Customer Segmentation Analysis
Loads, cleans, explores, clusters (K-Means), and interprets customer segments.
Exports cluster assignments + summary stats for the interactive report.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json

# ---------- 1. LOAD ----------
df = pd.read_csv("customers.csv")
print("Raw shape:", df.shape)

# ---------- 2. CLEAN & PREPROCESS ----------
before = len(df)
df = df.drop_duplicates(subset=["CustomerID"], keep="first")
df = df.drop_duplicates(subset=["Age", "Gender", "Annual Income (k$)", "Spending Score (1-100)"])
print(f"Removed {before - len(df)} duplicate rows")

df["Annual Income (k$)"] = df["Annual Income (k$)"].fillna(df["Annual Income (k$)"].median())

# ---------- 3. EXPLORE ----------
print("\nDescribe:\n", df[["Age", "Annual Income (k$)", "Spending Score (1-100)"]].describe())

# ---------- 4. K-MEANS CLUSTERING ----------
features = df[["Annual Income (k$)", "Spending Score (1-100)"]]
scaler = StandardScaler()
X = scaler.fit_transform(features)

# elbow method to justify k
inertias = []
K_range = range(2, 9)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(round(km.inertia_, 2))
print("\nElbow inertias (k=2..8):", inertias)

# chosen k=5 (matches the classic mall-customer segmentation pattern)
k = 5
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X)

# ---------- 5. INTERPRET CLUSTERS ----------
summary = df.groupby("Cluster").agg(
    Count=("CustomerID", "count"),
    AvgAge=("Age", "mean"),
    AvgIncome=("Annual Income (k$)", "mean"),
    AvgSpend=("Spending Score (1-100)", "mean"),
).round(1).reset_index()

income_rank = summary["AvgIncome"].rank(method="first")
spend_rank = summary["AvgSpend"].rank(method="first")
n_clusters = len(summary)

def rank_label(r, total):
    if r <= total / 3: return "Low"
    if r > total - total / 3: return "High"
    return "Mid"

def label_cluster(i):
    inc = rank_label(income_rank[i], n_clusters)
    spd = rank_label(spend_rank[i], n_clusters)
    if inc == "High" and spd == "High": tag = " (Target)"
    elif inc == "High" and spd == "Low": tag = " (Cautious)"
    elif inc == "Low" and spd == "High": tag = " (Impulsive)"
    elif inc == "Low" and spd == "Low": tag = " (Budget)"
    else: tag = " (Standard)"
    return f"{inc} Income / {spd} Spend{tag}"

summary["Label"] = [label_cluster(i) for i in summary.index]
print("\nCluster summary:\n", summary)

# ---------- 6. EXPORT ----------
label_map = dict(zip(summary["Cluster"], summary["Label"]))
df["Segment"] = df["Cluster"].map(label_map)

export = {
    "elbow": {"k": list(K_range), "inertia": inertias},
    "cluster_summary": summary.to_dict(orient="records"),
    "points": df[["CustomerID", "Age", "Gender", "Annual Income (k$)",
                  "Spending Score (1-100)", "Cluster", "Segment"]].to_dict(orient="records")
}
with open("segmentation_data.json", "w") as f:
    json.dump(export, f, indent=2)

df.to_csv("customers_clustered.csv", index=False)
print("\nExported segmentation_data.json and customers_clustered.csv")
