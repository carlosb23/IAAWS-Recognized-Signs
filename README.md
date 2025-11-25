# 🌍 Proyecto PIA: Geo-Localizador de Señales con IA y Reconocimiento de texto

Este proyecto es una aplicación full-stack que permite subir imágenes de señales de tráfico o calles, extraer el texto mediante **AWS Rekognition** y determinar la ubicación geográfica exacta utilizando la IA generativa de **Google Gemini**.

## 📋 Requisitos Previos

* Python 3.8 o superior.
* Una cuenta de AWS activa (con acceso a Rekognition y S3).
* Una API Key de Google Gemini.

## ⚙️ Instalación

1.  **Clonar o descargar el proyecto** en tu máquina local.
2.  **Crear un entorno virtual** (recomendado):
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```
3.  **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuración (Variables de Entorno)

El proyecto necesita un archivo `.env` en la raíz para funcionar. Crea un archivo llamado `.env` y rellena las siguientes claves:

```env
# Credenciales de AWS (Usuario IAM con permisos S3 y Rekognition)
AWS_ACCESS_KEY_ID=tu_clave_de_acceso_aws
AWS_SECRET_ACCESS_KEY=tu_clave_secreta_aws
AWS_REGION=eu-west-2   # O la región que uses (ej: us-east-1)

# Nombres de los Buckets de S3 (Deben existir en tu cuenta)
BUCKET_SOURCE=nombre-de-tu-bucket-origen

# Clave de Google AI para Gemini
GEMINI_API_KEY=tu_clave_api_gemini

# Configuración de Flask
FLASK_ENV=development
```


## ✍️ Autor

**Carlos Bustos**
* **Curso:** Especialización en Inteligencia Artificial y Big Data
* **Asignatura:** Programación de IA - Unidad 3 (AWS)

