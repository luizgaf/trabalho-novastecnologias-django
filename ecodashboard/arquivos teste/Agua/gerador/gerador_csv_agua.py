import csv
import random
import sys
from datetime import datetime

def generate_water_data():
    for month in range(1, 7):  # Janeiro a Junho
        filename = f"{month:02d}-2025-agua-registo-sensor.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['data_amostragem', 'ph', 'turbidez', 'oxigenio_dissolvido', 
                           'temperatura', 'qualidade', 'tipo'])
            
            for day in range(1, 32):  # 31 dias
                try:
                    date = datetime(2025, month, day)
                except ValueError:
                    continue  # Pula dias inválidos (ex: 31/04)
                
                data_amostragem = date.strftime('%Y-%m-%d 00:00:00')
                ph = round(random.uniform(6.0, 8.5), 2)
                turbidez = round(random.uniform(0.1, 5.0), 2)
                oxigenio = round(random.uniform(5.0, 10.0), 2)
                temperatura = round(random.uniform(15.0, 30.0), 1)
                
                # Determinar qualidade
                if ph < 6.5 or ph > 8.0 or oxigenio < 6.0:
                    qualidade = "Ruim"
                elif (6.5 <= ph <= 7.5) and (7.0 <= oxigenio <= 9.0) and turbidez < 2.0:
                    qualidade = "Boa"
                else:
                    qualidade = "Moderada"
                
                writer.writerow([data_amostragem, ph, turbidez, oxigenio, 
                               temperatura, qualidade, 'agua'])

if __name__ == "__main__":
    generate_water_data()
    print("Arquivos de dados de água gerados com sucesso! (01-2025 a 06-2025)")