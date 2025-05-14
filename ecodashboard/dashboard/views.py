from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadCSVForm
import csv
from datetime import datetime
from io import TextIOWrapper
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import AguaData, ArData


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login/')
@login_required(login_url='/login/')
def upload(request):
    form = UploadCSVForm()

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_csv = TextIOWrapper(request.FILES['arquivo'].file, encoding='utf-8')
            leitor = csv.DictReader(arquivo_csv)
            
            for linha in leitor:
                if linha['tipo'] == 'agua':  
                    AguaData.objects.create(
                        usuario=request.user,
                        arquivo_nome=request.FILES['arquivo'].name,
                        data_amostragem=datetime.strptime(linha['data'], '%Y-%m-%d'),
                        ph=linha.get('ph') or None,
                        turbidez=linha.get('turbidez') or None,
                        oxigenio_dissolvido=linha.get('oxigenio_dissolvido') or None,
                        temperatura=linha.get('temperatura') or None,
                        qualidade=linha.get('qualidade', 'desconhecida')
                    )
                elif linha['tipo'] == 'ar':
                    ArData.objects.create(
                        usuario=request.user,
                        arquivo_nome=request.FILES['arquivo'].name,
                        data_amostragem=datetime.strptime(linha['data'], '%Y-%m-%d'),
                        co2=linha.get('co2') or None,
                        pm25=linha.get('pm25') or None,
                        pm10=linha.get('pm10') or None,
                        o3=linha.get('o3') or None,
                        temperatura=linha.get('temperatura') or None,
                        umidade=linha.get('umidade') or None,
                        qualidade=linha.get('qualidade', 'desconhecida')
                    )
            return redirect('upload')  

    relatorios_agua = AguaData.objects.all().order_by('-data_registro')
    relatorios_ar = ArData.objects.all().order_by('-data_registro')
    return render(request, 'upload.html', {'form': form, 'relatorios_agua': relatorios_agua, 'relatorios_ar': relatorios_ar})


def excluir_relatorio(request, relatorio_id, tipo):
    # verifica se e um relatório de água ou de ar
    if tipo == 'agua':
        relatorio = get_object_or_404(AguaData, id=relatorio_id)
    elif tipo == 'ar':
        relatorio = get_object_or_404(ArData, id=relatorio_id)
    else:
        messages.error(request, "Tipo de relatório inválido.")
        return HttpResponseRedirect(reverse('upload'))

    # Verifica se o usuário pertence ao grupo moderadores ou o usuário que postou o relatório
    if request.user.groups.filter(name='moderadores').exists() or request.user == relatorio.usuario:
        relatorio.delete()
        messages.success(request, "Relatório excluído com sucesso.")
    else:
        messages.error(request, "Você não tem permissão para excluir este relatório.")

    return HttpResponseRedirect(reverse('upload'))


from django.contrib.auth import logout

def trocar_usuario(request):
    logout(request)
    
    return redirect('/login/')