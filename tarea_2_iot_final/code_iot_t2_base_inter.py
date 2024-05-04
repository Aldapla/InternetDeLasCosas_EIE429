# Tarea 2 IoT profesor Sebastian Bruna
# By Daniel Álvarez Placencia

# Interactua e imprime data


from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime  # Importa los componentes necesarios de SQLAlchemy.
from sqlalchemy.orm import declarative_base, sessionmaker  # Importa las funciones para definir modelos y crear sesiones.

# Actualización para SQLAlchemy 2.0
from sqlalchemy.orm import declarative_base  # Importa la función para definir la base de los modelos declarativos.

Base = declarative_base()  # Crea una clase base para los modelos de SQLAlchemy.

# Configuración de la conexión a la base de datos
engine = create_engine('postgresql://postgres:iot123@localhost/tarea2iot')  # Crea un motor de SQLAlchemy para conectar con PostgreSQL.
Session = sessionmaker(bind=engine)  # Crea una fábrica de sesiones vinculada al motor.
session = Session()  # Inicia una sesión de SQLAlchemy.

class Sensor(Base):  # Define una clase que mapea a una tabla de sensores en la base de datos.
    """Define la tabla de sensores."""
    __tablename__ = 'sensores'  # Nombre de la tabla en la base de datos.
    id = Column(Integer, primary_key=True)  # Define la columna de ID como clave primaria.
    tipo = Column(String)  # Define una columna para el tipo de sensor.
    ubicacion = Column(String)  # Define una columna para la ubicación del sensor.
    valor = Column(Float)  # Define una columna para el valor medido por el sensor.
    fecha_registro = Column(DateTime)  # Define una columna para la fecha de registro del valor.

# Crear la tabla en la base de datos (en caso de que no exista)
Base.metadata.create_all(engine)  # Crea las tablas en la base de datos según los modelos definidos.

def add_sensor(sensor):  # Función para añadir un sensor a la base de datos.
    """Añade un sensor a la base de datos."""
    session.add(sensor)  # Añade el sensor a la sesión.
    session.commit()  # Confirma la transacción para persistir el cambio.

def get_all_sensors():  # Función para obtener todos los sensores de la base de datos.
    """Obtiene todos los sensores de la base de datos."""
    return session.query(Sensor).all()  # Retorna una lista de todos los sensores registrados.

def plot_data():  # Función para realizar un gráfico de los datos de los sensores.
    """Realiza el gráfico de los datos de los sensores."""
    import matplotlib.pyplot as plt  # Importa la biblioteca para crear gráficos.
    sensors = get_all_sensors()  # Obtiene todos los sensores de la base de datos.

    # Suponiendo que los IDs de los dispositivos y los valores son los datos a graficar
    device_ids = [sensor.id for sensor in sensors]  # Lista de IDs de los sensores.
    values = [sensor.valor for sensor in sensors]  # Lista de valores de los sensores.

    plt.figure(figsize=(10, 5))  # Define el tamaño del gráfico.
    plt.plot(device_ids, values, marker='o', linestyle='-')  # Crea un gráfico de línea con puntos.
    plt.xlabel('Device ID')  # Etiqueta del eje X.
    plt.ylabel('Data Value')  # Etiqueta del eje Y.
    plt.title('Sensor Data')  # Título del gráfico.
    plt.show()  # Muestra el gráfico.

if __name__ == "__main__":
    # Agregar nuevos sensores
    from datetime import datetime
    new_sensor = Sensor(tipo="Temperatura", ubicacion="Oficina", valor=23.5, fecha_registro=datetime.now())
    add_sensor(new_sensor)  # Añade un nuevo sensor a la base de datos.

    # Mostrar todos los sensores
    all_sensors = get_all_sensors()  # Obtiene todos los sensores.
    for sensor in all_sensors:  # Imprime información de cada sensor.
        print(f"ID: {sensor.id}, Tipo: {sensor.tipo}, Ubicación: {sensor.ubicacion}, Valor: {sensor.valor}, Fecha: {sensor.fecha_registro}")

    # Graficar datos
    plot_data()  # Llama a la función para graficar los datos.

    session.close()  # Cierra la sesión de SQLAlchemy.
