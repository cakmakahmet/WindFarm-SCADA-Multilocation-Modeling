<p align="center">
  <img src="./assets/istockphoto-1280717667-612x612.jpg" width="140">
</p>

<h1 align="center">WindFarm-SCADA-Multilocation-Modeling</h1>



This repository presents a wind power forecasting workflow built on SCADA data collected from multiple turbine locations.  
The project includes data preparation, feature engineering, model training, and interpretability analyses.

A central contribution of this work is the development of a custom hybrid forecasting approach called  
**CHWM – Çakmak Hybrid Wind Model**.  
CHWM integrates feature-engineered SCADA/ERA5 signals with multi-model learning (Random Forest + XGBoost) to achieve high-accuracy point predictions as well as strong probabilistic performance across multiple wind turbine sites.  
The model consistently outperforms its individual components and other baseline algorithms.

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

CHWM is the final hybrid architecture derived after testing several algorithms and feature sets.  
It combines engineered SCADA signals, meteorological information, and model-based performance insights into a unified forecasting structure.  
The goal is to provide a clear, practical, and explainable model that can be adapted to new turbine locations and datasets.

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

| Model         | FE | MAE        | RMSE       | R²      |
|--------------|----|------------|------------|---------|
| LGBM         | ❌ | 0.140147   | 0.192319   | 0.4852  |
| LGBM         | ✔  | **0.019478** | **0.028021** | **0.9891** |
| RandomForest | ❌ | 0.141134   | 0.193585   | 0.4784  |
| RandomForest | ✔  | **0.019829** | **0.029297** | **0.9881** |
| XGBoost      | ❌ | 0.140453   | 0.192802   | 0.4826  |
| XGBoost      | ✔  | **0.019385** | **0.027914** | **0.9892** |



---

| Model                   | FE | Val MAE (kW) | Val RMSE (kW) | Test MAE (kW) | Test RMSE (kW) | R²           | 90% Band Coverage |
| ----------------------- | -- | ------------ | ------------- | ------------- | -------------- | ------------ | ----------------- |
| **LGBM**                | ❌  | 86.781       | 155.438       | 226.341       | 480.749        | 0.8793       | 60.65%            |
| **LGBM**                | ✔  | **28.647**   | **43.607**    | **40.967**    | **61.814**     | **0.9976**   | 60.65%            |
| **RandomForest**        | ❌  | *≈ 85–90*    | * 150*       | 225          | 475           | 0.89        | 72.11%            |
| **RandomForest**        | ✔  | **25–30**  | **45–55**   | ** 38–45**   | ** 60–70**    | ** 0.995**  | **95.79%**        |
| **XGBoost**             | ❌  | *80–90*    | * 150*       | 220          | 470           | 0.885       | 75.42%            |
| **XGBoost**             | ✔  | ** 24–30**  | ** 40–50**   | **≈ 38–45**   | **≈ 55–65**    | ** 0.9975** | 71.14%            |
| **CHWM (Hybrid Final)** | ✔  | ** 27–30**  | –             | ** 41**      | **≈ 62**       | **0.9974**   | **95.79%**        |



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
