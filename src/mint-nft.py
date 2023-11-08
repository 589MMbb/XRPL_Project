from xrpl.transaction import submit_and_wait
from xrpl.models.transactions import NFTokenMint, NFTokenMintFlag
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.clients import JsonRpcClient
from binascii import hexlify
import json

# Constants for the XRPL Testnet and the JSON file paths
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
COMBINED_NFT_METADATA_JSON_PATH = "CombinedNFTMetadata.json"

# Initialize the client to connect to the XRPL Testnet
client = JsonRpcClient(JSON_RPC_URL)

# Function to load metadata from JSON
def load_metadata():
    with open(COMBINED_NFT_METADATA_JSON_PATH, 'r') as file:
        return json.load(file)

# Function to generate a new wallet or use an existing one
def get_wallet(seed=""):
    if seed:
        return Wallet.from_seed(seed)
    else:
        # Request a new testnet wallet from the faucet
        return generate_faucet_wallet(client=client)

# Main function to mint the NFT
def mint_nft():
    # Load the combined NFT metadata
    combined_metadata = load_metadata()
    building_name = combined_metadata["building"]
    # Sample URI with the recommended ending
    metadata_uri = f"ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf4dfuylqabf3oclgtqy55fbzdi/{building_name}.json"

    # Convert the URI to hexadecimal format for XRPL
    metadata_uri_hex = hexlify(metadata_uri.encode()).upper().decode()

    # Get wallet details
    issuer_wallet = get_wallet()  # Pass a seed as argument if you have one

    # Print wallet details
    print(f"Issuer Account: {issuer_wallet.classic_address}")
    print(f"Seed: {issuer_wallet.seed}")

    # Construct NFTokenMint transaction to mint the NFT with the metadata URI
    mint_tx = NFTokenMint(
        account=issuer_wallet.classic_address,
        uri=metadata_uri_hex,  # Include the URI in hexadecimal format
        flags=NFTokenMintFlag.TF_TRANSFERABLE,  # Set the transferable flag
        nftoken_taxon=0  # No specific taxon
    )

    # Sign and submit the mint transaction
    response = submit_and_wait(transaction=mint_tx, client=client, wallet=issuer_wallet)

    # Check the result
    if response.is_successful():
        print(f"Mint Transaction successful: {response.result}")
    else:
        print(f"Mint Transaction failed: {response.result}")

# Run the minting process
if __name__ == "__main__":
    mint_nft()
