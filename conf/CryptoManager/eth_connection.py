from web3 import Web3
import json
import os

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

if not w3.is_connected():
    raise Exception("Не удалось подключиться к Ganache")

abi_path = os.path.join(os.path.dirname(__file__), '../../../NFTVC-crypto/contracts/Verify.sol')
with open(abi_path) as f:
    contract_abi = json.load(f)

contract_address = '0xВашАдресКонтракта'
contract = w3.eth.contract(address=contract_address, abi=contract_abi)