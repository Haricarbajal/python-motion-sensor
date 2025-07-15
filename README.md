# python-motion-sensor

Detector de movimiento en Python que utiliza la cámara web para identificar cambios en tiempo real mediante procesamiento de imágenes con OpenCV.

## Descripción

Este proyecto captura vídeo desde la cámara y detecta movimiento analizando las diferencias entre tres frames consecutivos. Cuando se detecta movimiento significativo (áreas con cambios mayores a un umbral), marca las zonas afectadas con rectángulos rojos, muestra la imagen original con las marcas y guarda una captura con la fecha y hora del evento.

El método principal consiste en calcular la diferencia absoluta entre imágenes consecutivas, aplicar umbralización y dilatación para identificar zonas con movimiento.

## Características

- Captura vídeo en tiempo real usando OpenCV
- Detección de movimiento basada en diferencias entre tres frames consecutivos
- Marcado visual de las zonas donde se detecta movimiento
- Guarda automáticamente capturas cuando se detecta movimiento
- Visualización en ventanas separadas: imagen original, diferencia y zonas marcadas
- Código limpio y comentado para facilitar modificaciones y aprendizaje

## Requisitos

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/python-motion-sensor.git
   cd python-motion-sensor
