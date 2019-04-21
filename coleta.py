import oauth2
import sys
import os
import json
import time
import csv
import pandas as pd
import nltk
from nltk.tokenize import TweetTokenizer


def criaJsonSaida(json_input):
    return {
        "id": json_input["id"],
        "data_criacao": json_input["created_at"],
        "text": json_input["full_text"].lower(),
        "usuario": json_input["user"]["name"],
        "e_sobre_a_empresa": None
    }


def get_requisicao(cliente, max_id, termo):
    requisicao = cliente.request(
        'https://api.twitter.com/1.1/search/tweets.json?q={termo}&tweet_mode=extended&result_type=recent&lang=pt-br&count=3&{max_id}'.format(max_id=max_id, termo=termo))
    decodificar = requisicao[1].decode()
    try:
        objeto = json.loads(decodificar)
        return objeto['statuses']
    except Exception:
        print(objeto)


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
                par_unico = (tweet_saida["usuario"],
                             tweet_saida["data_criacao"])
                if par_unico not in mantem_tweeets_nao_repetidos:
                    mantem_tweeets_nao_repetidos.add(par_unico)
                    tweetsColetados["tweets"] += [criaJsonSaida(tweet)]

                max_id = "max_id={max_id}&".format(max_id=tweet['id'])
                num_tweets_collected += 1
    except Exception as e:
        print(e)
    finally:
        with open(arquivo_saida, 'w') as f:
            f.write(json.dumps(tweetsColetados["tweets"], indent=2))


# inicializa keys
api_key = 'suaAPIKey'
api_secret_key = 'suaAPISecretKey'
token_key = 'suaTokenKey'
token_secret_key = 'suaTokenSecretKey'
termo = 'sadia'
num_tweets = 500
arquivo_com_tweetes_coletados = 'tweets_coletados.json'

try:
    coleta(api_key, api_secret_key, token_key,
           token_secret_key, termo, num_tweets, arquivo_com_tweetes_coletados)
except Exception as e:
    print(e)
