# 區塊鏈的架構
## Transaction
打造一個簡單的區塊鏈之前，先來了解區塊鏈的架構與裏頭具備哪些要點。就像我們平常習慣用的銀行轉帳一樣，每筆交易都會產生一筆交易明細，詳細記錄了這筆交易的發送人、接收者、金額、手續費與備註，交易明細的功能除了作為憑證外，同時在銀行端也可以拿來核對，也就是俗稱的"軋帳"，這裡的每一筆交易明細我們先稱之為Transaction。
![Transaction](http://www.lkm543.site/it_iron_man/day2_1.png)

## Blocks of transactions
所有的Transaction會根據時間順序被放置到一個個區塊(Block)內，就像是把銀行把每個工作日早上九點到下午三點半前的所有交易紀錄都存在同一天的帳本裡一樣，如此周而復始，當有新的區塊正在產出，新生成的所有交易紀錄都會被放置在該區塊之下。
![Blockchain](http://www.lkm543.site/it_iron_man/day2_2.png)

你可能會有疑問說為什麼要這樣設計？為什麼不把所有的交易紀錄通通放在同一個區塊就好？

一旦我們把所有的交易紀錄都存放在同一個區塊或陣列之中，那麼即便其中某一筆資料被竄改我們也無從得知，也無法確認是哪一筆交易/區塊遭到竄改。另一個好處是我們可以透過這種方式把交易區分成"已經被確認"(置入區塊內)與"等待中"(尚未致入區塊)，這樣使用者便可以得知自己的匯款是否已經完成。

也因為透過區塊的切割與依次加密，就好比是我們在區塊與區塊中加了獨立鎖鍊一般，一旦有人意圖不軌試圖竄改過去的資料，則他必須要付出的代價是：必須層層把鎖鍊解開，否則資料鍊就會從此斷開而輕易地被人抓包。

不過依次加密這其中牽涉到複雜的密碼學，因此在寫完一個簡易的區塊鏈後我們會進到下一個章節，也是區塊鏈不可或缺的個重點：密碼學。

## 今天的目標
1. 定義出交易格式
2. 定義出區塊格式
3. 建出區塊鍊的架構

### 交易格式

根據最上面我們談交易明細，一筆交易裏頭應該要有這些資訊：

1. 發送方(sender)：誰發起這筆交易的？同時也要確認是發送方底下餘額否足夠
2. 收款方(receiver)：誰接收這筆交易的款項？
3. 金額大小(amounts)：這筆交易的數目
4. 手續費(fee)：支付的手續費多寡
5. 訊息(message)：就像是轉帳的備註一般，可以留下資訊，通常是給收款方看
```python
class Transaction:
    def __init__(self, sender, receiver, amounts, fee, message):
        self.sender = sender
        self.receiver = receiver
        self.amounts = amounts
        self.fee = fee
        self.message = message
```

### 區塊格式

每一個區塊包含了許多筆交易(Transaction)，就像是帳本的內頁儲存了許多交易紀錄，值得一提的是這裡為了加密的需求會記錄前後一個區塊的哈希(hash)值，也就是每一塊之間的哈希值是環環相扣的，也可以把哈希值看做是每個區塊上的鎖頭，而礦工挖掘出的nonce則代表了能夠匹配這個鎖頭的鑰匙(或另一把鎖)，而且下一個區塊的哈希值又根據這個Nonce值而產生，如此一來只要其中任何一個交易紀錄、區塊被竄改，則整個鍊上的nonce跟hash都需要修正，並且需要在新的區塊產生前計算/修正完畢，這需要擁有異常龐大的計算量，也因此竄改區塊鏈是幾近不可能的事情。

![Hash and Nonce](http://www.lkm543.site/it_iron_man/day2_3.png)

至於甚麼是hash、區塊間如何加密的細節我們之後會再來探討。

所以

1. 前個區塊的哈希值(previous_hash)：為了加密需要我們會使用到前一個區塊的哈希值
2. 這個區塊的哈希值(hash)：這個區塊計算後的哈希值
3. nonce：礦工找到能夠解開鎖的鑰匙
4. 當前難度(difficulty)：指挖出這個區塊時所使用的困難度，之後會再詳述
5. 該區塊產生時的時間戳(timestamp)：紀錄了這是該區塊是在何時產生，之後調整挖礦難度會使用到
6. 交易紀錄(transactions)：紀錄了這個區塊中所有的交易紀錄
7. 挖掘礦工(miner)：紀錄了這個區塊中是由誰挖掘出來的
8. 礦工獎勵(miner_rewards)：紀錄了這個區塊中所有給礦工的獎勵

```python
class Block:
    def __init__(self, previous_hash, difficulty, miner, miner_rewards):
        self.previous_hash = previous_hash
        self.hash = ''
        self.difficulty = difficulty
        self.nonce = 0
        self.timestamp = int(time.time())
        self.transactions = []
        self.miner = miner
        self.miner_rewards = miner_rewards
```

### 區塊鏈架構

1. 難度調節區塊數(adjust_difficulty_blocks)：每多少個區塊調節一次難度
2. 目前難度(difficulty)：希望每個區塊的產出時間盡量保持一致，也因此隨著挖掘Nonce的機器數目與效能變動，挖掘難度也必須隨之調整以讓產出時間維持在動態平衡上，這個欄位代表了區塊鏈當下的難度
3. 出塊時間(block_time)：理想上多久能夠出一個區塊，當實際出塊時間塊於設定的理想值時，代表運算效能優於實際需要，因此必須將難度做相對應的提升，以維持出塊時間的動態平衡，反之亦然，詳情在之後的教學中會有進一步的說明。
4. 挖礦獎勵(miner_rewards)：獎勵挖礦者的金額多寡，挖出新區塊的礦工可以得到獎勵，藉此鼓勵礦工參與區塊鏈營運
5. 區塊容量(block_limitation)：每一個區塊能夠容納的交易上限，上限的存在是因為當礦工挖掘出新的Nonce時，他需要把所有被接受的交易連同區塊資料一併廣播給其他人知悉，因此如果容量過大會導致傳播過慢或是讓礦工需要的網速增加到不符合經濟效益的地步。
6. 區塊鏈(chain)：目前區塊鏈中儲存的所有區塊
7. 等待中的交易(pending_pranscations)：當使用者發送交易時，因為區塊鏈能夠吞吐的交易量有限，交易會先處在pending的狀況，當交易量過大時，礦工會首先選擇手續費高的交易先處理。

```python
class BlockChain:
    def __init__(self):
        self.adjust_difficulty_blocks = 10
        self.difficulty = 1
        self.block_time = 30
        self.mining_rewards = 10
        self.block_limitation = 32
        self.chain = []
        self.pending_transactions = []
```

今天先到此為止，明天我們再來研究怎麼樣讓區塊能夠被挖掘！

到目前為止的文章都會放置到[Github](https://github.com/lkm543/it_iron_man_2019)上，程式碼可則以參考[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day02.py)。
