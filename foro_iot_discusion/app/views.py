from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import *
from .forms import *
import requests
import random
import logging

# Configuración del logger para depuración
logger = logging.getLogger(__name__)

def zona_entretencion(request):
    # Obtener todos los posts de la sección de entretenimiento, ordenados por fecha de creación descendente
    posts = Post.objects.filter(seccion='entretencion').order_by('-fecha_creacion')

    # Llamar a la API para obtener la lista de capitales
    api_url = 'http://127.0.0.1:8000/api/capitales/'
    response = requests.get(api_url)
    if response.status_code == 200:
        capitales = response.json()  # Si la respuesta es exitosa, parsear JSON
    else:
        capitales = []  # Si hay un error, usar una lista vacía

    # Seleccionar una capital al azar de la lista obtenida
    capital_random = random.choice(capitales) if capitales else None

    # Registros de depuración para verificar los datos
    logger.debug(f'Posts: {list(posts)}')
    logger.debug(f'Capitales: {capitales}')
    logger.debug(f'Capital Random: {capital_random}')

    # Renderizar la plantilla con los datos obtenidos
    return render(request, 'zona_entretencion.html', {
        'posts': posts,
        'capitales': capitales,
        'capital_random': capital_random
    })

def obtener_capitales(request):
    # Obtener todas las capitales de la base de datos
    capitales = Capital.objects.all()
    # Formatear los datos en una lista de diccionarios
    data = [{'id': capital.id, 'pais': capital.pais, 'capital': capital.capital} for capital in capitales]
    # Devolver los datos como un JsonResponse
    return JsonResponse(data, safe=False)

def verificar_respuesta(request):
    if request.method == 'POST':
        form = VerificarCapitalForm(request.POST)
        if form.is_valid():
            capital_id = form.cleaned_data['capital_id']
            respuesta = form.cleaned_data['respuesta']

            # Buscar la capital en la base de datos usando el ID
            try:
                capital = Capital.objects.get(id=capital_id)
            except Capital.DoesNotExist:
                return HttpResponse('Capital no encontrada', status=404)

            # Verificar si la respuesta es correcta
            if capital.capital.lower() == respuesta.lower():
                return HttpResponse('¡Correcto!')
            else:
                return HttpResponse(f'Incorrecto. La capital de {capital.pais} es {capital.capital}.')
        else:
            # Registrar errores en el formulario
            logger.error(f"Errores del formulario: {form.errors}")
            return HttpResponse(f'Formulario no válido: {form.errors}', status=400)
    return HttpResponse('Método no permitido', status=405)

def adivinar_capital(request):
    # Llamar a la API para obtener la lista de capitales
    api_url = 'http://127.0.0.1:8000/api/capitales/'
    response = requests.get(api_url)
    if response.status_code == 200:
        capitales = response.json()  # Si la respuesta es exitosa, parsear JSON
    else:
        capitales = []  # Si hay un error, usar una lista vacía

    # Seleccionar una capital al azar de la lista obtenida si no está vacía
    if capitales:
        capital = random.choice(capitales)
        context = {
            'pais': capital['pais'],
            'capital_id': capital['capital'],  # Usar el nombre de la capital para la verificación
            'debug_capitales': capitales  # Datos de depuración
        }
    else:
        context = {'debug_capitales': capitales}

    # Renderizar la plantilla con los datos obtenidos
    return render(request, 'adivinar_capital.html', context)


# Uso API GitHub

def github_repos(request):
    user = 'Aldapla'  
    url = f'https://api.github.com/users/{user}/repos'
    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json()  # Parsear la respuesta JSON a un diccionario de Python
    else:
        repos = []

    # Renderizar la plantilla con la lista de repositorios
    return render(request, 'github_repos.html', {'repos': repos})

def listar_topicos(request):
    # Obtener todos los tópicos ordenados por la fecha de creación descendente
    topicos = Topico.objects.order_by('-fecha_creacion')
    # Renderizar la plantilla con la lista de tópicos
    return render(request, 'listar_topicos.html', {'topicos': topicos})

def index(request):
    # Renderizar la plantilla principal (index)
    return render(request, 'index.html')

def zona_estudio(request):
    # Obtener posts de la sección de estudio, ordenados por fecha de creación descendente
    posts = Post.objects.filter(seccion='estudio').order_by('-fecha_creacion')

    # Obtener repositorios de GitHub del usuario especificado
    github_user = 'Aldapla'  # Nombre de usuario de GitHub (puedes cambiarlo)
    github_url = f'https://api.github.com/users/{github_user}/repos'
    github_response = requests.get(github_url)

    if github_response.status_code == 200:
        repos = github_response.json()  # Parsear la respuesta JSON a un diccionario de Python
    else:
        repos = []

    # Obtener datos de la Wikipedia API para el término de búsqueda especificado
    search_query = 'Nikola Tesla'  # Término de búsqueda (puedes cambiarlo)
    wikipedia_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{search_query}'
    wikipedia_response = requests.get(wikipedia_url)

    if wikipedia_response.status_code == 200:
        wikipedia_summary = wikipedia_response.json()
    else:
        wikipedia_summary = {}

    # Pasar los datos obtenidos al contexto de la plantilla
    context = {
        'posts': posts,
        'repos': repos,
        'user': github_user,
        'wikipedia_summary': wikipedia_summary,
        'search_query': search_query
    }
    # Renderizar la plantilla con el contexto
    return render(request, 'zona_estudio.html', context)

def zona_debate(request):
    # Obtener posts de la sección de debate, ordenados por fecha de creación descendente
    posts = Post.objects.filter(seccion='debate').order_by('-fecha_creacion')
    # Renderizar la plantilla con la lista de posts
    return render(request, 'zona_debate.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el nuevo usuario en la base de datos
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}!')
            return redirect('login')  # Redirigir a la página de login
    else:
        form = UserCreationForm()
    # Renderizar la plantilla de registro con el formulario
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Iniciar sesión del usuario
                return redirect('index')  # Redirigir a la página principal
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    # Renderizar la plantilla de login con el formulario
    return render(request, 'login.html', {'form': form})

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user  # Asignar el autor del post al usuario actual
            post.save()  # Guardar el post en la base de datos
            messages.success(request, 'Post creado exitosamente.')
            return redirect('ver_post', post_id=post.id)  # Redirigir a la vista del post creado
    else:
        form = PostForm()
    # Renderizar la plantilla de creación de post con el formulario
    return render(request, 'crear_post.html', {'form': form})

def ver_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Obtener el post por ID, o devolver 404 si no existe
    comentarios = post.comentarios.all()  # Obtener todos los comentarios del post
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post  # Asignar el comentario al post actual
            comentario.autor = request.user  # Asignar el autor del comentario al usuario actual
            comentario.save()  # Guardar el comentario en la base de datos
            messages.success(request, 'Comentario agregado exitosamente.')
            return redirect('ver_post', post_id=post.id)  # Redirigir a la vista del post con el nuevo comentario
    else:
        form = ComentarioForm()
    # Renderizar la plantilla de vista del post con el formulario de comentarios
    return render(request, 'ver_post.html', {'post': post, 'comentarios': comentarios, 'form': form})

def listar_posts(request, seccion):
    # Obtener todos los posts de la sección especificada, ordenados por fecha de creación descendente
    posts = Post.objects.filter(seccion=seccion).order_by('-fecha_creacion')
    # Renderizar la plantilla con la lista de posts y la sección especificada
    return render(request, 'listar_posts.html', {'posts': posts, 'seccion': seccion})
