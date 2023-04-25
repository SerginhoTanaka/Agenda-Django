from django.urls import path
from accounts.views import dashboard
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('busca', views.busca, name='busca' ),
    path('contato/<int:contato_id>', views.ver_contato, name='ver_contato' ),
    path('dashbord/', dashboard, name='adicionar' ),
    path('contato/editar/<int:contato_id>', views.editar, name='editar' ),
    path('excluir/<int:contato_id>', views.excluir, name='excluir' ),
]
