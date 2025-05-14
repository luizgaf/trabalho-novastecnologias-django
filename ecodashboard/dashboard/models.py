from django.db import models
from django.contrib.auth.models import User

class AguaData(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    arquivo_nome = models.CharField(max_length=255)  # Nome original do arquivo CSV
    data_registro = models.DateTimeField(auto_now_add=True)  # Data do upload

    # Dados medidos 
    data_amostragem = models.DateField()  # Data da medição no CSV
    ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    turbidez = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    oxigenio_dissolvido = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Qualidade geral da água baseada em critérios
    qualidade = models.CharField(max_length=50, choices=[
        ('boa', 'Boa'),
        ('moderada', 'Moderada'),
        ('ruim', 'Ruim'),
        ('desconhecida', 'Desconhecida')
    ], default='desconhecida')

    def __str__(self):
        return f"Amostra em {self.data_amostragem} por {self.usuario.username}"


class ArData(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    arquivo_nome = models.CharField(max_length=255)
    data_registro = models.DateTimeField(auto_now_add=True)  # Data do upload

    # Data em que os dados foram coletados (informada no CSV)
    data_amostragem = models.DateField()

    # Indicadores da qualidade do ar
    co2 = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # ppm
    pm25 = models.DecimalField("Partículas PM2.5 (µg/m³)", max_digits=6, decimal_places=2, null=True, blank=True)
    pm10 = models.DecimalField("Partículas PM10 (µg/m³)", max_digits=6, decimal_places=2, null=True, blank=True)
    o3 = models.DecimalField("Ozônio (ppb)", max_digits=6, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    umidade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Classificação da qualidade do ar
    qualidade = models.CharField(max_length=50, choices=[
        ('boa', 'Boa'),
        ('moderada', 'Moderada'),
        ('ruim', 'Ruim'),
        ('desconhecida', 'Desconhecida')
    ], default='desconhecida')

    def __str__(self):
        return f"Amostra em {self.data_amostragem} por {self.usuario.username}"
