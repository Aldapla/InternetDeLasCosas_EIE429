# Tarea 2 IoT profesor Sebastian Bruna
# By Daniel Álvarez Placencia

# Programa Final


import psycopg2  # para la conexión con PostgreSQL.
from psycopg2 import extras  # Importa 'extras' para características adicionales como los DictCursor.
import serial  # comunicación con dispositivos serie.
import time  #  util para manejar funciones relacionadas con el tiempo.
from datetime import datetime  #  fechas y horas.
import matplotlib.pyplot as plt  #visualización de datos.

class Database:  # Define una clase para la interacción con la base de datos.
    def __init__(self, dbname, user, password, host, port):  # Constructor con configuración de la base de datos.
        self.connection = psycopg2.connect(  # Establece la conexión con la base de datos.
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  # Crea un cursor que devuelve los resultados como diccionarios.

    def insert_data(self, timestamp, device_type, device_id, query, data_value):  # Método para insertar datos.
        print("Creating: Insertando datos en la base de datos...")
        self.cursor.execute(  # Ejecuta una consulta SQL para insertar datos.
            "INSERT INTO Data (timestamp, device_type, device_id, query, data_value) VALUES (%s, %s, %s, %s, %s)",
            (timestamp, device_type, device_id, query, data_value)
        )
        self.connection.commit()  # Confirma los cambios en la base de datos.

    def fetch_data(self, query="SELECT * FROM Data"):  # Método para recuperar datos.
        print("Reading: Leyendo datos de la base de datos...")
        self.cursor.execute(query)  # Ejecuta una consulta SQL.
        return self.cursor.fetchall()  # Devuelve todos los registros recuperados.

    def update_data(self, device_id, new_data_value):  # Método para actualizar datos.
        print("Updating: Actualizando datos en la base de datos...")
        self.cursor.execute(  # Ejecuta una consulta SQL para actualizar datos.
            "UPDATE Data SET data_value = %s WHERE device_id = %s",
            (new_data_value, device_id)
        )
        self.connection.commit()  # Confirma los cambios.

    def delete_data(self, device_id):  # Método para eliminar datos.
        print("Deleting: Eliminando datos de la base de datos...")
        self.cursor.execute("DELETE FROM Data WHERE device_id = %s", (device_id,))
        self.connection.commit()  # Confirma los cambios.

    def close(self):  # Método para cerrar la conexión a la base de datos.
        self.cursor.close()  # Cierra el cursor.
        self.connection.close()  # Cierra la conexión.

class SerialReader:  # Define una clase para la lectura de datos serie.
    def __init__(self, port, baudrate, timeout=1):  # Constructor con configuración del puerto serie.
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def read_serial_data(self, duration=120):  # Método para leer datos del puerto serie por un tiempo determinado.
        """Lee datos del puerto serie durante un tiempo especificado (en segundos)."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)  # Abre el puerto serie.
            print(f"Leyendo datos desde {self.port} durante {duration} segundos...")
            data = []

            start_time = time.time()  # Registra el tiempo de inicio.
            while time.time() - start_time < duration:  # Lee datos mientras no se exceda la duración especificada.
                line = self.ser.readline().decode().strip()  # Lee y decodifica una línea de datos.
                if line:
                    data.append(line)

            self.ser.close()  # Cierra el puerto serie.
            return data

        except serial.SerialException as e:  # Captura excepciones relacionadas con la conexión serie.
            print("Error al abrir el puerto serie:", e)
            return None

    @staticmethod
    def convert_to_decimal(hex_string):  # Método estático para convertir de hexadecimal a decimal.
        """Convierte una cadena hexadecimal a un número decimal."""
        return int(hex_string, 16)

    def process_data(self, data):  # Método para procesar los datos leídos.
        """Procesa y muestra información detallada de los datos leídos."""
        processed_data = []

        for line in data:
            bytes_list = line.split()  # Separa los bytes en la línea.

            try: # Depu
                device_type = self.convert_to_decimal(bytes_list[1])
                device_id = self.convert_to_decimal(bytes_list[2])
                query = self.convert_to_decimal(bytes_list[3])
                data_value = self.convert_to_decimal(bytes_list[4])

                print(f"Device type: {device_type:02X}", end='-')
                if device_type == 1:
                    print("temperature", end=', ')
                    print(f"data: {data_value} grados")
                elif device_type == 2:
                    print("humidity", end=', ')
                    print(f"data: {data_value} %")

                print(f"id: {device_id:02X}", end=', ')
                print(f"query: {query:02X}")

                # Almacena la información para inserción en la base de datos
                processed_data.append((
                    datetime.now(),  # Utiliza la fecha y hora actuales
                    device_type,
                    device_id,
                    query,
                    data_value
                ))

            except (IndexError, ValueError) as e:  # Captura errores durante el procesamiento.
                print("Error al procesar la línea:", e)

        return processed_data

# Configuración del puerto serie
port = '/dev/ttyACM0'
baudrate = 9600

# Configuración de la base de datos
db = Database("arduino_data", "postgres", "hola123", "localhost", 5432)

# Crear una instancia de la clase SerialReader
serial_reader = SerialReader(port, baudrate)

# Leer datos del puerto serie durante 2 minutos
data = serial_reader.read_serial_data(duration=120)

if data:
    print("Datos leídos desde el puerto serie:")
    processed_data = serial_reader.process_data(data)

    for entry in processed_data:
        db.insert_data(*entry)

# b. Consulta relacional:
# Realizamos una consulta específica para analizar la integridad de los datos

print("\nConsulta relacional:")
related_data = db.fetch_data("SELECT device_id, AVG(data_value) AS average_value FROM Data GROUP BY device_id")
for row in related_data:
    print(f"Device ID: {row['device_id']}, Average Value: {row['average_value']}")

# c. Plot de una variable:
# Extraemos datos de `Data` para graficar
timestamps, values = [], []
for row in db.fetch_data("SELECT timestamp, data_value FROM Data ORDER BY timestamp"):
    timestamps.append(row['timestamp'])
    values.append(row['data_value'])

# Creamo el gráfico
plt.figure(figsize=(10, 5))
plt.plot(timestamps, values, marker='o', label='Data Value')

plt.xlabel('Timestamp')
plt.ylabel('Data Value')
plt.title('Data Value Over Time')
plt.legend()

# Mostrar la gráfica
plt.show()

# Cierra la conexión a la base de datos
db.close()
print("Conexión a la base de datos cerrada.")
