from ..cfgs.dependencies import Namespace, inspect
from ..datas.Prepare import rebuild_json


class Run_Methods():

	async def run_get_method(client: Namespace, address: str, method: str, stack: list = []):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('runGetMethod', json=json_, type_='post')
		return resp.json