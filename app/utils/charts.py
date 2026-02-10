# streamlit_app/utils/charts.py
import plotly.express as px
import plotly.graph_objects as go
from .colors import POSITIVO, NEGATIVO, PRINCIPAL, SECUNDARIO, TITULO

def create_histogram(df, column, color_by='baja_binary', title=None):
    """Crea histograma con colores corporativos"""
    fig = px.histogram(
        df,
        x=column,
        color=color_by,
        nbins=50,
        color_discrete_map={0: POSITIVO, 1: NEGATIVO},
        title=title or f"Distribución de {column}",
        labels={column: column.replace('_', ' ').title()}
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO)
    )
    return fig

def create_churn_bar(df, category_col, title=None):
    """Crea gráfico de barras apiladas de churn por categoría"""
    import pandas as pd
    churn_pct = pd.crosstab(df[category_col], df['baja_binary'], normalize='index') * 100
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='No Churn',
        x=churn_pct.index,
        y=churn_pct[0],
        marker_color=POSITIVO
    ))
    fig.add_trace(go.Bar(
        name='Churn',
        x=churn_pct.index,
        y=churn_pct[1],
        marker_color=NEGATIVO
    ))
    
    fig.update_layout(
        barmode='stack',
        title=title or f"Tasa de Churn por {category_col}",
        yaxis_title="Porcentaje (%)",
        xaxis_title=category_col.replace('_', ' ').title(),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO)
    )
    return fig

def create_gauge_chart(value, title="Probabilidad de Churn"):
    """Crea gauge chart para probabilidad de churn"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': TITULO}},
        delta={'reference': 26.5, 'font': {'color': TITULO}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': TITULO},
            'bar': {'color': PRINCIPAL},
            'steps': [
                {'range': [0, 30], 'color': POSITIVO},
                {'range': [30, 70], 'color': NEGATIVO},
                {'range': [70, 100], 'color': "#FF4136"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='white',
        font={'color': TITULO}
    )
    return fig