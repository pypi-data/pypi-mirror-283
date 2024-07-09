from ..cfgs.dependencies import Namespace, inspect
from ..datas.Prepare import rebuild_json



class Transactions_Methods():


	async def get_transactions(client: Namespace,
		address: str = '',
		limit: int = 128,
		lt: int = 0,
		hash: str = '',
		to_lt: int = 0,
		archival: bool = False
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getTransactions', json=json_, type_='get')
		return resp.json


	async def get_block_transactions(client: Namespace,
		workchain: int = -1,
		shard: int = 8000000000000000,
		seqno: int = 38682543,
		root_hash: str = '',
		file_hash: str = '',
		after_lt: int = 0,
		after_hash: str = '',
		count: int = 40
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getBlockTransactions', json=json_, type_='get')
		return resp.json


	async def get_block_transactions_ext(client: Namespace,
		workchain: int = -1,
		shard: int = 8000000000000000,
		seqno: int = 38682543,
		root_hash: str = '',
		file_hash: str = '',
		after_lt: int = 0,
		after_hash: str = '',
		count: int = 40
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getBlockTransactionsExt', json=json_, type_='get')
		return resp.json


	async def try_locate_tx(client: Namespace,
		source: str = '',
		destination: str = '',
		created_lt: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('tryLocateTx', json=json_, type_='get')
		return resp.json


	async def try_locate_result_tx(client: Namespace,
		source: str = '',
		destination: str = '',
		created_lt: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('tryLocateResultTx', json=json_, type_='get')
		return resp.json


	async def try_locate_source_tx(client: Namespace,
		source: str = '',
		destination: str = '',
		created_lt: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('tryLocateSourceTx', json=json_, type_='get')
		return resp.json