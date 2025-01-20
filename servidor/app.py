from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Configuración de Flask y MongoDB
app = Flask(__name__)

# Conexión a MongoDB (Local o Remoto)
client = MongoClient("mongodb+srv://user1:NpUGBWELvGVv77mW@prueba.d1kxq.mongodb.net/?retryWrites=true&w=majority&appName=prueba")
db = client['instrumentacion']  # Base de datos
lecturas_collection = db['datos']  # Colección para guardar lecturas

@app.route('/sensor_data', methods=['POST'])
def sensor_data():
    try:
        # Extraer datos del POST
        data = request.json
        id_dispositivo = data.get('id_dispositivo')
        velocidad = data.get('velocidad')
        posicion = data.get('posicion')
        rpm = data.get('rpm')

        # Validar datos obligatorios
        if not id_dispositivo or velocidad is None or posicion is None or rpm is None:
            return jsonify({"error": "Faltan datos obligatorioss"}), 400

        # Crear documento para MongoDB
        lectura = {
            "id_dispositivo": id_dispositivo,
            "velocidad": velocidad,
            "posicion": posicion,
            "rpm": rpm,
            "tiempo": datetime.utcnow()  # Tiempo en formato UTC
        }

        # Guardar en MongoDB
        lecturas_collection.insert_one(lectura)

        return jsonify({"message": "Datos guardados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test', methods=['GET'])
def test_connection():
    try:
        # Crear un documento de prueba
        documento = {
            "mensaje": "Hola, MongoDB Atlas desde Flask!",
            "status": "Conexión exitosa"
        }

        # Insertar el documento en la colección
        resultado = lecturas_collection.insert_one(documento)

        # Devolver el ID del documento insertado
        return jsonify({"message": "Conexión exitosa", "document_id": str(resultado.inserted_id)})
    except Exception as e:
        # Manejar errores
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
