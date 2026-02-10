# streamlit_app/pages/01_📈_EDA.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sys
import os

# Agregar path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.colors import TITULO, POSITIVO, NEGATIVO, PRINCIPAL
from utils.charts import create_histogram, create_churn_bar

st.set_page_config(page_title="EDA - Telco", page_icon="📈", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("clean_data/telco-customer.csv")
    if 'baja_binary' not in df.columns:
        df['baja_binary'] = df['baja'].map({'Yes': 1, 'No': 0})
    return df

df = load_data()

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
    
    var_num = st.selectbox(
        "Selecciona variable numérica:",
        ["tenure", "monthlycharges", "totalcharges"]
    )
    
    fig = create_histogram(df, var_num, title=f"Distribución de {var_num} por Churn")
    st.plotly_chart(fig, use_container_width=True)
    
    # Estadísticas comparativas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📊 No Churn")
        st.dataframe(df[df['baja_binary']==0][var_num].describe(), use_container_width=True)
    with col2:
        st.markdown("#### 📊 Churn")
        st.dataframe(df[df['baja_binary']==1][var_num].describe(), use_container_width=True)

with tab2:
    st.subheader("Análisis de Variables Categóricas")
    
    var_cat = st.selectbox(
        "Selecciona variable categórica:",
        ["contract", "paymentmethod", "internetservice", "multiplelines"]
    )
    
    fig = create_churn_bar(df, var_cat)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("🔗 Matriz de Correlación")
    
    # Matriz de correlación
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        aspect="auto",
        title="Correlación entre Variables Numéricas"
    )
    fig.update_layout(font=dict(color=TITULO))
    st.plotly_chart(fig, use_container_width=True)

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