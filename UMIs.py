import scanpy as sc
import squidpy as sq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path
path = "A1_NABHUG14_JAN26_merged_spaceranger/outs/binned_outputs/square_008um"


# Load data
adata = sc.read_visium(
    path=path,
    count_file="filtered_feature_bc_matrix.h5",
    load_images=False
)

adata.var_names_make_unique()


# QC metrics
adata.var["mt"] = adata.var_names.str.upper().str.startswith("MT-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)


# Load spatial coordinates
pos = pd.read_parquet(f"{path}/spatial/tissue_positions.parquet")
pos = pos.set_index("barcode")
pos = pos.loc[adata.obs_names]

adata.obs["in_tissue"] = pos["in_tissue"].values
adata.obsm["spatial"] = pos[["pxl_col_in_fullres", "pxl_row_in_fullres"]].to_numpy()


# Keep only tissue bins
adata = adata[adata.obs["in_tissue"] == 1].copy()


# Crop 
xy = adata.obsm["spatial"]
crop_mask = (
    (xy[:, 0] >= 0) & (xy[:, 0] <= 20000) &
    (xy[:, 1] >= 0) & (xy[:, 1] <= 17000)
)
adata = adata[crop_mask].copy()

# Cap total_counts at 95th percentile
p95_counts = np.percentile(adata.obs["total_counts"], 95)
adata.obs["total_counts_capped"] = adata.obs["total_counts"].clip(upper=p95_counts)

print(adata)
print(f"95th percentile total_counts = {p95_counts:.2f}")


# One spatial plot only
sq.pl.spatial_scatter(
    adata,
    color="total_counts_capped",
    img=False,
    size=0.1,
    shape=None,
    title="UMIs"
)
plt.gca().invert_yaxis()
plt.xlabel("")
plt.ylabel("")

plt.show()