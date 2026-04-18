import pandas as pd
import matplotlib.pyplot as plt

file_path = "/Users/cynthiarabay/Desktop/ImageAnalysis/im2/expression_calls_with_coords.tsv"
df = pd.read_csv(file_path, sep="\t")

# Find coordinate columns
x_col = [c for c in df.columns if "Centroid X" in c][0]
y_col = [c for c in df.columns if "Centroid Y" in c][0]

# Define cell types
def assign_cell_type(row):
    cd68 = row["CD68_expr"] == "YES"
    cd163 = row["CD163_expr"] == "YES"
    fap = row["FAP_expr"] == "YES"
    ck = row["Cytokeratin_expr"] == "YES"

    if ck:
        return "Tumor / Epithelial"
    elif fap:
        return "Fibroblast / CAF"
    elif  cd163:
        return "CD163 "
    elif cd68:
        return "CD68"
    else:
        return "Other"

df["cell_type"] = df.apply(assign_cell_type, axis=1)

# Cell types to show
cell_types_to_plot = [
    "CD163 ",
    "CD68",
]

color_map = {
    "CD163 ": "hotpink",
    "CD68": "purple",
}

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(8, 8))
for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
for ax in axes:
    ax.set_aspect('equal')
axes = axes.flatten()
for ax, cell_type in zip(axes, cell_types_to_plot):
    subset = df[df["cell_type"] == cell_type]

    print(f"{cell_type}: {len(subset)} cells")

    # 🔹 plot ALL cells in gray (background)
    ax.scatter(
        df[x_col],
        df[y_col],
        s=2,
        alpha=0.15,
        c="lightgray"
    )

    # 🔹 highlight target cells
    ax.scatter(
        subset[x_col],
        subset[y_col],
        s=2,
        alpha=0.9,
        c=color_map[cell_type]
    )

    ax.invert_yaxis()
    ax.set_title(f"{cell_type}")
    ##ax.set_xlabel(x_col)
    ##ax.set_ylabel(y_col)

plt.tight_layout()
plt.show()