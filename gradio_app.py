import urllib.parse

import gradio as gr
import requests
import os

from dotenv import load_dotenv

# Cargar variables para saber dónde está tu servidor Flask
load_dotenv()

# Si tu Flask corre en otro puerto, cámbialo aquí
FLASK_URL = "http://127.0.0.1:5000/analyze-sign"


def process_image(image_path):
    """
    Función que Gradio llama cuando el usuario sube una foto.
    Envía la foto a tu servidor Flask y formatea la respuesta.
    """
    if image_path is None:
        return "Por favor, sube una imagen.", "N/A"

    # Preparar la petición a Flask
    try:
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            print(f"Enviando imagen a {FLASK_URL}...")
            response = requests.post(FLASK_URL, files=files)

        if response.status_code == 200:
            data = response.json()

            texto_detectado = data.get('detected_text', '')
            ubicacion_info = data.get('location_info', '')

            # En esta parte he generado un mapa interactivo dentro de la web con ayuda IA
            # Sabia que se podia usar un iframe para meter el mapa pero no que gradio admitira HTML
            mapa_html = ""
            if texto_detectado and "No se ha detectado" not in texto_detectado:
                # Limpiamos el texto para la URL
                query = urllib.parse.quote(texto_detectado)

                # Usamos un iframe de Google Maps en modo 'embed'
                # Esto incrusta el mapa directamente en la web
                mapa_html = f"""
                    <div style="width: 100%; height: 400px; border-radius: 10px; overflow: hidden; border: 2px solid #ddd;">
                        <iframe 
                            width="100%" 
                            height="100%" 
                            frameborder="0" 
                            scrolling="no" 
                            marginheight="0" 
                            marginwidth="0" 
                            src="https://maps.google.com/maps?q={query}&t=&z=15&ie=UTF8&iwloc=&output=embed">
                        </iframe>
                    </div>
                    <div style="margin-top: 15px; padding: 10px; background-color: #f0f8ff; border-radius: 5px;">
                        <strong>Geminis Ubicación: </strong> {ubicacion_info}
                    </div>
                    """
            else:
                mapa_html = f"<div>No se pudo generar el mapa. Razón: {ubicacion_info}</div>"

            return texto_detectado, mapa_html

        else:
            return f"Error: {response.status_code}", f"<div>Error del servidor: {response.text}</div>"

    except Exception as e:
        return f"Error: {str(e)}", "<div>Verifica que application.py esté ejecutándose.</div>"


# Configuración de la Interfaz de Gradio

# Definimos el diseño visual
with gr.Blocks(title="Detector de Ubicación de Calles con IA", theme="dark") as demo:
    gr.Markdown("# ¿Web para buscar calles por reconocimiento de señales?")
    gr.Markdown("Sube una foto de una señal de una calle y la IA te dirá dónde se encuentra ese lugar.")

    with gr.Row():
        with gr.Column():
            # Entrada: Imagen (puede ser subida o webcam)
            input_image = gr.Image(type="filepath", label="Sube tu foto")
            btn_analyze = gr.Button("Analizar Ubicación", variant="primary")
            output_text = gr.Textbox(label="Texto leído en la señal con (AWS Rekognition)")

        with gr.Column():
            # Salidas: Texto detectado y Resultado de Gemini
            output_map = gr.HTML(label="Mapa de la Ubicación")


    # Conectar el botón con la función
    btn_analyze.click(
        fn=process_image,
        inputs=[input_image],
        outputs=[output_text, output_map]
    )


if __name__ == "__main__":
    print("Iniciando interfaz Gradio...")
    demo.launch()