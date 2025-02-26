import pyodbc
import pandas as pd

# Configuración de la conexión a SQL Server
def conectar_sql():
    conexion = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-6OTDB3M;"
        "DATABASE=Credi;"
        "UID=sa;"
        "PWD=Kukito0071;"
    )
    return conexion

# Función para cargar los datos desde SQL Server
def obtener_datos():
    conexion = conectar_sql()
    query = """
    SELECT TOP (1000) [Ingreso Mensual]
      ,[Deuda Total]
      ,[Historial de Pagos]
      ,[Cantidad de Créditos Activos]
      ,[Edad del Cliente]
      ,[Monto del Préstamo Solicitado]
      ,[Probabilidad de Incumplimiento]
      ,[Decisión Final]
  FROM [Credi].[dbo].[cliente]
    """
    df = pd.read_sql(query, conexion)
    conexion.close()
    
    # Convertimos la decisión final a valores numéricos (1 para "Sí", 0 para "No")
    
    df["Decisión Final"] = df["Decisión Final"].map({"Sí": 1, "No": 0})
    return df