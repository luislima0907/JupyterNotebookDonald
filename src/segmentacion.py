import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt

MUESTRA_SILHOUETTE = 10000


def calcular_elbow(X_scaled, max_clusters=10):
    inertias = []
    silhouette_scores = []
    K_range = range(2, max_clusters + 1)
    sample_size = min(MUESTRA_SILHOUETTE, len(X_scaled))

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(
            silhouette_score(X_scaled, kmeans.labels_,
                             sample_size=sample_size, random_state=42))

    return K_range, inertias, silhouette_scores


def entrenar_kmeans(X_scaled, n_clusters=4):

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    sample_size = min(MUESTRA_SILHOUETTE, len(X_scaled))
    silhouette_avg = silhouette_score(X_scaled, clusters,
                                      sample_size=sample_size, random_state=42)
    davies_bouldin = davies_bouldin_score(X_scaled, clusters)

    print(f"K-Means entrenado con {n_clusters} clusters")
    print(f"Silhouette Score: {silhouette_avg:.3f}")
    print(f"Davies-Bouldin Index: {davies_bouldin:.3f}")

    return kmeans, clusters


def asignar_clusters(df, clusters):
    df['Cluster'] = clusters
    return df


def etiquetar_segmentos(df):

    perfil = df.groupby('Cluster').agg(
        Proximidad=('Proximidad', 'mean'),
        Frecuencia=('Frecuencia', 'mean'),
        ValorMonetario=('ValorMonetario', 'mean'),
    )

    m_mean_global = df['ValorMonetario'].mean()
    segmentos = {}

    # 1) Clusters de alto valor -> VIP.
    vip = perfil[perfil['ValorMonetario'] >= m_mean_global].index
    for cid in vip:
        segmentos[cid] = "Clientes VIP"

    # 2) Clusters restantes ordenados por proximidad (asc = mas reciente primero).
    restantes = perfil.drop(index=vip).sort_values('Proximidad').index.tolist()
    n = len(restantes)
    for posicion, cid in enumerate(restantes):
        if n == 1:
            etiqueta = "Clientes Regulares"
        elif posicion == 0:
            etiqueta = "Clientes Regulares"                     # el mas reciente
        elif posicion == n - 1:
            etiqueta = "Clientes en Riesgo de Abandono"         # el mas lejano
        else:
            etiqueta = "Clientes Esporadicos de Bajo Ticket"    # intermedios
        segmentos[cid] = etiqueta

    df['Segmento'] = df['Cluster'].map(segmentos)

    print("Segmentos etiquetados:")
    print(df.groupby('Segmento').size())

    return df, segmentos


def resumen_clusters(df):

    resumen = df.groupby(['Cluster', 'Segmento']).agg({
        'Proximidad': 'mean',
        'Frecuencia': 'mean',
        'ValorMonetario': 'mean',
        'CodigoCliente': 'count'
    }).round(2)

    resumen = resumen.rename(columns={
        'Proximidad': 'Proximidad_media',
        'Frecuencia': 'Frecuencia_media',
        'ValorMonetario': 'ValorMonetario_medio',
        'CodigoCliente': 'Total_Clientes'
    })

    print("\nResumen por Cluster (perfil RFM):")
    print(resumen)

    return resumen
