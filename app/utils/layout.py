import streamlit as st
from utils.colors import TITULO, POSITIVO

def apply_global_style():
    st.markdown(f"""
    <style>
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
            color: {POSITIVO};
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
