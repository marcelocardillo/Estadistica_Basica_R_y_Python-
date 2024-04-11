import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Funciones para calcular la estadística descriptiva
def calcular_estadisticas_adicionales(datos):
    media = np.mean(datos)
    mediana = np.median(datos)
    desvio_absoluto_mediana = np.median(np.abs(datos - mediana))
    desvio_estandar_media = np.std(datos, ddof=1)
    coeficiente_variacion = (desvio_estandar_media / media) * 100  # En porcentaje
    cuartiles = np.percentile(datos, [25, 50, 75])
    
    return media, mediana, desvio_absoluto_mediana, desvio_estandar_media, coeficiente_variacion, cuartiles

# Función para calcular la media y el intervalo de confianza de la media a partir de 10,000 remuestreos
def calcular_media_intervalo_confianza(datos, num_remuestreos=10000, nivel_confianza=0.95):
    medias = []

    for _ in range(num_remuestreos):
        remuestreo = np.random.choice(datos, len(datos), replace=True)
        media = np.mean(remuestreo)
        medias.append(media)

    media_boot = np.mean(medias)
    error_estandar_boot = np.std(medias)
    margen_error = error_estandar_boot * stats.t.ppf((1 + nivel_confianza) / 2, df=len(medias)-1)

    intervalo_confianza = (media_boot - margen_error, media_boot + margen_error)

    return media_boot, intervalo_confianza, medias

# Título de la aplicación
st.title("Estadística descriptiva")

# Campo de texto para ingresar los datos
data_input = st.text_area("Ingrese los datos (copie y pegue desde Excel u otras fuentes)", "")

# Botón para calcular
if st.button("Calcular"):
    try:
        # Procesar los datos ingresados
        data = [float(line.strip()) for line in data_input.split("\n") if line.strip() != ""]

        # Calcular estadísticas adicionales
        media, mediana, desvio_absoluto_mediana, desvio_estandar_media, coeficiente_variacion, cuartiles = calcular_estadisticas_adicionales(data)

        # Calcular la media, el intervalo de confianza y obtener las medias de remuestreo usando bootstrap
        media_boot, intervalo_confianza, medias_remuestreo = calcular_media_intervalo_confianza(data)

        # Mostrar resultados con tres decimales
        st.subheader("Resultados:")
        st.write(f"Media: {round(media, 3)}")
        st.write(f"Mediana: {round(mediana, 3)}")
        st.write(f"Desvio Absoluto de la Mediana: {round(desvio_absoluto_mediana, 3)}")
        st.write(f"Desvio Estándar de la Media: {round(desvio_estandar_media, 3)}")
        st.write(f"Coeficiente de Variación: {round(coeficiente_variacion, 3)}%")
        st.write(f"Cuartiles: Q1 = {round(cuartiles[0], 3)}, Q2 (Mediana) = {round(cuartiles[1], 3)}, Q3 = {round(cuartiles[2], 3)}")
        
        # Mostrar histograma de la muestra
        st.subheader("Histograma de la variable")
        fig_muestra, ax_muestra = plt.subplots()
        ax_muestra.hist(data, bins=20, color="blue", alpha=0.5)
        ax_muestra.set_xlabel("Valores de la variable")
        ax_muestra.set_ylabel("Frecuencia")
        ax_muestra.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Media = {round(media, 2)}')
        ax_muestra.axvline(mediana, color='green', linestyle='dashed', linewidth=2, label=f'Mediana = {round(mediana, 2)}')
        ax_muestra.legend()
        st.pyplot(fig_muestra)

        # Mostrar histograma de las medias de remuestreo
        st.subheader("Histograma de las Medias de Remuestreo")
        fig_remuestreo, ax_remuestreo = plt.subplots()
        ax_remuestreo.hist(medias_remuestreo, bins=20, color="orange", alpha=0.7)
        ax_remuestreo.axvline(media_boot, color='r', linestyle='dashed', linewidth=2, label='Media Bootstrap')
        ax_remuestreo.axvline(intervalo_confianza[0], color='g', linestyle='dashed', linewidth=2, label='Intervalo de Confianza (Inferior)')
        ax_remuestreo.axvline(intervalo_confianza[1], color='b', linestyle='dashed', linewidth=2, label='Intervalo de Confianza (Superior)')
        ax_remuestreo.set_xlabel("Medias de Remuestreo")
        ax_remuestreo.set_ylabel("Frecuencia")
        ax_remuestreo.legend()
        st.pyplot(fig_remuestreo)

    except:
        st.error("Error al procesar los datos. Asegúrese de ingresar números separados por tabulación o copiar y pegar desde Excel u otras fuentes.")

st.write("Elaboración: Marcelo Cardillo, Prof. Adjunto de Métodos Cuantitativos, Facultad de Filosofía y Letras, Universidad de Buenos Aires.")
