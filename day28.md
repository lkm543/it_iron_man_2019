# 操作Bitcoin

在提完Bitcoin的交易架構與幾個重要發展後，我們來實際體驗如何操作Bitcoin的匯款與收款。因為使用圖形化介面(GUI)相較容易，但卻不利於後續的二次開發、使用上也較不彈性，因此我們今天主要是講解如何直接使用Command Line來進行Bitcoin上的各式交易與匯款。

# 圖形化介面

如果你沒有二次開發或是發送一些特殊交易的需求，那麼使用一般的圖形化介面(GUI)進行收款或匯款就可以了，至於要選擇使用何種程式，你可以到[bitcoin.org](https://bitcoin.org/en/)根據你的要求選擇，選擇過程中(下圖)你也可以看到我們昨天講到的`多重簽名(Multisig)`或是`隔離見證(SegWit)`的功能，在這裡可以都勾起來，畢竟不確定之後何時會使用到。

![Multisig&Segwit](http://www.lkm543.site/it_iron_man/day28_1.JPG)

圖片擷取自: [bitcoin.org](https://bitcoin.org/en/)

最後[bitcoin.org](https://bitcoin.org/en/)推薦我用[electrum](https://electrum.org/#download)這套軟體，下載安裝後打開，可以選擇想要開啟的錢包種類。

![Wallet Tye](https://www.lkm543.site/it_iron_man/day28_2.JPG)

圖片擷取自: [electrum](https://electrum.org)

最後開完錢包就大功告成啦！下圖是它的介面，有收款與付款兩大功能可以選擇，裏頭還蠻清楚的，因此就不另外詳述如何使用了。

![UI](https://www.lkm543.site/it_iron_man/day28_3.JPG)

圖片擷取自: [electrum](https://electrum.org)

# Bitcoin-core

我們今天主要的重點是`Bitcoin-core`的安裝與使用，`Bitcoin-core`是Bitcoin目前最主流與廣泛使用的主程式，裏頭包含了bitcoind、bitcoin-qt與bitcoin-cli三隻程式，先就這三個做簡單介紹。

- bitcoind
    `bitcoind`的字尾d可以看作是develop的縮寫，這隻城市的特色就是可以透過[RPC](https://zh.wikipedia.org/wiki/%E9%81%A0%E7%A8%8B%E9%81%8E%E7%A8%8B%E8%AA%BF%E7%94%A8)呼叫裏頭的子程式，可以把它看作是client-server架構下的server，所以特別適合用來做比特幣相關服務的二次開發或營運。跟我們之前寫的簡易區塊鏈比較，就是節點端的程式，功能也是負責接收外界的請求。

- bitcoin-qt
    `bitcoin-qt`的特色就是提供了圖形化前端介面(下圖)，讓一般非程式開發者也可以很容易地使用。

![bitcoin-qt](https://en.bitcoinwiki.org/upload/en/images/6/62/Bitcoin-qt.png)

圖片來源: [Wikipedia](https://en.bitcoinwiki.org/wiki/Bitcoin-Qt)

- bitcoin-cli
    `bitcoin-cli`的字尾cli是client客戶端的縮寫，它允許你直接發送[RPC](https://zh.wikipedia.org/wiki/%E9%81%A0%E7%A8%8B%E9%81%8E%E7%A8%8B%E8%AA%BF%E7%94%A8)給bitcoind，可以把它看作是client-server架構下的client，可以讓你在沒有營運一個完整節點的情形下仍然可以向其他節點發出交易或查詢的請求。跟我們之前寫的簡易區塊鏈比較，就是客戶端的程式，功能是向節點發出查詢餘額或是交易請求。

## 環境設定

我測試的環境是在win10下開一個Ubuntu的子系統，如果你也想在win10下測試的話可以參考[這裡](https://zhuanlan.zhihu.com/p/62658094)進行安裝。安裝後你就你可以到[bitcoin.org](https://bitcoin.org/en/download)找最新版本的Bitcoin-core來下載，你可以先開個資料夾後再下載並且展開。

```shell
mkdir bitcoin
wget https://bitcoin.org/bin/bitcoin-core-0.18.1/bitcoin-0.18.1-x86_64-linux-gnu.tar.gz
tar xf bitcoin-0.18.1-x86_64-linux-gnu.tar.gz
```

安裝完後記得把bin資料夾放入環境變數(PATH)中，因為我安裝在d槽下，所以我的路徑是`/mnt/d/bitcoin/bitcoin-0.18.1/bin/`

```shell
export PATH=$PATH:/mnt/d/bitcoin/bitcoin-0.18.1/bin/
```

在Linux系統下，上面三隻程式的設定值都會在下面這個檔案中

> $HOME/.bitcoin/bitcoin.conf

以nano打開後

```shell
nano $HOME/.bitcoin/bitcoin.conf
```

可以在裏頭設定RPC用的密碼，但我們之後的測試是在模擬環境下測試，所以不設定也沒關係

```shell
rpcpassword=YOUR_PASSWORD
```

在這裡另外說明一下，測試的方式有兩種：`Testnet`或`Regtest`，Testnet是連上比特幣的測試網路，也就是外網；而Regtest則是在本機端開啟一個完全私人的環境來做測試，目前主流的開發都是用Regtest了，因此我們之後的示範也會使用Regtest，但如果想要用testnet的話就在`$HOME/.bitcoin/bitcoin.conf`裏頭新增這一行就可以了。

```shell
testnet=1
```

另外修改權限只有我們能夠讀寫這個檔案

```shell
chmod 600 bitcoin.conf
```

到此就設定完畢了！

## 啟動與停止

在開始使用前先把bitcoind打開(如果使用testnet則不需要加-regtest)

```shell
bitcoind -regtest -daemon
```

接著你就會看到下面這行字，代表成功開啟了

```shell
Bitcoin server starting
```

要停止也很容易，下stop指令便行了。

```shell
bitcoin-cli stop
```

成功結束你會看到

```shell
Bitcoin server stopping
```

## 挖掘新區塊

創建新錢包的方式是透過`getnewaddress`指令

```shell
bitcoin-cli -regtest getnewaddress
```

因為regtest模式下block需要經過100個確認後才能夠花用裏頭的餘額，所以我們可以用`generatetoaddress`使產出的地址挖掘101個區塊，確保我們有50BTC可以用於後續的交易。

```shell
bitcoin-cli -regtest generatetoaddress 101 $(bitcoin-cli -regtest getnewaddress)
```

挖掘出來後你就可以利用`getbalance`查詢目前可支用的餘額

```shell
bitcoin-cli -regtest getbalance
```

就會發現裏頭有50元可以使用了！

```shell
50.00000000
```

## 發起交易

發起交易前我們先創建一個新的收款錢包

```shell
bitcoin-cli -regtest getnewaddress
```

> 2N1yF65i3KfXHJ7Pv6oxBeGoUSnGK2idzuQ

接著就可以利用`sendtoaddress`匯款給對方了

```shell
bitcoin-cli -regtest sendtoaddress 2N1yF65i3KfXHJ7Pv6oxBeGoUSnGK2idzuQ 5.00
```

匯款完後看到的這一連串Bytes便是我們的Transaction id!

```
7862877e89f9b2e14c42e508f31646c68f38d99e404c335769ad1092c9b33822
```

交易完之後記得再挖掘出一個新區塊，我們的交易才會被打包進去喔

```shell
bitcoin-cli -regtest generatetoaddress 1 $(bitcoin-cli -regtest getnewaddress)
```

## 手動簽發一筆交易

上面的交易其實省略了相當多步驟，也沒有逐步的簽署，所以我們來試試怎麼一步步從初始化交易到使用私鑰來簽發這比交易！但如果手動簽發出錯的話，手上的BTC可能會永久遺失，所以使用上請務必小心。

### 查詢UTXO

輸入`listunspent`指令就可以查詢目前還沒被使用的UTXO。

```shell
bitcoin-cli -regtest listunspent
```

![UTXO](http://www.lkm543.site/it_iron_man/day28_4.JPG)

### 初始化一筆交易

假設我們現在想要動用3ab2be755f676c9978c6a3bf42f87cfcb8f7393d10cf5c962a1590e3449c38d4這筆UTXO，那麼我們可以先設定：

> UTXO_ID=3ab2be755f676c9978c6a3bf42f87cfcb8f7393d10cf5c962a1590e3449c38d4
> UTXO_VOUT=0

接著我們利用`createrawtransaction`來初始化一筆交易，txid指我們想動用的UTXO編號，vout可以想成這筆UTXO的次序(可以在UTXO列表中找到這個值)。第二個JSON則是收款地址以及收款金額，注意收款金額與UTXO餘額的差就是手續費，兩者的差距必須小於0.1否則便會報錯。

```shell
bitcoin-cli -regtest createrawtransaction '''
    [
      {
        "txid": "'$UTXO_ID'",
        "vout": '$UTXO_VOUT'
      }
    ] 
    ''' '''
    {
      "2MyFEzBFSYb5PimVKGmeehY9MrxHJQrhGZF": 44.998
    }
    '''
```

接著就可以得到這筆交易的編碼後的資料了！

```shell
0200000001d4389c44e390152a965ccf103d39f7b8fc7cf842bfa3c678996c675f75beb23a0000000000ffffffff01c07f350c0100000017a91441d196828171b72dd14bf48378b5659bfde9e6ab8700000000
```

你可以用`decoderawtransaction`指令來看原本的交易內容

```shell
bitcoin-cli -regtest decoderawtransaction 0200000001d4389c44e390152a965ccf103d39f7b8fc7cf842bfa3c678996c675f75beb23a0000000000ffffffff01c07f350c0100000017a91441d196828171b72dd14bf48378b5659bfde9e6ab8700000000
```

![UTXO](http://www.lkm543.site/it_iron_man/day28_5.JPG)

### 簽署這筆交易

用`signrawtransactionwithwallet`指令來簽署這筆交易

```shell
bitcoin-cli -regtest signrawtransactionwithwallet 0200000001d4389c44e390152a965ccf103d39f7b8fc7cf842bfa3c678996c675f75beb23a0000000000ffffffff01c07f350c0100000017a91441d196828171b72dd14bf48378b5659bfde9e6ab8700000000
```

可以得到下面的回應，其中hex裏頭就是我的數位簽章了！你也可以發現它比交易的資料長非常多，這也是我們昨天有提到數位簽章的資料通常會佔到整體資料大小的2/3以上。

```json
{
  "hex": "02000000000101d4389c44e390152a965ccf103d39f7b8fc7cf842bfa3c678996c675f75beb23a0000000017160014d3c8facb4eb70ba6b14992951c1bb7260a759118ffffffff01c07f350c0100000017a91441d196828171b72dd14bf48378b5659bfde9e6ab870247304402204031dd9a2c8e78d4c41e8e758d2c33518f75012551793d086213f74edebe8efa0220161919fc3743dcbdfabf1f2ea44464bd59437cec2c225c0e27685e2d8cc4245b012103518af844b06091b5bed9ee5cf50ea372af8a1425afba9142a71d27b5ee38642a00000000",
  "complete": true
}
```

把數位簽章儲存成變數

> SIGNATURE=02000000000101d4389c44e390152a965ccf103d39f7b8fc7cf842bfa3c678996c675f75beb23a0000000017160014d3c8facb4eb70ba6b14992951c1bb7260a759118ffffffff01c07f350c0100000017a91441d196828171b72dd14bf48378b5659bfde9e6ab870247304402204031dd9a2c8e78d4c41e8e758d2c33518f75012551793d086213f74edebe8efa0220161919fc3743dcbdfabf1f2ea44464bd59437cec2c225c0e27685e2d8cc4245b012103518af844b06091b5bed9ee5cf50ea372af8a1425afba9142a71d27b5ee38642a00000000

最後就可以利用`sendrawtransaction`指令與我們剛剛簽發的數位簽章、想要動用的UTXO來交易了！

```
bitcoin-cli -regtest sendrawtransaction $SIGNATURE
```

你就可以得到一筆Transaction ID了

> 1089bff77424764ffadfaac6f12683b1c2265ebe0726598ee0cb28cf02dd017a

一樣挖掘新區塊後，就可以查詢有沒有新的UTXO生成

```shell
bitcoin-cli -regtest generatetoaddress 1 $(bitcoin-cli -regtest getnewaddress)
bitcoin-cli -regtest listunspent
```

新生成的UTXO結果如下

```json
 {
    "txid": "1089bff77424764ffadfaac6f12683b1c2265ebe0726598ee0cb28cf02dd017a",
    "vout": 0,
    "address": "2MyFEzBFSYb5PimVKGmeehY9MrxHJQrhGZF",
    "label": "",
    "redeemScript": "0014eac13ffacbced6b25fe7262ff14d8c4ffcf6b229",
    "scriptPubKey": "a91441d196828171b72dd14bf48378b5659bfde9e6ab87",
    "amount": 44.99800000,
    "confirmations": 1,
    "spendable": true,
    "solvable": true,
    "desc": "sh(wpkh([e6960773/0'/0'/2']038906fb9fb8259c15978872e186bc21897f4b51c01834f90ad53ed3056f44a328))#02k7gp80",
    "safe": true
  }
```

## 多重簽名

### 創設多重簽名的付款帳號

多重簽名的交易方法跟上面很類似，假設我們要創建一個2 of 3多重簽名的支付，利用`addmultisigaddress`指令：

```shell
bitcoin-cli -regtest addmultisigaddress 2 "
    [\"2MwgVmbPVRF9a44ar9AUB7sCHCrdDf81oxL\",
     \"2MwgVmbPVRF9a44ar9AUB7sCHCrdDf81oxL\", 
     \"2N1yF65i3KfXHJ7Pv6oxBeGoUSnGK2idzuQ\"
    ]
    "
```

就可以得到P2SH的新多重簽名收款地址了：

```json
{
  "address": "2MxKFjxNftmEnCJE2tmTktwVJKUqMAPQ1K3",
  "redeemScript": "522103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc92103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc921036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd53ae"
}
```

要付款給多重簽名的地址也只要把它當一般地址便可以了。

> bitcoin-cli -regtest sendtoaddress 2MxKFjxNftmEnCJE2tmTktwVJKUqMAPQ1K3 10.00

### 動用多重簽名的資金

首先一樣先利用下面這個指令把我們想要花用的UTXO編號找出來：

> bitcoin-cli -regtest listunspent

```json
{
    "txid": "241bb7af4262e475ee2bff4586a3b1c0b4a2f9efb8cb0901f5e16d7794451b83",
    "vout": 0,
    "address": "2MxKFjxNftmEnCJE2tmTktwVJKUqMAPQ1K3",
    "label": "",
    "redeemScript": "0020809d97cffc439727dd9fd38548c0e9c5a576e90f9ef11d99ef15635516453bcc",
    "witnessScript": "522103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc92103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc921036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd53ae",
    "scriptPubKey": "a914379bc18d46b35fed27f75c1128a8f36659615d5e87",
    "amount": 10.00000000,
    "confirmations": 1,
    "spendable": true,
    "solvable": true,
    "desc": "sh(wsh(multi(2,[e6960773/0'/0'/0']03ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc9,[e6960773/0'/0'/0']03ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc9,[e6960773/0'/0'/1']036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd)))#ys6kgphk",
    "safe": true
  }
```

一樣先初始化交易，假設我們要把裏頭的資金移轉到2NFZxvqDfa9EKvw7bMaBpRkAUfJZKUVCiKV

```shell
bitcoin-cli -regtest createrawtransaction '''
[
  {
    "txid": "241bb7af4262e475ee2bff4586a3b1c0b4a2f9efb8cb0901f5e16d7794451b83",
    "vout": 0
  }
]
''' '''
{
 "2NFZxvqDfa9EKvw7bMaBpRkAUfJZKUVCiKV": 9.998
}'''
```

> RAW_TX=0200000001831b4594776de1f50109cbb8eff9a2b4c0b1a38645ff2bee75e46242afb71b240000000000ffffffff01c0bc973b0000000017a914f4de1976c0e707fadff4a908f271d7091032268a8700000000

接著利用`dumpprivkey`把其中兩個私鑰取出，因為是2 of 3多重簽名，所以至少要經過兩個私鑰的簽署

```shell
bitcoin-cli -regtest dumpprivkey 2MwgVmbPVRF9a44ar9AUB7sCHCrdDf81oxL
bitcoin-cli -regtest dumpprivkey 2N1yF65i3KfXHJ7Pv6oxBeGoUSnGK2idzuQ
```

得到兩把私鑰

> cVaV7TWQodB8DhhMe4fiNtfV9paFpBmupQsbyWnwdBhN15EUhW9P
> cN3gCnSnyENguQQ49zyQ4SPrucTrCHVapvqq5qaYKVueSmTGpCoZ

接著先用第一把私鑰利用`signrawtransactionwithkey`簽署，並填入相對應的txid、vout、scriptPubKey、redeemScript、amount

```shell
bitcoin-cli -regtest signrawtransactionwithkey $RAW_TX '''
    [
      "cVaV7TWQodB8DhhMe4fiNtfV9paFpBmupQsbyWnwdBhN15EUhW9P"
    ]''' ''' 
    [
      {
        "txid": "241bb7af4262e475ee2bff4586a3b1c0b4a2f9efb8cb0901f5e16d7794451b83",
        "vout": 0,
        "redeemScript": "0020809d97cffc439727dd9fd38548c0e9c5a576e90f9ef11d99ef15635516453bcc",
        "witnessScript": "522103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc92103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc921036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd53ae",
        "scriptPubKey": "a914379bc18d46b35fed27f75c1128a8f36659615d5e87",        
        "amount": 10.00000000
      }
    ]
    '''
```

就可以得到以第一把私鑰簽過的數位簽章

```json
{
  "hex": "02000000000101831b4594776de1f50109cbb8eff9a2b4c0b1a38645ff2bee75e46242afb71b240000000023220020809d97cffc439727dd9fd38548c0e9c5a576e90f9ef11d99ef15635516453bccffffffff01c0bc973b0000000017a914f4de1976c0e707fadff4a908f271d7091032268a870400473044022047587f7a10c0f2107fa88bedb5268fbcbc6406d1cd14ae11dc90bed57dd5a849022070f6654daee33ee65e088754c54d301cf062f8fb434053617db82b6f3b42d5a301473044022047587f7a10c0f2107fa88bedb5268fbcbc6406d1cd14ae11dc90bed57dd5a849022070f6654daee33ee65e088754c54d301cf062f8fb434053617db82b6f3b42d5a30169522103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc92103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc921036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd53ae00000000",
  "complete": true
}
```

> FIRST_SIGNATURE=02000000000101831b4594776de1f50109cbb8eff9a2b4c0b1a38645ff2bee75e46242afb71b240000000023220020809d97cffc439727dd9fd38548c0e9c5a576e90f9ef11d99ef15635516453bccffffffff01c0bc973b0000000017a914f4de1976c0e707fadff4a908f271d7091032268a870400473044022047587f7a10c0f2107fa88bedb5268fbcbc6406d1cd14ae11dc90bed57dd5a849022070f6654daee33ee65e088754c54d301cf062f8fb434053617db82b6f3b42d5a301473044022047587f7a10c0f2107fa88bedb5268fbcbc6406d1cd14ae11dc90bed57dd5a849022070f6654daee33ee65e088754c54d301cf062f8fb434053617db82b6f3b42d5a30169522103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc92103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc921036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd53ae00000000

接著拿來簽章第二把

```shell
bitcoin-cli -regtest signrawtransactionwithkey $FIRST_SIGNATURE '''
    [
      "cN3gCnSnyENguQQ49zyQ4SPrucTrCHVapvqq5qaYKVueSmTGpCoZ"
    ]''' ''' 
    [
      {
        "txid": "241bb7af4262e475ee2bff4586a3b1c0b4a2f9efb8cb0901f5e16d7794451b83",
        "vout": 0,
        "redeemScript": "0020809d97cffc439727dd9fd38548c0e9c5a576e90f9ef11d99ef15635516453bcc",
        "witnessScript": "522103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc92103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc921036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd53ae",
        "scriptPubKey": "a914379bc18d46b35fed27f75c1128a8f36659615d5e87",        
        "amount": 10.00000000
      }
    ]
    '''
```

得到最後簽署的結果了！

```json
{
  "hex": "02000000000101831b4594776de1f50109cbb8eff9a2b4c0b1a38645ff2bee75e46242afb71b240000000023220020809d97cffc439727dd9fd38548c0e9c5a576e90f9ef11d99ef15635516453bccffffffff01c0bc973b0000000017a914f4de1976c0e707fadff4a908f271d7091032268a870400473044022047587f7a10c0f2107fa88bedb5268fbcbc6406d1cd14ae11dc90bed57dd5a849022070f6654daee33ee65e088754c54d301cf062f8fb434053617db82b6f3b42d5a301473044022047587f7a10c0f2107fa88bedb5268fbcbc6406d1cd14ae11dc90bed57dd5a849022070f6654daee33ee65e088754c54d301cf062f8fb434053617db82b6f3b42d5a30169522103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc92103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc921036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd53ae00000000",
  "complete": true
}
```

把最後的結果用`sendrawtransaction`發送出去，便可以移動資產了！

> bitcoin-cli -regtest sendrawtransaction 02000000000101831b4594776de1f50109cbb8eff9a2b4c0b1a38645ff2bee75e46242afb71b240000000023220020809d97cffc439727dd9fd38548c0e9c5a576e90f9ef11d99ef15635516453bccffffffff01c0bc973b0000000017a914f4de1976c0e707fadff4a908f271d7091032268a870400473044022047587f7a10c0f2107fa88bedb5268fbcbc6406d1cd14ae11dc90bed57dd5a849022070f6654daee33ee65e088754c54d301cf062f8fb434053617db82b6f3b42d5a301473044022047587f7a10c0f2107fa88bedb5268fbcbc6406d1cd14ae11dc90bed57dd5a849022070f6654daee33ee65e088754c54d301cf062f8fb434053617db82b6f3b42d5a30169522103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc92103ad88fdadd957df816e167d6598aad34f4b82cdc537b820b75fbe03e8e48c5cc921036874be266591da071920e700514ddc4571c67f465787888d4f16b1ce06e2decd53ae00000000

一樣交易後會得到一個交易id

> fd06828e8443aaa3e587e870c78752184a9a3712560c2fc666e3882778c825a0

這樣一來就完成多重簽名了，而且簽名的過程中可以分別在不同的本機簽署以避免私鑰外流的資安疑慮！另外一提，[bitcoin.org](https://bitcoin.org/en/developer-examples#testing-applications)裏頭的教學很多都是舊版的，如果用最新版(0.18.1)的話要注意一下寫法是不同的(踩了不少坑QQ)。

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。

# Ref:
- [Learning-Bitcoin-from-the-Command-Line](https://github.com/ChristopherA/Learning-Bitcoin-from-the-Command-Line)
- [比特币bitcoin-cli转账与交易的api使用总结](https://blog.csdn.net/a013152/article/details/81668629)
- [Original Bitcoin client/API calls list](https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_calls_list)
- [bitcoin全节点部署及bitcoind bitcoin-cli命令使用解释](https://blog.51cto.com/11975865/2384841)
- [Bitcoin Developer Examples](https://bitcoin.org/en/developer-examples#testing-applications)
