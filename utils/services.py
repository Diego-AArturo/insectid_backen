import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv('API_GEMINI')
genai.configure(api_key=api)

# Función para subir la imagen
def image(path: str):
    try:
        sample_file = genai.upload_file(path=path)
        return sample_file
    except Exception as e:
        print("Error al procesar la imagen:", e)
        return None  # Cambiamos a `None` para indicar un fallo en la subida de la imagen

# Función para clasificar el insecto
def classify_insect(sample_file):
    if not sample_file:  # Verificamos si `sample_file` es válido
        return {"error": "No se pudo subir la imagen"}

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    # Generamos el contenido con la imagen y el prompt
    try:
        response = model.generate_content(
            [sample_file, '''
            Responde como un entomólogo experto.
            Analiza la imagen y clasifica el insecto, proporcionando la siguiente información en formato JSON estructurado:
            {
            "Nombre_comun": "nombre común del insecto o null si no se encuentra",
            "Nombre_cientifico": "nombre científico del insecto o null si no se encuentra",
            "Clasificaciones_taxonomicas": "clasificaciones taxonómicas relevantes o null si no se encuentra",
            "Habitat_natural": "hábitat natural del insecto o null si no se encuentra",
            "Dieta": "dieta del insecto o null si no se encuentra",
            "Ciclo_de_vida": "ciclo de vida del insecto o null si no se encuentra",
            "Estado_de_conservacion": "estado de conservación del insecto o null si no se encuentra"
            }
            Si el animal en la imagen no es un insecto, responde con:
            {
            "error": "El animal no es un insecto"
            }
            '''],
            generation_config=genai.types.GenerationConfig(
                temperature=0.3)
        )

        # Intentamos obtener el texto de la respuesta
        response_text = response.text
        print("Response text from model:", response_text)  # Logging de la respuesta para depuración
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)        
        response_text = json_match.group(0)
        print("", response_text)
        
        # Intentamos deserializar la respuesta a JSON
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return {"error": "Invalid JSON format from model"}

    except Exception as e:
        print("Error in model generation:", e)
        return {"error": "Error generating response from model"}

# Función principal que llama a la subida y clasificación de la imagen
def id_insect(path: str) -> dict:
    sample_file = image(path)
    if sample_file is None:
        return {"error": "Error al subir la imagen"}

    Insect_classification = classify_insect(sample_file)
    return Insect_classification

