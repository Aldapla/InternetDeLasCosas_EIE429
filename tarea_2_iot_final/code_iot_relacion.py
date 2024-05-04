# Tarea 2 IoT profesor Sebastian Bruna
# By Daniel Álvarez Placencia

# Consulta Relacional


import psycopg2  # Importa la biblioteca psycopg2 para manejar la conexión con PostgreSQL.
from datetime import datetime  # Importa datetime para manejar fechas y horas.

class Database:  # Define una clase para manejar operaciones de la base de datos.
    def __init__(self, dbname, user, password, host, port):  # Constructor de la clase con parámetros de conexión.
        self.connection = psycopg2.connect(  # Establece la conexión con la base de datos.
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.connection.cursor()  # Crea un cursor para ejecutar operaciones SQL.

    def insert_sensor(self, tipo, ubicacion):  # Método para insertar un nuevo sensor.
        self.cursor.execute(  # Ejecuta una consulta SQL para insertar el sensor.
            "INSERT INTO sensores (tipo, ubicacion) VALUES (%s, %s) RETURNING id",
            (tipo, ubicacion)
        )
        sensor_id = self.cursor.fetchone()[0]  # Recupera el ID del sensor insertado.
        self.connection.commit()  # Confirma la transacción.
        return sensor_id  # Devuelve el ID del sensor.

    def insert_registro(self, sensor_id, valor, fecha_registro):  # Método para insertar un registro de sensor.
        self.cursor.execute(  # Ejecuta una consulta SQL para insertar el registro.
            "INSERT INTO registros (sensor_id, valor, fecha_registro) VALUES (%s, %s, %s)",
            (sensor_id, valor, fecha_registro)
        )
        self.connection.commit()  # Confirma la transacción.

    def get_records_by_sensor_type(self, sensor_type):  # Método para obtener registros por tipo de sensor.
        self.cursor.execute("""  # Ejecuta una consulta SQL para recuperar registros.
            SELECT sensores.tipo, registros.valor, registros.fecha_registro
            FROM sensores
            JOIN registros ON sensores.id = registros.sensor_id
            WHERE sensores.tipo = %s;
        """, (sensor_type,))
        return self.cursor.fetchall()  # Devuelve todos los registros obtenidos.

    def close(self):  # Método para cerrar la conexión con la base de datos.
        self.cursor.close()  # Cierra el cursor.
        self.connection.close()  # Cierra la conexión.

# Ejemplo de uso de la clase Database
db = Database("tarea2iot", "postgres", "iot123", "localhost", 5432)  # Crea una instancia de la clase Database.

# Insertar algunos sensores y registros
sensor_id = db.insert_sensor("Temperatura", "Laboratorio")  # Inserta un sensor y recupera su ID.
db.insert_registro(sensor_id, 23.5, datetime.now())  # Inserta un registro para el sensor.
db.insert_registro(sensor_id, 24.1, datetime.now())  # Inserta otro registro para el sensor.

sensor_id = db.insert_sensor("Humedad", "Oficina")  # Inserta otro sensor y recupera su ID.
db.insert_registro(sensor_id, 45.0, datetime.now())  # Inserta un registro para el segundo sensor.

# Realizar una consulta relacional
results = db.get_records_by_sensor_type("Temperatura")  # Recupera registros de sensores de temperatura.
print("Registros de sensores de temperatura:")  # Imprime un encabezado.
for result in results:  # Bucle para imprimir cada registro.
    print(result)

# Cerrar la conexión
db.close()  # Cierra la conexión con la base de datos.
