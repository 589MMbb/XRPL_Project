import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import NFTokenMint
from xrpl.models.requests import AccountNFTs
from xrpl.utils import str_to_hex

testnet_url = "https://s.altnet.rippletest.net:51234"

def mint_token(seed, uri, flags, transfer_fee, taxon):
    """mint_token"""
    # Get the client
    minter_wallet = Wallet.from_seed(seed)
    client = JsonRpcClient(testnet_url)

    # Get the sequence number for the wallet
    account_info = xrpl.account.get_account_info(minter_wallet.classic_address, client)
    if "account_data" in account_info.result:
        sequence = account_info.result["account_data"]["Sequence"]
    else:
        raise ValueError("Failed to retrieve account sequence number")

    # Define the mint transaction
    mint_tx = NFTokenMint(
        account=minter_wallet.classic_address,
        sequence=sequence,  # Include the sequence number in the transaction
        uri=str_to_hex(uri),
        flags=int(flags),
        transfer_fee=int(transfer_fee),
        nftoken_taxon=int(taxon)
    )

    # Submit the transaction and get results
    reply = ""
    try:
        response = xrpl.transaction.safe_sign_and_autofill_transaction(
            mint_tx, minter_wallet, client
        )
        response = xrpl.transaction.submit_and_wait(response, client)
        reply = response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply = f"Submit failed: {e}"

    return reply



def get_tokens(account):
    """get_tokens"""
    client=JsonRpcClient(testnet_url)
    acct_nfts=AccountNFTs(
        account=account
    )
    response=client.request(acct_nfts)
    return response.result


def burn_token(seed, nftoken_id):
    """burn_token"""
# Get the client
    owner_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
    burn_tx=xrpl.models.transactions.NFTokenBurn(
        account=owner_wallet.address,
        nftoken_id=nftoken_id    
    )
# Submit the transaction and get results
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(burn_tx,client,owner_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply