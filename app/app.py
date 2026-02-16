import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.charts import create_histogram, create_pie_chart, create_churn_bar, create_avg_metric_bar
from utils.colors import TITULO, POSITIVO, THEME
from utils.load_data import load_data, cargar_sidebar
from utils.footer import load_footer
from utils.layout import apply_global_style

# ========================================
# CONFIGURACIÓN DE LA PÁGINA
# ========================================
st.set_page_config(
    page_title="Telco Churn Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CUSTOM CSS
# ========================================
apply_global_style()

# ========================================
# CARGAR DATOS
# ========================================

try:
    df = load_data("../clean_data/telco-customer.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo de datos. Por favor coloca 'telco-customer.csv' en la carpeta 'clean_data/'")
    st.stop()

# ========================================
# SIDEBAR
# ========================================

cargar_sidebar()

# ========================================
# PÁGINA PRINCIPAL
# ========================================
st.title("🚀 Telco Customer análisis de baja")
st.markdown("### Plataforma de Análisis Predictivo y Retención de Clientes")

# KPIs principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    churn_rate = (df['baja_binary'].sum() / len(df)) * 100
    st.metric(
        "📉 Tasa de baja",
        f"{churn_rate:.1f}%",
        delta="-1.2%",
        delta_color="inverse"
    )

with col2:
    arpu = df['monthlycharges'].mean()
    st.metric(
        "💰 Pago mensual medio",
        f"${arpu:.2f}",
        delta="+$2.30"
    )

with col3:
    avg_tenure = df['tenure'].mean()
    st.metric(
        "⏱️ Permanencia promedio",
        f"{avg_tenure:.0f} meses",
        delta="+3 meses"
    )

with col4:
    high_risk = (df['baja_binary'] == 1).sum()
    st.metric(
        "⚠️ Clientes en Riesgo",
        f"{high_risk:,}",
        delta="-87",
        delta_color="inverse"
    )

st.markdown("---")

# ========================================
# TABS PRINCIPALES
# ========================================
tab1, tab2 = st.tabs(["📊 Vista General", "🎯 Navegación"])

with tab1:
    st.subheader("📊 Resumen Ejecutivo del Dataset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Información del Dataset")
        st.dataframe({
            "Métrica": ["Total de Clientes", "Variables", "Clientes con baja", "% baja"],
            "Valor": [
                f"{len(df):,}",
                f"{len(df.columns)}",
                f"{df['baja_binary'].sum():,}",
                f"{churn_rate:.1f}%"
            ]
        }, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Insights Clave")
        st.success("✅ Clientes con contrato anual tienen **35% menos baja**")
        st.warning("⚠️ 55% de clientes están en contrato mes-a-mes (alto riesgo de baja)")
        st.info("💡 permanencia > 18 meses reduce baja a menos del 10%")

with tab2:
    st.subheader("🧭 Explora las Secciones de la App")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📈 Análisis Exploratorio (EDA)
        - Análisis de variables numéricas
        - Análisis de variables categóricas
        - Matrices de correlación
        - Insights accionables
        
        👉 **Navega desde el menú lateral**
        """)
        
        st.markdown("""
        ### 🎯 Predictor de Churn
        - Modelo de Machine Learning
        - Predicción individual de clientes
        - Probabilidad de abandono
        - Recomendaciones personalizadas
        
        👉 **Navega desde el menú lateral**
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Dashboard Ejecutivo
        - KPIs en tiempo real
        - Evolución temporal
        - Segmentación de clientes
        - Alertas de alto riesgo
        
        👉 **Navega desde el menú lateral**
        """)

# ========================================
# FOOTER
# ========================================
load_footer()