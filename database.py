import mysql.connector
from mysql.connector import errorcode

class Database:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Conexión a la base de datos establecida exitosamente.")

        except mysql.connector.Error as err:
            print(f"Error al conectar con la base de datos: {err}")
            self.conn = None
            self.cursor = None
            raise err

    # Cerrar conexión
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    # Ejecuta las sentencias SQL
    def execute(self, query, params=None):
        if self.conn and self.cursor:
            self.cursor.execute(query, params)
            self.conn.commit()
        else:
            print("No se puede ejecutar la consulta, no hay conexión a la base de datos.")

    # Devuelve un solo registro
    def fetchone(self, query, params=None):
        if self.conn and self.cursor:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        else:
            print("No se puede ejecutar la consulta, no hay conexión a la base de datos.")
            return None

    # Devuelve listado de registros
    def fetchall(self, query, params=None):
        if self.conn and self.cursor:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        else:
             print("No se puede ejecutar la consulta, no hay conexión a la base de datos.")
             return []  # Devuelvo lista vacía para que no genere un error.

    # Obtener el último ID insertado
    def lastrowid(self):
        if self.cursor:
            return self.cursor.lastrowid
        else:
            print("No se puede obtener el último ID, no hay conexión a la base de datos.")
            return None