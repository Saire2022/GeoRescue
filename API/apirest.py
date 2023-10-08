from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configura la base de datos MySQL utilizando mysql-connector-python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@35.199.118.43:3306/apirest'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/apirest'

db = SQLAlchemy(app)
# Modelo para la tabla de usuarios
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=True)
    puntos = db.relationship('Punto', backref='usuario', lazy=True)

# Modelo para la tabla de puntos
class Punto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.String(20), nullable=False)
    longitud = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    if 'id' in data and 'nombre' in data:
        id_usuario = data['id']
        nombre = data['nombre']
        apellido = data.get('apellido', None)  # Se puede proporcionar o no
        
        # Verificar si el ID del usuario ya existe en la base de datos
        usuario_existente = Usuario.query.filter_by(id=id_usuario).first()
        
        if usuario_existente:
            return jsonify({'message': 'Usuario ya registrado'}), 400
        else:
            nuevo_usuario = Usuario(id=id_usuario, nombre=nombre, apellido=apellido)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return jsonify({'message': 'Usuario agregado correctamente', 'id': nuevo_usuario.id}), 201
    else:
        return jsonify({'error': 'Los campos id y nombre son requeridos'}), 400

@app.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{'id': usuario.id, 'nombre': usuario.nombre, 'apellido': usuario.apellido} for usuario in usuarios]
    return jsonify({'usuarios': usuarios_json})

@app.route('/agregar_punto', methods=['POST'])
def agregar_punto():
    data = request.get_json()
    if 'latitud' in data and 'longitud' in data and 'usuario_id' in data:
        latitud = data['latitud']
        longitud = data['longitud']
        usuario_id = data['usuario_id']
        nuevo_punto = Punto(latitud=latitud, longitud=longitud, usuario_id=usuario_id)
        db.session.add(nuevo_punto)
        db.session.commit()
        return jsonify({'message': 'Punto agregado correctamente', 'id': nuevo_punto.id}), 201
    else:
        return jsonify({'error': 'Los campos de latitud, longitud y usuario_id son requeridos'}), 400

@app.route('/obtener_puntos', methods=['GET'])
def obtener_puntos():
    puntos = Punto.query.all()
    puntos_json = [{'id': punto.id, 'latitud': punto.latitud, 'longitud': punto.longitud, 'fecha': punto.fecha, 'usuario_id': punto.usuario_id} for punto in puntos]
    return jsonify({'puntos': puntos_json})

@app.route('/eliminar_puntos/<int:usuario_id>', methods=['DELETE'])
def eliminar_puntos_por_usuario(usuario_id):
    # Verificar si el usuario existe en la base de datos
    usuario = Usuario.query.get(usuario_id)
    
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Eliminar los puntos asociados a ese usuario
    puntos_eliminados = Punto.query.filter_by(usuario_id=usuario_id).delete()
    
    db.session.commit()
    
    return jsonify({'message': f'Se eliminaron {puntos_eliminados} puntos del usuario con ID {usuario_id}'}), 200

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
    
@app.route('/', methods=['GET'])
def index():
    return '¡Hola, esta es la página de inicio de mi API!'

if __name__ == '__main__':
    #with app.app_context():
        #db.create_all()
    app.run()

    #app.run(host='0.0.0.0', port=5000, debug=True)
    
