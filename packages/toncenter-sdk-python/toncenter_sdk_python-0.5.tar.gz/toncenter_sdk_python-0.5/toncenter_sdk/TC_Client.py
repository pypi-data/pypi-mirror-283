from .cfgs.dependencies import asyncio, Namespace
from .sides import rest_ as r
from .sides.run_methods import Run_Methods


from .V2.accounts import Account_Methods as V2_accounts
from .V2.blocks import Blocks_Methods as V2_blocks
from .V2.transactions import Transactions_Methods as V2_transactions

from .V3.default_ import Default_Methods as V3_default



class Client(
	V2_accounts,
	V2_blocks, 
	V2_transactions,

	V3_default,


	Run_Methods
	):

	def __init__(self, api_key: str = '', testnet: bool = False): #v2,v3

		self.endpoints = Namespace(
			mainnet=Namespace(
				V2='https://toncenter.com/api/v2/',
				V3='https://toncenter.com/api/v3/'
			),
			testnet=Namespace(
				V2='https://testnet.toncenter.com/api/v2/',
				V3='https://testnet.toncenter.com/api/v3/'
			)
		)
		self.endpoints_set = self.endpoints.mainnet if testnet == False else self.endpoints.testnet
		self.api_key = api_key
		self.rest = r.Send(endpoints_set=self.endpoints_set, api_key=api_key)