from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadCSVForm
import csv
from datetime import datetime, timedelta
from io import TextIOWrapper
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import AguaData, ArData
from django.utils import timezone


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO

@login_required(login_url='/login/')
def dashboard(request):
    if request.method == 'POST':
        print("REQUISIÇÃO POST CHEGOU")
        titulo = request.POST.get('titulo')
        tipo_grafico = request.POST.get('tipo_grafico')
        tipo_dado = request.POST.get('tipo_dado')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        tipo = request.POST.get('tipo')  # 'agua' ou 'ar'
        formato = request.POST.get('formato')  # 'png' ou 'pdf'

        try:
            data_inicio = timezone.make_aware(datetime.strptime(data_inicio, '%Y-%m-%d'))
            data_fim = timezone.make_aware(datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1))
        except ValueError:
            return HttpResponse("Erro ao converter datas.", status=400)


        if tipo == 'agua':
            dados = AguaData.objects.filter(data_amostragem__range=(data_inicio, data_fim))
        else:
            dados = ArData.objects.filter(data_amostragem__range=(data_inicio, data_fim))

        valores = []
        datas = []
        for d in dados:
            valor = getattr(d, tipo_dado, None)
            if valor is not None:
                valores.append(valor)
                datas.append(d.data_amostragem)

        if not valores:
            return render(request, 'dashboard.html', {'erro': 'Nenhum dado encontrado para os critérios selecionados.'})

        plt.figure(figsize=(10, 6))
        if tipo_grafico == 'line':
            plt.plot(datas, valores, marker='o')
        elif tipo_grafico == 'bar':
            plt.bar(datas, valores)
        elif tipo_grafico == 'scatter':
            plt.scatter(datas, valores)
        
        plt.title(titulo)
        plt.xlabel('Data')
        plt.ylabel(tipo_dado.capitalize())
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format=formato)
        plt.savefig('./grafico_teste.png')
        plt.close()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type=f'image/{formato}' if formato == 'png' else 'application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{titulo}.{formato}"'
        return response

    return render(request, 'dashboard.html')


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

    relatorios_agua = AguaData.objects.all().order_by('-data_amostragem')
    relatorios_ar = ArData.objects.all().order_by('-data_amostragem')
    return render(request, 'upload.html', {'form': form, 'relatorios_agua': relatorios_agua, 'relatorios_ar': relatorios_ar})


def excluir_relatorio(request, relatorio_id, tipo):
    if tipo == 'agua':
        relatorio = get_object_or_404(AguaData, id=relatorio_id)
    elif tipo == 'ar':
        relatorio = get_object_or_404(ArData, id=relatorio_id)
    else:
        messages.error(request, "Tipo de relatório inválido.")
        return HttpResponseRedirect(reverse('upload'))

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