import json
import hashlib
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.account import get_account_info



JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

# Generate a new test wallet if required. This can be commented out if you're using a static test address and secret.
test_wallet = generate_faucet_wallet(client, debug=True)

def write_hash_to_file(hash_value: str):
    """Writes the given hash value to hash_value.txt."""
    with open('hash_value.txt', 'w') as f:
        f.write(hash_value)

def generate_hash_from_data(data):
    """Generates a SHA-256 hash from the given data."""
    serialized_data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialized_data.encode()).hexdigest()

def mint_nft(wallet, hash_reference: str):
    """Mints an NFT on the XRPL Testnet."""
    nft_amount = {
        "currency": hash_reference[:27],
        "value": "1",
        "issuer": wallet.classic_address
    }
    tx = Payment(
        account=wallet.classic_address,
        amount=nft_amount,
        destination=wallet.classic_address,
        last_ledger_sequence=get_latest_validated_ledger_sequence(client) + 20,

        fee="10",
        sequence=get_account_info(wallet.classic_address, client).sequence
    )
    signed_tx = wallet.sign_transaction(tx)
    response = client.submit_transaction(signed_tx)
    if response.is_successful():
        print(f"Successfully minted NFT with hash reference: {hash_reference}")
    else:
        print("Failed to mint NFT:", response.result["engine_result_message"])

if __name__ == "__main__":
    # Load your building data
    with open('building_data.json', 'r') as f:
        building_data = json.load(f)

    # Generate hash from data
    hash_value = generate_hash_from_data(building_data)

    # Write the hash to the file for verification or other purposes
    write_hash_to_file(hash_value)

    # Mint the NFT
    mint_nft(test_wallet, hash_value)
