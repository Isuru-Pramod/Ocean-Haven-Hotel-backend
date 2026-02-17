from web3 import Web3
import json
from config import SEPOLIA_RPC_URL, CONTRACT_ADDRESS

# Connect to Sepolia
web3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))

# Load ABI
with open("contract_abi.json") as f:
    contract_abi = json.load(f)

contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=contract_abi
)

def get_asset_count():
    return contract.functions.assetCount().call()

def get_asset(asset_id):
    return contract.functions.assets(asset_id).call()

def get_investors(asset_id):
    return contract.functions.getInvestors(asset_id).call()


def get_top_10(asset_id):
    investors = get_investors(asset_id)

    investor_data = []

    for address in investors:
        shares = contract.functions.ownership(asset_id, address).call()
        investor_data.append({
            "address": address,
            "shares": shares
        })

    # Sort descending
    sorted_data = sorted(investor_data, key=lambda x: x["shares"], reverse=True)

    return sorted_data[:10]
