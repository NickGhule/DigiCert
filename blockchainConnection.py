from web3 import Web3, HTTPProvider
import json

class blockchainConnection:
    def __init__(self):
        # Connect to the blockchain
        host = '127.0.0.1'
        port = '8545'
        self.w3 = Web3(HTTPProvider('http://' + host + ':' + port))
        
        contractBuild = open("build/contracts/digitalID.json", "r").read()
        _abi = json.loads(contractBuild)['abi']
        _address = "0x38448f15b3FB2Ba7587E4e25dBD5E7e4915ddCB5"  # This address is the address of the contract which changes for every deployment
        self.contract = self.w3.eth.contract(address = _address, abi = _abi)

    def addDocument(self, _userName, _documentID,  _documentHash, _address = None):
        if _address == None:
            _address = self.w3.eth.accounts[0]
        tx_hash = self.contract.functions.addDocumentHash(_userName, _documentID, _documentHash).transact( {'from': _address, 'gas': 1000000})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt
    
    def getDocumentHistory(self, _userName, _documentID):
        return self.contract.functions.getDocumentHashHistory(_userName, _documentID).call()


if __name__ == "__main__":
    bc = blockchainConnection()
    bc.addDocument("nick", "test", "test")
    print(bc.getDocumentHistory("nick", "test"))