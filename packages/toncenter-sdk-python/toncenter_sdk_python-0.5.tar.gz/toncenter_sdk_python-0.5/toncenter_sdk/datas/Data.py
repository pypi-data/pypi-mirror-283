from ..cfgs.dependencies import Namespace, inspect, json


async def wrap_namespace(namespace):
	if isinstance(namespace, Namespace):
		result = {}
		for key, value in namespace.__dict__.items():
			if isinstance(value, Namespace):
				result[key] = await wrap_namespace(value)
			else:
				result[key] = value
		return result
	else:
		return namespace


async def wrap_dict(d):

	d = dict(d)
	for k, v in d.items():
		if isinstance(v, str):
			try:
				json_data = json.loads(v)
				if isinstance(json_data, dict):
					d[k] = await wrap_dict(json_data)
			except json.JSONDecodeError:
				pass
		elif isinstance(v, list):
			d[k] = [await wrap_dict(item) if isinstance(item, dict) else item for item in v]
		elif isinstance(v, dict):
			d[k] = await wrap_dict(v)
	return Namespace(**d)



class RestAnswer(Namespace):

	def __str__(self):
		return str(vars(self))