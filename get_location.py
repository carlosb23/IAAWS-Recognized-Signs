import os
import google.generativeai as genai

# Configuración del Cliente de Gemini

try:
    # 'application.py' ya cargó .env, así que os.getenv funciona
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    if not GEMINI_API_KEY:
        raise ValueError("No se encontró la GEMINI_API_KEY en el .env")

    # Configura la API de Google
    genai.configure(api_key=GEMINI_API_KEY)

    # Eligimos el modelo de IA que vamos a usar
    model = genai.GenerativeModel('gemini-2.5-flash')

#
except Exception as e:
    print(f"Error fatal: No se pudo configurar Gemini.")
    print(f"Asegúrate de tener una 'GEMINI_API_KEY' válida en tu .env")
    print(f"Error: {e}")
    model = None


# Función de Funcionalidad Extra (Llamada a la IA)

def find_location_info(text_to_search):
    """
    Usa Gemini para obtener información de una ubicación
    basándose en el texto de una señal.
    """

    # Comprobación por si el modelo no se pudo cargar al inicio
    if model is None:
        return "Error: El servicio de localización (Gemini) no está configurado."

    # Creación del 'Prompt'
    # Le damos instrucciones a la IA.

    prompt = f"""
    Eres un asistente de geolocalización. 
    Te voy a dar el texto extraído de una señal de tráfico o de una calle.
    Tu trabajo es identificar la ubicación (ciudad, país, lugar específico)
    y devolver una descripción muy breve (máximo 2 frases).
    
    Si el texto es ambiguo o no parece una ubicación (ej: "STOP"),
    simplemente di "No se pudo determinar una ubicación específica".

    Texto de la señal: "{text_to_search}"
    """

    print(f"Llamando a Gemini con el prompt: '{text_to_search}'")

    try:
        #Llamada a la API de Gemini
        response = model.generate_content(prompt)

        location_description = response.text
        print(f"Respuesta de Gemini: {location_description}")

        return location_description.strip()

    except Exception as e:
        print(f"Error al llamar a la API de Gemini: {e}")
        return f"Error al procesar la solicitud de localización: {str(e)}"