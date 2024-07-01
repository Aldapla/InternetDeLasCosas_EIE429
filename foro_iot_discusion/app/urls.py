from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

# Definición de las rutas URL y su correspondiente vista
urlpatterns = [
    path('', index, name='index'),
    path('zona_estudio/', zona_estudio, name='zona_estudio'),
    path('zona_entretencion/', zona_entretencion, name='zona_entretencion'),
    path('zona_debate/', zona_debate, name='zona_debate'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('crear_post/', crear_post, name='crear_post'),
    path('post/<int:post_id>/', ver_post, name='ver_post'),
    path('posts/<str:seccion>/', listar_posts, name='listar_posts'),
    path('topicos/', listar_topicos, name='listar_topicos'),
    path('github_repos/', github_repos, name='github_repos'),
    path('api/capitales/', obtener_capitales, name='obtener_capitales'),
    path('verificar_respuesta/', verificar_respuesta, name='verificar_respuesta'),
    path('adivinar_capital/', adivinar_capital, name='adivinar_capital'),
]
