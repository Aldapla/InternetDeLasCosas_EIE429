import os  # Módulo para interactuar con el sistema operativo
import sys  # Módulo para manipular partes específicas del intérprete de Python

def main():
    """Ejecuta tareas administrativas."""
    # Establece la configuración predeterminada del módulo de configuraciones de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitio_web.settings')

    try:
        # Intenta importar la función execute_from_command_line desde django.core.management
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si la importación falla, lanza una excepción con un mensaje de error
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y "
            "disponible en tu variable de entorno PYTHONPATH? ¿Olvidaste activar "
            "un entorno virtual?"
        ) from exc
    # Ejecuta la línea de comandos de Django con los argumentos proporcionados
    execute_from_command_line(sys.argv)

# Punto de entrada del script: si este archivo es ejecutado directamente, llama a la función main()
if __name__ == '__main__':
    main()