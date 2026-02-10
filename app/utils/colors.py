# streamlit_app/utils/colors.py
"""
Paleta de colores corporativa Telco
"""

COLORES_TELCO = {
    'azul_profundo': '#0A2540',
    'azul_medio': '#1F6AE1',
    'celeste': '#4FA3FF',
    'verde_lima': '#2ED3A7',
    'naranja': '#FF9F43',
    'gris_neutro': '#E6E9EF'
}

# Aliases
POSITIVO = COLORES_TELCO['verde_lima']
NEGATIVO = COLORES_TELCO['naranja']
PRINCIPAL = COLORES_TELCO['azul_medio']
SECUNDARIO = COLORES_TELCO['celeste']
TITULO = COLORES_TELCO['azul_profundo']
FONDO = COLORES_TELCO['gris_neutro']

def get_color_map():
    """Retorna diccionario de colores para Plotly"""
    return {
        0: POSITIVO,  # No Churn
        1: NEGATIVO   # Churn
    }