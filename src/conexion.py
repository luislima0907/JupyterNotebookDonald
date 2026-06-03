import pandas as pd
import pyodbc
import os


def conectar_bd(server, database, user=None, password=None):
    """
    Conecta a la base de datos SQL Server.
    Si user y password son None, usa autenticación de Windows.
    """
    try:

        if user is None or password is None:
            connection_string = (
                f"Driver={{ODBC Driver 18 for SQL Server}};"
                f"Server={server};"
                f"Database={database};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes;"
            )

        else:
            connection_string = (
                f"Driver={{ODBC Driver 18 for SQL Server}};"
                f"Server={server};"
                f"Database={database};"
                f"UID={user};"
                f"PWD={password};"
                f"TrustServerCertificate=yes;"
            )

        conexion = pyodbc.connect(connection_string)

        print(f"Conexion exitosa a {database} en {server}")

        return conexion

    except pyodbc.Error as e:
        print(f"Error en la conexion: {e}")
        return None

def ejecutar_query(conexion, query):
    """
    Ejecuta una consulta SQL y retorna un DataFrame.
    """
    try:
        df = pd.read_sql(query, conexion)
        print(f"Query ejecutada exitosamente. Filas obtenidas: {len(df)}")
        return df
    except Exception as e:
        print(f"Error al ejecutar la query: {e}")
        return None


def cargar_query_desde_archivo(ruta_sql):
    """
    Carga una consulta SQL desde un archivo.
    """
    try:
        with open(ruta_sql, 'r', encoding='utf-8') as archivo:
            query = archivo.read()
        return query
    except FileNotFoundError:
        print(f"Archivo SQL no encontrado: {ruta_sql}")
        return None


def guardar_csv(df, ruta_salida):
    """
    Guarda un DataFrame a CSV.
    """
    try:
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        df.to_csv(ruta_salida, index=False, encoding='utf-8')
        print(f"Archivo guardado en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar CSV: {e}")
