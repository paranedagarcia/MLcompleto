# streamlit_app/pages/01_📈_EDA.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sys
import os
import plotly.graph_objects as go

# Agregar path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.colors import TITULO, POSITIVO, NEGATIVO, PRINCIPAL
from utils.charts import create_histogram, create_churn_bar, create_pie_chart, create_avg_metric_bar
from utils.load_data import load_data

st.set_page_config(page_title="EDA - Telco", page_icon="📈", layout="wide")

df = load_data("../clean_data/telco-customer.csv")

# ========================================
# CONTENIDO
# ========================================
st.title("📈 Análisis Exploratorio de Datos (EDA)")
st.markdown("Exploración profunda del dataset de Telco Customer Churn")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Variables Numéricas",
    "📝 Variables Categóricas",
    "🔗 Correlaciones",
    "💡 Insights"
])

with tab1:
    st.subheader("Distribución de Variables Numéricas")

    # Diccionario: lo que se ve -> lo que existe en el CSV
    var_num_dict = {
        "Permanencia": "tenure",
        "Pago mensual": "monthlycharges",
        "Pago total": "totalcharges"
    }

    # Selectbox mostrando nombres amigables
    var_num_label = st.selectbox(
        "Selecciona variable numérica:",
        list(var_num_dict.keys())
    )

    # Columna real del dataframe
    var_num_col = var_num_dict[var_num_label]

    fig = create_histogram(
        df,
        var_num_col,
        title=f"Distribución de {var_num_label} por baja"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Estadísticas comparativas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Alta")
        st.dataframe(
            df[df['baja_binary'] == 0][var_num_col].describe(),
            use_container_width=True
        )

    with col2:
        st.markdown("#### 📊 Baja")
        st.dataframe(
            df[df['baja_binary'] == 1][var_num_col].describe(),
            use_container_width=True
        )

with tab2:
    st.subheader("Análisis de Variables Categóricas")
    
    var_cat = st.selectbox(
        "Selecciona variable categórica:",
        ["Tipo de contrato", "Tipo de internet", "Múltiples líneas de teléfono",'Jubilados']
    )
    
    var_cat_map = {
        "Tipo de contrato": "contract",
        "Tipo de internet": "internetservice",
        "Múltiples líneas de teléfono": "multiplelines",
        "Jubilados": "seniorcitizen",
    }

    # ========================================
    # CASO ESPECIAL: SENIOR CITIZEN
    # ========================================
    if var_cat == "Jubilados":
        st.markdown("---")
        st.markdown("### 👴 Análisis Detallado: Senior Citizen vs baja")

        # ==============================
        # 1️⃣ GRÁFICO BARRAS (usar tu método)
        # ==============================
        st.markdown("#### 📊 Distribución de baja por Senior Citizen")

        fig_bar = create_churn_bar(
            df,
            category_col="seniorcitizen",
            title="Tasa de baja por Senior Citizen"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        # ==============================
        # 2️⃣ PIE CHARTS COMPARATIVOS
        # ==============================
        st.markdown("#### 🥧 Proporción de baja: Comparación Senior vs No Senior")

        col1, col2 = st.columns(2)

        df_no_senior = df[df['seniorcitizen'] == 'noSeniorCitizen']
        df_senior = df[df['seniorcitizen'] == 'SeniorCitizen']

        with col1:
            if not df_no_senior.empty:
                fig_pie_no = create_pie_chart(
                    df_no_senior,
                    color_by='baja_binary',
                    title="No Senior Citizen"
                )
                st.plotly_chart(fig_pie_no, use_container_width=True)
            else:
                st.warning("⚠️ No hay datos para No Senior Citizen")

        with col2:
            if not df_senior.empty:
                fig_pie_senior = create_pie_chart(
                    df_senior,
                    color_by='baja_binary',
                    title="Senior Citizen"
                )
                st.plotly_chart(fig_pie_senior, use_container_width=True)
            else:
                st.warning("⚠️ No hay datos para Senior Citizen")

        # ==============================
        # 3️⃣ INSIGHTS (esto se mantiene igual)
        # ==============================

        st.markdown("---")
        st.markdown("### 💡 Insights Clave")

        senior_data = df_senior['baja_binary'].value_counts()
        no_senior_data = df_no_senior['baja_binary'].value_counts()

        churn_rate_no_senior = (
            (no_senior_data.get(1, 0) / no_senior_data.sum()) * 100
            if not no_senior_data.empty else 0
        )

        churn_rate_senior = (
            (senior_data.get(1, 0) / senior_data.sum()) * 100
            if not senior_data.empty else 0
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Porcentaje de baja - No Senior",
                f"{churn_rate_no_senior:.1f}%"
            )

        with col2:
            st.metric(
                "Porcentaje de baja - Senior",
                f"{churn_rate_senior:.1f}%",
                delta=f"{churn_rate_senior - churn_rate_no_senior:+.1f}pp"
            )

        with col3:
            if churn_rate_senior > churn_rate_no_senior:
                risk_diff = churn_rate_senior - churn_rate_no_senior
                st.error(f"⚠️ Senior Citizens tienen {risk_diff:.1f}pp más riesgo de baja")
            else:
                st.success("✅ No hay diferencia significativa")

        st.info("""
        **📌 Conclusión:**
        
        Los clientes Senior Citizen muestran una tasa de churn diferente a los no-senior. 
        Esto sugiere que se deberían implementar estrategias de retención específicas para este segmento.
        """)
    
    fig = create_churn_bar(df, var_cat_map[var_cat])
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("🔗 Matriz de Correlación")

    # ==============================
    # 1️⃣ MATRIZ DE CORRELACIÓN
    # ==============================
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    corr_matrix = df[numeric_cols].corr()

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        aspect="auto",
        title="Correlación entre Variables Numéricas"
    )

    fig_corr.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO)
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    # ==============================
    # 2️⃣ ANTIGÜEDAD PROMEDIO
    # ==============================
    fig_tenure = create_avg_metric_bar(
        df,
        metric_col='tenure',
        title="Antigüedad Promedio por Estado",
        yaxis_title="Antigüedad Promedio (Meses)"
    )

    st.plotly_chart(fig_tenure, use_container_width=True)

    # ==============================
    # 3️⃣ CARGOS TOTALES PROMEDIO
    # ==============================
    fig_charges = create_avg_metric_bar(
        df,
        metric_col='totalcharges',
        title="Cargos Totales Promedio por Estado",
        yaxis_title="Cargos Totales Promedio ($)",
        is_currency=True
    )

    st.plotly_chart(fig_charges, use_container_width=True)

with tab4:
    st.subheader("💡 Insights Clave del Análisis")
    
    st.success("### ✅ Factores Protectores (reducen churn)")
    st.markdown("""
    - **Contratos largos**: Clientes con contrato de 1-2 años tienen churn de 3-10% vs 45% mes-a-mes
    - **Antigüedad alta**: Tenure > 18 meses reduce churn dramáticamente
    - **Múltiples servicios**: Clientes con MultipleLines tienen 2x menos churn
    - **Alto gasto acumulado**: TotalCharges > $1,500 protege contra abandono
    """)
    
    st.error("### ⚠️ Factores de Riesgo (aumentan churn)")
    st.markdown("""
    - **Contrato mes-a-mes**: 45% de tasa de churn (factor crítico)
    - **Senior Citizens**: Correlación positiva +0.15
    - **Pago con cheque electrónico**: Mayor fricción = más abandono
    - **Cargos mensuales altos sin antigüedad**: Clientes nuevos con precios altos se van
    """)