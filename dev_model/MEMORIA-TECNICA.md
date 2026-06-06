# Memoria Técnica

![Hojas de Café](images/Cafe_CJoseTacana.JPG)

## Descripción de los Notebooks

Este repositorio contiene notebooks clave que abordan el análisis fitosanitario de las hojas de café desde la ingeniería de datos hasta el modelado de vanguardia:

### 📝 `EDA.ipynb`
Este notebook se enfoca en la construcción, limpieza y análisis del **Dataset_rocole_Maestro**. Se documenta el proceso de ingeniería de datos, proporcionando información sobre:
- Integración de fuentes independientes (dataset peruano y RoCoLe original).
- Balanceo de clases (Sanas, Ojo de Gallo, Roya y Araña Roja) y partición de datos (70/10/20) mediante semilla de reproducibilidad (`seed = 42`).
- Aplicación de segmentación topológica utilizando el modelo fundacional **SAM-2**.
- Análisis exploratorio de datos (EDA), identificando métricas clave y documentando cualitativamente el fenómeno de **aprendizaje de atajos (shortcut learning)** asociado a los fondos segmentados.

El objetivo es establecer un corpus de datos estructurado y auditable, comprendiendo a fondo los sesgos ambientales y morfológicos antes de la fase de modelado.

### 📝 `ResNet18_DataAugmentation.ipynb`
Este script detalla la implementación de una **Red Neuronal Convolucional (ResNet-18)** para la clasificación multiclase, optimizada con técnicas de enriquecimiento de datos.
- **Data Augmentation Balanceado:** Se generaron variaciones sintéticas de las imágenes hasta alcanzar exactamente **2,000 muestras por categoría**, asegurando un entrenamiento sin desequilibrio de clases.
- **Aislamiento de Entrenamiento:** Las transformaciones se aplicaron **exclusivamente al conjunto de entrenamiento**. Los datos de validación y prueba se mantuvieron en su estado original para evitar la
  filtración de información (*data leakage*) y medir el rendimiento real.
- **Entrenamiento Corto (10 Épocas):** El ciclo de aprendizaje se limitó a **10 épocas**. Gracias al alto volumen de datos generados por el aumento, el modelo logró una convergencia rápida, minimizando eficazmente el riesgo de sobreajuste (*overfitting*).
Este enfoque permite la automatización del diagnóstico agrícola, ofreciendo una herramienta tecnológica robusta para asistir a los productores y especialistas en el monitoreo de los cultivos.

🚀 **Ambos notebooks complementan el estudio de enfermedades fitosanitarias desde un enfoque de ciencia de datos e inteligencia artificial, proporcionando información valiosa para la agricultura de precisión.**
