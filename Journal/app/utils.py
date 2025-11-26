from web3 import Web3


def sendTransaction(message):

    w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/a046a626ce8146b49725bd807759e1a8'))
    privateKey = 'e378b1fe4ec732eba8df6e8b68eef6ddecb63afb1dd2b076322553b785f3a48b'
    address = '0x78322513602c06ed359357645F56E0980Edcaa69'
              
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.sign_transaction(dict(
        nonce = nonce,
        gasPrice = gasPrice,
        gas = 100000,
        to = '0x0000000000000000000000000000000000000000',
        value = value,
        data = w3.toHex(b'hello world')
    ), privateKey)

    tx = w3.eth.send_raw_transaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    print(txId)
