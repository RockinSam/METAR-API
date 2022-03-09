from django.http import Http404, JsonResponse
from . import converter
import requests, redis, json


redis_client = redis.Redis()
DEF_EXP_TIME = 300


def test(req):
    result = redis_client.ping()
    if result:
        return JsonResponse({'data': 'pong'}, safe=False)
    else:
        raise Http404()


def index(req):

    scode = req.GET['scode']
    scode = scode.upper()
    
    info = redis_client.get(scode)

    if info:
        return JsonResponse({"data": eval(info.decode())}, safe=False)

    url = f'https://tgftp.nws.noaa.gov/data/observations/metar/stations/{scode}.TXT'
    res = requests.get(url)

    if res.status_code == 404:
        raise Http404(f"The requested data for station identifier '{scode}' was not found.")

    info = converter.convert(res.text.split())
    redis_client.setex(scode, DEF_EXP_TIME, info)

    return JsonResponse({"data": eval(info)}, safe=False)



    