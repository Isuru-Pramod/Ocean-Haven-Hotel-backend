import os
import json
from web3 import Web3
from dotenv import load_dotenv

# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()

SEPOLIA_RPC = os.getenv("SEPOLIA_RPC")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

if not SEPOLIA_RPC:
    raise Exception("SEPOLIA_RPC not found in .env")

if not CONTRACT_ADDRESS:
    raise Exception("CONTRACT_ADDRESS not found in .env")

# ==================================================
# CONNECT TO ETHEREUM
# ==================================================

w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))

if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum network")

contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)

# ==================================================
# LOAD ABI
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABI_PATH = os.path.join(BASE_DIR, "..", "contract_abi.json")

if not os.path.exists(ABI_PATH):
    raise Exception("contract_abi.json file not found")

with open(ABI_PATH, "r") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

# ==================================================
# READ FUNCTIONS
# ==================================================

def get_asset_count():
    try:
        return contract.functions.assetCount().call()
    except Exception:
        return 0


def get_total_assets():
    try:
        total = contract.functions.assetCount().call()
        return {"success": True, "total_assets": total}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_asset(asset_id):
    try:
        asset = contract.functions.assets(asset_id).call()

        return {
            "success": True,
            "asset": {
                "id": asset[0],
                "name": asset[1],
                "location": asset[2],
                "description": asset[3],   # 🔥 NEW
                "imageURL": asset[4],      # 🔥 NEW
                "totalShares": asset[5],
                "sharePrice": asset[6],
                "sharesSold": asset[7],
                "creator": asset[8],
                "isActive": asset[9]
            }
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_listing(listing_id):
    try:
        listing = contract.functions.listings(listing_id).call()

        return {
            "success": True,
            "listing": {
                "assetId": listing[0],
                "seller": listing[1],
                "amount": listing[2],
                "pricePerShare": listing[3],
                "active": listing[4]
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================================================
# ANALYTICS FUNCTIONS
# ==================================================

def get_top_10():
    try:
        total = contract.functions.assetCount().call()
        assets_list = []

        for i in range(1, total + 1):
            asset = contract.functions.assets(i).call()

            assets_list.append({
                "id": asset[0],
                "name": asset[1],
                "sharesSold": asset[7]
            })

        sorted_assets = sorted(
            assets_list,
            key=lambda x: x["sharesSold"],
            reverse=True
        )

        return sorted_assets[:10]

    except Exception:
        return []


# ==================================================
# BUILD TRANSACTIONS (WRITE FUNCTIONS)
# ==================================================

def _build_base_tx(wallet, value=0):
    wallet = Web3.to_checksum_address(wallet)

    return {
        "from": wallet,
        "nonce": w3.eth.get_transaction_count(wallet),
        "gas": 500000,
        "gasPrice": w3.to_wei("10", "gwei"),
        "value": value
    }


# --------------------------------------------------
# CREATE ASSET
# --------------------------------------------------

def build_create_asset_tx(name, location, description, image_url,
                          total_shares, price, wallet):
    try:

        tx = contract.functions.createAsset(
            name,
            location,
            description,
            image_url,
            total_shares,
            price
        ).build_transaction(
            _build_base_tx(wallet)
        )

        return {"success": True, "tx": tx}

    except Exception as e:
        return {"success": False, "error": str(e)}


# --------------------------------------------------
# UPDATE ASSET
# --------------------------------------------------

def build_update_asset_tx(asset_id, name, location,
                          description, image_url,
                          price, wallet):
    try:

        tx = contract.functions.updateAsset(
            asset_id,
            name,
            location,
            description,
            image_url,
            price
        ).build_transaction(
            _build_base_tx(wallet)
        )

        return {"success": True, "tx": tx}

    except Exception as e:
        return {"success": False, "error": str(e)}


# --------------------------------------------------
# DELETE ASSET
# --------------------------------------------------

def build_delete_asset_tx(asset_id, wallet):
    try:

        tx = contract.functions.deleteAsset(
            asset_id
        ).build_transaction(
            _build_base_tx(wallet)
        )

        return {"success": True, "tx": tx}

    except Exception as e:
        return {"success": False, "error": str(e)}


# --------------------------------------------------
# BUY PRIMARY SHARES
# --------------------------------------------------

def build_buy_primary_tx(asset_id, amount, wallet, value_wei):
    try:

        tx = contract.functions.buyShares(
            asset_id,
            amount
        ).build_transaction(
            _build_base_tx(wallet, value=value_wei)
        )

        return {"success": True, "tx": tx}

    except Exception as e:
        return {"success": False, "error": str(e)}


# --------------------------------------------------
# LIST SHARES
# --------------------------------------------------

def build_list_shares_tx(asset_id, amount, price_per_share, wallet):
    try:

        tx = contract.functions.listSharesForSale(
            asset_id,
            amount,
            price_per_share
        ).build_transaction(
            _build_base_tx(wallet)
        )

        return {"success": True, "tx": tx}

    except Exception as e:
        return {"success": False, "error": str(e)}


# --------------------------------------------------
# BUY LISTING
# --------------------------------------------------

def build_buy_listing_tx(listing_id, wallet, value_wei):
    try:

        tx = contract.functions.buyListedShares(
            listing_id
        ).build_transaction(
            _build_base_tx(wallet, value=value_wei)
        )

        return {"success": True, "tx": tx}

    except Exception as e:
        return {"success": False, "error": str(e)}