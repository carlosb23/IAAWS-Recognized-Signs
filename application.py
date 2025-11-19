import os
import uuid  # Para generar nombres de archivo únicos
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError

# 1. --- Configuración Inicial ---

# Cargar variables de entorno (claves, buckets) desde .env
load_dotenv()

# --- IMPORTANTE: Ahora importamos nuestros archivos ---
import aws_services  # Archivo 2
import get_location  # Archivo 3

app = Flask(__name__)

# Leer la configuración de AWS desde las variables de entorno
AWS_ACCESS_KEY = os.getenv('ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')
AWS_REGION = os.getenv('REGION')
BUCKET_SOURCE = os.getenv('BUCKET_SOURCE')  # El bucket para subir las fotos

# Validar que las variables se han cargado
if not all([AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, BUCKET_SOURCE]):
    raise ValueError("Error: Faltan variables de entorno de AWS (KEY, SECRET, REGION o BUCKET)")

# 2. --- Creación del cliente de S3 ---
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


def upload_file_to_s3(file_obj, bucket_name, object_name):
    """Sube un objeto de archivo a un bucket S3"""
    try:
        s3_client.upload_fileobj(file_obj, bucket_name, object_name)
        print(f"Archivo {object_name} subido a {bucket_name}.")
    except NoCredentialsError:
        print("Error: Credenciales de AWS no encontradas.")
        return False
    except Exception as e:
        print(f"Error al subir a S3: {e}")
        return False
    return True


# 3. --- Definición del Endpoint de la API ---

@app.route('/analyze-sign/', methods=['POST'])
def analyze_sign_endpoint():
    """
    Este endpoint recibe una imagen y devuelve la localización.
    """

    # --- A. Validar la Petición ---
    if 'image' not in request.files:
        return jsonify({"error": "Petición inválida: falta el archivo 'image'"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "Petición inválida: no se ha seleccionado ningún archivo"}), 400

    # --- ¡CAMBIO! ---
    # Ya no necesitamos 'target_language'
    # ------------------

    # --- B. Lógica de Almacenamiento (Requisito) ---
    unique_filename = f"uploads/{uuid.uuid4()}_{file.filename}"

    if not upload_file_to_s3(file, BUCKET_SOURCE, unique_filename):
        return jsonify({"error": "Fallo al subir la imagen a S3"}), 500

    # --- C. Llamada al Archivo 2 (Servicios AWS) (Requisito) ---

    print(f"Iniciando análisis de {unique_filename}...")
    try:
        # --- ¡CAMBIO! ---
        # 1. Llamamos a la nueva función
        # 2. Ya no devuelve un diccionario, solo el texto
        original_text = aws_services.get_text_from_s3_image(
            bucket=BUCKET_SOURCE,
            s3_key=unique_filename
        )

    except Exception as e:
        # Capturar cualquier error de Rekognition
        print(f"Error en aws_services: {e}")
        return jsonify({"error": f"Error en los servicios de IA: {str(e)}"}), 500

    # --- D. Llamada al Archivo 3 (Funcionalidad Extra) (Requisito) ---

    location_info = "No se buscó ubicación (no se detectó texto)."

    # Solo buscamos la ubicación si Rekognition encontró texto
    if original_text and "No se ha detectado texto" not in original_text:
        print(f"Buscando ubicación para: {original_text}")
        try:
            # Esta llamada a Gemini sigue igual y es perfecta
            location_info = get_location.find_location_info(original_text)

        except Exception as e:
            # Capturar cualquier error de Gemini
            print(f"Error en get_location (Gemini): {e}")
            location_info = "Error al contactar el servicio de localización (Gemini)."

    # --- E. Devolver Respuesta Final ---

    # --- ¡CAMBIO! ---
    # Simplificamos la respuesta final
    final_response = {
        "image_source": f"s3://{BUCKET_SOURCE}/{unique_filename}",
        "detected_text": original_text,
        "location_info": location_info
    }

    return jsonify(final_response), 200


# 4. --- Ejecución del Servidor ---

if __name__ == '__main__':
    app.debug = True
    app.run()