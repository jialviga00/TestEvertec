from lib.PlaceToPayException import PlaceToPayException
from django.conf import settings
from datetime import datetime
from base64 import b64encode
import requests
import hashlib
import os

class PlaceToPay:

	"""
		Class for requests PlaceToPay.

		Attributes:
			@config -- dict of configuration PlaceToPay [optional]
	"""
	
	_config = {}
	_nonce = None
	_encode = 'utf-8'
	_algorithm = 'sha1'
	_response = {}
	_SITE_URL = ''
	_FAILED_EVERTEC = "FAILED"
	_SUCCESS_PLACETOPAY = "OK"
	_PROCESSING = "PROCESSING"
	_SUCCESS_EVERTEC = "SUCCESS"
	_FAILED_PLACETOPAY = "FAILED"

	def __init__(self, config = {}):
		self.setConfig(config)

	def setConfig(self, config = {}):
		"""
			set config to connect to PlaceToPay
			@config -- dict of configuration PlaceToPay [optional]
		"""
		if not config:
			if not hasattr(settings, 'PLACE_TO_PAY_CONFIG'):
				raise PlaceToPayException('No PLACE_TO_PAY_CONFIG in settings provided to use')
			else:
				config = settings.PLACE_TO_PAY_CONFIG
		
		if not config.get('URL', False):
			raise PlaceToPayException('No service URL provided to use')

		if not config.get('LOGIN', False):
			raise PlaceToPayException('No LOGIN provided to use')

		if not config.get('TRANKEY', False):
			raise PlaceToPayException('No TRANKEY provided to use')

		self._config = config

		if not hasattr(settings, 'SITE_URL'):
			raise PlaceToPayException('No SITE in settings provided to use')

		self._SITE_URL = settings.SITE_URL
			
	def getConfig(self):
		"""
			get config to connect to PlaceToPay
		"""
		return self._config
	
	def getNonce(self, decode=False):
		if self._nonce is not None:
			nonce = self._nonce
		else:
			nonce = b64encode(os.urandom(40)).decode('utf-8')[0:16]
			self._nonce = nonce
		if decode is False:
			return nonce
		return b64encode(bytes(nonce, encoding=self._encode)).decode(self._encode)
		
	def getSeed(self):
		return datetime.now().isoformat()

	def digest(self, cadena):
		h = hashlib.new(self._algorithm, cadena.encode(self._encode))
		return b64encode(h.digest()).decode(self._encode)

	def getResponseStatus(self):
		return self._getResponseKey('status', '__UNDEFINED_STATUS__')

	def getResponseMessage(self):
		return self._getResponseKey('message', '__UNDEFINED_MESSAGE__')

	def getResposeRequestId(self):
		return self._response.get('requestId', '__UNDEFINED_REQUESTID__')

	def getResposeProcessUrl(self):
		return self._response.get('processUrl', '__UNDEFINED_PROCESSURL__')

	def _getResponseKey(self, key, default='__UNDEFINED__'):
		return self._response.get('status', {}).get(key, default)

	def sendToPlaceTopay(self, data):
		SEED = self.getSeed()
		data['auth'] = {
			'login': self._config.get('LOGIN'),
			'tranKey': self.digest(self.getNonce(False)+str(SEED)+self._config.get('TRANKEY')),
			'nonce': self.getNonce(True),
			'seed': SEED,
		}
		response = requests.post(
	   	 	self._config.get('URL'), 
			json=data
		)
		self._response = response.json()
		return self._response

	def getRequestInformation(self, request_id):
		URL = '{url}{request_id}'.format(url=self._config.get('URL'), request_id=request_id)
		SEED = self.getSeed()
		data = {
			'auth' : {
				'login': self._config.get('LOGIN'),
				'tranKey': self.digest(self.getNonce(False)+str(SEED)+self._config.get('TRANKEY')),
				'nonce': self.getNonce(True),
				'seed': SEED,
			}
		}
		response = requests.post(
			URL, 
			json=data
		)
		self._response = response.json()
		return self._response