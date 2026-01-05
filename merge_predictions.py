# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Wind Power Results Dashboard", layout="wide")
st.title("Wind Power Forecast — Results Dashboard")

# =========================================================
# 1) BURAYA SADECE SONUÇLARINI YAPIŞTIR
# Her satır = 1 deney (Model + FE + Dataset + Val/Test metrikleri + (opsiyonel) Coverage/BandWidth)
# Not: coverage (%) ise 82.0 gibi yaz (yüzde), band width kW ise sayı.
# =========================================================
SONUCLAR = [
    # =========================
    # NORMALIZED DATASET (Table I)
    # (Val metrikleri yok → None bıraktım, Test metriklerine yazdım)
    # =========================
    {"dataset":"Normalized", "model":"LGBM", "fe":0,
     "test_mae":0.14, "test_rmse":0.192, "test_r2":0.485,
     "coverage":None, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Normalized", "model":"LGBM", "fe":1,
     "test_mae":0.019, "test_rmse":0.028, "test_r2":0.989,
     "coverage":None, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Normalized", "model":"Random Forest", "fe":0,
     "test_mae":0.141, "test_rmse":0.194, "test_r2":0.478,
     "coverage":None, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Normalized", "model":"Random Forest", "fe":1,
     "test_mae":0.02, "test_rmse":0.029, "test_r2":0.988,
     "coverage":None, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Normalized", "model":"XGBoost", "fe":0,
     "test_mae":0.14, "test_rmse":0.193, "test_r2":0.483,
     "coverage":None, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Normalized", "model":"XGBoost", "fe":1,
     "test_mae":0.019, "test_rmse":0.028, "test_r2":0.989,
     "coverage":None, "band_width_mean":None, "band_width_median":None},

    # =========================
    # YALOVA DATASET (Table II)
    # =========================
    {"dataset":"Yalova", "model":"LGBM", "fe":0,
     "val_mae":91.8, "val_rmse":164.4, "val_r2":None,
     "test_mae":162.3, "test_rmse":258.3, "test_r2":0.95,
     "coverage":66.3, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Yalova", "model":"LGBM", "fe":1,
     "val_mae":66.8, "val_rmse":100.5, "val_r2":None,
     "test_mae":96.7, "test_rmse":158.7, "test_r2":0.98,
     "coverage":82.6, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Yalova", "model":"Random Forest", "fe":0,
     "val_mae":69.1, "val_rmse":138.0, "val_r2":None,
     "test_mae":129.7, "test_rmse":237.4, "test_r2":0.96,
     "coverage":67.3, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Yalova", "model":"Random Forest", "fe":1,
     "val_mae":83.6, "val_rmse":118.3, "val_r2":None,
     "test_mae":127.4, "test_rmse":205.4, "test_r2":0.97,
     "coverage":91.2, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Yalova", "model":"XGBoost", "fe":0,
     "val_mae":96.8, "val_rmse":169.0, "val_r2":None,
     "test_mae":169.3, "test_rmse":262.3, "test_r2":0.95,
     "coverage":53.5, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Yalova", "model":"XGBoost", "fe":1,
     "val_mae":65.9, "val_rmse":99.5, "val_r2":None,
     "test_mae":95.45, "test_rmse":159.5, "test_r2":0.98,
     "coverage":74.2, "band_width_mean":None, "band_width_median":None},

    {"dataset":"Yalova", "model":"CHWM (Hybrid)", "fe":1,
     "val_mae":65.7, "val_rmse":99.0, "val_r2":None,
     "test_mae":94.9, "test_rmse":159.0, "test_r2":0.98,
     "coverage":86.4, "band_width_mean":None, "band_width_median":None},
]

# =========================================================
# 2) DataFrame
# =========================================================
df = pd.DataFrame(SONUCLAR)

required_cols = ["dataset","model","fe","val_mae","val_rmse","val_r2","test_mae","test_rmse","test_r2","coverage","band_width_mean","band_width_median"]
for c in required_cols:
    if c not in df.columns:
        df[c] = None

df["fe"] = df["fe"].astype(int)
df["FE"] = df["fe"].map({1:"FE=1", 0:"FE=0"})

# =========================================================
# 3) Filtreler
# =========================================================
st.sidebar.header("Filtreler")

datasets = ["(All)"] + sorted(df["dataset"].dropna().astype(str).unique().tolist())
models = ["(All)"] + sorted(df["model"].dropna().astype(str).unique().tolist())

sel_dataset = st.sidebar.selectbox("Dataset", datasets, index=0)
sel_model = st.sidebar.selectbox("Model", models, index=0)

fe_mode = st.sidebar.radio("FE seçimi", ["Hepsi", "Sadece FE=1", "Sadece FE=0"], index=0)

metric_block = st.sidebar.radio("Hangi blok?", ["TEST", "VAL"], index=0)
metric_name = st.sidebar.selectbox("Metrik", ["MAE", "RMSE", "R2", "Coverage", "BandWidth Mean", "BandWidth Median"], index=0)

view_mode = st.sidebar.radio("Görünüm", ["Tablo + Grafik", "Sadece Tablo", "Sadece Grafik"], index=0)

work = df.copy()
if sel_dataset != "(All)":
    work = work[work["dataset"].astype(str) == sel_dataset]
if sel_model != "(All)":
    work = work[work["model"].astype(str) == sel_model]
if fe_mode == "Sadece FE=1":
    work = work[work["fe"] == 1]
elif fe_mode == "Sadece FE=0":
    work = work[work["fe"] == 0]

# =========================================================
# 4) Özet Kartlar
# =========================================================
# Kartlarda seçilen blokta (VAL/TEST) MAE/RMSE/R2 gösterelim
def safe_mean(s):
    s = pd.to_numeric(s, errors="coerce")
    return float(s.mean()) if s.notna().any() else None

if metric_block == "TEST":
    k_mae, k_rmse, k_r2 = "test_mae","test_rmse","test_r2"
else:
    k_mae, k_rmse, k_r2 = "val_mae","val_rmse","val_r2"

c1, c2, c3, c4 = st.columns(4)
c1.metric(f"{metric_block} MAE (kW)",  f"{safe_mean(work[k_mae]):.2f}" if safe_mean(work[k_mae]) is not None else "—")
c2.metric(f"{metric_block} RMSE (kW)", f"{safe_mean(work[k_rmse]):.2f}" if safe_mean(work[k_rmse]) is not None else "—")
c3.metric(f"{metric_block} R²",        f"{safe_mean(work[k_r2]):.4f}" if safe_mean(work[k_r2]) is not None else "—")
c4.metric("Kayıt Sayısı", f"{len(work)}")

# =========================================================
# 5) Tablo
# =========================================================
def table_df(dfx):
    cols_show = ["dataset","model","fe","FE",
                 "val_mae","val_rmse","val_r2",
                 "test_mae","test_rmse","test_r2",
                 "coverage","band_width_mean","band_width_median"]
    out = dfx[cols_show].copy()
    out = out.sort_values(["dataset","model","fe"])
    out = out.drop(columns=["fe"])  # ekranda fe görünmesin istiyorsan
    return out

# =========================================================
# 6) Grafik hazırlığı
# =========================================================
metric_map = {
    ("TEST","MAE"): "test_mae",
    ("TEST","RMSE"): "test_rmse",
    ("TEST","R2"): "test_r2",
    ("TEST","Coverage"): "coverage",
    ("TEST","BandWidth Mean"): "band_width_mean",
    ("TEST","BandWidth Median"): "band_width_median",
    ("VAL","MAE"): "val_mae",
    ("VAL","RMSE"): "val_rmse",
    ("VAL","R2"): "val_r2",
    ("VAL","Coverage"): "coverage",
    ("VAL","BandWidth Mean"): "band_width_mean",
    ("VAL","BandWidth Median"): "band_width_median",
}
ycol = metric_map[(metric_block, metric_name)]

plot_df = work.copy()
plot_df[ycol] = pd.to_numeric(plot_df[ycol], errors="coerce")
plot_df = plot_df.dropna(subset=[ycol])

# X ekseni: Model + FE birlikte görünsün
plot_df["label"] = plot_df["model"].astype(str) + " | " + plot_df["FE"].astype(str)

# =========================================================
# 7) Render
# =========================================================
if view_mode in ["Tablo + Grafik", "Sadece Tablo"]:
    st.subheader("Sonuç Tablosu")
    st.dataframe(table_df(work), use_container_width=True)

if view_mode in ["Tablo + Grafik", "Sadece Grafik"]:
    st.subheader(f"{metric_block} {metric_name} Grafiği")
    if plot_df.empty:
        st.warning("Seçilen filtrelerde bu metrik için veri yok (None olabilir).")
    else:
        fig = px.bar(
            plot_df,
            x="label",
            y=ycol,
            color="dataset",
            barmode="group",
            hover_data=["model","FE","dataset"]
        )
        fig.update_layout(xaxis_title="", yaxis_title=ycol, height=520)
        st.plotly_chart(fig, use_container_width=True)

st.caption("Not: Coverage/BandWidth sadece ilgili değerleri girersen görünür. Boş bırakırsan otomatik gizlenir.")
