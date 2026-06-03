import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def limpiar_datos(df):
    """
    Limpia datos: elimina nulos, duplicados y valores extremos.
    """
    df = df.dropna(subset=['CodigoCliente', 'Monetary'])
    df = df.drop_duplicates(subset=['CodigoCliente'])
    
    print(f"Datos limpios. Filas: {len(df)}")
    return df


def validar_monetary(df):
    """
    Valida que los valores RFM sean validos
    """
    df = df[df['Monetary'] > 0]
    print(f"Datos validados. Filas finales: {len(df)}")
    return df


def calcular_monetary_score(df):
    """
    Calcula scores RFM en escalas de 1 a 5 para cada cliente
    """
    df['M_Score'] = pd.qcut(df['Monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    df['M_Score'] = df['M_Score'].astype(int)
    
    print("Score Monetario calculado")
    return df


def preparar_para_clustering(df):
    """
    Prepara los datos para K-means: selecciona columnas, estandariza y retorna matriz lista para clustering
    """
    X = df[['Monetary']].copy()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("Datos estandarizados para clustering")
    return X_scaled, scaler


def preparar_monetary_completo(df):
    """
    Ejecuta el pipeline de completo de preparación de datos para segmentación RFM
    """
    df = limpiar_datos(df)
    df = validar_monetary(df)
    df = calcular_monetary_score(df)
    
    X_scaled, scaler = preparar_para_clustering(df)
    
    return df, X_scaled, scaler
