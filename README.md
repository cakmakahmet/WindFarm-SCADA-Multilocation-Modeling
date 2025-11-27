<p align="center">
  <img src="./assets/istockphoto-1280717667-612x612.jpg" width="140">
</p>

<h1 align="center">WindFarm-SCADA-Multilocation-Modeling</h1>



This repository contains a wind power forecasting workflow built on SCADA data collected from multiple turbine locations.  
The project includes data preparation, feature engineering, model training, and interpretability analyses.

---

## Overview

The aim of this work is to develop a reproducible machine learning pipeline for wind turbine power prediction.  
The pipeline brings the following components together:

- Merging ERA5 meteorological data with SCADA signals  
- Constructing feature engineering steps (rolling statistics, lag features, turbulence metrics, density adjustments, etc.)  
- Training and evaluating multiple regression models (LGBM, XGBoost, RandomForest)  
- Comparing feature-engineered and non-engineered datasets  
- Interpreting model behaviour through SHAP value analysis  
- Selecting a final methodology referred to as **CHWM – Çakmak Hybrid Wind Model**

---

## CHWM – Çakmak Hybrid Wind Model

CHWM is the final version of the model obtained after testing several algorithms and feature sets.  
It combines engineered signals, meteorological information, and model selection findings into a single forecasting approach.

The intention is to provide a clear, practical, and explainable model structure that can be extended or adapted to new sites.

---

## Repository Structure

WindFarm-SCADA-Multilocation-Modeling/
│
├── chwm.py
├── lgbmfinal.py
├── xgboostfinal.py
├── randomforestfinal.py
│
├── SHAP for CHWM/
│ └── shap_for_chwm.png
│
├── LICENSE
├── .gitignore
└── README.md


## SHAP Analysis

SHAP plots are used to examine how individual features influence the predictions of the final CHWM model.

### Global Summary Plot


![SHAP Feature Value](./SHAP%20for%20CHWM/SHAP%20Feature%20Value.png)


This plot illustrates how different ranges of each feature influence the CHWM model’s output.
Higher SHAP values indicate a stronger positive contribution to predicted power, while lower
values represent a negative impact. The color gradient represents the actual feature values,
helping reveal non-linear patterns and how different feature intervals shape the model's
forecasting behavior.


---

## Model Performance

### 1) AllCombined Dataset (Normalized)

| Model               | FE | MAE        | RMSE       | R²      |
|--------------------|----|------------|------------|---------|
| LGBM               | ❌ | 0.140147   | 0.192319   | 0.4852  |
| LGBM               | ✔ | **0.019478** | **0.028021** | **0.9891** |
| RandomForest       | ❌ | 0.141134   | 0.193585   | 0.4784  |
| RandomForest       | ✔ | 0.019829   | 0.029297   | 0.9881  |
| XGBoost            | ❌ | 0.140453   | 0.192802   | 0.4826  |
| XGBoost            | ✔ | **0.019385** | **0.027914** | **0.9892** |
| **CHWM (Final)**   | ✔ | **0.019385** | **0.027914** | **0.9892** |

**CHWM (Çakmak Hybrid Wind Model)** is based on the best-performing feature-engineered model on the AllCombined dataset.

---

### 2) T1 Dataset (0–3600 kW → Normalized for Reporting)

| Model        | FE | MAE_norm | RMSE_norm | R²      | 90% Band Coverage |
|--------------|----|----------|-----------|---------|--------------------|
| LGBM         | ❌ | 0.06287  | 0.13354   | 0.8793  | 60.65% |
| LGBM         | ✔ | **0.01138** | **0.01717** | **0.9976** | 60.65% |
| RandomForest | ❌ | 0.05982  | 0.12757   | 0.8899  | 72.11% |
| RandomForest | ✔ | **0.01273** | **0.02374** | **0.9954** | **95.79%** |
| XGBoost      | ❌ | 0.06192  | 0.13038   | 0.8850  | 75.42% |
| XGBoost      | ✔ | **0.01063** | **0.01747** | **0.9975** | 71.14% |
| **CHWM (Final)** | ✔ | **0.01066** | **0.01786** | **0.9974** | **95.79%** |

**CHWM (T1)** corresponds to the hybrid combination model, using RF and XGB contributions.  
It achieves a **90% band coverage of 95.79%**, indicating strong reliability under uncertainty.

---

## Notes

- The repository does **not** include raw SCADA or ERA5 data.
- CHWM represents the finalized hybrid approach evaluated on both normalized and T1 datasets.
- Probabilistic band results are included for all T1 models, including CHWM.

---

## Contact

**Ahmet Melih Çakmak**  
GitHub: https://github.com/cakmakahmet
