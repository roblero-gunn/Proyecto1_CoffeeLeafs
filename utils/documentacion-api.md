# Documentación General de la API - Clasificador Fitosanitario

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
   - [Clonación del Repositorio](#clonación-del-repositorio)
   - [Configuración del Entorno](#configuración-del-entorno)
4. [Uso de Docker](#uso-de-docker)
   - [Construcción de la Imagen](#construcción-de-la-imagen)
   - [Ejecución del Contenedor](#ejecución-del-contenedor)
   - [Detener y Eliminar Contenedores](#detener-y-eliminar-contenedores)
5. [Endpoints de la API](#endpoints-de-la-api)
   - [POST /predict](#post-predict)
6. [Manejo de Errores](#manejo-de-errores)

---

## Introducción
Esta API permite la clasificación de imágenes de hojas de café para detectar su estado fitosanitario. Utiliza modelos avanzados de aprendizaje profundo construidos en PyTorch (ResNet-18 y DINOv2) para ofrecer predicciones precisas entre cuatro categorías: Sanas, Ojo de Gallo, Roya y Araña Roja. Además, integra técnicas de explicabilidad visual (Grad-CAM y Attention Rollout) que resaltan las lesiones o regiones de interés que fundamentan la predicción del modelo.

[Ir a la documentación interactiva de la API (Swagger UI)](#) *(Nota: Actualizar este enlace cuando la API esté desplegada en producción)*

---

## Requisitos Previos
- Docker instalado.
- Git instalado.
- Python 3.11 o superior (para desarrollo local sin Docker).
- Configuración básica del sistema operativo.

## Instalación

### Clonación del Repositorio
Clona el repositorio del proyecto en tu máquina local:
```bash
git clone [https://github.com/roblero-gunn/Proyecto1_CoffeeLeafs.git](https://github.com/roblero-gunn/Proyecto1_CoffeeLeafs.git)
cd Proyecto1_CoffeeLeaves
```

## Carga de los Modelos
Los archivos de los pesos entrenados para ResNet-18 y DINOv2 son pesados y no están incluidos directamente en el control de versiones del repositorio para evitar saturación. Puedes descargarlos desde el siguiente enlace:

Descargar pesos de los modelos (.pth) ResNet18: (https://drive.google.com/file/d/1Ddo51OuIg4se2ZzWR4_pBz-znlFwXg9l/view?usp=sharing)
DINOv2: (https://drive.google.com/file/d/1s74dvTnLFJh6c5V9AnqAh4gwaXpjrOwG/view?usp=drive_link)

Por favor, asegúrate de guardar los archivos .pth en el directorio principal de la aplicación (ej. /app/models/) para que la API pueda instanciarlos correctamente al arrancar.

## Uso de Docker
Construcción de la Imagen
Construye la imagen de Docker empaquetando la API y sus dependencias:
```bash
docker build -t api-coffee-leafs
```

## Ejecución del Contenedor
Inicia el contenedor exponiendo el puerto configurado:
```bash
docker run -d -p 80:80 api-coffee-leafs
```
Una vez en ejecución, puedes acceder a http://localhost:80/docs para interactuar directamente con la documentación autogenerada (FastAPI/Swagger).

## Detener y Eliminar Contenedores
Para detener el servicio:
``` bash
docker stop <id_contenedor>
```
Para limpiar tu entorno eliminando el contenedor:
``` bash
docker rm <id_contenedor>
```

## Endpoints de la API
### POST /predict
**Descripción:** Recibe una fotografía de una hoja de café y devuelve el diagnóstico fitosanitario junto con su mapa de explicabilidad espacial.

**Request Body:**
``` json
{
    "image_base64": "/9j/4AAQSkZJRgAB...",
    "model_type": "dinov2" 
}
```
