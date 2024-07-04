

# usuarios.py

class Usuarios:
    def __init__(self, db):
        self.db = db  # Instancia de la clase Database

    def agregarUsuario(self, nombre, apellido, mail, dni, nacimiento, genero, imagen):
        sql = "INSERT INTO usuarios (nombre, apellido, mail, dni, nacimiento, genero, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre, apellido, mail, dni, nacimiento, genero, imagen)
        self.db.execute(sql, valores)  # Cambiado de self.cursor.execute a self.db.execute
        return self.db.lastrowid()  # Cambiado de self.cursor.lastrowid a self.db.lastrowid

    def consultarUsuario(self, id_usuario):
        sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
        return self.db.fetchone(sql, (id_usuario,))  # Cambiado de self.cursor.execute a self.db.fetchone

    def modificarUsuario(self, id_usuario, nNombre, nApellido, nMail, nDni, nNacimiento, nGenero, nImagen):
        sql = "UPDATE usuarios SET nombre = %s, apellido = %s, mail = %s, dni = %s, nacimiento = %s, genero = %s, imagen = %s WHERE id_usuario = %s"
        valores = (nNombre, nApellido, nMail, nDni, nNacimiento, nGenero, nImagen, id_usuario)
        self.db.execute(sql, valores)  # Cambiado de self.cursor.execute a self.db.execute
        return self.db.cursor.rowcount > 0  # Cambiado de self.cursor.rowcount a self.db.cursor.rowcount

    def eliminarUsuario(self, id_usuario):
        sql = "DELETE FROM usuarios WHERE id_usuario = %s"
        self.db.execute(sql, (id_usuario,))  # Cambiado de self.cursor.execute a self.db.execute
        return self.db.cursor.rowcount > 0  # Cambiado de self.cursor.rowcount a self.db.cursor.rowcount

    def listarUsuarios(self):
        sql = "SELECT * FROM usuarios"
        return self.db.fetchall(sql)  # Cambiado de self.cursor.execute a self.db.fetchall
