import streamlit as st
import pandas as pd
import sqlite3
from PIL import Image

# Configuración de la base de datos
def crear_db():
    conn = sqlite3.connect('registros_imc.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, peso REAL, altura REAL, imc REAL, estado TEXT)''')
    conn.commit()
    conn.close()

def guardar_datos(nombre, peso, altura, imc, estado):
    conn = sqlite3.connect('registros_imc.db')
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (nombre, peso, altura, imc, estado) VALUES (?,?,?,?,?)", 
              (nombre, peso, altura, imc, estado))
    conn.commit()
    conn.close()

# Lógica de Categorización
def obtener_estado(imc):
    if imc < 18.5: return "Bajo Peso", "🔵"
    elif 18.5 <= imc < 24.9: return "Normal", "🟢"
    elif 25 <= imc < 29.9: return "Sobrepeso", "🟡"
    else: return "Obesidad", "🔴"

# Interfaz de Usuario
st.set_page_config(page_title="Gestor IMC Pro", layout="wide")
crear_db()

st.title("📊 Sistema de Gestión de IMC")

menu = ["Calcular / Alta", "Consultas y Modificación", "Reporte e Impresión"]
choice = st.sidebar.selectbox("Menú de Navegación", menu)

if choice == "Calcular / Alta":
    st.subheader("📝 Nuevo Registro")
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre del Paciente")
        peso = st.number_input("Peso (kg)", min_value=1.0, step=0.1)
        altura = st.number_input("Altura (m)", min_value=0.5, step=0.01)
        
        if st.button("Calcular y Guardar"):
            valor_imc = round(peso / (altura ** 2), 2)
            estado, emoji = obtener_estado(valor_imc)
            guardar_datos(nombre, peso, altura, valor_imc, estado)
            st.success(f"¡Guardado! IMC: {valor_imc} - {estado} {emoji}")

    with col2:
        st.info("Visualización de Parámetro")
        # Aquí se cargaría la imagen dinámicamente
        st.write("Representación visual según el rango detectado.")

elif choice == "Consultas y Modificación":
    st.subheader("🔍 Historial de Registros")
    conn = sqlite3.connect('registros_imc.db')
    df = pd.read_sql_query("SELECT * FROM usuarios", conn)
    st.dataframe(df, use_container_width=True)
    
    id_mod = st.number_input("ID del registro a eliminar/editar", step=1)
    if st.button("Eliminar Registro"):
        conn.execute(f"DELETE FROM usuarios WHERE id={id_mod}")
        conn.commit()
        st.warning("Registro eliminado.")
    conn.close()

elif choice == "Reporte e Impresión":
    st.subheader("🖨️ Generar Reporte")
    conn = sqlite3.connect('registros_imc.db')
    df = pd.read_sql_query("SELECT * FROM usuarios", conn)
    st.table(df)
    st.button("Imprimir (Ctrl + P)")
    conn.close()
	