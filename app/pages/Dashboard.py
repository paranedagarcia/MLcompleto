import streamlit as st
import numpy as np
import pandas as pd

from utils.load_data import load_data
from utils.footer import load_footer
from utils.colors import THEME
from utils.charts import (
    create_pie_chart,
    create_churn_bar,
    create_histogram,
    create_avg_metric_bar,
)
from utils.layout import apply_global_style

st.set_page_config(page_title="Panel Ejecutivo - Telco", page_icon="📊", layout="wide")
apply_global_style()

df = load_data("../clean_data/telco-customer.csv")

if "totalcharges" in df.columns:
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")

st.title("📊 Panel Ejecutivo de Clientes")
st.markdown(
    "Análisis completo de **bajas de clientes**, perfil, servicios contratados y facturación."
)

# =========================
# FUNCIÓN FILTRO SIMPLE
# =========================
def select_todos(df, col, label):
    if col not in df.columns:
        return df

    options = ["Todos"] + sorted(df[col].dropna().unique().tolist())
    choice = st.sidebar.selectbox(label, options, key=f"sb_{col}")

    if choice == "Todos":
        return df
    return df[df[col] == choice]


# =========================
# BARRA LATERAL
# =========================
st.sidebar.title("🔎 Filtros")

df_f = df.copy()
df_f = select_todos(df_f, "contract", "Tipo de contrato")
df_f = select_todos(df_f, "internetservice", "Servicio de internet")
df_f = select_todos(df_f, "paymentmethod", "Método de pago")
df_f = select_todos(df_f, "paperlessbilling", "Factura electrónica")
df_f = select_todos(df_f, "seniorcitizen", "Cliente jubilado")
df_f = select_todos(df_f, "partner", "Tiene pareja")
df_f = select_todos(df_f, "dependents", "Tiene dependientes")

with st.sidebar.expander("🎚️ Filtros por rango"):
    if "tenure" in df.columns:
        tmin, tmax = int(df["tenure"].min()), int(df["tenure"].max())
        tenure_range = st.slider("Antigüedad (meses)", tmin, tmax, (tmin, tmax), key="tenure_slider")
        df_f = df_f[df_f["tenure"].between(*tenure_range)]

    if "monthlycharges" in df.columns:
        mcmin, mcmax = float(df["monthlycharges"].min()), float(df["monthlycharges"].max())
        monthly_range = st.slider(
            "Pago mensual ($)",
            float(round(mcmin, 2)),
            float(round(mcmax, 2)),
            (float(round(mcmin, 2)), float(round(mcmax, 2))),
            key="monthly_slider"
        )
        df_f = df_f[df_f["monthlycharges"].between(*monthly_range)]

if df_f.empty:
    st.warning("No hay datos con los filtros seleccionados.")
    st.stop()

# =========================
# MÉTRICAS PRINCIPALES
# =========================
total = len(df_f)
bajas = int(df_f["baja_binary"].sum())
tasa_baja = (bajas / total) * 100

ingreso_medio = df_f["monthlycharges"].mean()
antiguedad_media = df_f["tenure"].mean()

tasa_global = (df["baja_binary"].sum() / len(df)) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total clientes", f"{total:,}")
col2.metric("📉 Clientes que se dieron de baja", f"{bajas:,}")
col3.metric("🔥 Tasa de baja", f"{tasa_baja:.1f}%")
col4.metric("💰 Ingreso mensual promedio", f"${ingreso_medio:.2f}")

st.markdown("---")

# =========================
# SECCIONES
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Visión general",
    "🧩 Servicios contratados",
    "💳 Contrato y pagos",
    "👤 Perfil del cliente"
])

# =========================
# VISIÓN GENERAL
# =========================
with tab1:

    c1, c2 = st.columns(2)

    with c1:
        fig = create_pie_chart(df_f, color_by="baja_binary", title="Distribución de clientes (activos vs baja)", theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="pie_general")

    with c2:
        fig = create_churn_bar(df_f, "contract", theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="bar_contrato_general")

    c3, c4 = st.columns(2)

    with c3:
        fig = create_histogram(df_f, "tenure", title="Antigüedad según estado del cliente", theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="hist_antiguedad")

    with c4:
        fig = create_histogram(df_f, "monthlycharges", title="Pago mensual según estado del cliente", theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="hist_pago")

# =========================
# SERVICIOS
# =========================
with tab2:

    service_cols = [
        "internetservice", "phoneservice", "multiplelines",
        "onlinesecurity", "onlinebackup", "deviceprotection",
        "techsupport", "streamingtv", "streamingmovies"
    ]

    service_cols = [c for c in service_cols if c in df_f.columns]

    if service_cols:
        servicio = st.selectbox("Selecciona un servicio", service_cols, key="servicio_select")
        fig = create_churn_bar(df_f, servicio, theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="bar_servicio")

# =========================
# CONTRATO Y PAGOS
# =========================
with tab3:

    c1, c2 = st.columns(2)

    with c1:
        fig = create_churn_bar(df_f, "contract", theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="bar_contrato_tab3")

    with c2:
        fig = create_churn_bar(df_f, "paymentmethod", theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="bar_pago_tab3")

    c3, c4 = st.columns(2)

    with c3:
        fig = create_churn_bar(df_f, "paperlessbilling", theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="bar_factura")

    with c4:
        fig = create_avg_metric_bar(
            df_f,
            metric_col="monthlycharges",
            title="Ingreso mensual promedio por estado",
            yaxis_title="$",
            is_currency=True,
            theme=THEME
        )
        st.plotly_chart(fig, use_container_width=True, key="avg_pago_tab3")

# =========================
# PERFIL
# =========================
with tab4:

    perfil_cols = ["gender", "seniorcitizen", "partner", "dependents"]
    perfil_cols = [c for c in perfil_cols if c in df_f.columns]

    if perfil_cols:
        variable = st.selectbox("Selecciona variable de perfil", perfil_cols, key="perfil_select")
        fig = create_churn_bar(df_f, variable, theme=THEME)
        st.plotly_chart(fig, use_container_width=True, key="bar_perfil")

st.markdown("---")
load_footer()
