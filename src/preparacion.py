import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

COLUMNAS_RFM = ['Proximidad', 'Frecuencia', 'ValorMonetario']


def limpiar_datos(df):
    df = df.dropna(subset=['CodigoCliente'] + COLUMNAS_RFM)
    df = df.drop_duplicates(subset=['CodigoCliente'])

    print(f"Datos limpios. Filas: {len(df)}")
    return df


def validar_rfm(df):
    df = df[(df['Frecuencia'] >= 1) &
            (df['Proximidad'] >= 0) &
            (df['ValorMonetario'] >= 0)]
    print(f"Datos validados. Filas finales: {len(df)}")
    return df


def calcular_scores_rfm(df):

    df['Puntaje_Proximidad'] = pd.qcut(df['Proximidad'].rank(method='first', ascending=False),
                                       q=5, labels=[1, 2, 3, 4, 5], duplicates='drop').astype(int)
    df['Puntaje_Frecuencia'] = pd.qcut(df['Frecuencia'].rank(method='first'),
                                       q=5, labels=[1, 2, 3, 4, 5], duplicates='drop').astype(int)
    df['Puntaje_ValorMonetario'] = pd.qcut(df['ValorMonetario'].rank(method='first'),
                                           q=5, labels=[1, 2, 3, 4, 5], duplicates='drop').astype(int)

    df['Puntaje_RFM'] = (df['Puntaje_Proximidad'].astype(str) +
                         df['Puntaje_Frecuencia'].astype(str) +
                         df['Puntaje_ValorMonetario'].astype(str))

    print("Puntajes RFM (Proximidad, Frecuencia, ValorMonetario) calculados")
    return df


def preparar_para_clustering(df):
    X = df[COLUMNAS_RFM].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Datos RFM estandarizados para clustering")
    return X_scaled, scaler


def preparar_rfm_completo(df):

    df = limpiar_datos(df)
    df = validar_rfm(df)
    df = calcular_scores_rfm(df)

    X_scaled, scaler = preparar_para_clustering(df)

    return df, X_scaled, scaler
