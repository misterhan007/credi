import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from database import obtener_datos  # Importamos la función desde database.py

# Cargar los datos desde SQL Server
df = obtener_datos()

# Variables predictoras y variable objetivo
X = df[["Ingreso Mensual", "Deuda Total", "Historial de Pagos", "Cantidad de Créditos Activos", "Edad del Cliente", "Monto del Préstamo Solicitado"]]
y = df["Decisión Final"]

# División en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalado de datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entrenar modelo
modelo = LogisticRegression()
modelo.fit(X_train_scaled, y_train)

# Evaluar modelo
y_pred = modelo.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, modelo.predict_proba(X_test_scaled)[:, 1])

print(f"✅ Precisión del modelo: {accuracy:.2f}")
print(f"✅ Área bajo la curva (AUC): {auc:.2f}")

# Guardar modelo y escalador
joblib.dump(modelo, "modelo_regresion.pkl")
joblib.dump(scaler, "scaler.pkl")
print("✅ Modelo y escalador guardados exitosamente.")

# Función para evaluar clientes en tiempo real
def evaluar_cliente(ingreso, deuda, historial, creditos, edad, monto_prestamo):
    modelo_cargado = joblib.load("modelo_regresion.pkl")
    scaler_cargado = joblib.load("scaler.pkl")
    
    cliente_data = np.array([[ingreso, deuda, historial, creditos, edad, monto_prestamo]])
    cliente_data_scaled = scaler_cargado.transform(cliente_data)
    
    probabilidad_aprobacion = modelo_cargado.predict_proba(cliente_data_scaled)[:, 1][0]
    decision = "Aprobado" if probabilidad_aprobacion >= 0.5 else "Rechazado"
    
    return {"Probabilidad de Aprobación": probabilidad_aprobacion, "Decisión": decision}
