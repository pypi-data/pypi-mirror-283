import pandas as pd
import requests 
import zipfile  
import numpy as np
import urllib.request
from pathlib import Path

path = 'https://raw.githubusercontent.com/victorncg/financas_quantitativas/main/Data%20Extraction/Stock%20Exchange/Index%20Composition/'
file = 'backend_index.py'


with urllib.request.urlopen(path + file) as response:
    py_content = response.read().decode('utf-8')

exec(py_content)



def _parse_ibov():

    try:

        url = "https://raw.githubusercontent.com/victorncg/financas_quantitativas/main/IBOV.csv"
        df = pd.read_csv(
            url, encoding="latin-1", sep="delimiter", header=None, engine="python"
        )
        df = pd.DataFrame(df[0].str.split(";").tolist())

        return df

    except:

        print("An error occurred while parsing data from IBOV.")



def _standardize_ibov():

    try:
        df = _parse_ibov()
        df.columns = list(df.iloc[1])
        df = df[2:][["Código", "Ação", "Tipo", "Qtde. Teórica", "Part. (%)"]]
        df.reset_index(drop=True, inplace=True)

        return df
    except:

        print("An error occurred while manipulating data from IBOV.")



def _standardize_sp500():
    """
    This function fetches the updated composition of the S&P 500 index. 
    
    Parameters
    ----------
    
    """

    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    df = table[0]

    return df



def _adapt_index(
    index: object, assets: object = "all", mode: object = "df"
):
    """
    This function processes the data from the latest composition of either IBOV or S&P 500. 
    
    Parameters
    ----------
    index : choose the index to be returned, if IBOV or S&P 500
    ativos : you can pass a list with the desired tickets. Default = 'all'.
    mode: you can return either the whole dataframe from B3, or just the list containing the tickers which compose IBOV. Default = 'df'.
    
    """

    if index == "sp500":

        df = _standardize_sp500()

        if assets != "all":
            df = df[df["Symbol"].isin(assets)]

        if mode == "list":
            df = list(df.Symbol)

    else:

        df = return_index(index)

        if assets != "all":
            df = df[df["cod"].isin(assets)]

        if mode == "list":
            df = list(df.cod)
    
    return df



def index_composition(
    index: object, assets: object = "all", mode: object = "df"
):
    """
    This function captures the latest composition of either IBOV or S&P 500. It is updated every 4 months.
    
    Parameters
    ----------
    index : choose the index to be returned, if IBOV or S&P 500
    ativos : you can pass a list with the desired tickets. Default = 'all'.
    mode: you can return either the whole dataframe from B3, or just the list containing the tickers which compose IBOV. Default = 'df'.
    
    """

    df = _adapt_index(index, assets, mode)

    return df



def B3_DataProcessing(df):
    """
    It is used in the function get_sectors in order to processing 
    the zipfile data fetched from the url. 
    objective: clearing the columns and split informations into specific columns; 
    """
                  

    
    df.rename(columns = {'LISTAGEM': 'CÓDIGO', 'Unnamed: 4':'SEGMENTO B3'}, inplace = True)
        
    df['NOME NO PREGÃO'] = df['SEGMENTO'].copy()
        
    df.dropna(subset = ['NOME NO PREGÃO'], inplace = True)
    indexNames = df[df['SETOR ECONÔMICO'] == 'SETOR ECONÔMICO'].index
    df.drop(indexNames, inplace=True)
        
    df['SEGMENTO'] = np.where(df['CÓDIGO'].isna(),df['NOME NO PREGÃO'],pd.NA )    
    df['SETOR ECONÔMICO'] = df['SETOR ECONÔMICO'].ffill()
    df['SUBSETOR'] = df['SUBSETOR'].ffill()
    df['SEGMENTO'] = df['SEGMENTO'].ffill()
    df.dropna(subset = ['CÓDIGO'], inplace = True)

    df.reset_index(drop=True, inplace=True)

    df = df[['SETOR ECONÔMICO','SUBSETOR','SEGMENTO','NOME NO PREGÃO','CÓDIGO','SEGMENTO B3']]
    
    return df


def get_sectors(stock_exchange:object, *tickers):
    """
    This fuction gets the economic and activity sectors classification 
    of the companies listed on Nasdaq or Brazilian stock exchange (B3). 


    You can leave the  'tickers' parameter empty if you wish to return all companies, or 
    specify a variable number of tickers. 
    
    Parameters:
    ----------
    stock_exchange: you have to specify the stock exchange code ('NASDAQ' or 'B3'). 
    tickers : you can pass a specific company's ticker. For brazilian companies you can pass
    the symbol with the B3 segment number (e.g. 'PETR4') or w/o it (e.g. 'PETR')

    """ 
    
    
    stock_exchange = stock_exchange.upper()
      
    if stock_exchange == 'B3':

        url_dataset = r"https://www.b3.com.br/data/files/57/E6/AA/A1/68C7781064456178AC094EA8/ClassifSetorial.zip"

        download = requests.get(url_dataset)
        with open('ClassifSetorial.zip', "wb") as dataset_B3:
            dataset_B3.write(download.content)
        arquivo_zip = zipfile.ZipFile('ClassifSetorial.zip')
        dataset = arquivo_zip.open(arquivo_zip.namelist()[0])

        df = pd.read_excel(dataset, header = 6)
        
        df = B3_DataProcessing(df)   

        if not tickers:
            df = df

        else:
            tickers = list(tickers)
            tickers = [ ticker[:4].upper() for ticker in tickers]
            df = df.loc[df['CÓDIGO'].isin(tickers)]
            
        df.rename(columns = {'SETOR ECONÔMICO': 'sector', 'SUBSETOR':'industry',
                             'SEGMENTO':'subsector','NOME NO PREGÃO': 'name',
                             'CÓDIGO': 'symbol', 'SEGMENTO B3':'B3 listing segment'}, inplace = True)
            
    elif stock_exchange == 'NASDAQ':
        url = \
        'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true'
        headers = {'Accept-Language': 'en-US,en;q=0.9',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'User-Agent': 'Java-http-client/'}

        response = requests.get(url, headers=headers)

        json = response.json()

        df = pd.DataFrame(json['data']['rows'])
        
        df = df[['sector', 'industry', 'name', 'symbol', 'country']]
        
        if not tickers:
            df = df
            
        else:
            tickers = list(tickers)
            tickers = [ticker.upper() for ticker in tickers]
            df = df.loc[df['symbol'].isin(tickers)]
    
    return df
