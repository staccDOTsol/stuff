import json 
with open ('./somejson.json', 'r') as f:

    sauces = json.loads(f.read())
csv = "contractAddress,tokenId,name,creator,owner,airdropAddress,_\n"
from time import sleep 
for s in sauces:
    for val in s.values():
        if 'username' in val:
            csv = csv + (val['username'])
        else:
            csv =  csv + (str(val)) 
        if 'airdropAddressEth' in val:
            if val['airdropAddressEth'] != None:
                csv = csv + ',' + (val['airdropAddressEth'])
            else:
                csv = csv + ',' + 'None'
        csv = csv + ','
    csv = csv + '\n'
with open('./sauce.csv', 'w') as f:
    f.write(csv)