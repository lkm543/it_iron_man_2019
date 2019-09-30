# Merkle Tree

![Merkle Tree](https://www.lkm543.site/it_iron_man/day14_1.PNG)

我們在密碼學的開頭已經講解過哈希(湊雜)的原理以及應用，而今天要談到的`Merkle Tree`其實是演算法裏頭的一種二元樹，透過兩兩計算哈希值的方法來驗證資料的正確性跟完整性。以上圖為例，上面的Merkle Tree最底層可以看做是Bitcoin的每一筆交易，每一筆交易可以分別計算出哈希值，接著在兩兩一對分別計算兩哈希值的哈希值，直到最後只剩下一個哈希值hash(ABCD)，這時候我們稱它為`Merkle Root`。

## 為什麼不直接連接(concatenation)所有交易再Hash就好？

我們在之前的實作區塊鏈中，定義了我們的哈希值是由四種不同的狀態透過哈希函式sha-1計算而得(其實sha-1已經被破譯了，實務上盡量避免用sha-1)：

1. 前一個區塊的哈希值
2. 區塊最初的時間
3. 把所有的交易訊息連接成一個字串
4. nonce值(複習一下：礦工在找的就是這個nonce值)

```python
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

這是很簡單也很容易理解的算法：只要這個區塊中的任何一個交易被修改過，由交易紀錄連接起來的字串會跟著改變，那麼最後算出來的哈希值也必定會發生改變，從而讓我們得知裏頭的資料並不可信。

但如果我們的確這樣做的話，我們會如何驗證一筆交易是否真的存在呢？這時候只能照著自己設計的演算法需求把該區塊的所有交易通通都收集起來，然後再連接、再跟其他參數計算Hash看有沒有吻合，也就是說**為了驗證一筆交易，必須把同一區塊內的所有交易紀錄都下載下來**。

## Merkle Tree如何驗證交易

![Merkle Tree Verify](https://www.lkm543.site/it_iron_man/day14_2.png)

但有了Merkle Tree就不一樣了，以上圖為例，假設我們想要確認Tx D是否存在這個區塊中，那我們只需要下載這個區塊的Hash(C)、Hash(AB)、跟Hash(ABCD)三個值(順待一提，這裡的Hash(ABCD)就是這個區塊的Merkle Root)，驗證的方法就是：

1. 計算Tx D的哈希值Hash(D)
2. 計算Hash(D)與Hash(C)的哈希值Hash(CD)
3. 計算Hash(AB)與Hash(CD)的哈希值Hash(ABCD)
4. 確認我們計算出來的Hah(ABCD)跟區塊裡的Merkle Root或Hash(ABCD)有沒有一致
5. 一致→該筆交易的確存在這個區塊，不一致→該筆交易不存在於這個區塊

以bitcoin而言，實際上一個區塊平均會有3-500筆交易在裏頭(可以參考[這裡](https://www.quora.com/How-many-transactions-are-included-in-a-block-chain))，為了方便計算我們假定這個區塊中有512筆交易。也就是最下面代表交易的交易node有512個點、再上一層有256個點、再上一層有128個點....，那麼透過Merkle Tree，我們只需要取得Merkle Root跟另外8個Hash值便可以驗證該筆交易是否為真。

`512筆交易 vs 8個Hash`，需要的資料整整少了64倍(因為交易的大小會大於Hash大小，實際上會節省更多空間)，這就是Merkle Tree的威力！

## Second preimage attack

但有沒有可能即便算出來的Merkle Root是一致的，但裏頭的Transaction不一樣呢？當然有可能，如果你有印象之前提到的生日碰撞，該問題是：給定一哈希值H，要找出經過哈希函數轉後後也是H的任一明文；而這裡的問題有點小小的不同：給定明文(在這裡是交易)M1後，要找出另一個明文M2跟M1在特定的哈希函數下擁有相同的哈希值，白話文就是我要找到另外一個交易紀錄同樣經過哈希函數後可以吻合Merkle Root的話，我就可以騙過整個驗證系統，這就是密碼學上所稱的`Second preimage attack`。

不過這個機率很小很小，小到幾乎可以忽略，因為Bitcoin使用的是SHA-256加密法，也就是說每次新產生的交易M2跟欲攻擊的交易M1有相通Hash值的機率只有2^-256次方。

## Bitcoin中的Merkle Tree

下圖是應用在Bitcoin上的Merkle Tree，最底層是每一筆交易，透過計算每筆交易的哈希值後再兩兩運算可以得到Merkle Tree供以後驗證之用，大抵上的過程跟我們上頭講解的是一樣的(~~因為原本就是用Bitcoin來舉例~~)

![Bitcoin](https://en.bitcoinwiki.org/upload/en/images/thumb/9/95/Hash_Tree.svg/500px-Hash_Tree.svg.png)

圖片來源：[BitcoinWiki](https://en.bitcoinwiki.org/wiki/Main_Page)

建立好Merkle Tree後就可以大幅減少驗證交易所需要的資訊量，也因此Bitcoin提供了兩種節點`Full node`與`SPV(Simplified Payment Verification) node`：

### Full Node

Full Node的話很好理解，就是儲存了自創世塊以來的所有交易，如果你想要開一個Full Node的話，[Bitcoin org](https://bitcoin.org/en/full-node#special-cases)有建議的硬體規格如下：

- 200 GB的儲存空間，另外讀寫速度都要在100MB/s以上.
- 2GB以上的記憶體
- 上傳速度400 Kbps的網路

可以發現最難的還是卡在Full Node為了儲存所有交易紀錄所需要的空間(建議200GB)，這對筆記型電腦或個人PC來說或許不難，可是對手機等行動裝置來說就有點太大了，不然你可以看[iPhone在各個容量上的價錢](https://www.apple.com/tw/shop/buy-iphone/iphone-11-pro).....

### SPV(Simplified Payment Verification) Node

但有了Merkle Tree的協助，行動端的裝置可以只安裝SPV Node，裏頭只有每個Block的Header(約80個Bytes)，一但有檢查交易紀錄是否存在於某個區塊中，就去訪問Full Node並且索取該區塊的Merkle Tree以供驗證，這個方法又稱之為`Merkle Path Proof`。

下面是中本聰在[白皮書](https://bitcoin.org/bitcoin.pdf)中所留的一段話

> A block header with no transactions would be about 80 bytes. If we suppose blocks are generated every 10 minutes, 80 bytes * 6 * 24 * 365 = 4.2MB per year. With computer systems typically selling with 2GB of RAM as of 2008, and Moore's Law predicting current growth of 1.2GB per year, storage should not be a problem even if the block headers must be kept in memory.

簡單翻譯就是：並非所有裝置都有足夠的資源當full node，但如果某些輕型裝置只有驗證或發送交易需求的話，那麼它並不需要儲存自創世塊以來的全部區塊的交易資料，只需要儲存每Block的標頭，這樣即使一年過去了，你的手機也只會增加4.2MB的資料！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。
# Ref:
- [Merkle Tree（默克爾樹）演算法解析](https://www.itread01.com/content/1544187062.html)
- [維基百科-哈希樹](https://zh.wikipedia.org/zh-tw/%E5%93%88%E5%B8%8C%E6%A0%91)
- [Wikipedia-Merkle Tree](https://en.bitcoinwiki.org/wiki/Merkle_tree)
- [Why use Merkle Root (and not just concatonation of all hashes?](https://bitcoin.stackexchange.com/questions/76811/why-use-merkle-root-and-not-just-concatonation-of-all-hashes)
- [Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf)
- [What is the Merkle root?](https://bitcoin.stackexchange.com/questions/10479/what-is-the-merkle-root)
- [Full Node和SPV Node如何驗證Transaction？](https://countchu2.blogspot.com/2017/03/full-nodespv-nodetransaction.html)
- [Attacking Merkle Trees With a Second Preimage Attack](https://flawed.net.nz/2018/02/21/attacking-merkle-trees-with-a-second-preimage-attack)
