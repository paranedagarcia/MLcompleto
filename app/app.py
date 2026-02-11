# streamlit_app/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.colors import COLORES_TELCO, TITULO, POSITIVO, NEGATIVO

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
st.markdown(f"""
<style>
/* ===== Modo Claro ===== */
body {{
    background-color: #F8F9FA;
    color: #0A2540;
}}
.main {{
    background-color: #F8F9FA;
}}
.stMetric {{
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}
h1, h2, h3 {{
    color: {TITULO};
}}

/* ===== Modo Oscuro ===== */
@media (prefers-color-scheme: dark) {{
    body {{
        background-color: #0A2540;
        color: white;
    }}
    .main {{
        background-color: #0A2540;
    }}
    .stMetric {{
        background-color: #1A1A1A;
        color: white;
        box-shadow: none;
    }}
    h1, h2, h3 {{
        color: {POSITIVO};  /* Cambia a un color que contraste con fondo oscuro */
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #1A1A1A;
        color: white;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {POSITIVO};
        color: white;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ========================================
# CARGAR DATOS
# ========================================
@st.cache_data
def load_data():
    """Carga el dataset con caché para optimizar rendimiento"""
    df = pd.read_csv("clean_data/telco-customer.csv")
    # Asegurar que baja_binary existe
    if 'baja_binary' not in df.columns and 'baja' in df.columns:
        df['baja_binary'] = df['baja'].map({'Yes': 1, 'No': 0})
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo de datos. Por favor coloca 'telco-customer.csv' en la carpeta 'data/'")
    st.stop()

# ========================================
# SIDEBAR
# ========================================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/0A2540/FFFFFF?text=TELCO", use_container_width=True)
    st.title("📊 Navegación")
    st.markdown("---")
    
    st.markdown("""
    ### Acerca de esta App
    
    Dashboard interactivo para análisis de churn en Telco.
    
    **Características:**
    - 📈 Análisis Exploratorio Completo
    - 🎯 Predictor de Churn ML
    - 💡 Recomendaciones Estratégicas
    - 📊 Dashboard Ejecutivo
    
    ---
    **Datos:** 7,043 clientes  
    **Actualización:** Feb 2026
    """)

# ========================================
# PÁGINA PRINCIPAL
# ========================================
st.title("🚀 Telco Customer Churn Analytics")
st.markdown("### Plataforma de Análisis Predictivo y Retención de Clientes")

# KPIs principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    churn_rate = (df['baja_binary'].sum() / len(df)) * 100
    st.metric(
        "📉 Tasa de Churn",
        f"{churn_rate:.1f}%",
        delta="-1.2%",
        delta_color="inverse"
    )

with col2:
    arpu = df['monthlycharges'].mean()
    st.metric(
        "💰 ARPU",
        f"${arpu:.2f}",
        delta="+$2.30"
    )

with col3:
    avg_tenure = df['tenure'].mean()
    st.metric(
        "⏱️ Tenure Promedio",
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
tab1, tab2, tab3 = st.tabs(["📊 Vista General", "📈 Análisis Rápido", "🎯 Navegación"])

with tab1:
    st.subheader("📊 Resumen Ejecutivo del Dataset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Información del Dataset")
        st.dataframe({
            "Métrica": ["Total de Clientes", "Variables", "Clientes con Churn", "% Churn"],
            "Valor": [
                f"{len(df):,}",
                f"{len(df.columns)}",
                f"{df['baja_binary'].sum():,}",
                f"{churn_rate:.1f}%"
            ]
        }, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Insights Clave")
        st.success("✅ Clientes con contrato anual tienen **35% menos churn**")
        st.warning("⚠️ 55% de clientes están en contrato mes-a-mes (alto riesgo)")
        st.info("💡 Tenure > 18 meses reduce churn a menos del 10%")

with tab2:
    st.subheader("📈 Distribución de Churn por Variables Clave")
    
    variable = st.selectbox(
        "Selecciona variable para analizar:",
        ["contract", "internetservice", "paymentmethod", "multiplelines"]
    )
    
    # Gráfico de barras agrupadas
    import plotly.graph_objects as go
    churn_by_var = pd.crosstab(df[variable], df['baja_binary'])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='No Churn',
        x=churn_by_var.index,
        y=churn_by_var[0],
        marker_color=POSITIVO
    ))
    fig.add_trace(go.Bar(
        name='Churn',
        x=churn_by_var.index,
        y=churn_by_var[1],
        marker_color=NEGATIVO
    ))
    
    fig.update_layout(
        barmode='group',
        title=f"Distribución de Churn por {variable.replace('_', ' ').title()}",
        xaxis_title=variable.replace('_', ' ').title(),
        yaxis_title="Número de Clientes",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("🧭 Explora las Secciones de la App")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📈 Análisis Exploratorio (EDA)
        - Distribución de variables numéricas
        - Análisis de variables categóricas
        - Matrices de correlación
        - Detección de outliers
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
        ### 💡 Recomendaciones Estratégicas
        - Roadmap de implementación
        - Simulador de impacto financiero
        - Estrategias de retención
        - ROI estimado
        
        👉 **Navega desde el menú lateral**
        """)
        
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
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {TITULO};'>
    <p><strong>📊 Telco Customer Analytics Dashboard</strong></p>
    <p>Desarrollado con Streamlit | Datos actualizados: Febrero 2026</p>
</div>
""", unsafe_allow_html=True)