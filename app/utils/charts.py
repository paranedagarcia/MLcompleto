# streamlit_app/utils/charts.py
import plotly.express as px
import plotly.graph_objects as go
from .colors import POSITIVO, NEGATIVO, PRINCIPAL, SECUNDARIO, TITULO

def create_histogram(df, column, color_by='baja_binary', title=None):
    """Crea histograma con colores corporativos y etiquetas amigables"""
    
    df_plot = df.copy()

    # Mapear valores binarios a etiquetas
    if color_by == 'baja_binary':
        df_plot[color_by] = df_plot[color_by].map({
            0: 'Alta',
            1: 'Baja'
        })
        color_map = {
            'Alta': POSITIVO,
            'Baja': NEGATIVO
        }
    else:
        color_map = None

    fig = px.histogram(
        df_plot,
        x=column,
        color=color_by,
        nbins=50,
        color_discrete_map=color_map,
        title=title or f"Distribución de {column}",
        labels={
            column: column.replace('_', ' ').title(),
            color_by: "Estado"
        }
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO),
        legend_title_text="Estado"
    )

    return fig

def create_pie_chart(df, color_by='baja_binary', title=None):
    """Crea gráfico tipo pie con colores corporativos y etiquetas amigables"""
    
    df_plot = df.copy()
    
    # Mapear valores binarios a etiquetas
    if color_by == 'baja_binary':
        df_plot[color_by] = df_plot[color_by].map({
            0: 'Alta',
            1: 'Baja'
        })
    
    fig = px.pie(
        df_plot,
        names=color_by,
        color=color_by,
        color_discrete_map={
            'Alta': POSITIVO,
            'Baja': NEGATIVO
        },
        title=title or "Distribución"
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

    churn_pct = pd.crosstab(
        df[category_col],
        df['baja_binary'],
        normalize='index'
    ) * 100

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Alta',
        x=churn_pct.index,
        y=churn_pct[0],
        marker_color=POSITIVO
    ))

    fig.add_trace(go.Bar(
        name='Baja',
        x=churn_pct.index,
        y=churn_pct[1],
        marker_color=NEGATIVO
    ))

    fig.update_layout(
        barmode='stack',
        title=title or f"Tasa de baja por {category_col}",
        yaxis_title="Porcentaje (%)",
        xaxis_title=category_col.replace('_', ' ').title(),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO)
    )

    return fig

def create_gauge_chart(value, title="Probabilidad de baja"):
    """Crea gauge chart para probabilidad de baja"""
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

def create_avg_metric_bar(df, metric_col, title=None, yaxis_title=None, is_currency=False):
    """Crea gráfico de barras para promedio de una métrica por estado de churn"""
    
    import pandas as pd

    avg_data = (
        df.groupby('baja_binary')[metric_col]
        .mean()
        .reset_index()
    )

    # Mapear etiquetas
    avg_data['Estado'] = avg_data['baja_binary'].map({
        0: 'Alta',
        1: 'Baja'
    })

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=avg_data['Estado'],
        y=avg_data[metric_col],
        marker_color=[POSITIVO, NEGATIVO],
        text=avg_data[metric_col].round(1 if not is_currency else 0),
        textposition='auto'
    ))

    fig.update_layout(
        title=title or f"Promedio de {metric_col}",
        xaxis_title="Estado",
        yaxis_title=yaxis_title or metric_col.replace('_', ' ').title(),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=TITULO),
        showlegend=False
    )

    return fig
