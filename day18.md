# 礦工間的戰爭

挖礦是有利潤的，但也因為區塊鏈的出塊與獎勵是固定的，挖礦對於所有參與的礦工是一場[零和遊戲](https://zh.wikipedia.org/wiki/%E9%9B%B6%E5%92%8C%E5%8D%9A%E5%BC%88)。為了增加自己的收益，方法大致可以分為提高獲利、壓低成本兩種方式，下面就幾種常見增加收益的方法做個簡單說明(~~屏除違法的偷接電~~)。

## 壓低成本(電費)

電費的成本可以佔到總成本的30-60%不等(視硬體價格而定，目前因為幣價相對低點，因此硬體價格與折舊費用低廉，電費可以佔到總成本的60%左右)，並且因為挖礦所需的消費型3C硬體的價格往下談的空間不大，壓低成本的方式最常從電費下手。

### 硬體調校

透過軟體與參數的調校可以稍微減少供耗，以Ethereum的Dagger-Hashimoto演算法為例，它需要記憶體的頻寬，但對於核心的計算能力反而不太要求，但核心往往是整張GPU中最耗電的部分，因此我們可以透過降低核心電壓頻率、拉高記憶體頻率的方式來達到提高算力的同時也減少供耗的效果。

### 契約用電與時間電價

除了調校GPU的參數外，也可以向[台電](http://taipowerdsm.taipower.com.tw/)申請時間電價(補充個小知識：台灣並沒有工業用電這種東西，只有契約用電！)或契約用電，透過在離峰時間才啟動挖礦程式可以讓每度電的電費壓在1.8元以下。而契約用電的成本則落在2.5-2.8元左右/度，比起家用最高級距動輒5、6元便宜許多。但申請前要注意台電的時間電價與契約電都有綁約一年的限制，而且契約電每月需要根據簽訂的容量繳交相對應的基本費(即便你一度電都沒用也得繳)，所以契約電對於專業礦場較為適合、家用時間電價對於散戶較為友善。

![時間電價](http://taipowerdsm.taipower.com.tw/images/form_01.png)
圖片來源：[台電](http://taipowerdsm.taipower.com.tw/)

## 增加挖礦期望值

如果對區塊鏈或礦池的運作夠熟悉，也可以透過區塊廣播或打包的眉眉角角來獲取更大的利益。這裡要另外說明，因為挖礦對所有礦工而言是一個零和遊戲，在增加自己獲利的同時也會損害到其他人的利益，因此某些為了使自己的利益最大化的方式往往被認為是不道德的。

### 挖空塊

其中一個礦池的作弊方式便是`挖空塊`，還記得我們在之前寫的簡易區塊鏈中是這樣處理接收到的區塊的：

```python
def receive_broadcast_block(self, block_data):
    last_block = self.chain[-1]
    # Check the hash of received block
    if block_data.previous_hash != last_block.hash:
        print("[**] Received block error: Previous hash not matched!")
        return False
    elif block_data.difficulty != self.difficulty:
        print("[**] Received block error: Difficulty not matched!")
        return False
    elif block_data.hash != self.get_hash(block_data, block_data.nonce):
        print(block_data.hash)
        print("[**] Received block error: Hash calculation not matched!")
        return False
    else:
        if block_data.hash[0: self.difficulty] == '0' * self.difficulty:
            for transaction in block_data.transactions:
                self.pending_transaction.remove(transaction)
            self.receive_verified_block = True
            self.chain.append(block_data)
            return True
        else:
            print(f"[**] Received block error: Hash not matched by diff!")
            return False
```

大抵而言可以把步驟簡化成：

1. 確認該區塊的哈希數是否符合當下難度的規範
2. 如果符合就把該區塊內的交易(`pending_transaction`)自等待中的交易內移除
3. 結束目前的挖礦
4. 把新的交易放置入新的區塊中
5. 開始挖掘新區塊

但在步驟進行過程中，礦池的算力是停擺的，但是礦機卻仍然在持續運行著。因此有些礦池會為了節省時間與能源，在尚未接收到整個區塊的廣播時就直接開始挖掘下一塊，但也因為如此礦池根本不知道這區塊內有哪些交易，也因此無法確認哪些等待中的交易(`pending_transaction`)是已經被打包進去/交易過的，所以在下一區塊的挖掘中礦池無法加入任何交易紀錄，所以即便礦池真的挖掘出新區塊，裏頭也沒有任何交易，俗稱空區塊，他們接收到廣播的區塊後的方式如下。

1. 確認該區塊的哈希數是否符合當下難度的規範
2. 不置入任何交易就開始挖掘新區塊

因為少了確認交易內容、打包新交易的過程，所以挖空塊能夠比正常挖礦者更快進入nonce值的計算階段，但此時的區塊卻沒有辦法驗證任何人的交易。所以有些人會覺得礦池為了自身利益不打包其他人的交易實在是母湯的行為。更多挖空塊的細節可以參考[這裡](https://zhuanlan.zhihu.com/p/46372884)。

### 跳跳池

在講跳跳池前就必須先談礦池的運作與分潤方式：可以把礦池想像成接受到難題後，就把該難題拆解成許多小難題分派給參與的礦工，每當礦工解決完一個小難題後便回傳給礦池，此時稱為一個`share`，主流幾種礦池在出塊後與礦工們的分潤方式：

#### RBPPS(Round Base Pay Per Share)

RBPPS是當礦池挖掘到新區塊後，就立刻把新區塊的收益根據這段時間的大家的`share`數目來分派收益，因此礦工本身也承擔了風險，如果多出塊，礦工就多賺；沒出塊，礦工就會虧錢。

#### PPS(Pay Per Share)

PPS的方式是不論礦池出塊與否，礦池都會根據礦工所解決的`share`數目給礦工應當的收益，因此出塊與否的風險是由礦池承擔的，如果礦池運氣好多出幾塊礦池就會大賺，但如果運氣不好就會大虧了。

#### PPLNS(Pay Per Last N Share)

PPLNS是只根據礦池出塊後過去的N個`share`數目給礦工應當的收益，至於為什麼會這樣設計是為了避免跳跳池的礦工(以下說明))。

#### 跳跳池

了解跳跳池的原理前先來了解一個值：`幸運值`。根據礦池持有的算力佔全網算力的比例可以算出預期的出塊時間，比方說Ethereum大約每15秒會出一塊，如果礦池持有總算力的1%，則平均下來大概每25分鐘可以出一塊，計算方式如下：

> 出塊時間15秒/持有算力1% = 預期出塊時間1500秒 = 25分鐘

幸運值的意思是現在的挖掘時間是預期出塊時間的多少百分比，也就是說長時間平均下來，大約幸運值累積到100%就能夠出一塊，如果幸運值小於100%時就挖到區塊，代表礦池的運氣很好，礦工們的收益會高於預估；但如果幸運值大於100%才出塊，代表礦池的運氣不好，得花費比期望值高的算力才能夠出塊。

> 幸運值 = 已挖掘區塊時間/預期出塊時間 * 100%

在[臺灣乙太幣礦池](http://tweth.tw/)中的幸運值就在預期出塊那裏(下圖)，也可以透過使用者介面發現臺灣乙太幣礦池是修改我們幾天前介紹的[Open source礦池程式碼](https://github.com/sammy007/open-ethereum-pool)而來。

![Lucky](https://www.lkm543.site/it_iron_man/day20_1.JPG)

而跳跳池的做法就是：當幸運值小於100%時進入RBPPS的礦池，等到幸運值大於100%的時候就轉出到其他礦池以獲取更大的收益。乍聽之下好像很不合理，畢竟挖礦的時間不是都一樣嗎？為什麼跳來跳去能夠取得較大的收益？

要理解這個原因可以從期望值的問題下手：**每留在礦池中的固定一段時間能夠獲得多少收益？**

因為每段時間的出塊機率是固定的，當礦池的幸運值為X%時，如果挖出區塊，便需要跟前面X%所累積出來的`share`數目均分出塊收益，因此留在礦池繼續挖一段時間的收益期望值便是`PPS收益/X`。

由此可見，當X小於100%時，留在RBPPS的礦池的收益會大於PPS池，但當X大於100%時，留在RBPPS的礦池的收益就會小於PPS池，所以當幸運值小於100%時進入RBPPS礦池、當幸運值大於100%時退出RBPPS礦池便能夠獲取更高的收益。為了避免這種情形才會衍伸出第三種PPLNS的礦池分潤：只根據前面N個share進行分潤，若礦工中途退出，則之前的收益全數歸零。

這裡我們可以做一個小實驗，假設有兩人持有同樣算力，其中一人老實地挖完全程，另一人只挖到幸運值100%後就轉去PPS池(這裡我們都以1%為單位，每經過1%幸運值就會有1%機率挖到)：

1. 對於始終留在同一個RBPPS、而且沒有礦工提前跳走的的礦池而言，礦工的收益跟預期差不多。

    ```python
    pool_reward = 0
    try_times = 10000
    mine_time = 0

    # RBPPS Miner
    for i in range(try_times):
        luck = 1
        while(True):
            if random.randint(0,100) == 0:
                # Mine Block!
                pool_reward += 100
                mine_time += luck
                break
            luck += 1
    print(f"Expect RBPPS miner: {pool_reward/mine_time}")
    ```

    > Expect RBPPS miner: 0.9913583294422519

2. 但如果有礦工每到幸運值100%便跳去另外一個PPS池，即便在原本RBPPS池的收益會減少成`200*(100/(100+luck))`但同時也會增加PPS的收益`luck - 100`，另外因為礦工在幸運值100%後便離開，在幸運值100%之後的出塊機率也會變成1/2，因此要多篩一次`random.randint(0,1) == 0`：

    ```python
    miner_reward = 0
    pool_reward = 0
    mine_time = 0
    # RBPPS + PPS Miner and Pool
    for i in range(try_times):
        luck = 1
        while(True):
            if random.randint(0,100) == 0:
                # Mine Block!
                if luck < 100:
                    miner_reward += 100
                    pool_reward += 100
                    mine_time += luck
                    break
                else:
                    if random.randint(0,1) == 0:
                        miner_reward += 200*(100/(100+luck))
                        pool_reward += 200*(luck/(100+luck))
                        miner_reward += luck - 100
                        mine_time += luck
                        break
            luck += 1
    print(f"Expect RBPPS + PPS miner: {miner_reward/mine_time}")
    print(f"Expect RBPPS + PPS pool: {pool_reward/mine_time}")
    ```

> Expect RBPPS + PPS miner: 1.1591529571485477
> Expect RBPPS + PPS pool: 0.8354135084376128

可以發現採用跳跳池的礦工可以高出近20%的收益，而留在原池的礦工則會減少近20%的收益，兩者一來一往就差了將近40%！

## 扣塊攻擊

另一種礦池間的攻擊手法就是利用PPS的漏洞：動用手下的算力去幫別人礦池挖礦，但只發送沒挖掘成功的share，一但確認自己挖到正確的share之後卻不廣播給礦池，所以送出的share都是無效的！但因為PPS分潤制的關係，導致礦池仍然要配發無效share的收益給該名礦工，長期下來礦池配發的收益會與挖掘到的收益不合比例，而導致PPS制礦池的倒閉。

既然有這麼明顯的漏洞，為什麼還是有礦池使用PPS制呢？因為當礦池規模小時，為了吸引礦工們前來礦池只能使用PPS制(出塊機率太低、預期出塊時間太長，礦工沒有耐心等待)來固定配發收益給前來的礦工們。

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，至於今天模擬跳跳池收益的程式碼則放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day20.py)。

# Ref:
- [打压对手，让其他矿池倒闭，神鱼所说的扣块攻击究竟是什么？](https://www.chainnews.com/articles/806780761278.htm)
- [淺談礦池挖礦機制 (Pooled Mining)](https://justhodl.blogspot.com/2018/04/pooled-mining.html)
- [加密貨幣與他們的產地](https://medium.com/taipei-ethereum-meetup/%E5%8A%A0%E5%AF%86%E8%B2%A8%E5%B9%A3%E8%88%87%E4%BB%96%E5%80%91%E7%9A%84%E7%94%A2%E5%9C%B0-21a52c51427f)
- [POW 矿池挖空块原理和解决方案](https://www.chainnews.com/articles/210557815167.htm)
- [神鱼发怒，揭露矿圈“扣块攻击”，矿池江湖暗流涌动](https://www.chainnews.com/articles/445562632637.htm)
- [科普入门 | 空块是什么？为什么矿工要挖空块？](https://m.mifengcha.com/news/5bbd7a3a22285b8f5a903bb5)
