from ..cfgs.dependencies import Namespace, inspect
from ..datas.Prepare import rebuild_json



class Default_Methods():

	async def blocks(client: Namespace, 
		workchain: int = -1, 
		shard: int = 8000000000000000, 
		seqno: int = 38682543, 
		start_utime: int = 0,
		end_utime: int = 0,
		start_lt: int = 0,
		end_lt: int = 0,
		limit: int = 128,
		offset: int = 0,
		sort: str = 'desc'
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('blocks', json=json_, type_='get', api_version=3)
		return resp.json


	async def master_chain_block_shard_state(client: Namespace,
		seqno: int = 38682543
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('masterchainBlockShardState', json=json_, type_='get', api_version=3)
		return resp.json


	async def address_book(client: Namespace,
		address: list = ['EQA6jZZPqx-gBqBacu38NAtSkdCKhWUuEtJ6U46brqUD0z-l']
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('addressBook', json=json_, type_='get', api_version=3)
		return resp.json


	async def masterchain_block_shards(client: Namespace,
		seqno: int = 38682543,
		include_mc_block: bool = False
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('masterchainBlockShards', json=json_, type_='get', api_version=3)
		return resp.json


	async def transactions(client: Namespace, 
		workchain: int = -1, 
		shard: int = 8000000000000000, 
		seqno: int = 38682543, 
		account: list = [],
		exclude_account: list = [],
		hash: str = '',
		lt: int = 0,
		start_utime: int = 0,
		end_utime: int = 0,
		start_lt: int = 0,
		end_lt: int = 0,
		limit: int = 128,
		offset: int = 0,
		sort: str = 'desc'
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('transactions', json=json_, type_='get', api_version=3)
		return resp.json


	async def transactions_by_masterchain_block(client: Namespace, 
		seqno: int = 38682543, 
		limit: int = 128,
		offset: int = 0,
		sort: str = 'desc'
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('transactionsByMasterchainBlock', json=json_, type_='get', api_version=3)
		return resp.json


	async def transactions_by_message(client: Namespace, 
		direction: str = 'in',
		msg_hash: str = '',
		limit: int = 128,
		offset: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('transactionsByMessage', json=json_, type_='get', api_version=3)
		return resp.json


	async def adjacent_transactions(client: Namespace, 
		hash: str = '',
		direction: str = 'both',
		limit: int = 128,
		offset: int = 0,
		sort: str = 'desc'
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('adjacentTransactions', json=json_, type_='get', api_version=3)
		return resp.json


	async def messages(client: Namespace, 
		hash: str = '',
		source: str = '',
		destination: str = '',
		body_hash: str = '',
		limit: int = 128,
		offset: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('messages', json=json_, type_='get', api_version=3)
		return resp.json





	async def wallet(client: Namespace, 
		address: str = ''
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('wallet', json=json_, type_='get', api_version=3)
		return resp.json





	async def nft_collections(client: Namespace, 
		collection_address: str = '',
		owner_address: str = '',
		limit: int = 128,
		offset: int = 0
		):

		json_ = await rebuild_json(locals())
		return resp.json
		resp = await client.rest.query('nft/collections', json=json_, type_='get', api_version=3)


	async def nft_items(client: Namespace, 
		address: str = '',
		owner_address: str = '',
		collection_address: str = '',
		index: int = 0,
		limit: int = 128,
		offset: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('nft/items', json=json_, type_='get', api_version=3)
		return resp.json







	async def jetton_masters(client: Namespace, 
		address: str = '',
		admin_address: str = '',
		limit: int = 128,
		offset: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('jetton/masters', json=json_, type_='get', api_version=3)
		return resp.json


	async def jetton_masters(client: Namespace, 
		address: str = '',
		admin_address: str = '',
		limit: int = 128,
		offset: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('jetton/masters', json=json_, type_='get', api_version=3)
		return resp.json


	async def jetton_wallets(client: Namespace, 
		address: str = '',
		owner_address: str = '',
		jetton_address: str = '',
		limit: int = 128,
		offset: int = 0
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('jetton/wallets', json=json_, type_='get', api_version=3)
		return resp.json


	async def jetton_transfers(client: Namespace, 
		address: str = '',
		jetton_wallet: str = '',
		jetton_master: str = '',
		direction: str = 'in',
		start_utime: int = 0,
		end_utime: int = 0,
		start_lt: int = 0,
		end_lt: int = 0,
		limit: int = 128,
		offset: int = 0,
		sort: str = 'desc'
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('jetton/transfers', json=json_, type_='get', api_version=3)
		return resp.json


	async def jetton_burns(client: Namespace, 
		address: str = '',
		jetton_wallet: str = '',
		jetton_master: str = '',
		start_utime: int = 0,
		end_utime: int = 0,
		start_lt: int = 0,
		end_lt: int = 0,
		limit: int = 128,
		offset: int = 0,
		sort: str = 'desc'
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('jetton/transfers', json=json_, type_='get', api_version=3)
		return resp.json






	async def message(client: Namespace,
		boc: str = '' 
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('message', json=json_, type_='post', api_version=3)
		return resp.json


	async def estimate_fee(client: Namespace,
		address: str = '',
		body: str = '',
		init_code: str = '',
		init_data: str = '',
		ignore_chksig: bool = True
		):

		json_ = await rebuild_json(locals())
		resp = await client.rest.query('estimateFee', json=json_, type_='post', api_version=3)
		return resp.json