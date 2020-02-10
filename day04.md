昨天我們已經有能力產生出新區塊，但區塊的產生時間會根據運算力的多寡而浮動，因此今天我們要處理的第一件事便是根據現在運算力多寡調整挖礦的難度，除此之外我們在處理交易前也必須事先確認該帳戶的餘額是否足夠，最後是確認我們的區塊鏈是不是有被竄改過。

總結今天的三件事情：

1. 調整哈希難度
2. 計算帳戶餘額
3. 確認哈希值是否正確

# 調整哈希難度
由於每區塊裏頭都記錄著區塊被挖掘出的當下時間戳(`timestamp`)，因此我們可以知道每個區塊的產出時間(也就是找出符合的`nonce`所耗費的時間)，如果難度是固定的，那麼參與挖礦的運算力如果成長十倍，區塊的平均產出時間也會連帶變成十分之一，因此順應運算力的多寡而調整難度對區塊鏈的長久運行是很重要的。

那怎麼去評估區塊的產生時間呢？如果單純採用前一個區塊的產出時間很明顯的是不可行，因為`POW`的核心精神是利用隨機數去猜到可能可以符合的`nonce`，因此每一個區塊的產出時間會變動相當大：

![Block time diversity](https://www.lkm543.site/it_iron_man/day4_1.jpg)

根據上圖看到我們的區塊鏈在難度5的狀況下，連續十塊的出塊時間從0.47秒到39.44秒都有可能，昨天提到的[區塊鍊瀏覽器](https://www.blockchain.com/explorer)裏頭也可以發現出塊時間會不斷跳動，因此根據單個區塊的出塊時間決定難度是萬萬不可行的，取而代之的方法便是取多個區塊的出塊時間再取平均，有點像是訊號處理中的均值濾波器。

在這裡我們設定如果平均出塊時間小於設定的出塊時間，就把難度加1，如果平均出塊時間大於設定的出塊時間，就把難度減1。這裡難度的定義是挖到的`nonce`值必須要滿足讓Hash的頭幾個Bytes為0，因此難度每加1，實際上的運算量會增加16倍(位元組是兩兩16進位構成的)，也因為調整幅度太大，所以其實這裡設計的並不是很好的難度調整算法。


```python
def adjust_difficulty(self):
    if len(self.chain) % self.adjust_difficulty_blocks != 0:
        return self.difficulty
    elif len(self.chain) <= self.adjust_difficulty_blocks:
        return self.difficulty
    else:
        start = self.chain[-1*self.adjust_difficulty_blocks-1].timestamp
        finish = self.chain[-1].timestamp
        average_time_consumed = round((finish - start) / (self.adjust_difficulty_blocks), 2)
        if average_time_consumed > self.block_time:
            print(f"Average block time:{average_time_consumed}s. Lower the difficulty")
            self.difficulty -= 1
        else:
            print(f"Average block time:{average_time_consumed}s. High up the difficulty")
            self.difficulty += 1
```

實際上比特幣每過2016個區塊，會根據前面2016個區塊的平均出塊時間調整難度，如果前面2016個區塊的平均出塊時間大於十分鐘，代表現在的運算力過少、挖礦難度偏高使出塊時間變長，因此需要降低挖礦難度；反之如果這2016個區塊的平均出塊時間小於十分鐘，代表現在的運算力過多、挖礦難度偏低使出塊時間變短，因此需要提升挖礦難度。這2016個區塊所需的時間大概是：

![https://chart.googleapis.com/chart?cht=tx&chl=2016(Blocks)*10(Minutes%20per%20Block)%2F1440(Minutes%20per%20Day)%3D14(Days))](https://chart.googleapis.com/chart?cht=tx&chl=2016(Blocks)*10(Minutes%20per%20Block)%2F1440(Minutes%20per%20Day)%3D14(Days)))

也就是平均大約兩個禮拜Bitcoin會調整一次難度。你也可以在[這個網站](https://bitinfocharts.com/comparison/bitcoin-difficulty.html)上看到歷史Bitcoin/Ethereum的挖礦難度。如果真的點開那個網站，應該可以很快發現難度往往是不斷增加而很少下降的，造成難度不斷上漲的主要原因有兩點：

1. 幣價上漲導致更多人參與挖礦以獲取Bitcoin
2. 硬體效能的進步使運算能力飛速成長 

特別是第二點的硬體能力，BTC使用的`SHA-256`挖礦演算法目前已經被特殊應用積體電路（Application-specific integrated circuit，ASIC）所主宰，個人PC的硬體效能已經無力跟ASIC競爭。非但如此，ASIC的推陳出新也逐步刷新效能的上限，[這裡](https://en.bitcoin.it/wiki/Mining_hardware_comparison)可以看到各ASIC主要型號的運算力，從運算力中可以發現比特大陸的Antminer S1出到S9的過程中，運算力整整增加了快80倍(180,000Mh/s→14,000,000Mh/s)，如果難度保持不便，即使在機台數都沒有增加的狀況下，出塊的時間也會縮短成1/80，多麼可怕的數據。

關於挖礦相關的技術細節，我們在之後的挖礦實戰會細談這件事情。

# 計算帳戶餘額

除了難度調整，在發起交易當下也必須檢查匯款人的餘額是否足夠，同時也限制不能匯出超過自己帳戶的餘額，而帳戶餘額總共只有三種來源：

- 區塊獎勵：挖出區塊的礦工能得到區塊的獎勵
- 手續費收入：挖出區塊的礦工能得到該比區塊內所有交易的手續費
- 匯款收入：收到別人匯款的款項

因此我們寫一個簡單的函式，從第一個區塊的第一筆交易開始檢查，一路檢查到最後一筆後便可以得到該帳戶的餘額。

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

# 確認哈希值是否正確
為了避免我們的資料被竄改，也必須時常檢查資料的正確性。還記得我們每個區塊的哈希數都是環環相扣的吧?在昨天每個哈希數都由下面這四筆資料計算出來：

1. 前一個區塊的hash(`previous_hash`)
2. 區塊產生的時間戳
3. 所有的交易紀錄
4. `nonce`

所以檢查的方式就是從第一個區塊的哈希數一路算到最後一個，一旦中間開始的某個哈希數算完之後對不起來，那麼就代表其中的某筆交易紀錄被竄改過。

```python
def verify_blockchain(self):
    previous_hash = ''
    for idx,block in enumerate(self.chain):
        if self.get_hash(block, block.nonce) != block.hash:
            print("Error:Hash not matched!")
            return False
        elif previous_hash != block.previous_hash and idx:
            print("Error:Hash not matched to previous_hash")
            return False
        previous_hash = block.hash
    print("Hash correct!")
    return True
```

## 測試一下：

如果我們在其中一個區塊插入了一筆偽造的交易，那麼透過一連串哈希的確認與計算，我們便可以發現hash數是對不起來的！

```python
if __name__ == '__main__':
    block = BlockChain()
    block.create_genesis_block()
    block.mine_block('lkm543')

    block.verify_blockchain()
    
    print("Insert fake transaction.")
    fake_transaction = Transaction('test123', 'address', 100, 1, 'Test')    
    block.chain[1].transactions.append(fake_transaction)
    block.mine_block('lkm543')

    block.verify_blockchain()
```

![Fake Transaction](https://www.lkm543.site/it_iron_man/day4_2.jpg)

除此之外你也可以到[這裡](https://anders.com/blockchain/blockchain)玩玩看區塊鏈，一開始所有資料都是正確無誤的，所以會顯示綠色：

![Demo](https://www.lkm543.site/it_iron_man/day4_3.jpg)

一旦你在前面區塊中亂插入一些紀錄，你會發現從該區塊之後的所有哈希數通通被打亂了！像是在這裡我插入：
`"I am Bill Gates"`

![Demo](https://www.lkm543.site/it_iron_man/day4_4.jpg)

被更改的區塊後的所有區塊都必須從新被計算哈希數，否則會完全對不起來而被輕易發現資料被竄改過！當然可以選擇重新計算所有的哈希數，但當主鏈夠長時，重新計算所有的哈希數所需要的運算量與成本非常可怕，也因此保障了區塊鏈的不可竄改性。更何況在重新計算時，正常的塊也在不停的被一般的礦工產出，要跟所有的礦工競爭幾近天方夜譚。

# 今天的問題
但有個問題：我要怎麼知道發起交易的那方便是帳戶的持有者？如果不事先確認的話，代表任意路人都可以把別人的帳戶餘額領走，是萬萬不可的事情。那麼我們又要如何確認誰擁有這個帳號？誰有權力發起交易？

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，至於程式碼則放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day04.py)。

# Ref:
- [比特幣系統是如何調整挖礦難度的？](https://kknews.cc/zh-tw/tech/mpz4rjg.html)
- [Cryptocurrency Mining: Why Use FPGA for Mining? FPGA vs GPU vs ASIC Explained](https://medium.com/fpga-guide/cryptocurrency-mining-why-use-fpga-for-mining-fpga-vs-gpu-vs-asic-explained-5aaa400082b9)
