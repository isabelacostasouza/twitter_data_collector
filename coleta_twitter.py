#pip3 install oauth2
import oauth2
import json

#inicializa keys
api_key = 'suaAPIKey'
api_secret_key = 'suaAPISecreyKey'

token_key = 'suaTokenKey'
token_secret_key = 'suaTokenSecretKey'

consumer = oauth2.Consumer(api_key, api_secret_key)
token = oauth2.Token(token_key, token_secret_key)
cliente = oauth2.Client(consumer, token)

#coleta os dados
requisicao = cliente.request('https://api.twitter.com/1.1/search/tweets.json?q=brasil&result_type=popular')
decodificar = requisicao[1].decode()

objeto = json.loads(decodificar)
twittes = objeto['statuses']

#printa dados completos
for twit in twittes:
    print(twit['user']['screen_name'])
    print(twit['text'])
    print()

