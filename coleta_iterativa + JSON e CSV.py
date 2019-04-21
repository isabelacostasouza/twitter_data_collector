#realizar coleta
import oauth2
import json
from dateutil import parser
from datetime import datetime

#gerar CSV
import sys
import os
import time
import csv
import pandas as pd
import nltk
from nltk.tokenize import TweetTokenizer

def get_requisicao(cliente, max_id, termo):
    requisicao = cliente.request(
        'https://api.twitter.com/1.1/search/tweets.json?q={termo}&tweet_mode=extended&result_type=recent&lang=pt-br&{max_id}'.format(max_id=max_id, termo=termo))
    decodificar = requisicao[1].decode()
    try:
        objeto = json.loads(decodificar)
        return objeto['statuses']
    except Exception:
        print("ERROR!")

def coleta(api_key, api_secret_key, token_key, token_secret_key, termo, num_tweets, arquivo_saida):
    consumer = oauth2.Consumer(api_key, api_secret_key)
    token = oauth2.Token(token_key, token_secret_key)
    cliente = oauth2.Client(consumer, token)
    strUrl = ""
    max_id = ""
    num_tweets_collected = 0

    tweetsColetados = {
        "tweets": []
    }

    mantem_tweeets_nao_repetidos = set()
    
    try:
        # coleta os tweets
        while(num_tweets_collected < num_tweets):
            tweets = get_requisicao(cliente, max_id, termo)            
            for tweet in tweets:
                tweet_saida = criaJsonSaida(tweet)
                par_unico = (tweet_saida["usuario"], tweet_saida["data_criacao"])
                tweetsColetados["tweets"] += [criaJsonSaida(tweet)]
                
                max_id = "max_id={max_id}&".format(max_id=tweet['id'])
                num_tweets_collected += 1
    except Exception:
        print("ERROR!")
    finally:
        with open(arquivo_saida, 'w') as f:
            f.write(json.dumps(tweetsColetados["tweets"], indent=2))

def criaJsonSaida(json_input):
    return {
        "id": json_input["id"],
        "data_criacao": json_input["created_at"],
        "text": json_input["full_text"].lower(),
        "usuario": json_input["user"]["name"],
    }


# Inicializa keys
api_key = 'TEZZMKbaNjyZa4n51YXi5VOwa'
api_secret_key = 'kaLLbccEyOSQ76GSxNGey1vcl2eZB0enstIzNDr1HbhB2ASGmI'
token_key = '1115390331112108033-T2u84Yrhw8zYTTTkBWDxiYuadmXrUH'
token_secret_key = 'QnD1Nnc5dpZ5lNylndJ0ktuSMT2GU4s0JczOBl6bWScko'
termo = 'sadia'
num_tweets = 500
arquivo_com_tweetes_coletados = 'tweets_coletados.json'

coleta(api_key, api_secret_key, token_key, token_secret_key, termo, num_tweets, arquivo_com_tweetes_coletados)

# Gera csv com os tweets a serem rotulados
with open(arquivo_com_tweetes_coletados, 'r') as f:
    dic_tweets = json.loads(f.read())
    tweetsDF = pd.read_json(json.dumps(dic_tweets))
nome_arquivo_com_tweetes_rotulados = 'tweets_coletados.csv'
tweetsDF.to_csv(nome_arquivo_com_tweetes_rotulados, quoting=csv.QUOTE_ALL, index=False)