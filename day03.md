我們在昨天已經定義完交易、區塊、區塊鏈的主要格式與資料，今天的目標是架構起我們的簡易區塊鏈，並且能夠做到下面這四件事情

1. 產生哈希/湊雜數(Hash)
2. 產生創世塊
3. 放置交易明細至新區塊中
4. 挖掘新區塊

# 產生哈希數(Hash)
哈希/湊雜數可以想做是一種轉換方式，可以把**任意長度的輸入轉換成固定長度的輸出**，以SHA-1為例，它能夠把輸入值轉換成固定20個位元組的輸出。

哈希函數(`hash function`)必須同時滿足兩個條件：

> 1. 同樣的輸入值必定得到相同的輸出值
> 2. 得到的哈希數無法反推回原本的資料

以下面為例，`Hello World!`的字串能夠透過`SHA-1`的哈希函數轉換成：

> 2ef7bde608ce5404e97d5f042f95f89f1c232871

但同時產生的`2ef7bde608ce5404e97d5f042f95f89f1c232871`無法反推回原本的`Hello World!`。由於輸入資料的不同，往往我們可以把哈希數視作幾近隨機的位元組所構成(但仍然會因為哈希函數的不同而有所變異)

![hash](https://www.lkm543.site/it_iron_man/day3_1.jpg)
[這個網址](https://www.fileformat.info/tool/hash.htm)有更多的哈希函式的轉換可以試玩看看，以`Hello World!`這個字串為例，各種轉換法輸出的哈希值也不相同。

![Hello World!](https://www.lkm543.site/it_iron_man/day3_2.jpg)

在這裡我們先把下面這些資料連接後作為哈希函式的輸入：

1. 前一個區塊的哈希值(`previous_hash`)
2. 區塊產生當下的時間戳(`timestamp`)
3. 所有的交易明細(`transactions`)
4. 挖掘中的`nonce`值

![Our Hash](https://www.lkm543.site/it_iron_man/day3_3.jpg)

下面是我們今天的程式碼，其中`transaction_to_string`負責把交易明細轉換成字串、`get_transactions_string`負責把區塊紀錄的所有交易明細轉換成一個字串、`get_hash`負責依據這四筆資料產生相對應的哈希數。


```python
import hashlib

def transaction_to_string(self, transaction):
    transaction_dict = {
        'sender': str(transaction.sender),
        'receiver': str(transaction.receiver),
        'amounts': transaction.amounts,
        'fee': transaction.fee,
        'message': transaction.message
    }
    return str(transaction_dict)

def get_transactions_string(self, block):
    transaction_str = ''
    for transaction in block.transactions:
        transaction_str += self.transaction_to_string(transaction)
    return transaction_str

def get_hash(self, block, nonce):
    s = hashlib.sha1()
    s.update(
        (
            block.previous_hash
            + str(block.timestamp)
            + self.get_transactions_string(block)
            + str(nonce)
        ).encode("utf-8")
    )
    h = s.hexdigest()
    return h
```

# 產生創世塊(genesis block)

創世塊就是開始部署區塊鏈時所產生的第一個區塊，創世塊通常具有劃時代的意義，雖然以第一個區塊的角度而言它不需要帶有任何交易紀錄、是個空區塊，但創造鏈的人可以把精神或是象徵性的東西寫入創世塊中藉此提醒後人(?)，並以比特幣來說，比特幣的創世塊可以在[這個網址](https://sourceforge.net/p/bitcoin/code/133/tree/trunk/main.cpp#l1630)查詢到。

```c
const char* pszTimestamp = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks";
```

> The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.

是中本聰寫入創世塊中的一句話，這也是2009/01/03英國《泰晤士報》的頭版標題，這時候的世界還陷在2008金融風暴的危機中，這篇報導敘述了當時的英國正考慮進行財務紓困，或許中本聰只是單純想證明這區塊確實是當天寫入的，又或許透過《泰晤士報》的頭版標題又對政府與中心化金融機構進行一次諷刺。

![The Times](https://image1.thenewslens.com/2018/1/56z78h9i5pg5erdou6gjbgmmfejc15.jpg)
圖片來源：[The News Lens](https://hk.thenewslens.com/)

由於這是我們的第一個區塊鏈，所以我們就在`previous_hash`的欄位給...........`Hello World!` 藉此紀念一下 ，並且難度與挖礦獎勵設定成區塊鏈的預設值，礦工這裡就直接填入我們的姓名，產生創世塊後就直接把創世塊加入到`chain`之中

```python
def create_genesis_block(self):
    print("Create genesis block...")
    new_block = Block('Hello World!', self.difficulty, 'lkm543', self.miner_rewards)
    new_block.hash = self.get_hash(new_block, 0)
    self.chain.append(new_block)
```

# 放置交易紀錄至新區塊中

區塊過大會導致在網路傳播上的不易與耗時，也因此每個區塊的承載量是有容量大小的上限，那礦工如何選擇哪幾筆交易應該被優先處理呢？礦工通常會根據自身的利益選擇手續費高的交易優先被處理，因此在這裡我們選擇手續費最高的幾筆交易優先加入區塊中。但如果等待中的交易(`pending_transactions`)數目沒有到區塊的承載量上限的話，那麼自然我們可以全部處理了！

而大家所熟知的Bitcoin的區塊容量上限是`1MB`，在1MB的容量下平均可以接受`3.3-7 TPS`(Transaction per Seconds，每秒幾筆交易)([來源](https://en.wikipedia.org/wiki/Bitcoin_scalability_problem))，這數字大家可能沒甚麼概念，但與大家常使用的Visa做個比較─Visa的平均處理速度為`1700 TPS`([來源](https://hackernoon.com/the-blockchain-scalability-problem-the-race-for-visa-like-transaction-speed-5cce48f9d44))，因此在bitcoin大規模被應用之前如何改進與增大TPS為社群熱門的研究題目，中本聰原先給的解決方案是增加區塊的容量，也就是提升原先設定的1MB區塊容量大小限制即可應對，增加TPS的路線與方法的不同甚至導致了社群的分裂，甚至產生了分岔(Fork)而生成了新的貨幣Bitcoin Cash(BCH)，關於BTC與BCH的路線之爭與差異有興趣繼續深入研究的人可以參考[這裡](https://cointelegraph.com/bitcoin-cash-for-beginners/btc-bch-differences)，關於分岔的議題之後我們會再探討。

而Ethereum的區塊容量則是根據耗用資源的多寡以`Gas`為單位，每個區塊有`800萬Gas`的限制，關於Ethereum耗用Gas的機制因為較為複雜，我們之後也會另外說明，它們都有區塊容量的上限以確保挖角到新區塊後廣播過程的順利。

```python
def add_transaction_to_block(self, block):
    # Get the transaction with highest fee by block_limitation
    self.pending_transactions.sort(key=lambda x: x.fee, reverse=True)
    if len(self.pending_transactions) > self.block_limitation:
        transcation_accepted = self.pending_transactions[:self.block_limitation]
        self.pending_transactions = self.pending_transactions[self.block_limitation:]
    else:
        transcation_accepted = self.pending_transactions
        self.pending_transactions = []
    block.transactions = transcation_accepted
```

# 挖掘新區塊

接著我們就可以來挖掘產生新區塊了，挖掘的步驟是透過改變`nonce`值(從0,1,2,3....直到找到符合的`nonce`)而得到新的哈希數，在這裡我們把難度定義為"開頭有幾個0"，也就是每次改變`nonce`、產生一個新的`hash`數後來確認有沒有符合要求(開頭有幾個0)，如果符合就代表我們找到一個合規`nonce`值了！但如果沒有，就只好持續的往下找了。也因為運算量越大能夠找到合規的`nonce`值的機率也越大，也因此這個方法又被稱為`Proof of Work(POW)`。

![Mine](https://www.lkm543.site/it_iron_man/day3_4.jpg)

但透過這個方式區塊的產生時間會非常地不穩定，你可以到[bitcoin的區塊瀏覽器](https://www.blockchain.com/explorer)看看產出的時間，bitcoin預設是每十分鐘應該要產出一個區塊，但也可以發現實際上每個區塊的產生時間會跟十分鐘有點落差，這是POW的必然結果。

在這裡的實作中，我們生成一個區塊後不停計算不一樣的`nonce`值，直到我們能夠找到合規的`nonce`為止，直到發現(挖掘)合規的`nonce`之後，就可以把挖出來的區塊置入鏈裡頭。

```python
def mine_block(self, miner):
    start = time.process_time()

    last_block = self.chain[-1]
    new_block = Block(last_block.hash, self.difficulty, miner, self.miner_rewards)

    self.add_transaction_to_block(new_block)
    new_block.previous_hash = last_block.hash
    new_block.difficulty = self.difficulty
    new_block.hash = self.get_hash(new_block, new_block.nonce)

    while new_block.hash[0: self.difficulty] != '0' * self.difficulty:
        new_block.nonce += 1
        new_block.hash = self.get_hash(new_block, new_block.nonce)

    time_consumed = round(time.process_time() - start, 5)
    print(f"Hash found: {new_block.hash} @ difficulty {self.difficulty}, time cost: {time_consumed}s")
    self.chain.append(new_block)
```

# 今天的問題

問題來了：如果參與挖掘的人越來越多，那麼區塊不是一下就會被挖掘出來了嗎？是的，所以明天我們會來談談怎麼根據實際情形改變挖掘的難度！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，至於程式碼則放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day03.py)。

# Ref
- [維基百科-雜湊函式](https://zh.wikipedia.org/wiki/%E6%95%A3%E5%88%97%E5%87%BD%E6%95%B8)
- [資訊與網路安全概論-粘添壽](https://www.tsnien.idv.tw/Security_WebBook/%E7%AC%AC%E5%9B%9B%E7%AB%A0%20%E9%9B%9C%E6%B9%8A%E8%88%87%E4%BA%82%E6%95%B8%E6%BC%94%E7%AE%97%E6%B3%95.html)
- [區塊鏈原理最清晰最直觀的解釋](https://bigdatafinance.tw/index.php/finance/fintech/465-2017-10-07-15-08-09)
