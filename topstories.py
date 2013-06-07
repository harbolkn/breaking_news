import csv
import simplejson as json
import requests

access_token = "bafda5b39a752043052cbec72ae9908e5e15c9d4"
api_base = "https://api-ssl.bitly.com"

def data():
	endpoint = api_base+"/v3/search"
	top = {}
	with open('cities.csv', 'r') as city_file:
		reader = csv.reader(city_file, delimiter=',')
		for line in reader:
			if line[1] != 'api_name': 
   				query_params={'access_token': access_token, 'limit': 1, 'cities': line[1], 'fields': 'title,url'}
				response=requests.get(endpoint, params= query_params)
				data = json.loads(response.content)['data']
				if 'results' in data and len(data['results'])>0:
					print data['results']
					results = data['results'][0]
					top[line[0]] = [ results['title'] , results['url']]

	return jsonify(top)

if __name__ == '__main__':
	print data()
