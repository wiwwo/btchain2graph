# Bitcoin Blockchain to Graph

Blockchain is nothing more than list of "From A to B, amount N" list.
<bt>It's ingteresting to "follow the money".
<br>This is what this code is for.

## How to run
Code start from the latest block, returned by [getLatestBlock()] (https://github.com/wiwwo/btchain2graph/blob/d9848d7dcb0f3d51d0e4a34b27715bd398301645/functions/myFunctions.py#L7)
<br>The parameter is an integer telling code how many blocks in the past you want to dig.
<br>Code execution sample:
```
$ ./btchain2graph.py 2
2017-10-19 17:34:46,837 [        1881] - Hello you!
2017-10-19 17:34:46,838 [        1881] - Depth: 2
2017-10-19 17:34:46,956 [        2000] - Starting block 1/2
2017-10-19 17:34:57,855 [       12899] - Starting block 2/2
2017-10-19 17:35:12,300 [       27343] - Now spooling addresses.csv.gz
2017-10-19 17:35:12,503 [       27546] - Now spooling block.csv.gz
2017-10-19 17:35:12,507 [       27550] - Now spooling transactions.csv.gz
2017-10-19 17:35:12,565 [       27608] - That's all folks!
```

Log files in `log` directory.
<br>Resulting files in `output` directory.

## Output files samples
Output files are gemerated to be quickly and easly imported in neo4j.
<br>Code procudes 3 files:

### Addresses.csv.gz
Contains Addressed list (nodes in graph DB)
```
$ zcat addresses.csv.gz | head -5
":LABEL","id:id(address)"
"address","mine"
"address","1Hz96kJKF2HLPGY15JWLB5m9qGNxvt8tHJ"
"address","1B6wVxwMNvjoe3sjBECm9NVrMCktzqnzDE"
"address","1AwGjBv34BvmRmw21PZEqo99xUQRdKkaAp"
```

### block.csv.gz
Contains Blocks list (nodes in graph DB)
```
$ zcat block.csv.gz | head -5
":LABEL","prev_block","id:id(block)","time"
"block","000000000000000000c1a9f728c715616f7dbb5a0d1028933e10fad3bd823b65","000000000000000000db8aa29a5c4c9feeb6fcfed04c30c15c6e27dc1527736e","1508426999"
"block","0000000000000000005cae673509ca4061c5bb67afd29ca5e25cd31e2c0d0823","000000000000000000c1a9f728c715616f7dbb5a0d1028933e10fad3bd823b65","1508426733"
```

### transactions.csv.gz
Contains transaction list (relation in graph DB, between two addresses)
```
$ zcat transactions.csv.gz | head -5
":END_ID(address)","hash","spent","value",":START_ID(address)","time",":TYPE"
"1jdBT5Vc2toUx7VgYdRZisEZEY4FS53Fk","7f8567b42abe19aedba0339196cdd2ae646447c05117738da391ee465d83c88c","False","0","mine","1508426999","transaction"
"1B7LCyAmH7MB8MWz8LZRQ4pKN6Uu3Bdcok","4803832ff7fb6d2f0e9e1013a770de37f18bdb386d4a0252a68dc710ef2736a4","False","20000000","1B6wVxwMNvjoe3sjBECm9NVrMCktzqnzDE","1508412634","transaction"
"1Mewm1ZsCV8MGt285PCfe8iB6TTLSnFXQE","1486af9b7b4566491454dad4ff02448ecedc5a4efe98df88dbc7a9dc23924a19","False","228800000","1Hhr67kbfpcewPjZCMYq4Xssz9jP8MGhyE","1508426938","transaction"
"1Kwh6KJszVFo15oHPmWkJupjhrDTAMnRT","0174fb811521995c2365d0ac47efef575905db84d8924118b457d6683858c6e0","False","1152462466","19rdJPyvUkaJDgfbzj5yWLXdKeySqJWwCX","1508426999","transaction"
```


## Blockchain info source
This won't be possible without [blockchain.info](blockchain.info) website

API description [here](https://blockchain.info/api/blockchain_api)
<br>Latest Block [here](https://blockchain.info/latestblock)
<br>
You can get a specific block by calling https://blockchain.info/rawblock/$block_hash
<br>Eg. [https://blockchain.info/block/0000000000000000018a430d91c5bf045a4a6d24601a1c88e5326adb7d17b9ba](https://blockchain.info/block/0000000000000000018a430d91c5bf045a4a6d24601a1c88e5326adb7d17b9ba)
<br>[Block by timestamp](https://blockchain.info/blocks/1294047694000)
