import io
import os
import requests
from PIL import Image
import gradio as gr

# URL local para cuando corra en Docker o en el test de Colab
API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

def procesar_diagnostico(imagen):
    if imagen is None:
        return "Error: No se proporcionó ninguna imagen.", 0.0, "Inactivo"
    
    # Convertir imagen a bytes
    bufer = io.BytesIO()
    imagen.save(bufer, format="JPEG")
    datos_binarios = bufer.getvalue()
    
    archivos = {"file": ("hoja.jpg", datos_binarios, "image/jpeg")}
    
    try:
        respuesta = requests.post(API_URL, files=archivos, timeout=15)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            
            # Usamos .get() para evitar KeyErrors. Si la imagen era inválida, 
            # la API no manda estos datos, así que por defecto pondrá 0.0 y "N/A"
            diagnostico = datos.get("diagnostico", "Error desconocido")
            confianza = datos.get("confianza", 0.0)
            monitoreo = datos.get("monitoreo_ops", "N/A (Objeto inválido)")
            
            return diagnostico, confianza, monitoreo
        else:
            return f"Error en API (HTTP {respuesta.status_code})", 0.0, "Error"
    except requests.exceptions.ConnectionError:
        return "Error: Backend no responde.", 0.0, "Desconectado"

interfaz = gr.Interface(
    fn=procesar_diagnostico,
    # ¡Aquí agregamos height=400 para hacer la caja visual mucho más grande!
    inputs=gr.Image(type="pil", height=500, label="Sube una fotografía de la hoja de café"),
    outputs=[
        gr.Textbox(label="Diagnóstico Fitosanitario"),
        gr.Number(label="Nivel de Confianza %"),
        gr.Textbox(label="Monitoreo de Data Drift")
    ],
    title="Clasificador de Enfermedades del Café (DINOv2)",
    description="Sube una imagen para analizarla con el modelo optimizado."
)

if __name__ == "__main__":
    interfaz.launch(server_name="0.0.0.0", server_port=7860)