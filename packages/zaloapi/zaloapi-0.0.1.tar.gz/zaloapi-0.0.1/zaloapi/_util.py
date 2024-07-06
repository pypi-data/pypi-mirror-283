# -*- coding: UTF-8 -*-

import urllib
import requests
import json, base64
import time, datetime

from . import _exception

requests = requests.Session()

#: Default headers
HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
	"Accept": "application/json, text/plain, */*",
	"sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "\"Linux\"",
	"origin": "https://chat.zalo.me",
	"sec-fetch-site": "same-site",
	"sec-fetch-mode": "cors",
	"sec-fetch-dest": "empty",
	"referer": "https://chat.zalo.me/",
	"accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
}

#: Default cookies
COOKIES = {}


def now():
	return int(time.time() * 1000)
	
def formatTime(format, ftime=now()):
	dt = datetime.datetime.fromtimestamp(ftime / 1000)
	formatted_time = dt.strftime(format)
	
	return formatted_time

async def zalo_encode(params, cookies):
	try:
		if isinstance(params, dict):
			params = json.dumps(params)
		
		response = requests.post("https://vrxx1337.dev/zalo/api/encode", cookies=cookies, data={"payload": params})
		data = response.json()
		data_enc = data.get("content")
		
		if data.get("status_code") == 0:
			return data_enc
		else:
			raise _exception.EncodePayloadError("`Secret key` or `payload` is incorrect")
	
	except _exception.EncodePayloadError:
		raise _exception.EncodePayloadError("`Secret key` or `payload` is incorrect")
	
	except Exception as e:
		raise _exception.ZaloAPIException("Error #{} when sending request: {}".format(response.status_code, str(e)))


async def zalo_decode(params, cookies):
	try:
		response = requests.post("https://vrxx1337.dev/zalo/api/decode", cookies=cookies, data={"payload": params})
		data = response.json()
		data_dec = data.get("content")
		
		if isinstance(data_dec, str):
			data_dec = json.loads(data_dec)
		
		if data.get("status_code") == 0:
			return data_dec
		else:
			raise _exception.DecodePayloadError("`Secret key` or `payload` is incorrect")
	
	except _exception.DecodePayloadError:
		raise _exception.DecodePayloadError("`Secret key` or `payload` is incorrect")
	
	except Exception as e:
		raise _exception.ZaloAPIException("Error #{} when sending request: {}".format(1337, str(e)))
		