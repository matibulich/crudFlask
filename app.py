from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import time
from database import Database
from usuarios import Usuarios

app = Flask(__name__)
CORS(app)

# Ruta para guardar las imágenes
RUTA_DESTINO = "./static/imagenes"

# Conexión con la base de datos
db = Database(host="localhost", user="root", password="matias123", database="cancha_db")
usuarios = Usuarios(db)

#------------------------------------------------------------LISTAR USUARIOS--------------------------------------------------------------------------     
@app.route("/usuarios", methods=["GET"])
def listarUsuarios():
    respuesta = usuarios.listarUsuarios()
    return jsonify(respuesta)

#------------------------------------------------------------CONSULTAR USUARIO--------------------------------------------------------------------------     
@app.route("/usuarios/<int:id_usuario>", methods=["GET"])
def consultarUsuario(id_usuario):
    respuesta = usuarios.consultarUsuario(id_usuario)  # Corrección del nombre del método
    if respuesta:
       respuesta['nacimiento'] = respuesta['nacimiento'].strftime('%d/%m/%Y')
       return jsonify(respuesta), 200
    else:
        return "Usuario no encontrado.", 404

#------------------------------------------------------------AGREGAR USUARIO--------------------------------------------------------------------------     
@app.route("/usuarios", methods=["POST"])
def agregarUsuario():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    mail = request.form["mail"]
    dni = request.form["dni"]
    nacimiento = request.form["nacimiento"]
    genero = request.form["genero"]
    imagen = request.files["imagen"]
    
    nombreImagen = secure_filename(imagen.filename)
    nombreImagenBase, extension = os.path.splitext(nombreImagen)
    nombreImagen = f"{nombreImagenBase}_{int(time.time())}{extension}"
    
    nuevo_codigo = usuarios.agregarUsuario(nombre, apellido, mail, dni, nacimiento, genero, nombreImagen)
    if nuevo_codigo:
        imagen.save(os.path.join(RUTA_DESTINO, nombreImagen))
        return jsonify({"mensaje": "Usuario agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombreImagen}), 201
    else:
        return jsonify({"mensaje": "Error al agregar el usuario."}), 500

#--------------------------------------------------------------MODIFICAR USUARIO--------------------------------------------------------------------------   
@app.route("/usuarios/<int:id_usuario>", methods=["PUT"])
def modificarUsuario(id_usuario):
    nueva_nombre = request.form.get("nombre")
    nueva_apellido = request.form.get("apellido")
    nuevo_mail = request.form.get("mail")
    nuevo_nacimiento = request.form.get("nacimiento")
    nuevo_genero = request.form.get("genero")
    
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        nombreImagen = secure_filename(imagen.filename)
        nombreImagenBase, extension = os.path.splitext(nombreImagen)
        nombreImagen = f"{nombreImagenBase}_{int(time.time())}{extension}"
        imagen.save(os.path.join(RUTA_DESTINO, nombreImagen))

        imagenUsuario = usuarios.consultarUsuario(id_usuario)
        if imagenUsuario:
            imagen_vieja = imagenUsuario["imagen"]
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    else:
        imagenUsuario = usuarios.consultarUsuario(id_usuario)
        if imagenUsuario:
            nombreImagen = imagenUsuario["imagen"]

    if usuarios.modificarUsuario(id_usuario, nueva_nombre, nueva_apellido, nuevo_mail, dni, nuevo_nacimiento, nuevo_genero, nombreImagen):
        return jsonify({"mensaje": "Usuario modificado correctamente"}), 200
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

#--------------------------------------------------------------ELIMINAR USUARIO--------------------------------------------------------------------------  
@app.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def eliminarUsuario(id_usuario):
    respuesta = usuarios.consultarUsuario(id_usuario)
    if respuesta:
        imagen_vieja = respuesta["imagen"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        if usuarios.eliminarUsuario(id_usuario):
            return jsonify({"mensaje": "Usuario eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar usuario"}), 500
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
