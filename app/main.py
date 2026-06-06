import io
import os
import numpy as np
import pandas as pd
from torchvision import transforms
import torch
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
import onnxruntime as ort

app = FastAPI(title="API Fitosanitaria de Inferencia de Café (ONNX)")

# Rutas relativas para el contenedor de Docker
MODEL_PATH = "app/modelo_optimizado.onnx"
LOG_PATH = "drift_log.csv"

# Cargar el modelo ONNX Runtime apuntando a Drive (o local en Docker)
session = ort.InferenceSession(MODEL_PATH)

# Inicializar el archivo de registro de monitoreo si no existe
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w") as f:
        f.write("confianza\n")

def evaluar_drift(nueva_confianza: float) -> str:
    """Registra la confianza actual y calcula la media móvil para detectar anomalías."""
    # Guardar el registro de la inferencia actual
    with open(LOG_PATH, "a") as f:
        f.write(f"{nueva_confianza}\n")
    
    try:
        # Leer el histórico para analizar el comportamiento reciente del lote de producción
        df = pd.read_csv(LOG_PATH)
        if len(df) >= 10:
            media_reciente = df["confianza"].tail(10).mean()
            # Umbral de tolerancia estadística para activar la alerta de Data Drift
            if media_reciente < 0.75:
                return "ALERTA: Posible Data Drift. Confianza degradada en el entorno actual."
        return "Sistema Estable"
    except Exception:
        return "Monitoreo No Disponible"

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validar que el archivo de entrada corresponda efectivamente a una imagen
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo enviado no corresponde a una imagen válida.")
    
    try:
        # 1. Lectura de la imagen original
        contenido_imagen = await file.read()
        imagen_pil = Image.open(io.BytesIO(contenido_imagen)).convert("RGB")
        
        # 2. Preprocesamiento matemático idéntico al entrenamiento original (Fuerza Cuadrado)
        # ---> AQUÍ ESTÁ EL CAMBIO CLAVE <---
        transformacion = transforms.Compose([
            transforms.Resize((224, 224)),  # Aplasta la imagen exactamente a la misma geometría de entrenamiento
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
        ])
        
        # 3. Aplicar las transformaciones (devuelve un tensor de PyTorch)
        img_tensor = transformacion(imagen_pil)
        
        # 4. Convertir a NumPy y agregar la dimensión de lote (Batch) para ONNX
        img_np = img_tensor.unsqueeze(0).numpy()
        
        # 5. Ejecutar la inferencia usando el grafo optimizado de ONNX
        nombre_entrada = session.get_inputs()[0].name
        salidas_modelo = session.run(None, {nombre_entrada: img_np})
        
        # Calcular Softmax sobre los logits de salida para obtener probabilidades reales
        logits = salidas_modelo[0][0]
        logits_estables = logits - np.max(logits)  # Evitar desbordamiento numérico
        valores_exponenciales = np.exp(logits_estables)
        probabilidades = valores_exponenciales / np.sum(valores_exponenciales)
        
        # Extraer predicción de confianza más alta
        clase_id = int(np.argmax(probabilidades))
        confianza_calculada = float(probabilidades[clase_id])

        # Mapeo descriptivo corregido (Lista normal)
        mapa_enfermedades = ['Ojo de Gallo', 'Roya', 'Sana', 'Araña Roja']
        
        # --- FILTRO DE UMBRAL DE CONFIANZA (OUT-OF-DISTRIBUTION) ---
        UMBRAL_CONFIANZA = 0.45
        
        if confianza_calculada < UMBRAL_CONFIANZA:
            # 1. Si es basura, detenemos el proceso y devolvemos un JSON limpio
            return {
                "clase_index": -1,
                "diagnostico": "⚠️ Objeto no reconocido. Sube una foto clara de una hoja de café.",
                "confianza": round(confianza_calculada, 4)
            }
        else:
            # 2. Si la imagen pasa el filtro, definimos el diagnóstico
            diagnostico_final = mapa_enfermedades[clase_id]

            # 3. Solo registramos en el Log de Drift si la imagen fue verdaderamente una hoja
            estado_sistema = evaluar_drift(confianza_calculada)

            # 4. Devolvemos el JSON completo con toda la telemetría
            return {
                "clase_index": clase_id,
                "diagnostico": diagnostico_final,
                "confianza": round(confianza_calculada, 4),
                "monitoreo_ops": estado_sistema
            }
            
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Fallo interno en el pipeline de inferencia: {str(error)}")