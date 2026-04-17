import pandas as pd
import numpy as np

# ----------------------------------
# LOAD ORIGINAL QUPATH EXPORT
# ----------------------------------
file_path = "/Users/cynthiarabay/Desktop/ImageAnalysis/im2/data.csv.txt"
df = pd.read_csv(file_path, sep="\t")

print("Columns available:")
for c in df.columns:
    print(c)

# ----------------------------------
# FIND COORDINATE COLUMNS
# ----------------------------------
possible_x = [
    "Centroid X px", "Centroid X µm", "Centroid X um",
    "Nucleus: Centroid X px", "Nucleus: Centroid X µm", "Nucleus: Centroid X um",
    "Cell: Centroid X px", "Cell: Centroid X µm", "Cell: Centroid X um"
]

possible_y = [
    "Centroid Y px", "Centroid Y µm", "Centroid Y um",
    "Nucleus: Centroid Y px", "Nucleus: Centroid Y µm", "Nucleus: Centroid Y um",
    "Cell: Centroid Y px", "Cell: Centroid Y µm", "Cell: Centroid Y um"
]

x_col = next((c for c in possible_x if c in df.columns), None)
y_col = next((c for c in possible_y if c in df.columns), None)

if x_col is None or y_col is None:
    raise ValueError("Could not find centroid columns in the original QuPath file.")

print(f"\nUsing coordinates: {x_col}, {y_col}")

# ----------------------------------
# DEFINE MARKERS
# ----------------------------------
marker_cols = {
    "FOXP3": "Cell: FOXP3 mean",
    "CD68": "Cell: CD68 mean",
    "CD163": "Cell: CD163 mean",
    "FAP": "Cell: FAP mean",
    "CD8": "Cell: CD8 mean",
    "Cytokeratin": "Cell: Cytokeratin mean",
}
marker_cols = {k: v for k, v in marker_cols.items() if v in df.columns}

# ----------------------------------
# COMPUTE THRESHOLDS + YES/NO
# ----------------------------------
thresholds = {}

for marker, col in marker_cols.items():
    vals = pd.to_numeric(df[col], errors="coerce").dropna()
    thresholds[marker] = np.percentile(vals, 90)

for marker, col in marker_cols.items():
    vals = pd.to_numeric(df[col], errors="coerce")
    thr = thresholds[marker]
    df[f"{marker}_threshold_80"] = thr
    df[f"{marker}_expr"] = np.where(vals > thr, "YES", "NO")

    if marker=="cd163": 
        thresholds[marker] = np.percentile(vals, 80)

# ----------------------------------
# SAVE FULL SPATIAL TABLE
# ----------------------------------
keep_cols = [
    "Object ID",
    x_col,
    y_col,
]

keep_cols += [v for v in marker_cols.values()]
keep_cols += [f"{m}_threshold_80" for m in marker_cols.keys()]
keep_cols += [f"{m}_expr" for m in marker_cols.keys()]

keep_cols = [c for c in keep_cols if c in df.columns]

out_path = "/Users/cynthiarabay/Desktop/hackathon3/im2/expression_calls_with_coords.tsv"
df[keep_cols].to_csv(out_path, sep="\t", index=False)

print(f"\nSaved: {out_path}")