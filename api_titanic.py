from flask import Flask
from flask_ngrok import run_with_ngrok#, Resource, Api
from flask_restful import Resource, Api

import json
import requests
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
run_with_ngrok(app)  
api = Api(app) 


def salva_figura(df, classe):
    fig = plt.figure(figsize=(10, 5))
    sns.boxplot(data = df, x='survived', y='age', hue='sex');
    plt.title(f'Idade dos passageiros da {classe}ª classe')
    fig.savefig('grafico.jpg')

class Filtro(Resource):
    def get(self, filtro, valor):
        df_filtrado = df.query(f'{filtro} == "{valor}"')
        df_agrupado = df_filtrado.groupby('sex')['age'].mean().to_frame().reset_index()

        df_agrupado.to_csv('resposta.csv')
        
        salva_figura(df_filtrado, valor)

        return df_agrupado.to_json()

@app.route("/")
def home():
    return "<h1>Selecione um '/FILTRO/VALOR' a URL</h1>"

api.add_resource(Filtro, '/<string:filtro>/<int:valor>')

if __name__ == '__main__':

    df = pd.read_csv('https://www.openml.org/data/get_csv/16826755/phpMYEkMl')
    df['age'] = df['age'].replace({'?':None}).astype(float)
    
    app.run()
