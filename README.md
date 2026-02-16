# 🚀 Telco Customer Churn Prediction

<p align="center">
  <b>🔗 Aplicación en Producción:</b><br>
  <a href="https://proyecto-8-problema-de-clasificacion-eaty.onrender.com/" target="_blank">
    https://proyecto-8-problema-de-clasificacion-eaty.onrender.com/
  </a>
</p>

---

Proyecto de Machine Learning para predicción de baja en clientes Telco.


## 📌 Descripción General

Este proyecto desarrolla una solución completa de **Machine Learning** para predecir la **baja de clientes (Churn)** en una empresa de telecomunicaciones.

El sistema incluye:

- 📊 Análisis Exploratorio de Datos (EDA)
- 🧹 Proceso completo de ETL y Feature Engineering
- 🤖 Entrenamiento y evaluación de múltiples modelos de ML
- 📈 Dashboard interactivo desarrollado con Streamlit
- 🐳 Containerización con Docker
- ☁️ Despliegue en la nube (Render)

---

## 👩‍💻 Contribuyentes

  | Nombre           | GitHub | LinkedIn |
|------------------|--------|----------|
| Jaime Amuedo     | [![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/JaimeAmuedoJAH) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jaime-amuedo-hidalgo-a432bb354/) |
| Ruben Camacho    | [![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RubenCG1997) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ruben-camacho-gomez) |
| Pablo Rodríguez  | [![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PabloRodMu) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pablo-rodríguez-muñoz-357890185) |
| Andrés Pérez     | [![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/andresdatalyst) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andresproviraprogramador/) |

## 👥 Equipo de Trabajo

- **Rubén** — Product Owner  
- **Pablo** — Scrum Master  
- **Jaime** — Data Analyst  
- **Andrés** — Data Analyst  

---
# 🧠 Objetivo del Proyecto

Predecir si un cliente abandonará el servicio (**Churn = Yes/No**) utilizando variables demográficas, contractuales y de consumo.

El objetivo de negocio es:

- Reducir tasa de abandono
- Identificar clientes en riesgo
- Optimizar estrategias de retención
- Maximizar ingresos

---

# 🏗️ Arquitectura del Proyecto

El proyecto está organizado por ramas especializadas para trabajo colaborativo:

| Rama | Responsabilidad | Entregable Principal |
|------|-----------------|----------------------|
| `data-cleaning` | Limpieza y transformación | Dataset limpio |
| `exploratory-analysis` | EDA e insights | Visualizaciones |
| `machine-learning` | Modelado predictivo | Modelos entrenados |
| `dashboard-development` | Interfaz interactiva | App Streamlit |
| `deployment` | Docker + producción | Imagen desplegable |

---

# 📂 Estructura del Proyecto
```
Proyecto-8-Problema-de-clasificacion-Grupo-3/
│
├── README.md
├── requirements.txt
├── dockerfile
├── docker-compose.yml
│
├── app/
│ ├── app.py
│ ├── assets/
│ ├── pages/
│ │ ├── Dashboard.py
│ │ ├── EDA.py
│ │ └── Predictor.py
│ └── utils/
│ ├── charts.py
│ ├── colors.py
│ ├── footer.py
│ ├── layout.py
│ └── load_data.py
│
├── notebooks/
│ ├── data_cleaning.ipynb
│ ├── EDA.ipynb
│ └── ML.ipynb
│
├── clean_data/
│ └── telco-customer.csv
│
├── csv/
│ └── telco.csv
│
└── models/
└── *.pkl
```

---

# 📊 Notebooks del Proyecto

## 1️⃣ data_cleaning.ipynb — ETL y Feature Engineering

**Objetivo:** Transformar datos crudos en un dataset listo para modelado.

### Incluye:

- Carga de datos
- Análisis de valores faltantes
- Tratamiento de outliers
- Codificación de variables categóricas
- Normalización
- Creación de nuevas features
- Validación de calidad
- Exportación a `clean_data/telco-customer.csv`

**Tecnologías:** Pandas, NumPy, Seaborn

---

## 2️⃣ EDA.ipynb — Análisis Exploratorio

**Objetivo:** Identificar patrones relevantes asociados al churn.

### Análisis realizados:

- Estadísticas descriptivas
- Distribuciones univariantes
- Matriz de correlación
- Análisis multivariante
- Comparación clientes churn vs no churn
- Impacto de contratos, servicios y cargos

**Tecnologías:** Pandas, Matplotlib, Seaborn, Plotly

---

## 3️⃣ ML.ipynb — Modelado Predictivo

**Objetivo:** Construir y evaluar modelos de clasificación.

### Modelos entrenados:

- Regresión Logística
- KNN
- SVM
- Árbol de Decisión
- XGBoost (mejor desempeño)

### Evaluación:

- Matriz de confusión
- Precision, Recall, F1-Score
- ROC-AUC
- Curva ROC
- Cross Validation
- GridSearchCV

**Tecnologías:** Scikit-learn, XGBoost, Joblib

---

# 🖥️ Aplicación Web (Streamlit)

La app permite:

## 📈 Dashboard
- KPIs principales
- Tasa de churn
- Análisis por servicio
- Métricas clave

## 🔎 EDA Interactivo
- Visualizaciones dinámicas
- Análisis segmentado
- Correlaciones

## 🤖 Predictor
- Ingreso manual de datos
- Predicción individual
- Probabilidad de churn
- Recomendaciones básicas

---

# ⚙️ Instalación Local

### Clonar el repositorio
```
git clone https://github.com/Bootcamp-Data-Analyst/Proyecto-8-Problema-de-clasificacion-Grupo-3.git
```
### Crear entorno virtual
```bash
python -m venv venv
```
Activar entorno
```
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```
Instalar dependencias
```
pip install --upgrade pip
pip install -r requirements.txt
````
Ejecutar aplicación
```
streamlit run app/app.py
```
Acceder en:
```
http://localhost:8501
```
## Docker
Construir imagen
```
docker build -t telco-churn:latest .
```
Ejecutar imagen
```
docker run -p 8000:8000 telco-churn:latest
```
Acceder en:
```
http://localhost:8000
```
Comandos útiles
```
docker images
docker ps
docker stop <id>
docker logs <id>
docker-compose up
docker-compose down

```
# ☁️ Despliegue en Render

## 🚀 Pasos Generales

1. Subir el proyecto a GitHub  
2. Crear un **Web Service** en Render  
3. Seleccionar **Runtime: Docker**  
4. Configurar los siguientes parámetros:

| Campo | Valor |
|-------|--------|
| **Runtime** | Docker |
| **Build Command** | `docker build -t telco-churn .` |
| **Start Command** | `streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0` |

---

## 🌍 Resultado del Deploy

Después del despliegue obtendrás una URL:

https://proyecto-8-problema-de-clasificacion-eaty.onrender.com/


---

# 📦 Dependencias Principales
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)

- joblib
- missingno
- xgboost
- seaborn

---

# 🔐 Buenas Prácticas

- No subir datos sensibles al repositorio
- Utilizar `.gitignore` correctamente
- Configurar variables de entorno en producción
- HTTPS habilitado por defecto en Render

---

# 🤝 Flujo de Contribución

1. Crear nueva rama
2. Implementar cambios
3. Realizar commit descriptivo
4. Push a la rama remota
5. Crear Pull Request
6. Code Review
7. Merge a la rama principal

---

# 📄 Licencia

MIT License
