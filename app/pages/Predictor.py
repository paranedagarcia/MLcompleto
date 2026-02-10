# streamlit_app/pages/02_🎯_Predictor.py
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.colors import TITULO, POSITIVO, NEGATIVO
from utils.charts import create_gauge_chart

st.set_page_config(page_title="Predictor - Telco", page_icon="🎯", layout="wide")

st.title("🎯 Predictor de Churn Individual")
st.markdown("Predice la probabilidad de que un cliente abandone el servicio")

st.info("ℹ️ **Modelo en desarrollo**: Esta versión usa reglas heurísticas. Próximamente se integrará modelo ML.")

# Formulario de entrada
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📋 Información Básica")
        tenure = st.slider("Antigüedad (meses)", 0, 72, 12)
        monthly_charges = st.number_input("Cargo Mensual ($)", 0.0, 200.0, 70.0, step=5.0)
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
    
    with col2:
        st.markdown("#### 📱 Servicios")
        contract = st.selectbox("Tipo de Contrato", ["Month-to-month", "One year", "Two year"])
        internet_service = st.selectbox("Servicio Internet", ["No", "DSL", "Fiber optic"])
        multiple_lines = st.selectbox("Múltiples Líneas", ["No", "Yes"])
    
    with col3:
        st.markdown("#### 💳 Pago y Adicionales")
        payment_method = st.selectbox(
            "Método de Pago",
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
        )
        tech_support = st.selectbox("Soporte Técnico", ["No", "Yes"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes"])
    
    submitted = st.form_submit_button("🔮 Predecir Probabilidad de Churn", type="primary")

if submitted:
    # Modelo heurístico simple (reemplazar con ML real)
    churn_prob = 0.26  # Base rate
    
    # Ajustes según reglas de negocio
    if contract == "Month-to-month":
        churn_prob += 0.20
    elif contract == "Two year":
        churn_prob -= 0.20
    
    if tenure < 12:
        churn_prob += 0.15
    elif tenure > 24:
        churn_prob -= 0.15
    
    if multiple_lines == "Yes":
        churn_prob -= 0.08
    
    if tech_support == "Yes":
        churn_prob -= 0.10
    
    if payment_method == "Electronic check":
        churn_prob += 0.10
    
    if senior_citizen == "Yes":
        churn_prob += 0.05
    
    # Limitar entre 0 y 1
    churn_prob = max(0, min(1, churn_prob))
    
    st.markdown("---")
    st.subheader("📊 Resultado de la Predicción")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = create_gauge_chart(churn_prob)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Interpretación")
        
        if churn_prob > 0.7:
            st.error("🔴 **RIESGO MUY ALTO**")
            risk_level = "crítico"
        elif churn_prob > 0.5:
            st.warning("🟠 **RIESGO ALTO**")
            risk_level = "alto"
        elif churn_prob > 0.3:
            st.info("🟡 **RIESGO MODERADO**")
            risk_level = "moderado"
        else:
            st.success("🟢 **RIESGO BAJO**")
            risk_level = "bajo"
        
        st.metric("Probabilidad de Churn", f"{churn_prob*100:.1f}%")
        st.metric("Nivel de Riesgo", risk_level.upper())
    
    # Recomendaciones
    st.markdown("---")
    st.subheader("💡 Acciones Recomendadas")
    
    if churn_prob > 0.5:
        st.markdown("""
        ### ⚠️ Plan de Retención de Alta Prioridad
        
        1. **🎁 Oferta Especial Inmediata**
           - Descuento del 25% en upgrade a contrato anual
           - 3 meses gratis de Streaming Premium
        
        2. **📞 Contacto Personal**
           - Asignar al equipo de retención VIP
           - Llamada dentro de 24 horas
        
        3. **💳 Incentivo de Pago**
           - Bono de $50 por cambio a pago automático
           - Facturación sin costos por 6 meses
        
        4. **📊 Seguimiento**
           - Encuesta de satisfacción personalizada
           - Check-in mensual durante 3 meses
        """)
    else:
        st.markdown("""
        ### ✅ Plan de Mantenimiento
        
        1. **🎁 Programa de Fidelidad**
           - Puntos por cada mes de permanencia
           - Descuentos en renovación
        
        2. **📧 Comunicación Proactiva**
           - Newsletter mensual con tips
           - Ofertas exclusivas para clientes leales
        
        3. **🆙 Upselling Suave**
           - Sugerir servicios complementarios
           - Promociones en bundles
        """)