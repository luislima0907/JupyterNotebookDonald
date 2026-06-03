import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt


def calcular_elbow(X_scaled, max_clusters=10):
    """
    Calcula la inercia para diferentes numeros de clusters (metodo Elbow).
    """
    inertias = []
    silhouette_scores = []
    K_range = range(2, max_clusters + 1)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    
    return K_range, inertias, silhouette_scores


def entrenar_kmeans(X_scaled, n_clusters=4):
    """
    Entrena modelo K-Means con el numero de clusters especificado.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    silhouette_avg = silhouette_score(X_scaled, clusters)
    davies_bouldin = davies_bouldin_score(X_scaled, clusters)
    
    print(f"K-Means entrenado con {n_clusters} clusters")
    print(f"Silhouette Score: {silhouette_avg:.3f}")
    print(f"Davies-Bouldin Index: {davies_bouldin:.3f}")
    
    return kmeans, clusters


def asignar_clusters(df, clusters):
    """
    Asigna los clusters al DataFrame original.
    """
    df['Cluster'] = clusters
    return df


def etiquetar_segmentos(df):
    """
    Etiqueta los clusters con nombres de negocio.
    """
    segmentos = {}
    
    for cluster_id in sorted(df['Cluster'].unique()):
        grupo = df[df['Cluster'] == cluster_id]
        monetary_mean = grupo['Monetary'].mean()
        
        if monetary_mean > df['Monetary'].quantile(0.75):
            etiqueta = "Alto Valor"
        elif monetary_mean > df['Monetary'].quantile(0.50):
            etiqueta = "Valor Medio"
        else:
            etiqueta = "Bajo Valor"
        
        segmentos[cluster_id] = etiqueta
    
    df['Segmento'] = df['Cluster'].map(segmentos)
    
    print("Segmentos etiquetados:")
    print(df.groupby('Segmento').size())
    
    return df, segmentos


def resumen_clusters(df):
    """
    Genera resumen estadistico por cluster.
    """
    resumen = df.groupby(['Cluster', 'Segmento']).agg({
        'Monetary': ['mean', 'min', 'max'],
        'CodigoCliente': 'count'
    }).round(2)
    
    resumen.columns = ['_'.join(col).strip() for col in resumen.columns.values]
    resumen = resumen.rename(columns={'CodigoCliente_count': 'Total_Clientes'})
    
    print("\nResumen por Cluster:")
    print(resumen)
    
    return resumen
