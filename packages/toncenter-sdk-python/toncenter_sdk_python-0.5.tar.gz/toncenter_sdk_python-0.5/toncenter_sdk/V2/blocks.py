from ..cfgs.dependencies import Namespace, inspect
from ..datas.Prepare import rebuild_json



class Blocks_Methods():


	async def get_masterchain_info(client: Namespace):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getMasterchainInfo', json=json_, type_='get')
		return resp.json


	async def get_masterchain_block_signatures(client: Namespace, seqno: int):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getMasterchainBlockSignatures', json=json_, type_='get')
		return resp.json


	async def get_shard_block_proof(client: Namespace, workchain: int, shard: int, seqno: int, from_seqno: int = 0):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getShardBlockProof', json=json_, type_='get')
		return resp.json


	async def get_consensus_block(client: Namespace, 
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getConsensusBlock', json=json_, type_='get')
		return resp.json


	async def lookup_block(client: Namespace,
		workchain: int = -1,
		shard: int = 8000000000000000,
		seqno: int = 38682543,
		lt: int = 0,
		unixtime: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('lookupBlock', json=json_, type_='get')
		return resp.json


	async def shards(client: Namespace,
		seqno: int = 38682543
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('shards', json=json_, type_='get')
		return resp.json


	async def get_block_transactions(client: Namespace,
		workchain: int = -1,
		shard: int = 8000000000000000,
		seqno: int = 38682543,
		root_hash: str = '',
		file_hash: str = '',
		after_lt: int = '',
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
		after_lt: int = '',
		after_hash: str = '',
		count: int = 40
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getBlockTransactionsExt', json=json_, type_='get')
		return resp.json


	async def get_block_header(client: Namespace,
		workchain: int = -1,
		shard: int = 8000000000000000,
		seqno: int = 38682543,
		root_hash: str = '',
		file_hash: str = ''
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getBlockHeader', json=json_, type_='get')
		return resp.json


	async def get_out_msg_queue_sizes(client: Namespace,
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('getOutMsgQueueSizes', json=json_, type_='get')
		return resp.json