#pip3 install oauth2
import oauth2
import json
from dateutil import parser
from datetime import datetime

def format_date(obj_datetime):
	print(obj_datetime)
	return obj_datetime.strftime("%Y-%m-%d")

def get_requisicao(cliente, max_id, termo):
	requisicao = cliente.request('https://api.twitter.com/1.1/search/tweets.json?q={termo}&tweet_mode=extended&result_type=recent&lang=pt-br&{max_id}'.format(max_id=max_id,termo=termo))
	decodificar = requisicao[1].decode()
	objeto = json.loads(decodificar)
	return objeto['statuses']

def coleta(api_key, api_secret_key, token_key, token_secret_key, termo, num_tweets):
	consumer = oauth2.Consumer(api_key, api_secret_key)
	token = oauth2.Token(token_key, token_secret_key)
	cliente = oauth2.Client(consumer, token)
	strUrl = ""
	max_id = ""
	num_tweets_collected = 0

	#coleta os tweets
	while(num_tweets_collected < num_tweets):

		tweets = get_requisicao(cliente, max_id, termo)

		#printa dados filtrados do JSON
		for tweet in tweets:
			print(tweet['user']['screen_name'])
			print(tweet['created_at'])
			print(tweet['full_text'])
			print()
			max_id = "max_id={max_id}&".format(max_id=tweet['id'])
			num_tweets_collected += 1

#inicializa keys
api_key = 'suaAPIKey'
api_secret_key = 'suaAPISecretKey'
token_key = 'suaTokenKey'
token_secret_key = 'suaTokenSecretKey'
termo = 'seuTermo'
num_tweets = numIteracoes

coleta(api_key, api_secret_key, token_key, token_secret_key, termo, num_tweets)
