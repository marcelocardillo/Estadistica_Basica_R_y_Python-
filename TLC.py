import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def TLC(poblacion, n_muestra, num_muestras):
    promedios = np.empty(num_muestras)
    medias_acumuladas = np.empty(num_muestras)
    errores_estandar = np.empty(num_muestras)

    for i in range(num_muestras):
        muestra = np.random.choice(poblacion, size=n_muestra, replace=False)
        promedios[i] = np.mean(muestra)
        medias_acumuladas[i] = np.mean(promedios[:i+1])

        # Calcular el error estándar
        errores_estandar[i] = np.std(promedios[:i+1]) / np.sqrt(i + 1)

    # Gráfico de líneas
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.plot(range(1, num_muestras + 1), medias_acumuladas, color="blue")
    plt.xlabel("Número de Simulación")
    plt.ylabel("Media Acumulada")
    plt.axhline(np.mean(poblacion), color="red", linestyle="--", linewidth=2)

    # Agregar líneas punteadas para el error estándar
    plt.plot(range(1, num_muestras + 1), medias_acumuladas + errores_estandar, color="green", linestyle="--")
    plt.plot(range(1, num_muestras + 1), medias_acumuladas - errores_estandar, color="green", linestyle="--")

    # Gráfico de densidad de la población
    plt.subplot(122)
    plt.hist(poblacion, density=True, color="blue", alpha=0.5)
    
    # Agregar una etiqueta con la media de la población
    media_poblacion = np.mean(poblacion)
    plt.text(media_poblacion, 0.03, f"Media poblacional = {round(media_poblacion, 2)}", color="red")

    # Agregar una línea punteada para la media de la población
    plt.axvline(media_poblacion, color="red", linestyle="--")
    
    st.pyplot(plt)

# Interfaz de Streamlit
st.title("Simulación del Teorema Central del Límite")

# Opciones interactivas para el usuario
n_muestra = st.slider("Tamaño de la muestra (entre 1 y 100)", min_value=1, max_value=100, value=30)
num_muestras = st.number_input("Número de muestras (entre 10 y 10,000)", min_value=10, max_value=10000, value=1000)

poblacion = np.random.poisson(lam=3, size=1000)  # Ejemplo de una población Poisson

# Agregar un botón para iniciar la simulación
if st.button("Ejecutar Simulación"):
    TLC(poblacion, n_muestra, num_muestras)
