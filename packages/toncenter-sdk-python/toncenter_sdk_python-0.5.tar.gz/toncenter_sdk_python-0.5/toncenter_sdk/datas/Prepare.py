from ..cfgs.dependencies import Namespace


async def check_empty_value(val_):

	empty_values = {
		'list': [],
		'dict': {},
		'int': 0,
		'str': '',
		'bool': None
	}

	val_type = str(type(val_)).split("'")[1].split("'")[0]
	if val_ != empty_values[val_type]:
		return val_


async def dict_to_args(d: dict = {}):

	args_ = ''
	args_l = []

	for i in d.items():
		if await check_empty_value(i[1]) != None:
			if type(i[1]) != list:
				args_l.append(f'{i[0]}={i[1] if type(i[1]) != bool else str(i[1]).lower()}')
			else:
				for r in i[1]:
					args_l.append(f'{i[0]}={r if type(r) != bool else str(r).lower()}')

	args_ = '&'.join(args_l)	
	return args_


async def rebuild_json(loc: Namespace = None):

	del loc['client']
	return loc