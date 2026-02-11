import streamlit as st
import pandas as pd
import os
from utils.colors import TITULO, POSITIVO, NEGATIVO
from utils.charts import create_gauge_chart
from utils.load_data import load_data  # ← función genérica que creamos

st.set_page_config(page_title="Predictor - Telco", page_icon="🎯", layout="wide")

st.title("🎯 Predictor de baja de cliente")
st.markdown("Predice la probabilidad de que un cliente abandone el servicio")
st.info("ℹ️ **Modelo ML utilizado**: XGBOOST")

# =========================
# 1️⃣ Cargar modelo
# =========================
model = load_data("../models/xgboost_model.pkl")  # ⚡ usa nuestra función genérica para cualquier archivo pkl

# =========================
# 2️⃣ Formulario de entrada
# =========================
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

# =========================
# 3️⃣ Predicción con ML
# =========================
if submitted:
    # Crear DataFrame con la misma estructura que usó el modelo
    input_df = pd.DataFrame([{
        "tenure": tenure,
        "monthlycharges": monthly_charges,
        "seniorcitizen": 1 if senior_citizen == "Yes" else 0,
        "contract": contract,
        "internetservice": internet_service,
        "multiplelines": multiple_lines,
        "paymentmethod": payment_method,
        "techsupport": tech_support,
        "streamingtv": streaming_tv
    }])

    # ⚠️ IMPORTANTE: Aplicar exactamente el mismo preprocesamiento que el entrenamiento
    # Si el modelo fue entrenado con OneHotEncoder:
    input_encoded = pd.get_dummies(input_df)

    # Asegurarse de que las columnas coincidan con las del modelo
    model_cols = model.get_booster().feature_names
    input_encoded = input_encoded.reindex(columns=model_cols, fill_value=0)

    # Obtener probabilidad de churn
    churn_prob = model.predict_proba(input_encoded)[0][1]

    # =========================
    # 4️⃣ Visualización del resultado
    # =========================
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
    
    # =========================
    # 5️⃣ Recomendaciones
    # =========================
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