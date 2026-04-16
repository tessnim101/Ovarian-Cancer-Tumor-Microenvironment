# Ovarian-Cancer-Tumor-Microenvironment

##  Project Overview

High-Grade Serous Ovarian Cancer (HGSOC) is the most aggressive form of ovarian cancer and is characterized by its dissemination within the peritoneal cavity, leading to peritoneal carcinomatosis. This mode of spread contributes to poor prognosis, treatment resistance, and limited therapeutic efficacy.

A key factor underlying this behavior is the **tumor microenvironment (TME)**, which consists of tumor cells, immune cells, stromal components, and vascular structures interacting in a spatially organized manner. Understanding the spatial architecture of the TME is essential to:

- identify tumor–immune interactions  
- characterize immune infiltration or exclusion  
- detect spatial heterogeneity  
- uncover mechanisms of therapy resistance (e.g., platinum resistance)  

Traditional transcriptomics lacks spatial resolution. In contrast, **spatial transcriptomics** allows us to map gene expression directly onto tissue sections, providing both molecular and spatial context.

---

## 🎯 Project Aims

This project aims to:

1. **Understand the disease context**
   - HGSOC progression in the peritoneal cavity  
   - Challenges of peritoneal carcinomatosis  
   - Role of the tumor microenvironment  

2. **Understand and leverage spatial transcriptomics data**
   - What information each data type provides  
   - Why spatial organization matters  

3. **Characterize the tumor microenvironment (TME)**
   - Identify immune and stromal components  
   - Define spatial regions within tumors  
   - Detect spatial heterogeneity  

4. **Link spatial patterns to biological mechanisms**
   - Tumor–immune interactions  
   - Potential resistance mechanisms  
   - Hypothetical patient comparisons  

5. **Extract biological insights**
   - Key spatial patterns  
   - Associations with aggressiveness or resistance  
   - Potential therapeutic implications  

---

##  Data Processing Pipeline

### 1. Raw Data Processing

Raw FASTQ files obtained from spatial transcriptomics experiments were processed using:

- **Space Ranger (10x Genomics)**

This step includes:
- alignment to the reference genome  
- barcode assignment  
- UMI counting  
- generation of spatially-resolved gene expression matrices  

The output of this step is a structured dataset containing:
- gene expression matrix (genes × spatial spots)  
- spatial coordinates of each spot  
- histological tissue images  

---

### 2. Downstream Analysis (Python)

The processed data was analyzed using Python-based tools such as:

- Scanpy  
- Squidpy  

The main steps include:
 

####  UMI Visualization
- Visualization of total UMI counts per spatial spot  
- Assessment of data quality and tissue coverage  

####  Clustering
- Dimensionality reduction (PCA)  
- Graph-based clustering (Leiden algorithm)  
- Identification of transcriptomically distinct regions  

####  UMAP Projection
- Visualization of transcriptomic similarity between spots  
- Exploration of global structure of the dataset  

####  Spatial Mapping
- Projection of clusters back onto the tissue  
- Identification of spatial domains (tumor, immune, stroma)  

---

