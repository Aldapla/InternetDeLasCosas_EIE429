# Tarea 2 IoT profesor Sebastian Bruna
# By Daniel Álvarez Placencia

# Operaciones CRUD 

# Importar las librerías necesarias para la base de datos y la comunicación serial
import psycopg2
import serial
import time
from datetime import datetime

# Clase para manejar operaciones en PostgreSQL
class BaseDatos:
    def __init__(self, nombre_bd, usuario, contraseña, host, puerto):
        # Establecer una conexión con la base de datos PostgreSQL
        self.conexion = psycopg2.connect(
            dbname=nombre_bd, user=usuario, password=contraseña, host=host, port=puerto
        )
        # Crear un objeto cursor para ejecutar consultas
        self.cursor = self.conexion.cursor()

    # Método para insertar datos en la base de datos
    def insertar_datos(self, fecha_hora, tipo_dispositivo, id_dispositivo, codigo_comando, valor_datos):
        print("Creando: Insertando datos en la base de datos...")
        self.cursor.execute(
            "INSERT INTO Datos (fecha_hora, tipo_dispositivo, id_dispositivo, codigo_comando, valor_datos) VALUES (%s, %s, %s, %s, %s)",
            (fecha_hora, tipo_dispositivo, id_dispositivo, codigo_comando, valor_datos)
        )
        self.conexion.commit()

    # Método para obtener datos de la base de datos
    def obtener_datos(self, consulta="SELECT * FROM Datos"):
        print("Leyendo: Leyendo datos de la base de datos...")
        self.cursor.execute(consulta)
        return self.cursor.fetchall()

    # Método para actualizar datos en la base de datos
    def actualizar_datos(self, id_dispositivo, nuevo_valor_datos):
        print("Actualizando: Actualizando datos en la base de datos...")
        self.cursor.execute(
            "UPDATE Datos SET valor_datos = %s WHERE id_dispositivo = %s",
            (nuevo_valor_datos, id_dispositivo)
        )
        self.conexion.commit()

    # Método para eliminar datos de la base de datos
    def eliminar_datos(self, id_dispositivo):
        print("Eliminando: Eliminando datos de la base de datos...")
        self.cursor.execute("DELETE FROM Datos WHERE id_dispositivo = %s", (id_dispositivo,))
        self.conexion.commit()

    # Método para cerrar la conexión a la base de datos y el cursor
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()

# Clase para leer datos seriales de dispositivos
class LectorSerial:
    def __init__(self, puerto, tasa_baudios, tiempo_espera=1):
        self.puerto = puerto
        self.tasa_baudios = tasa_baudios
        self.tiempo_espera = tiempo_espera

    # Método para leer datos del puerto serial durante un tiempo especificado
    def leer_datos_serial(self, duracion=120):
        try:
            self.dispositivo_serial = serial.Serial(self.puerto, self.tasa_baudios, timeout=self.tiempo_espera)
            print(f"Leyendo datos desde {self.puerto} durante {duracion} segundos...")
            datos = []
            tiempo_inicio = time.time()
            while time.time() - tiempo_inicio < duracion:
                linea = self.dispositivo_serial.readline().decode().strip()
                if linea:
                    datos.append(linea)
            self.dispositivo_serial.close()
            return datos
        except serial.SerialException as e:
            print("Error al abrir el puerto serial:", e)
            return None

    # Método estático para convertir cadena hexadecimal a decimal
    @staticmethod
    def convertir_a_decimal(cadena_hex):
        return int(cadena_hex, 16)

    # Método para procesar y mostrar información detallada de los datos leídos
    def procesar_datos(self, datos):
        datos_procesados = []
        for linea in datos:
            lista_bytes = linea.split()
            try:
                tipo_dispositivo = self.convertir_a_decimal(lista_bytes[1])
                id_dispositivo = self.convertir_a_decimal(lista_bytes[2])
                codigo_comando = self.convertir_a_decimal(lista_bytes[3])
                valor_datos = self.convertir_a_decimal(lista_bytes[4])
                print(f"Tipo de dispositivo: {tipo_dispositivo:02X}", end='-')
                if tipo_dispositivo == 1:
                    print("temperatura", end=', ')
                    print(f"datos: {valor_datos} grados")
                elif tipo_dispositivo == 2:
                    print("humedad", end=', ')
                    print(f"datos: {valor_datos} %")
                print(f"id: {id_dispositivo:02X}", end=', ')
                print(f"comando: {codigo_comando:02X}")
                datos_procesados.append((
                    datetime.now(),  # Usar fecha y hora actual
                    tipo_dispositivo,
                    id_dispositivo,
                    codigo_comando,
                    valor_datos
                ))
            except (IndexError, ValueError) as e:
                print("Error al procesar línea:", e)
        return datos_procesados

# Configuración del puerto serial
puerto_serial = '/dev/ttyACM0'
tasa_baudios = 9600

# Configuración de la base de datos
config_db = BaseDatos("datos_arduino", "postgres", "iot123", "localhost", 5432)

# Crear una instancia de la clase LectorSerial
lector_serial = LectorSerial(puerto_serial, tasa_baudios)

# Leer datos del puerto serial durante 2 minutos
datos_serial = lector_serial.leer_datos_serial(duracion=120)

if datos_serial:
    print("Datos leídos del puerto serial:")
    datos_serial_procesados = lector_serial.procesar_datos(datos_serial)

    print("\nInsertando datos en la base de datos...")
    for entrada in datos_serial_procesados:
        config_db.insertar_datos(*entrada)

# Leer y mostrar datos de la base de datos
datos_almacenados = config_db.obtener_datos("SELECT * FROM Datos")
print("\nDatos en la base de datos:")
for fila in datos_almacenados:
    print(fila)

# Actualizar un registro en la base de datos
config_db.actualizar_datos(1, 75.0)  # Actualizar `valor_datos` para `id_dispositivo=1`

# Eliminar un registro en la base de datos
config_db.eliminar_datos(1)

# Cerrar la conexión con la base de datos
config_db.cerrar()
print("Conexión con la base de datos cerrada.")
