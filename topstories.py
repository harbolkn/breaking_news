import globals as gl


######
#ToDo:
#  Add get phrase for new story
######
def update_city(city_id):
    endpoint = gl.api_base+"/v3/search"

    query_params = {'access_token': gl.access_token, 'limit':1,
            'cities': city_id, 'fields': 'title,url,summaryText'}

    response = requests.get(endpoint, params= query_params)
    data = json.loads(response.content)['data']

    if 'results' in data and len(data['results']) > 0:
        results = data['results'][0]
        return {'city_id':city_id, 'title': results['title'], 'link':results['url'], 'summary':results['summaryText']}
    else:
        return -1


######
#ToDo:
#  Find a more efficient way of doing this
######
def check_timer(cur, prev):
    if cur.hour == prev.hour:
        if cur.minute - prev.minute >= 10:
            return 1
        else:
            return 0
    elif cur.hour > prev.hour:
        if (cur.minute + 60) - prev.minute >= 10:
            return 1
        else:
            return 0
    else:
        return -1
