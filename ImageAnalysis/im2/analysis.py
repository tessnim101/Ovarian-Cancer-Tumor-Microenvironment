import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# LOAD FILE
# -----------------------------
file_path = "/Users/cynthiarabay/Desktop/ImageAnalysis/im2/data.csv.txt"
df = pd.read_csv(file_path, sep="\t")

# -----------------------------
# SELECT MARKERS
# -----------------------------
marker_cols = [
    "Nucleus: FOXP3 mean",
    "Nucleus: CD68 mean",
    "Nucleus: CD163 mean",
    "Nucleus: FAP mean",
    "Nucleus: CD8 mean",
    "Nucleus: Cytokeratin mean",
]

# Keep only existing columns
marker_cols = [col for col in marker_cols if col in df.columns]

print("Using markers:", marker_cols)

# -----------------------------
# CREATE SUBPLOTS
# -----------------------------
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, col in enumerate(marker_cols):
    values = pd.to_numeric(df[col], errors="coerce").dropna()

    # Remove zeros (log scale can't handle 0)
    values = values[values > 0]

    # Optional: remove extreme outliers
    upper = np.percentile(values, 99.5)
    values = values[values <= upper]

    axes[i].hist(values, bins=100, log=True)
    axes[i].set_title(col)
    axes[i].set_xlabel("Mean intensity")
    axes[i].set_ylabel("Log(cell count)")

# Hide unused plots if needed
for j in range(len(marker_cols), len(axes)):
    axes[j].axis("off")

plt.tight_layout()
plt.show()
