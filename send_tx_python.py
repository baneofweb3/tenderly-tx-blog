import os
from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

# Set up tenderly gateway as our provider. We pull the url which contains our access token from an environment variable.
web3 = Web3(Web3.HTTPProvider(os.getenv("TENDERLY_URL")))

# Set up the addresses.
# sender is an object that contains the private key as well as the public address of the sender.
# receiver is just the public address to which we will be sending SEP. We don't need a private key here.
sender = {
    "private_key": os.getenv("PRIVATE_KEY"), # Extract this from your environment so we can share the script.
    "address": "", # Sender public address - make sure this account has some SEP on sepolia.
}
receiver = "" # Receiver public address goes here.

# Query the blockchain to see the current balance of the receiver.
receiverBalance = web3.eth.getBalance(receiver)
receiverBalanceETH = web3.fromWei(receiverBalance, "ether")
print(f'Destination balance before transfer: {receiverBalanceETH} ETH')

# This will ask the provider to suggest the gas price. In python we have to state this explicitely.
web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

# Create the tx object and sign it.
tx_create = web3.eth.account.sign_transaction(
    {
        "nonce": web3.eth.get_transaction_count(sender["address"]),
        "gasPrice": web3.eth.generate_gas_price(), # You might need to play around with this parameter if the network is overwhelmed.
        "gas": 21000,
        "to": receiver,
        "value": web3.toWei("0.001", "ether"), # Set how much SEP you want to send here.
        "chainId": 11155111, # Sepolia network ID is 11155111, change it if you are using a different network.
    },
    sender["private_key"],
)

# Send the transaction and wait for the receipt.
tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
print("Sent! 🎉")
print(f"TX hash: { tx_hash.hex() }")
print("Waiting for receipt...")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Print out the link to transaction details on the Tenderly Dashboard.
print(f"TX details: https://dashboard.tenderly.co/tx/sepolia/{tx_hash.hex()}")

# Query the blockchain again to see the new balance of the receiver. It should be increased now.
receiverBalance = web3.eth.getBalance(receiver)
receiverBalanceETH = web3.fromWei(receiverBalance, "ether")
print(f'Destination balance after transfer: {receiverBalanceETH} ETH')