from ..cfgs.dependencies import Namespace, aiohttp, partial
from ..datas.Prepare import dict_to_args
from ..datas.Data import RestAnswer, wrap_dict


class Send():

	def __init__(self, endpoints_set, api_key):
		self.endpoints_set = endpoints_set
		self.headers = {'X-Api-Key': api_key}

	async def query(self, path: str = '', json: dict = {}, type_: str = '', api_version: int = 2):

		self.endpoint = self.endpoints_set.V2 if api_version == 2 else self.endpoints_set.V3
		response_status = None
		response_text = None
		response_json = None
		response = None

		async with aiohttp.ClientSession(headers=self.headers) as session:
			
			if type_ == 'get':
				response = await session.get(url=self.endpoint+path+f'?{await dict_to_args(json)}')
			else:
				response = await session.post(url=self.endpoint+path, json=json)

			response_status = response.status

			try:
				response_text = await response.text(encoding='UTF-8')
				response_json = await response.json()
			except Exception as e:
				pass

		js_ns = await wrap_dict(response_json)
		wrap_js = RestAnswer(**js_ns.__dict__)
		
		return Namespace(status=response_status, json=wrap_js, text=response_text)