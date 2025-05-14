from django.urls import path
from .views import dashboard, upload, excluir_relatorio,trocar_usuario

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upload/', upload, name='upload'),
    path('dashboard/excluir/<str:tipo>/<int:relatorio_id>/', excluir_relatorio, name='excluir_relatorio'),
    path('trocar_usuario/', trocar_usuario, name='trocar_usuario'),
]