#pip3 install oauth2
import oauth2
import json

def coleta(api_key, api_secret_key, token_key, token_secret_key):
	#inicializa cliente oauth
	consumer = oauth2.Consumer(api_key, api_secret_key)
	token = oauth2.Token(token_key, token_secret_key)
	cliente = oauth2.Client(consumer, token)

	#coleta os dados
	requisicao = cliente.request('https://api.twitter.com/1.1/search/tweets.json?q=sadia&result_type=recent')
	decodificar = requisicao[1].decode()

	objeto = json.loads(decodificar)
	tweets = objeto['statuses']

	#printa dados completos
	for tweet in tweets:
	    print(tweet['user']['screen_name'])
	    print(tweet['text'])
	    print()

#inicializa keys
api_key = 'suaAPIKey'
api_secret_key = 'suaAPISecretKey'
token_key = 'suaTokenKey'
token_secret_key = 'suaTokenSecretKey'

coleta(api_key, api_secret_key, token_key, token_secret_key)
