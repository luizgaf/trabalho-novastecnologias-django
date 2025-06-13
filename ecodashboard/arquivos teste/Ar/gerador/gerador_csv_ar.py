import csv
import random
import sys
from datetime import datetime

def generate_air_data():
    for month in range(1, 7):  # Janeiro a Junho
        filename = f"{month:02d}-2025-ar-registo-sensor.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['data_amostragem', 'co2', 'pm25', 'pm10', 'o3', 
                           'temperatura', 'umidade', 'qualidade', 'tipo'])
            
            for day in range(1, 32):  # 31 dias
                try:
                    date = datetime(2025, month, day)
                except ValueError:
                    continue  # Pula dias inválidos
                
                data_amostragem = date.strftime('%Y-%m-%d 00:00:00')
                co2 = round(random.uniform(350.0, 600.0), 1)
                pm25 = round(random.uniform(5.0, 50.0), 1)
                pm10 = round(random.uniform(10.0, 100.0), 1)
                o3 = round(random.uniform(0.01, 0.15), 3)
                temperatura = round(random.uniform(15.0, 35.0), 1)
                umidade = round(random.uniform(30.0, 90.0), 1)
                
                # Determinar qualidade
                if pm25 > 35 or pm10 > 50 or co2 > 450 or o3 > 0.08:
                    qualidade = "Ruim"
                elif pm25 < 15 and pm10 < 30 and co2 < 400 and o3 < 0.05:
                    qualidade = "Boa"
                else:
                    qualidade = "Moderada"
                
                writer.writerow([data_amostragem, co2, pm25, pm10, o3, 
                               temperatura, umidade, qualidade, 'ar'])

if __name__ == "__main__":
    generate_air_data()
    print("Arquivos de dados de ar gerados com sucesso! (01-2025 a 06-2025)")