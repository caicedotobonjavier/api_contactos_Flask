from flask import Flask, request, jsonify
#
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contactos.db"

db = SQLAlchemy(app)


#crear modelo
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(100), nullable=False, unique=True)

    def serializer(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono
        }


#crear tabals en la base de datos
with app.app_context():
    db.create_all()



#crear rutas
@app.route('/contactos', methods=['GET'])
def get_contactos():
    contactos = Contacto.query.all()
    resultado = []
    for contacto in contactos:
        resultado.append(contacto.serializer())
    
    return jsonify({
        'contactos' : resultado
    })



@app.route('/crear-contacto', methods=['POST'])
def crear_contacto():
    #recibo los datos enviados desde postman con el request.get_json()
    datos = request.get_json()
    contacto = Contacto(
        nombre = datos['nombre'],
        correo = datos['correo'],
        telefono = datos['telefono']
    )
    db.session.add(contacto)
    db.session.commit()

    return {
        'mensaje' : 'OK',
        'estado' : 200,
        'contacto' : datos['nombre']
    }


def buscador_contactos(id):
    contacto = Contacto.query.get(id)
    return contacto

@app.route('/buscar/<int:id>', methods=['GET'])
def buscar(id):
    contacto = buscador_contactos(id)
    if contacto:
        return jsonify({
            'estado' : 200,
            'contacto' : contacto.serializer()
        })
    else:
        return{
            'estado' : 404,
            'mensaje' : 'Contacto no encontrado'
        }
        


@app.route('/actualizar', methods=['PUT', 'PATCH'])
def actualizar():
    data = request.get_json()
    contacto = buscador_contactos(data['id'])
    if contacto:
        contacto.nombre = data['nombre']
        contacto.correo = data['correo']
        contacto.telefono = data['telefono']
        db.session.commit()

        return jsonify({
            'estado' : 200,
            'mensaje' : 'OK',
            'contacto' : contacto.serializer()
        })
    else:
        return{
            'estado' : 404,
            'mensaje' : 'Contacto no encontrado'
        }
        


@app.route('/eliminar', methods=['DELETE'])
def eliminar():
    data = request.get_json()
    contacto = buscador_contactos(data['id'])
    if contacto:
        db.session.delete(contacto)
        db.session.commit()

        return jsonify(
            {
                'estado' : 200,
                'mensaje' : 'OK',
                'contacto_eliminado' : contacto.serializer()
            }
        )
    else:
        return{
            'estado' : 404,
            'mensaje' : 'Contacto no encontrado'
        }