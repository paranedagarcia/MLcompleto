import streamlit as st
import pandas as pd
import os
from typing import Callable, Optional


@st.cache_data
def load_data(
    relative_path: str,
    transform_func: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None
) -> pd.DataFrame:
    """
    Función genérica para cargar datasets (CSV, PKL, Parquet, JSON)
    con opción de transformación.

    Parameters
    ----------
    relative_path : str
        Ruta relativa desde la carpeta streamlit_app.
        Ejemplo: "clean_data/telco-customer.csv"

    transform_func : Callable, optional
        Función que recibe el dataframe y devuelve el dataframe transformado.

    Returns
    -------
    pd.DataFrame
    """

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, relative_path)

    # Detectar extensión y usar método adecuado
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
        # Asegurar que baja_binary existe
        if 'baja_binary' not in df.columns and 'baja' in df.columns:
            df['baja_binary'] = df['baja'].map({'Yes': 1, 'No': 0})
    elif ext == ".pkl":
        df = pd.read_pickle(file_path)
    else:
        raise ValueError(f"Formato de archivo no soportado: {ext}")

    # Aplicar transformación si existe
    if transform_func:
        df = transform_func(df)

    return df