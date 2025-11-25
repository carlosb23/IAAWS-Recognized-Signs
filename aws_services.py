import boto3
import os

# Creación del Cliente de AWS

# Leemos los nombres de variable personalizados de nuestro .env
REGION = os.getenv('REGION')
ACCESS_KEY = os.getenv('ACCESS_KEY_ID')
SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')

# Validamos que se han cargado
if not REGION or not ACCESS_KEY or not SECRET_KEY:
    raise ValueError("Error: Faltan variables de AWS (REGION, ACCESS_KEY_ID, ACCESS_SECRET_KEY) en .env")

try:
    rekognition_client = boto3.client(
        'rekognition',
        region_name=REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
except Exception as e:
    print(f"Error fatal: No se pudo crear un cliente de Boto3.")
    print(f"Error: {e}")
    raise


# Funciones de Servicio (Llamadas a la API)

def _get_text_from_rekognition(bucket, s3_key):
    """
    Función interna: Llama a Rekognition 'DetectText'
    """
    print(f"Llamando a Rekognition para: s3://{bucket}/{s3_key}")
    try:
        response = rekognition_client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': s3_key
                }
            }
        )

        text_detections = response.get('TextDetections', [])
        if not text_detections:
            return "No se ha detectado texto."

        # Filtramos solo por líneas de texto y las juntamos
        detected_lines = [
            item['DetectedText'] for item in text_detections
            if item['Type'] == 'LINE'
        ]

        full_text = " ".join(detected_lines)
        print(f"Texto detectado por Rekognition: '{full_text}'")
        return full_text

    except Exception as e:
        print(f"Error en Rekognition 'detect_text': {e}")
        raise ValueError(f"Error al analizar la imagen en Rekognition: {str(e)}")


# Función Principal
def get_text_from_s3_image(bucket, s3_key):

    # Obtener texto de la imagen usando Rekognition
    original_text = _get_text_from_rekognition(bucket, s3_key)

    # Devolver el texto directamente
    return original_text