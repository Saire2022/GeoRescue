from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puntos.db'  # Nombre de la base de datos
db = SQLAlchemy(app)

# Modelo para la tabla de puntos
class Punto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitud = db.Column(db.String(20), nullable=False)
    longitud = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

#Add Points
@app.route('/agregar_punto', methods=['POST'])
def agregar_punto():
    data = request.get_json()
    if 'latitud' in data and 'longitud' in data:
        latitud = data['latitud']
        longitud = data['longitud']
        nuevo_punto = Punto(latitud=latitud, longitud=longitud)
        db.session.add(nuevo_punto)
        db.session.commit()
        return jsonify({'message': 'Punto agregado correctamente'}), 201
    else:
        return jsonify({'error': 'Los campos de latitud y longitud son requeridos'}), 400
#Get Points
@app.route('/obtener_puntos', methods=['GET'])
def obtener_puntos():
    puntos = Punto.query.all()
    puntos_json = [{'id': punto.id, 'latitud': punto.latitud, 'longitud': punto.longitud, 'fecha': punto.fecha} for punto in puntos]
    return jsonify({'puntos': puntos_json})

#Delete
@app.route('/eliminar_puntos', methods=['DELETE'])
def eliminar_puntos():
    try:
        # Eliminar todos los registros de la tabla Punto
        num_registros_eliminados = db.session.query(Punto).delete()
        db.session.commit()

        return jsonify({'message': f'Se eliminaron {num_registros_eliminados} registros correctamente'}), 200
    except Exception as e:
        app.logger.error(f'Error al eliminar puntos: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Ocurrió un error al eliminar los registros'}), 500

#Delete a point
@app.route('/eliminar_punto/<int:punto_id>', methods=['DELETE'])
def eliminar_punto(punto_id):
    try:
        # Buscar el punto por su ID
        punto = Punto.query.get(punto_id)
        
        if punto:
            # Eliminar el punto de la base de datos
            db.session.delete(punto)
            db.session.commit()
            return jsonify({'message': f'Se eliminó el punto con ID {punto_id} correctamente'}), 200
        else:
            return jsonify({'error': 'El punto no se encontró en la base de datos'}), 404
    except Exception as e:
        app.logger.error(f'Error al eliminar el punto: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Ocurrió un error al eliminar el punto'}), 500

@app.route('/', methods=['GET'])
def index():
    return '¡Hola, esta es la página de inicio de mi API!'

if __name__ == '__main__':
    with app.app_context():  # Agrega esta línea para crear tablas dentro del contexto de la aplicación
        db.create_all()
    #app.run(debug=True)
    app.run(host='172.23.211.214', port=5000, debug=True)

