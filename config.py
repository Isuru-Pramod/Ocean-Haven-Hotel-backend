import os
from dotenv import load_dotenv

load_dotenv()

SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
