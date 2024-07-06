import requests
import datetime

QueryParameter = ['?', '&']


class AccountsApi:
    def __init__(self):
        self.url_base = ('https://api.fraxscan.com/api?'
                         'module=account')
        self.api_key = None

    def set_api_key_token(self, api_key: str):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET", request_data=None):
        try:
            headers = {
                "x-api-key": self.api_key
            }
            response = requests.request(url=self.url_base + endpoint, method=method, headers=headers, data=request_data)
            if response.status_code == 200:
                response_object = response.json()
                # response_object['status_code'] = 200
                return response_object
            elif response.status_code == 404:
                return f'{self.url_base}{endpoint} is not found'
            else:
                return response.json()
        except Exception as err:
            print(f'Got Exception :{err}')

    def get_frxETH_balance(self, address: str):
        endpoint = f'&action=balance&address={address}&tag=latest&apikey={self.api_key}'
        return self.api_key(endpoint)

    def get_frxETH_balance_for_multiple_address(self, address: list):
        addr = ','.join(address)
        endpoint = f'&action=balancemulti&address={addr}&tag=latest&apikey={self.api_key}'
        return self.api_key(endpoint)

    def get_normal_transaction(self, address: str,
                               start_block: int = 0,
                               end_block='latest'):
        endpoint = (f'&action=txlist&address={address}&startblock={start_block}&'
                    f'endblock={end_block}&page=1&offset=10&sort=asc'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_internal_transaction(self, address: str,
                                 start_block: int = 0,
                                 end_block='latest'):
        endpoint = (f'&action=txlistinternal&address={address}&startblock={start_block}&'
                    f'endblock={end_block}&page=1&offset=10&sort=asc'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_internal_transaction_transaction_hash(self, txhash: str):
        endpoint = f'&action=txlistinternal&txhash={txhash}&apikey={self.api_key}'
        return self.api_key(endpoint)

    def get_ERC20_token_transfers(self, address: str,
                                  contract_address: str,
                                  start_block: int = 0,
                                  end_block='latest'):
        endpoint = (f'&action=tokentx&contractaddress={contract_address}'
                    f'&address={address}&startblock={start_block}&'
                    f'endblock={end_block}&page=1&offset=10&sort=asc'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_ERC721_token_transfers(self, address: str,
                                   contract_address: str,
                                   start_block: int = 0,
                                   end_block='latest'):
        endpoint = (f'&action=tokennfttx&contractaddress={contract_address}'
                    f'&address={address}&startblock={start_block}&'
                    f'endblock={end_block}&page=1&offset=10&sort=asc'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_ERC1155_token_transfers(self, address: str,
                                    contract_address: str,
                                    start_block: int = 0,
                                    end_block='latest'):
        endpoint = (f'&action=tokennfttx&contractaddress={contract_address}'
                    f'&address={address}&startblock={start_block}&'
                    f'endblock={end_block}&page=1&offset=10&sort=asc'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)


class TransactionsApi:
    def __init__(self):
        self.url_base = ('https://api.fraxscan.com/api?'
                         'module=transaction')
        self.api_key = None

    def set_api_key_token(self, api_key: str):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET", request_data=None):
        try:
            headers = {
                "x-api-key": self.api_key
            }
            response = requests.request(url=self.url_base + endpoint, method=method, headers=headers, data=request_data)
            if response.status_code == 200:
                response_object = response.json()
                # response_object['status_code'] = 200
                return response_object
            elif response.status_code == 404:
                return f'{self.url_base}{endpoint} is not found'
            else:
                return response.json()
        except Exception as err:
            print(f'Got Exception :{err}')

    def get_transaction_status(self, txhash: str):
        endpoint = f'&action=gettxreceiptstatus&txhash={txhash}&apikey={self.api_key}'
        return self.api_key(endpoint)


class BlocksApi:
    def __init__(self):
        self.url_base = ('https://api.fraxscan.com/api?'
                         'module=block')
        self.api_key = None

    def set_api_key_token(self, api_key: str):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET", request_data=None):
        try:
            headers = {
                "x-api-key": self.api_key
            }
            response = requests.request(url=self.url_base + endpoint, method=method, headers=headers, data=request_data)
            if response.status_code == 200:
                response_object = response.json()
                # response_object['status_code'] = 200
                return response_object
            elif response.status_code == 404:
                return f'{self.url_base}{endpoint} is not found'
            else:
                return response.json()
        except Exception as err:
            print(f'Got Exception :{err}')

    def get_block_rewards_by_blockNo(self, blockno: str):
        endpoint = f'&action=getblockreward&blockno={blockno}&apikey={self.api_key}'
        return self.api_key(endpoint)

    def get_estimated_block_countdown_time_by_blockNo(self, blockno: str):
        endpoint = f'&action=getblockcountdown&blockno={blockno}&apikey={self.api_key}'
        return self.api_key(endpoint)

    def get_block_no_by_timestamp(self, timestamp: str):
        endpoint = (f'&action=getblocknobytime&timestamp={timestamp}'
                    f'&closest=before&apikey={self.api_key}')
        return self.api_key(endpoint)


class StatsApi:
    def __init__(self):
        self.url_base = ('https://api.fraxscan.com/api?'
                         'module=stats')
        self.api_key = None

    def set_api_key_token(self, api_key: str):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET", request_data=None):
        try:
            headers = {
                "x-api-key": self.api_key
            }
            response = requests.request(url=self.url_base + endpoint, method=method, headers=headers,
                                        data=request_data)
            if response.status_code == 200:
                response_object = response.json()
                # response_object['status_code'] = 200
                return response_object
            elif response.status_code == 404:
                return f'{self.url_base}{endpoint} is not found'
            else:
                return response.json()
        except Exception as err:
            print(f'Got Exception :{err}')

    def get_ERC20_token_by_contractaddress(self, contract_address: str):
        endpoint = f'&action=tokensupply&contractaddress={contract_address}&apikey={self.api_key}'
        return self.api_key(endpoint)

    def get_ERC20_token_account_balance(self, contract_address: str, address: str):
        endpoint = (f'&action=tokenbalance&contractaddress={contract_address}'
                    f'&address={address}&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_total_supply_of_frxETH(self):
        endpoint = f'&action=ethsupply&apikey={self.api_key}'
        return self.api_key(endpoint)

    def get_frxETH_last_price(self):
        endpoint = f'&action=ethprice&apikey={self.api_key}'
        return self.api_key(endpoint)


class GethProxyApi:
    def __init__(self):
        self.url_base = ('https://api.fraxscan.com/api?'
                         'module=proxy')
        self.api_key = None

    def set_api_key_token(self, api_key: str):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET", request_data=None):
        try:
            headers = {
                "x-api-key": self.api_key
            }
            response = requests.request(url=self.url_base + endpoint, method=method, headers=headers,
                                        data=request_data)
            if response.status_code == 200:
                response_object = response.json()
                # response_object['status_code'] = 200
                return response_object
            elif response.status_code == 404:
                return f'{self.url_base}{endpoint} is not found'
            else:
                return response.json()
        except Exception as err:
            print(f'Got Exception :{err}')

    def get_eth_block_number(self):
        endpoint = f'&action=eth_blockNumber&apikey={self.api_key}'
        return self.api_key(endpoint)

    def get_eth_block_by_number(self,tag: str):
        endpoint = (f'&action=eth_blockNumber&tag={tag}'
                    f'&boolean=true&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_eth_block_transaction_count_by_number(self,tag: str):
        endpoint = (f'&action=eth_getBlockTransactionCountByNumber&tag={tag}'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_eth_transaction_by_hash(self,txhash: str):
        endpoint = (f'&action=eth_getTransactionByHash&txhash={txhash}'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_eth_transaction_by_blocknumber_and_index(self,tag: str,index:str):
        endpoint = (f'&action=eth_getTransactionByBlockNumberAndIndex'
                    f'&tag={tag}&index={index}'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_eth_transaction_count(self,address: str,index:str):
        endpoint = (f'&action=eth_getTransactionCount'
                    f'&address={address}&tag=latest'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def send_raw_transaction(self,hex: str):
        endpoint = (f'&action=eth_sendRawTransaction'
                    f'&hex={hex}'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)

    def get_transaction_receipt(self,txhash: str):
        endpoint = (f'&action=eth_getTransactionReceipt'
                    f'&txhash={txhash}'
                    f'&apikey={self.api_key}')
        return self.api_key(endpoint)
