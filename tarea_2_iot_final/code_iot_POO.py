# Tarea 2 IoT profesor Sebastian Bruna
# By Daniel Álvarez Placencia

# Leer e Imprimir Datos desde el Arduino

import serial  # Importa la librería para manejar la comunicación serie.
import time  # Importa la librería para manejar funciones relacionadas con el tiempo.

class SerialReader:  # Define una clase para leer datos del puerto serie.
    def __init__(self, port, baudrate, timeout=1):  # Constructor de la clase con parámetros de configuración inicial.
        self.port = port  # Asigna el puerto serie.
        self.baudrate = baudrate  # Asigna la velocidad en baudios.
        self.timeout = timeout  # Asigna el tiempo de espera para la conexión.

    def read_serial_data(self, num_lines=20):  # Método para leer datos del puerto serie.
        """Lee datos del puerto serie."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)  # Inicia la conexión serie.
            print(f"Leyendo datos desde {self.port}...")  # Mensaje indicando que se está leyendo del puerto.
            data = []  # Lista para almacenar los datos leídos.
            for _ in range(num_lines):  # Bucle para leer varias líneas de datos.
                line = self.ser.readline().decode().strip()  # Lee una línea, la decodifica y elimina espacios.
                data.append(line)  # Agrega la línea a la lista de datos.
            self.ser.close()  # Cierra la conexión serie.
            return data  # Devuelve la lista de datos.
        except serial.SerialException as e:  # Captura excepciones relacionadas con la conexión serie.
            print("Error al abrir el puerto serie:", e)  # Imprime el error.
            return None

    @staticmethod
    def convert_to_decimal(hex_string):  # Método estático para convertir hexadecimal a decimal.
        """Convierte una cadena hexadecimal a un número decimal."""
        return int(hex_string, 16)  # Realiza la conversión y devuelve el resultado.

    def print_data_info(self, data):  # Método para imprimir la información de los datos leídos.
        """Imprime la información detallada de los datos leídos."""
        for i, line in enumerate(data, start=1):  # Bucle para procesar cada línea de datos.
            print(f"Dato {i}:")  # Imprime el número de dato.
            bytes_list = line.split()  # Divide la línea en componentes.
            try:
                device_type = self.convert_to_decimal(bytes_list[1])  # Obtiene el tipo de dispositivo.
                device_id = self.convert_to_decimal(bytes_list[2])  # Obtiene el ID del dispositivo.
                query = self.convert_to_decimal(bytes_list[3])  # Obtiene la consulta.
                data_value = self.convert_to_decimal(bytes_list[4])  # Obtiene el valor de los datos.

                print(f"Device type: {device_type:02X}", end='-')  # Imprime el tipo de dispositivo en hexadecimal.
                if device_type == 1:
                    print("temperature", end=', ')  # Especifica que el tipo de dato es temperatura.
                    print(f"data: {data_value} grados")  # Imprime el valor de la temperatura.
                elif device_type == 2:
                    print("humidity", end=', ')  # Especifica que el tipo de dato es humedad.
                    print(f"data: {data_value} %")  # Imprime el valor de la humedad.
                print(f"id: {device_id:02X}", end=', ')  # Imprime el ID del dispositivo.
                print(f"query: {query:02X}")  # Imprime la consulta.
            except (IndexError, ValueError) as e:  # Captura errores durante el procesamiento.
                print("Error al procesar la línea:", e)  # Imprime el error.

# Configuración del puerto serie
port = '/dev/ttyACM0'  # Asigna el puerto serie.
baudrate = 9600  # Asigna la velocidad en baudios.

# Crear una instancia de la clase
serial_reader = SerialReader(port, baudrate)  # Crea un objeto de la clase SerialReader.

# Esperar 2 segundos antes de la lectura inicial de datos
print("Esperando 2 segundos antes de la lectura de los datos...")  # Mensaje de espera.
time.sleep(2)  # Pausa de 2 segundos.

# Leer datos del puerto serie
data = serial_reader.read_serial_data(num_lines=4)  # Lee 4 líneas de datos del puerto serie.
if data:  # Si se leyeron datos.
    print("Datos leídos desde el puerto serie:")  # Mensaje de datos leídos.
    for i, line in enumerate(data[1:], start=1):  # Bucle para imprimir cada línea de datos.
        print(f"Dato {i+1}: {line}")

    print("\nInformación detallada:")  # Mensaje de información detallada.
    serial_reader.print_data_info(data[1:])  # Imprime información detallada de los datos.
else:
    print("No se pudieron leer datos desde el puerto serie.")  # Mensaje si no se pudieron leer datos.
