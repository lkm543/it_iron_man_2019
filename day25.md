# Bitcoin與Ethereum的架構

昨天我們提到了區塊鏈與代幣的發展，今天我們會來解說目前最主流的兩大公鏈─Bitcoin與Ethereum。還記得我們在Day02-Day07有嘗試寫出一個最基本的區塊鏈嗎？稍後我們在講解架構時也會拿我們之前所寫的簡易區塊鏈做個簡單對照。

# Bitcoin與Ethereum的交易格式

回憶一下我們之前所寫的`get_balance`是專門用來取得某特定帳戶的餘額，因為區塊鏈上的代幣只會有三種來源：挖礦獎勵、挖到區塊中的手續費總和、收到別人的匯款款項，因此我們可以利用這三個來源把該帳戶的餘額統整起來。

```python
def get_balance(self, account):
    balance = 0
    for block in self.chain:
        # Check miner reward
        miner = False
        if block.miner == account:
            miner = True
            balance += block.miner_rewards
        for transaction in block.transactions:
            if miner:
                balance += transaction.fee
            if transaction.sender == account:
                balance -= transaction.amounts
                balance -= transaction.fee
            elif transaction.receiver == account:
                balance += transaction.amounts
    return balance
```

只是這樣並沒有辦法預防`雙花攻擊(Double Spending)`，也就是我們的確可以知道發起交易當下的用戶資產是否足夠，但卻無法保證使用者的餘額是否會被重複花用，因此只要交易紀錄尚未被寫進區塊內，`get_balance`所取得的餘額永遠不會減少，使用者可以無限制的發起交易並放置入`pending_transactions`等待礦工驗證。

即便是下面礦工打包交易所用的`add_transaction`函式中檢查餘額也只是檢查之前所有區塊的餘額，當下區塊的交易支出並沒有被計算進去，因此同一筆交易可以在新區塊中中不停出現而且不會被扣款。

```python
def add_transaction(self, transaction, signature):
    public_key = '-----BEGIN RSA PUBLIC KEY-----\n'
    public_key += transaction.sender
    public_key += '\n-----END RSA PUBLIC KEY-----\n'
    public_key_pkcs = rsa.PublicKey.load_pkcs1(public_key.encode('utf-8'))
    transaction_str = self.transaction_to_string(transaction)
    if transaction.fee + transaction.amounts > self.get_balance(transaction.sender):
        return False, "Balance not enough!"
    try:
        # 驗證發送者
        rsa.verify(transaction_str.encode('utf-8'), signature, public_key_pkcs)
        self.pending_transactions.append(transaction)
        return True, "Authorized successfully!"
    except Exception:
        return False, "RSA Verified wrong!"
```

因此區塊鏈上所使用的交易格式必須能夠有效對抗這類的`雙花攻擊(Double Spending)`，另外也因為日常使用必須頻繁地確認帳戶餘額，同時交易格式的設計也要考量到盡可能地減少查閱餘額所需要的運算量。

## Bitcoin的UTXO(Unspent Transaction Output)架構

Bitcoin採用的是`UTXO(Unspent Transaction Output)架構`，直接翻譯過來便是還沒被用來支付的交易。你可以先把UTXO看作是一連串支票的集合，每張支票上面的數目不一，當你匯款給別人時，其實就是開給別人一張尚未支付的支票(UTXO)，接著如果別人想要使用，就把支票(UTXO)拿去匯款生成另一張尚未支付的UTXO給被匯款者，如果匯款後自身仍然有餘額便會再生成一張支票(UTXO給自己)

![UTXO](http://www.lkm543.site/it_iron_man/day26_2.JPG)

以上圖為例，當Bob收到別人所支付的5BTC時，就相當於收到別人給的5BTC的支票(UTXO)，如果Bob日後匯款2BTC給Ally，就等於利用這張5BTC的支票開給Ally一張價值2BTC的UTXO，至於剩下的3BTC則會生成另一張支票(UTXO給自己)，這個方式也能夠有效對抗雙花攻擊，因為每一張UTXO最多只能被使用一次。

![blockstream](http://www.lkm543.site/it_iron_man/day26_3.JPG)

圖片來源: [blockstream](https://blockstream.info)

在[這裡](https://blockstream.info)你可以看到每個區塊中的交易，上圖便是一筆交易動用了兩個UTXO後，生成四個新的UTXO給不同的對方，會使用到兩個UTXO代表單一UTXO並無法支應全部的開銷。

![blockstream](http://www.lkm543.site/it_iron_man/day26_4.jpg)

圖片來源: [blockstream](https://blockstream.info)

展開交易紀錄你也可以直接看到哪幾個UTXO是處在尚未被使用(Unspent)的狀態，因此帳戶目前可以動用餘額(Balance)其實就是所有持有UTXO的金額總和！

打開Bitcoin的[區塊鏈瀏覽器](https://www.blockchain.com/explorer)你更可以看到目前總共有大約6000萬個[UTXO](https://utxo-stats.com/)，至於目前Transaction的總數目大約落在5億左右([參考資料](https://www.quandl.com/data/BCHAIN/NTRAT-Bitcoin-Total-Number-of-Transactions))。

### UTXO如何預防雙花攻擊

UTXO如同支票一般，限制了每張支票(UTXO)都只能夠被使用一次，透過了限制UTXO的使用次數來避免雙花攻擊。但UTXO有個缺陷就是在交易被納入區塊前，該UTXO是可以無限制地被使用的，至於哪筆交易會實際被礦工採納則視交易手續費決定，因此在收款前請務必確認UTXO已被礦工打包進入區塊中。

### UTXO的優點

#### Scalability

UTXO的架構是以UTXO為單位進行交易，因此可以同時發起複數個交易給不同的收款方，在擴展性上有優勢。

#### Privacy

雖然Bitcoin並沒有辦法做到完全的資訊隱藏，但在UTXO架構下以支票為單位作為交易相較容易保障雙方的隱私。

## Ethereum的Account架構

上頭提到UTXO的架構有個缺陷是在UTXO正式進入區塊前該UTXO可被使用無數次，因此匯款方可以使用同一個UTXO重複付款，一但收款方沒有仔細確認是否已經被區塊打包就可能受騙上當，在Ethereum的白皮書[A Next-Generation Smart Contract and Decentralized Application Platform](http://blockchainlab.com/pdf/Ethereum_white_paper-a_next_generation_smart_contract_and_decentralized_application_platform-vitalik-buterin.pdf)中是這樣舉例的：

> If one entity has 50 BTC, and simultaneously sends the same 50 BTC to A and to B, only the transaction that gets confirmed first will process. 

因此Ethereum採用的是Account架構，也就是相當於銀行的簽帳卡，每張簽帳卡都有對應到帳戶的餘額，每次發送交易前也都會再次確認餘額是否足夠，Ethereum上同時也會記錄每個錢包地址目前的餘額。

![Etherscan](http://www.lkm543.site/it_iron_man/day26_5.JPG)

圖片來源: [etherscan](https://etherscan.io/address/0xc88f7666330b4b511358b7742dc2a3234710e7b1)

在[Etherscan](https://etherscan.io/)上，任意點開一個地址(上圖)，便可以發現裏頭清楚記錄了關於這個地址每一筆交易的相關細節，像是收款方、匯款方、金額、或手續費等。這便是我們提到的Account架構─每個帳戶都清楚記錄了目前的狀態，交易明細也只要簡單記錄收款與匯款方即可。

### Account架構如何預防雙花攻擊

為了避免雙花攻擊，Ethereum會給單一Account發出的交易一個逐漸遞增的nonce值，也就是下圖中的紅色框框，nonce值較小的交易便會優先執行，因此收款方便可以透過查閱該帳戶所有簽發過的交易次序來事先確認該交易的優先順序為何。

![Etherscan](http://www.lkm543.site/it_iron_man/day26_6.JPG)

圖片來源: [etherscan](https://etherscan.io/tx/0x5b9e49b7d8f1a8709ab8f334691c4152ea395ada213159679ff3292f1dcd3a76)

### Input Data

如果你有仔細看的話應該會發現Ethereum的交易紀錄中有一欄`Input Data`，該欄位也可以拿來觸發過幾天後我們會提到的智能合約的功能，透過Input Data告知區塊鏈上的礦工我們想要觸發智能合約裡的哪個函式，或是可以用來記錄這筆交易的用途，有時候甚至會利用區塊鏈的不可竄改特性特意遺留某些文字在區塊鏈上。

比方說在[這裡](https://etherscan.io/tx/0xf56d81301da93f71368ad7f8d605648d77be6edb13e8875cf3e5906f38d1b548)你可以看到由Ryu Gi-hyeok寫入的南北韓和平宣言(下圖)，或是由不知名人士為避免政府封鎖所寫入的[北大性侵案](https://etherscan.io/tx/0x2d6a7b0f6adeff38423d4c62cd8b6ccb708ddad85da5d3d06756ad4d8a04a6a2)。要觀看這些文字只需要簡單按下Click to see More，並再View input as那欄選擇UTF-8便可以用文字的形式閱讀。

![Etherscan](http://www.lkm543.site/it_iron_man/day26_7.JPG)

圖片來源: [etherscan](https://etherscan.io/tx/0xf56d81301da93f71368ad7f8d605648d77be6edb13e8875cf3e5906f38d1b548)

### Account架構的優點

#### Simplicity

Account架構的優點就是簡單明瞭，跟我們平常生活中所使用的銀行、金融卡原理上是一致的，相較容易被大眾理解與接受。

#### Efficiency

Account架構的另一個優點是在簡單、一對一的交易中效率較高，只需要單純對兩方的餘額做增減，並不需要產生額外的UTXO即可完成。

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。

# Ref:
-  [UTXO vs Account/Balance Model](https://medium.com/@sunflora98/utxo-vs-account-balance-model-5e6470f4e0cf)
- [比特幣UTXO模型介紹-如何解讀比特幣交易](https://steemit.com/cn-cryptocurrency/@antonsteemit/utxo)
- [UTXO 和 Account 模型对比](https://zhuanlan.zhihu.com/p/57272282)
- [【以太坊區塊鏈】紀錄歷史性的一刻：南北韓和平宣言](https://www.blocktempo.com/historic-korean-peace-declaration-recorded-on-ethereum-blockchain/)
