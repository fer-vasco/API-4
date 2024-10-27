import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import yfinance as yf


def Parametros_de_visualizacion():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)


def y_market_cap(ticker):
    info = yf.Ticker(ticker).fast_info

    return info['market_cap']
    

def fetch_gainers(api_key):
    url = f'https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey={api_key}'
    response = requests.get(url)
    gainers = response.json()
    
    df_empresas = pd.DataFrame()
    simbolos = []
    nombres = []
    cambios = []
    capitales = []
    
    for gainer in gainers:

        simbolos.append(gainer['symbol'])
        nombres.append(gainer['name'])
        cambios.append(gainer['changesPercentage'])
        capitales.append(y_market_cap(gainer['symbol']))
        

    df_empresas = pd.DataFrame(list(zip(simbolos, nombres, cambios, capitales)),
           columns =['Ticker', 'Empresa', 'Cambio', 'Capital'])

    df_empresas.sort_values(by=['Capital'], ascending=False, inplace=True)
    df_empresas['Capital'] = round(df_empresas['Capital']/1000000,1).astype('str') + ' M'
    df_empresas['Cambio'] = round(df_empresas['Cambio'],1).astype('str') + '%'
    df_empresas.set_index('Ticker', inplace=True)
    
    return df_empresas


def Calcular_e_imprimir_df(api_key):
    resultados = fetch_gainers(api_key)
    st.dataframe(resultados)


def Graficar_tickers():
    companies = ['META'] 
    tickers = yf.Tickers(companies)
    tickers_hist = tickers.history(period='5d',interval='1d')
    
    return tickers_hist


# Inicio del programa
api_key = 'BKewxsq6oAF5okFIZ5b84WGWGiy3kiOm'
clave = str(123)
st.title('🍁 Resultados GIT')
text_input = st.text_input("Clave 👇", type="password")


if text_input:
    df = Graficar_tickers()
    st.dataframe(df)

exit()







if text_input:
    if str(text_input) == clave:
        Parametros_de_visualizacion()
        corrida = datetime.now() - timedelta(hours=3)
        corrida = corrida.strftime('%d-%m-%y %H:%M')
        st.write(f'Actualización de datos:')
        st.write(corrida)
        Calcular_e_imprimir_df(api_key)
    else:
        st.write("Clave incorrecta")
