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
        ["contract", "paymentmethod", "internetservice", "multiplelines",'seniorcitizen']
    )

     # ========================================
    # CASO ESPECIAL: SENIOR CITIZEN
    # ========================================
    if var_cat == "seniorcitizen":
        st.markdown("---")
        st.markdown("### 👴 Análisis Detallado: Senior Citizen vs Churn")
        
        # Preparar datos
        
     # Si es string: 'SeniorCitizen' / 'noSeniorCitizen'
        churn_by_senior = df.groupby(['seniorcitizen', 'baja_binary']).size().unstack(fill_value=0)
        senior_data = df[df['seniorcitizen'] == 'SeniorCitizen']['baja_binary'].value_counts().sort_index()
        no_senior_data = df[df['seniorcitizen'] == 'noSeniorCitizen']['baja_binary'].value_counts().sort_index()
        senior_labels = ['No Senior Citizen', 'Senior Citizen']
        
        # --- GRÁFICO 1: Barras Agrupadas ---
        st.markdown("#### 📊 Distribución de Churn por Senior Citizen")
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name='No Churn',
            x=senior_labels,
            y=churn_by_senior[0],
            marker_color=POSITIVO,
            text=churn_by_senior[0],
            textposition='auto',
        ))
        fig_bar.add_trace(go.Bar(
            name='Churn',
            x=senior_labels,
            y=churn_by_senior[1],
            marker_color=NEGATIVO,
            text=churn_by_senior[1],
            textposition='auto',
        ))
        
        fig_bar.update_layout(
            title="Cantidad de Clientes por Estado de Churn",
            xaxis_title="Senior Citizen",
            yaxis_title="Número de Clientes",
            barmode='group',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color=TITULO, size=12),
            height=450,
            showlegend=True,
            legend=dict(title="Estado", orientation="h", y=1.1, x=0.5, xanchor='center',itemclick=False,
            itemdoubleclick=False)
        )
        fig_bar.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig_bar.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # --- GRÁFICO 2: Pie Charts Comparativos ---
        st.markdown("#### 🥧 Proporción de Churn: Comparación Senior vs No Senior")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart: No Senior Citizen
            if len(no_senior_data) == 2:
                fig_pie_no_senior = go.Figure(data=[go.Pie(
                    labels=['No Churn', 'Churn'],
                    values=no_senior_data.values,
                    marker=dict(colors=[POSITIVO, NEGATIVO]),
                    textinfo='label+percent',
                    textfont=dict(size=13, color='white', family='Arial Black'),
                    hole=0.3,  # Donut chart
                    pull=[0, 0.1]  # Resaltar Churn
                )])
                
                fig_pie_no_senior.update_layout(
                    title=dict(
                        text="<b>No Senior Citizen</b>",
                        font=dict(size=16, color=TITULO),
                        x=0.5,
                        xanchor='center'
                    ),
                    showlegend=True,
                    height=400,
                    paper_bgcolor='white',
                    annotations=[dict(
                        text=f'Total<br>{no_senior_data.sum()}',
                        x=0.5, y=0.5,
                        font_size=14,
                        showarrow=False,
                        font=dict(color=TITULO)
                    )]
                )
                
                st.plotly_chart(fig_pie_no_senior, use_container_width=True)
            else:
                st.warning("⚠️ Solo hay una categoría en No Senior Citizen")
        
        with col2:
            # Pie Chart: Senior Citizen
            if len(senior_data) == 2:
                fig_pie_senior = go.Figure(data=[go.Pie(
                    labels=['No Churn', 'Churn'],
                    values=senior_data.values,
                    marker=dict(colors=[POSITIVO, NEGATIVO]),
                    textinfo='label+percent',
                    textfont=dict(size=13, color='white', family='Arial Black'),
                    hole=0.3,
                    pull=[0, 0.1]
                )])
                
                fig_pie_senior.update_layout(
                    title=dict(
                        text="<b>Senior Citizen</b>",
                        font=dict(size=16, color=TITULO),
                        x=0.5,
                        xanchor='center'
                    ),
                    showlegend=True,
                    height=400,
                    paper_bgcolor='white',
                    annotations=[dict(
                        text=f'Total<br>{senior_data.sum()}',
                        x=0.5, y=0.5,
                        font_size=14,
                        showarrow=False,
                        font=dict(color=TITULO)
                    )]
                )
                
                st.plotly_chart(fig_pie_senior, use_container_width=True)
            else:
                st.warning("⚠️ Solo hay una categoría en Senior Citizen")
        
        # --- INSIGHTS ---
        st.markdown("---")
        st.markdown("### 💡 Insights Clave")
        
        # Calcular tasas de churn
        if len(no_senior_data) == 2:
            churn_rate_no_senior = (no_senior_data[1] / no_senior_data.sum()) * 100
        else:
            churn_rate_no_senior = 0
        
        if len(senior_data) == 2:
            churn_rate_senior = (senior_data[1] / senior_data.sum()) * 100
        else:
            churn_rate_senior = 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Churn Rate - No Senior",
                f"{churn_rate_no_senior:.1f}%",
                delta=None
            )
        
        with col2:
            st.metric(
                "Churn Rate - Senior",
                f"{churn_rate_senior:.1f}%",
                delta=f"{churn_rate_senior - churn_rate_no_senior:+.1f}pp"
            )
        
        with col3:
            if churn_rate_senior > churn_rate_no_senior:
                risk_diff = churn_rate_senior - churn_rate_no_senior
                st.error(f"⚠️ Senior Citizens tienen **{risk_diff:.1f}pp** más riesgo de churn")
            else:
                st.success("✅ No hay diferencia significativa")
        
        # Conclusión
        st.info("""
        **📌 Conclusión:**
        
        Los clientes Senior Citizen muestran una tasa de churn diferente a los no-senior. 
        Esto sugiere que se deberían implementar estrategias de retención específicas para este segmento,
        como soporte técnico mejorado, interfaces simplificadas o programas de fidelización para adultos mayores.
        """)
    
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


    # Calcular la antigüedad promedio por estado de baja
    average_tenure_by_churn = (
        df
        .groupby('baja_binary')['tenure']
        .mean()
        .reset_index()
    )

    labels_baja = ['No Baja', 'Baja']

    fig_tenure = go.Figure()

    fig_tenure.add_trace(go.Bar(
        x=labels_baja,
        y=average_tenure_by_churn['tenure'],
        marker_color=[POSITIVO, NEGATIVO],
        text=average_tenure_by_churn['tenure'].round(1),
        textposition='auto',
        hovertemplate='Estado: %{x}<br>Antigüedad promedio: %{y:.1f} meses<extra></extra>'
    ))

    fig_tenure.update_layout(
        title="Antigüedad Promedio por Estado de Baja",
        xaxis_title="Estado de Baja",
        yaxis_title="Antigüedad Promedio (Meses)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO, size=12),
        height=450,
        showlegend=False
    )

    fig_tenure.update_yaxes(showgrid=True, gridcolor='lightgray')
    fig_tenure.update_xaxes(showgrid=False)

    st.plotly_chart(
        fig_tenure,
        use_container_width=True,
        config={"displayModeBar": False}
    )


    # Calcular cargos totales promedio por estado de baja
    average_total_charges_by_churn = (
        df
        .groupby('baja_binary')['totalcharges']
        .mean()
        .reset_index()
    )

    fig_charges = go.Figure()

    fig_charges.add_trace(go.Bar(
        x=labels_baja,
        y=average_total_charges_by_churn['totalcharges'],
        marker_color=[POSITIVO, NEGATIVO],
        text=average_total_charges_by_churn['totalcharges'].round(0),
        textposition='auto',
        hovertemplate='Estado: %{x}<br>Cargos promedio: $%{y:,.0f}<extra></extra>'
    ))

    fig_charges.update_layout(
        title="Cargos Totales Promedio por Estado de Baja",
        xaxis_title="Estado de Baja",
        yaxis_title="Cargos Totales Promedio",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO, size=12),
        height=450,
        showlegend=False
    )

    fig_charges.update_yaxes(showgrid=True, gridcolor='lightgray')
    fig_charges.update_xaxes(showgrid=False)

    st.plotly_chart(
        fig_charges,
        use_container_width=True,
        config={"displayModeBar": False}
    )


    

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