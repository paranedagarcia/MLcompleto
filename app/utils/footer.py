import streamlit as st
from utils.colors import FONDO

# ========================================
# FOOTER
# ========================================
def load_footer():
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: {FONDO};'>
        <p><strong>📊 Telco Customer Analytics Dashboard</strong></p>
        <p>Desarrollado con Streamlit | Datos actualizados: Febrero 2026</p>
    </div>
    """, unsafe_allow_html=True)