# 🌱 ECO DASHBOARD

Aplicação web desenvolvida com Django para análise de dados ambientais, focando na qualidade da **água** e do **ar**. O sistema permite o upload de arquivos CSV, geração de gráficos com base nos dados e exportação dos gráficos em formato PNG ou PDF.

## 🚀 Funcionalidades

- Upload de arquivos CSV contendo dados ambientais
- Armazenamento e visualização de dados de **água** e **ar**
- Filtros por data e tipo de dado
- Geração de gráficos (linha, barra ou dispersão)
- Exportação dos gráficos como imagem (PNG) ou documento (PDF)
- Interface de administração para gerenciamento de dados

## 🛠️ Tecnologias utilizadas

- Python 3.x
- Django 4+
- Matplotlib
- HTML/CSS (estilização básica)
- SQLite (padrão do Django)

## 📁 Estrutura dos CSVs

### Para dados de **água**
```csv
data_amostragem,ph,turbidez,oxigenio_dissolvido,temperatura,qualidade,tipo
2024-05-01,7.1,2.3,6.8,22,boa,agua
```

### Para dados de **ar**
```csv
data_amostragem,co2,pm25,pm10,o3,temperatura,umidade,qualidade,tipo
2024-05-01,400,35,50,0.03,25,60,razoavel,ar
```

## ⚙️ Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/eco-dashboard.git
cd eco-dashboard
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute as migrações do banco de dados:

```bash
python manage.py migrate
```

5. Inicie o servidor:

```bash
python manage.py runserver
```

6. Acesse via navegador:

```
http://127.0.0.1:8000/
```

## 🔐 Login

O sistema utiliza autenticação de usuário. Crie um superusuário para acessar o painel admin:

```bash
python manage.py createsuperuser
```

## 📌 Observações

- Os dados devem estar no formato CSV com colunas corretamente nomeadas e o campo `tipo` preenchido com `agua` ou `ar`.
- O sistema ignora valores inválidos ou campos vazios nos gráficos.