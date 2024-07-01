from django.db import models  
from django.contrib.auth.models import User  

class Topico(models.Model):
    # Define un campo de texto con longitud máxima de 200 caracteres para el título del tópico
    titulo = models.CharField(max_length=200)
    # Define un campo de texto para el contenido del tópico.
    contenido = models.TextField()
    # Define un campo de la fecha y hora actuales cuando se crea el objeto
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Devuelve el valor del campo título como la representación de cadena del objeto Topico.
        return self.titulo

class Post(models.Model):

    titulo = models.CharField(max_length=200)
    # Define un campo de texto para el contenido del post.
    contenido = models.TextField()
    # Define un campo de fecha y hora que se establece automáticamente a la fecha y hora actuales cuando se crea el objeto.
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Define una relación de clave foránea con el modelo User. Si se elimina el usuario, también se eliminan sus posts.
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    # Define un campo de texto con longitud máxima de 50 caracteres para la sección del post. Incluye opciones predefinidas.
    seccion = models.CharField(max_length=50, choices=[
        ('estudio', 'Zona de Estudio'),
        ('entretencion', 'Zona de Entretención'),
        ('debate', 'Zona de Debate'),
    ])

    def __str__(self):
        # Devuelve el valor del campo título como la representación de cadena del objeto Post.
        return self.titulo

class Comentario(models.Model):
    # Define una relación de clave foránea con el modelo Post. Si se elimina el post, también se eliminan sus comentarios.
    post = models.ForeignKey(Post, related_name='comentarios', on_delete=models.CASCADE)
    # Define una relación de clave foránea con el modelo User. Si se elimina el usuario, también se eliminan sus comentarios.
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    # Define un campo de texto para el contenido del comentario.
    contenido = models.TextField()
    # Define un campo de fecha y hora que se establece automáticamente a la fecha y hora actuales cuando se crea el objeto.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Devuelve una cadena que incluye el nombre de usuario del autor y el título del post como la representación de cadena del objeto Comentario.
        return f'Comentario de {self.autor.username} en {self.post.titulo}'

class Capital(models.Model):
    # Define un campo de texto con longitud máxima de 100 caracteres para el nombre del país.
    pais = models.CharField(max_length=100)
    # Define un campo de texto con longitud máxima de 100 caracteres para el nombre de la capital.
    capital = models.CharField(max_length=100)

    def __str__(self):
        # Devuelve una cadena que incluye el nombre de la capital y el país como la representación de cadena del objeto Capital.
        return f'{self.capital}, {self.pais}'
