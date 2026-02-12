import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .colors import POSITIVO, NEGATIVO, PRINCIPAL, SECUNDARIO, TITULO, get_color_by_baja_binary, get_color_map, get_color_by_labels

def create_histogram(df, column, color_by='baja_binary', title=None, theme='light'):
    """Crea histograma con colores corporativos y etiquetas amigables"""
    
    df_plot = df.copy()

    # Mapear valores binarios a etiquetas
    if color_by == 'baja_binary':
        df_plot[color_by] = df_plot[color_by].map({
            0: 'Alta',
            1: 'Baja'
        })
        color_map = get_color_by_baja_binary()
    else:
        color_map = get_color_by_labels(df_plot[color_by].unique())

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

    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color=TITULO),
            legend_title_text="Estado"
        )

    return fig

def create_pie_chart(df, color_by='baja_binary', title=None, theme='light'):
    """Crea gráfico tipo pie con colores corporativos y etiquetas amigables"""
    
    df_plot = df.copy()
    
     # Mapear valores binarios a etiquetas
    if color_by == 'baja_binary':
        df_plot[color_by] = df_plot[color_by].map({
            0: 'Alta',
            1: 'Baja'
        })
        color_map = get_color_by_baja_binary()
    else:
        color_map = get_color_by_labels((df[color_by].unique()))
    
    fig = px.pie(
        df_plot,
        names=color_by,
        color=color_by,
        color_discrete_map=color_map,
        title=title or "Distribución"
    )
    
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color=TITULO)
        )
    
    return fig

def create_churn_bar(df, category_col, title=None, theme='light'):
    """Crea gráfico de barras apiladas de churn por categoría"""

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

    if theme == 'dark':
        fig.update_layout(
            barmode='stack',
            title=title or f"Tasa de baja por {category_col}",
            yaxis_title="Porcentaje (%)",
            xaxis_title=category_col.replace('_', ' ').title(),
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color=TITULO)
        )

    return fig

def create_gauge_chart(value, title="Probabilidad de baja", theme='light'):
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
    if theme == 'dark':
        fig.update_layout(
            paper_bgcolor='black',
            font={'color': TITULO}
        )
    return fig

def create_avg_metric_bar(df, metric_col, title=None, yaxis_title=None, is_currency=False, theme='light'):
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

    if theme == 'dark':
        fig.update_layout(
            title=title or f"Promedio de {metric_col}",
            xaxis_title="Estado",
            yaxis_title=yaxis_title or metric_col.replace('_', ' ').title(),
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color=TITULO),
            showlegend=False
        )

    return fig

def create_correlation_heatmap(corr_matrix, title=None, theme='light'):
    """Crea mapa de calor de correlación con soporte para modo claro/oscuro"""

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        aspect="auto",
        title=title or "Correlación entre Variables Numéricas"
    )

    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color=TITULO),
            coloraxis_colorbar=dict(
                tickfont=dict(color=TITULO),
                titlefont=dict(color=TITULO)
            )
        )

    return fig
