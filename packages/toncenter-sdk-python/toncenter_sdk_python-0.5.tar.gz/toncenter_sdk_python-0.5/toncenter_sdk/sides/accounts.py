from ..cfgs.dependencies import Namespace, inspect
from ..datas.Prepare import rebuild_json



class Account_Methods():


	async def get_address_information(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getAddressInformation', json=json_, type_='get')
		return resp.json


	async def get_extended_address_information(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getExtendedAddressInformation', json=json_, type_='get')
		return resp.json


	async def get_wallet_information(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getWalletInformation', json=json_, type_='get')
		return resp.json


	async def get_transactions(client: Namespace, address: str, limit: int = 10, lt: int = 0, hash: str = '', to_lt: int = 0, archival: bool = False):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getTransactions', json=json_, type_='get')
		return resp.json


	async def get_address_balance(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getAddressBalance', json=json_, type_='get')
		return resp.json


	async def get_address_state(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getAddressState', json=json_, type_='get')
		return resp.json


	async def pack_address(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('packAddress', json=json_, type_='get')
		return resp.json


	async def unpack_address(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('unpackAddress', json=json_, type_='get')
		return resp.json


	async def get_token_data(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getTokenData', json=json_, type_='get')
		return resp.json


	async def detect_address(client: Namespace, address: str):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('detectAddress', json=json_, type_='get')
		return resp.json