import streamlit as st 
from Models.Models import evaluar_cliente


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=200) 


st.title("CREDICEFI - Evaluador de Credito")

ingreso = st.number_input("Ingreso Mensual", min_value=0)
deuda = st.number_input("Deuda Total", min_value=0)
historial = st.slider("Historial de Pagos (%)", 0, 100, 50)
creditos = st.number_input("Cantidad de Créditos Activos", min_value=0)
edad = st.number_input("Edad del Cliente", min_value=18)
monto_prestamo = st.number_input("Monto del Préstamo Solicitado", min_value=0)

if st.button("Evaluar Cliente"):
    resultado = evaluar_cliente(ingreso, deuda, historial, creditos, edad, monto_prestamo)
    st.write(f"📊 **Probabilidad de Aprobación:** {resultado['Probabilidad de Aprobación']:.2f}")
    st.write(f"🔍 **Decisión Final:** {resultado['Decisión']}")
    