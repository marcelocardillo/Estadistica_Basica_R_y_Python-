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

    # Crear una figura con 3 subgráficos en una columna
    fig, axs = plt.subplots(3, 1, figsize=(8, 16))

    # Gráfico de líneas de la media acumulada
    axs[0].plot(range(1, num_muestras + 1), medias_acumuladas, color="blue")
    axs[0].set_xlabel("Número de Simulación")
    axs[0].set_ylabel("Media Acumulada")
    axs[0].axhline(np.mean(poblacion), color="red", linestyle="--", linewidth=2)
    axs[0].plot(range(1, num_muestras + 1), medias_acumuladas + errores_estandar, color="green", linestyle="--")
    axs[0].plot(range(1, num_muestras + 1), medias_acumuladas - errores_estandar, color="green", linestyle="--")

    # Gráfico de densidad de la población
    axs[1].hist(poblacion, density=True, color="blue", alpha=0.5)
    media_poblacion = np.mean(poblacion)
    axs[1].text(media_poblacion, 0.03, f"Media poblacional = {round(media_poblacion, 2)}", color="red")
    axs[1].axvline(media_poblacion, color="red", linestyle="--")

    # Histograma de las medias muestrales
    axs[2].hist(promedios, bins=20, color="purple", alpha=0.7)
    axs[2].set_xlabel("Medias Muestrales")
    axs[2].set_ylabel("Frecuencia")

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

# Interfaz de Streamlit
st.title("Simulación del Teorema Central del Límite")

# Opciones interactivas para el usuario
n_muestra = st.slider("Tamaño de la muestra (entre 1 y 100)", min_value=1, max_value=100, value=30)
num_muestras = st.number_input("Número de muestras (entre 10 y 10,000)", min_value=10, max_value=10000, value=1000)

poblacion = np.random.poisson(lam=3, size=1000)  # Ejemplo de una población Poisson

# Agregar un botón para iniciar la simulación
if st.button("Ejecutar Simulación"):
    TLC(poblacion, n_muestra, num_muestras)

st.write("La población es una distribución de Poisson de 1000 casos generada aleatoriamente. Se sugiere cambiar las condiciones del muestreo para observar diferentes escenarios. La línea punteada indica el valor de la media poblacional o verdadero valor del parámetro.")
st.write("Elaboración: Marcelo Cardillo, Profesor Adjunto de Métodos Cuantitativos, Facultad de Filosofía y Letras, Universidad de Buenos Aires.")
