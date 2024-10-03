from flask import Flask, request, jsonify
import os
from utils import services
import json  # Importa el módulo json para trabajar con la conversión de cadenas JSON

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Ruta para verificar el estado del backend
@app.route('/', methods=['GET'])
def pedidos():
    return 'InsectID'  # Retorna un mensaje simple

# Ruta para procesar la imagen
@app.route('/intelligentid', methods=['POST'])
def enviar_imagen():
    if 'image' not in request.files:
        return jsonify({"error": "No image found in the request"}), 400

    # Obtiene la imagen de la solicitud
    image = request.files['image']

    # Guarda temporalmente la imagen
    image_path = os.path.join('temp', image.filename)
    os.makedirs('temp', exist_ok=True)  # Crea el directorio temp si no existe
    image.save(image_path)

    try:
        # Llama a la función que procesa la imagen
        result = services.id_insect(image_path)
        print("Result from services.id_insect:", result)
        
        # Verifica si `result` ya es un objeto Python o si necesita deserializarse
        if isinstance(result, str):
            try:
                result_json = json.loads(result)  # Deserializa la cadena JSON si es necesario
            except json.JSONDecodeError as e:
                return jsonify({"error": "Error processing the JSON", "details": str(e)}), 500
        else:
            result_json = result  # Si ya es un objeto Python, úsalo directamente

    finally:
        # Elimina la imagen temporal, asegurando que siempre se elimine
        try:
            os.remove(image_path)
        except OSError as e:
            print(f"Error removing the file: {e}")

    # Retorna el resultado como un objeto JSON
    return jsonify(result_json)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0')




