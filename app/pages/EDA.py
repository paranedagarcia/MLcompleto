import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sys
import os
import plotly.graph_objects as go
from utils.footer import load_footer
from utils.load_data import cargar_sidebar, load_data, cargar_logo

# Agregar path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.colors import TITULO, POSITIVO, NEGATIVO, PRINCIPAL, THEME
from utils.charts import create_histogram, create_churn_bar, create_pie_chart, create_avg_metric_bar, create_correlation_heatmap

st.set_page_config(page_title="EDA - Telco", page_icon="📈", layout="wide")

df = load_data("../clean_data/telco-customer.csv")

cargar_sidebar()

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
        title=f"Distribución de {var_num_label} por baja",
        theme=THEME
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
        
    if var_num_dict == 'Permanencia': 
        st.markdown("""
                    Vemos que los clientes que se van (baja) tienen una permanencia promedio de 20 meses, mientras que los 
                    que se quedan (alta) tienen una permanencia promedio de 37 meses. 
                    Esto sugiere que la antigüedad es un factor protector clave contra la baja de clientes. 
                    """) 
    elif var_num_dict == 'Pago mensual': 
        st.markdown(""" 
                    Los clientes que se van (baja) tienen un pago mensual promedio de $70, mientras que los que se quedan (alta) 
                    tienen un pago mensual promedio de $60. Esto podría indicar que los clientes con cargos mensuales más altos 
                    son más propensos a abandonar, posiblemente debido a la percepción de menor valor o mayor fricción. 
                    """)
    else:
        st.markdown("""
                    Los clientes que se van (baja) suelen ser clientes mas nuevos, ya que a partir de que se paguen alrededor de 1500€
                    suelen darse menos de baja con respecto a los que menos tiempo llevan. 
                    """)
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
        # 2️⃣ PIE CHARTS COMPARATIVOS
        # ==============================
        col1, col2 = st.columns(2)

        df_no_senior = df[df['seniorcitizen'] == 'noSeniorCitizen']
        df_senior = df[df['seniorcitizen'] == 'SeniorCitizen']

        with col1:
            if not df_no_senior.empty:
                fig_pie_no = create_pie_chart(
                    df_no_senior,
                    color_by='baja_binary',
                    title="No jubilado",
                    theme=THEME
                )
                st.plotly_chart(fig_pie_no, use_container_width=True)
            else:
                st.warning("⚠️ No hay datos para No Senior Citizen")

        with col2:
            if not df_senior.empty:
                fig_pie_senior = create_pie_chart(
                    df_senior,
                    color_by='baja_binary',
                    title="Jubilado",
                    theme=THEME
                )
                st.plotly_chart(fig_pie_senior, use_container_width=True)
            else:
                st.warning("⚠️ No hay datos para Senior Citizen")
    
    fig = create_pie_chart(df, var_cat_map[var_cat], theme=THEME)
    st.plotly_chart(fig, use_container_width=True)
    
    fig = create_churn_bar(df, var_cat_map[var_cat], theme=THEME)
    st.plotly_chart(fig, use_container_width=True)
        
    if var_cat == "Jubilados":
        st.markdown("""
                    Otro factor que tenemos en cuenta es la edad. Vemos que los clientes jubilados tienen una tasa de baja 
                    de aproximadamente 30%, mientras que los no jubilados tienen una tasa de alrededor de 15%. 
                    Esto sugiere que los clientes mayores pueden ser más propensos a abandonar el servicio, 
                    posiblemente debido a necesidades cambiantes o menor adaptabilidad a nuevas tecnologías.
                    """)
    elif var_cat == "Tipo de contrato":
        st.markdown("""
                    Vemos que conforme mayor sea el tiempo de contrato, mayor es la proporción de clientes que se mantienen.
                    Esto sugiere que la antigüedad es un factor protector clave contra el churn. 
                    """)
    elif var_cat == "Tipo de internet":
        st.markdown("""
                    Los clientes con servicio de internet de fibra óptica tienen una tasa de baja significativamente mayor (40%)
                    en comparación con aquellos con internet DSL (20%) o sin servicio de internet (10%).
                    """)
    else:
        st.markdown("""
                    Vemos que los clientes con múltiples líneas de teléfono tienen una tasa de baja significativamente menor (10%) 
                    en comparación con aquellos sin múltiples líneas (30%).
                    """)

with tab3:
    st.subheader("🔗 Matriz de Correlación")

    # ==============================
    # 1️⃣ MATRIZ DE CORRELACIÓN
    # ==============================
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    corr_matrix = df[numeric_cols].corr()


    fig_corr = create_correlation_heatmap(
        corr_matrix=corr_matrix,
        theme=THEME
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    # ==============================
    # 2️⃣ ANTIGÜEDAD PROMEDIO
    # ==============================
    fig_tenure = create_avg_metric_bar(
        df,
        metric_col='tenure',
        title="Antigüedad Promedio por Estado",
        yaxis_title="Antigüedad Promedio (Meses)",
        theme=THEME
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
        is_currency=True,
        theme=THEME
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
    
load_footer()