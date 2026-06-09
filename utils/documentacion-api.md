# Documentación General de la API - Clasificador Fitosanitario (ONNX)

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Uso de Docker](#uso-de-docker)
5. [Endpoints de la API](#endpoints-de-la-api)
   - [POST /predict](#post-predict)
6. [Monitoreo y Telemetría (MLOps)](#monitoreo-y-telemetría-mlops)
7. [Manejo de Errores](#manejo-de-errores)

---

## Introducción
Esta API permite la clasificación automatizada de hojas de café para la detección de enfermedades (Sanas, Ojo de Gallo, Roya y Araña Roja). La arquitectura está impulsada por un motor de inferencia de alto rendimiento (**ONNX Runtime**), garantizando baja latencia computacional. Además, cuenta con filtros de distribución (*Out-of-Distribution*) y un sistema de monitoreo en tiempo real para detectar la degradación del modelo (*Data Drift*).

---

## Requisitos Previos
- Docker y Git instalados.
- Python 3.11 o superior (para desarrollo local).

## Instalación y Configuración

### Clonación del Repositorio
```bash
git clone [https://github.com/roblero-gunn/Proyecto1_CoffeeLeafs.git](https://github.com/roblero-gunn/Proyecto1_CoffeeLeafs.git)
cd Proyecto1_CoffeeLeafs
```

## Carga del Modelo Optimizado
El motor de la API requiere el grafo computacional exportado en formato ONNX.

Descarga el archivo de pesos: Descargar modelo_optimizado.onnx (app/modelo_optimizado.onnx).

Guarda el archivo exactamente en la ruta app/modelo_optimizado.onnx.

## Uso de Docker
Construcción de la Imagen
```bash
docker build -t api-coffee-leafs .
```
Ejecución del Contenedor
```bash
docker run -d -p 80:80 api-coffee-leafs
```
Accede a http://localhost:80/docs para interactuar con la interfaz Swagger UI generada automáticamente por FastAPI.

## Endpoints de la API

### POST /predict
**Descripción:** Recibe un archivo de imagen directo (fotografía de la hoja) y devuelve el diagnóstico fitosanitario junto con la telemetría del sistema.

**Formato de Petición:** multipart/form-data

Parámetro: file (Archivo binario de imagen: .jpg, .png, etc.)

Ejemplo de Solicitud con cURL:

```bash
curl -X POST "http://localhost:80/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@hoja_sospechosa.jpg"
```

Ejemplo de Respuesta (Diagnóstico Exitoso):

``` json
{
  "clase_index": 3,
  "diagnostico": "Araña Roja",
  "confianza": 0.9854,
  "monitoreo_ops": "Sistema Estable"
}
```
Ejemplo de Respuesta (Filtro Out-of-Distribution Activado):
Ocurre cuando el usuario sube una imagen que no corresponde al entorno agrícola entrenado (confianza < 45%).

``` json
{
  "clase_index": -1,
  "diagnostico": "⚠️ Objeto no reconocido. Sube una foto clara de una hoja de café.",
  "confianza": 0.2312
}
```

## Monitoreo y Telemetría (MLOps)
La API cuenta con un módulo de estabilidad operativa que evalúa de forma continua el rendimiento del modelo en producción:

Prevención de Errores (OOD): Si la confianza máxima extraída mediante Softmax no supera el 0.45, la API bloquea el diagnóstico para evitar falsos positivos.

Detección de Data Drift: Cada predicción exitosa alimenta el archivo log drift_log.csv. El sistema calcula una media móvil con las últimas 10 inferencias. Si la media de confianza del lote cae por debajo del 75%, el estado de monitoreo_ops advertirá de una posible degradación en la captura de imágenes, permitiendo tomar acciones correctivas inmediatas en campo.

## Manejo de Errores
400 (Bad Request): El cliente envió un archivo que no es una imagen válida.

500 (Internal Server Error): Fallo en el pipeline de inferencia interno (ej. modelo ONNX no encontrado o corrupto).
