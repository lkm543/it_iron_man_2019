# Bitcoin的發展

自中本聰在2009年1月正式推出Bitcoin以來，為了擴展交易速度或增加實用性，也經歷了不少次的版本升級，今天我們便來介紹其中三個較為人知也影響較大的發展項目：多重簽名、隔離驗證、閃電網路。

# 多重簽名

我們在之前談到非對稱加密時有提到非對稱加密會產生一對公私鑰，透過私鑰簽署、公鑰驗證的過程我們便可以讓礦工驗證這筆交易的確是由我們發出的。但是這種交易方式完全仰賴於單一金鑰，如果持有金鑰的人是單一行為人，那麼對於公司或企業的資產保障都是不足的，因此多重簽名的功能便是讓資產的動用必須經過多重的核可才能夠進行。

## 多重簽名的原理

在[BIP11](https://github.com/bitcoin/bips/blob/master/bip-0011.mediawiki)中，是這樣介紹多重簽名的：

> This BIP proposes M-of-N-signatures required transactions as a new 'standard' transaction type.

這裡的N代表所有的公鑰數目，M代表的是要取得其中多少公鑰的驗證後才能准許這筆交易，也就是當同意這筆交易的公鑰數目≧當初所設定的公鑰門檻M時，該交易才會被執行，舉例來說如果公司的董事會有八人，必須取得過半數(五人)才能夠移動資產的話，這時候的交易便是5-of-8-signatures。

## Pay to Multi Signature(P2MS)

`Pay to Multi Signature(P2MS)`顧名思義就是開立一張必需有多人簽名才能動用的支票(UTXO)，在這裡如果我們想要開立一張總人數為n，而且至少要取得其中m個簽名才能動支的UTXO我們可以這樣實作，：

```shell
m {pubkey_1} {pubkey_2}...{pubkey_n} n OP_CHECKMULTISIG
```

如果要動支這筆UTXO，只需要取得這n個公鑰背後的私鑰簽章即可動支這筆UTXO！

```shell
OP_0 {signature_1} {signature_2}
```

順帶一提，目前n個公鑰的上限為15個喔！

## Pay to Script Hash(P2SH)

但P2MS有一個重大缺陷就是付款方必須使用特別的交易格式或軟體，同時付款的交易非常的冗長，比方說如果客戶要付款給公司帳戶，而公司帳戶的動支規定為八個董事中超過五個同意才能動支的話，這筆交易的付款方式對客戶而言就是：

```shell
5
1FAnKjxL3u1skWqwZaJnPpHe6hCL89Dgr3 19rpuEq7vviLu4S4vUVHqKhB16ws7dx23W
15BSBGRBh7WFsz4RESK6EXhtRZAPDkRPtY 19EWhNncVwGn4Bg1nS6pHL5XY4xSzanDHG
1DxXFUr79TJD7Vth4rRVa7S1uLqCmvbGYb 1JbMgzWWPY4eG1m6b5a6ZSJwf5a4dnZB4m
15cJgaTYikDChKUL6feNQjY5KjawwLJF4f 15TG8KCtqeu5qEj6Bp6L1BpJK1MTZ59UCi
14sCN3g5YqLds9mGUa3GtkoSvgW4mNSLwc 1NsshQhjptKTJy8gRVJP2ZV6nVz8LuDh6o 
8 OP_CHECKMULTISIG
```

不只如此，當這筆交易送上鏈去給礦工驗證時也會佔去相對應的空間，因此在[BIP13](https://github.com/bitcoin/bips/blob/master/bip-0013.mediawiki)中所描述的`Pay to Script Hash(P2SH)`便應運而生，它把其中的P2MS的指令(script)編碼成20Bytes的大小，像是編碼成3aaaf9a2c06124ad1bf433ba9b2f78634b81e77b，這樣付款方就可以直接把多重簽名的付款當作是一般的付款來執行了！

除此之外因為經過P2SH的編碼開頭都是3，所以如果你看到3開頭的地址就可以知道這是P2SH的地址了！實際上你到交易所或是[Bitmex大賭場](https://www.bitmex.com/)上的入金地址大部分都是3開頭的便是這個原因。

```shell
OP_HASH160 3aaaf9a2c06124ad1bf433ba9b2f78634b81e77b OP_EQUAL
```

這樣對於付款方而言不就簡單多了嗎？除此之外對於減少區塊鏈上的工作與儲存量也會大有幫助！

# 隔離驗證(Segregated Witness，Segwit)

`隔離驗證(Segregated Witness，Segwit)`提供了一種方案把交易時鏈上所需要占用的空間減少，總地來說它只會降低交易所需的費用，對於區塊鏈整體的架構或共識並沒有很大的更動，因此也屬於軟分岔的一種。

在[Blockstream](https://blockstream.info)裏頭如果點開任何一筆交易便可以看到下面這段文字：

![Segwit@blockstream](https://www.lkm543.site/it_iron_man/day27_1.JPG)

圖片擷取自: [Blockstream](https://blockstream.info)

意即Segwit大約可以為每筆交易節省約1/3的手續費費用，節省手續費費用也代表所需佔用的鏈上空間減少，單一區塊內能夠容納更多的交易，讓Bitcoin有更高的TPS(Transaction per Second)。那麼Segwit是如何在不變動區塊大小的情形下做到這件事情的呢？

在最初始的Bitcoin中，每一筆交易都會搭配由公鑰持有人簽章的數位簽章，而Segwit則是把數位簽章移到區塊的最末端(下圖)，這些數位簽章可以稱為`Witness Data`，也因為把這些Witness Data隔離出來所以才稱這種方式為`Segregated Witness`。

![Segwit](https://i1.wp.com/ethereumworldnews.com/wp-content/uploads/2019/05/segwit-coin-explained-1024x506.png)

圖片來源：[ethereumworldnews](https://ethereumworldnews.com/bitcoin-core-0-18-0-bets-on-segwit-adoption-and-hints-at-offline-tx-signing/)

一旦礦工在計算1MB的區塊大小時不計入Witness Data的大小，只存放交易的紀錄，那麼同一區塊內能夠存放的交易數目就變多了！但Witness Data的大小也必須被限制，因此出現另外一個詞叫做`Block weight`，對於Block weight的容量計算與限制是這樣的：

> Block weight = 去掉Witness Data的交易空間大小\*3 + 交易空間大小 ≦ 4MB

因此對於一個沒有使用隔離見證的區塊而言，Block weight的上限大約就是原本區塊容量1MB的四倍=4MB，但如果裏頭含有隔離見證的資料，那麼Block weight的大小上限就會小於4MB。

與原本的區塊容量比較，在完全沒有隔離驗證的情形下會變成下面：

> 4\*交易空間大小 ≦ 4MB

也就是說即便你尚未完成Segwit的升級，那麼也不會影響原本區塊大小的限制(1MB)，所以Segwit為軟分岔。

至於實際上的交易容量中大約2/3的大小都被拿來用作儲存Witness Data之用，把2/3這個數據套入上面的公式可以得到：

> Block weight = 1/3\*交易空間大小\*3 + 交易空間大小 = 2\*交易空間大小 ≦ 4MB

> 交易空間大小 ≦ 2MB

> 區塊大小 = 1/3\*交易空間大小 ≦ 1MB

也就是說如果交易全部採用隔離見證方式的話，大約相較傳統方式可以提升區塊兩倍的交易量，同時也可以符合原先區塊容量1MB的限制！。

## 為什麼不直接加大區塊

既然隔離見證可以提升區塊兩倍的交易量，那麼為什麼不直接提升區塊容量的限制到2MB就好？答案是可以的，只是路線的方法不同，然後支持直接擴容到2MB方案的派系輸了......

反對擴容方的意見則是認為目前Visa的交易吞吐量約為1700 TPS([來源](https://hackernoon.com/the-blockchain-scalability-problem-the-race-for-visa-like-transaction-speed-5cce48f9d44))，如果要把目前Bitcoin大約7 TPS擴充到跟VISA類似規模的話需要讓區塊大小達到200-300MB之多，對於儲存或許不是困難，這在網路廣播區塊時會非常遲緩，因為挖礦的算力必須基於新區塊才能被視為有效算力，假設目前傳遞1MB區塊的資料到全網平均需要1秒，那傳遞250MB的區塊大小大約平均需要4分鐘，但在平均出塊時間只有10分鐘的情形下，大約40%的算力會被視為無效算力間接導致區塊鏈的安全風險，也因如此他們認為區塊大小不能無限制的膨脹，遲早得走其他的路。

# 閃電網路(Lightning Network)

因為區塊鏈本身的特性，把交易上鏈的成本非常高、耗時也長，如果要把全部交易上鏈那麼勢必無法完成即時或是手續費低的要求，因此閃電網路提供的解決方案就是鏈下擴容─把微小的支付交易都移到鏈下，等到要結算時再統一上鏈，另外推行隔離驗證的其中一個目的是為了之後的閃電網路鋪路。

閃電網路的概念就是如果是小額、頻繁地消費的話那麼這些瑣碎的交易並不會送到鏈上，而是先到鏈上去開閃電支付的通道，接著到鏈下去把簽署過的交易資訊給對方，等到想要結算時在把所有交易都上鏈。

比方說你每天都會到家裡巷口的超商買東西，那麼為了避免每次小額支付都必須要支付高額的手續費與等待交易上鏈，那麼你可以跟便利超商開出一個鏈下支付通道，每次支付就相當於發出一個交易並簽發一個數位簽章給對方，等到想結算時再一起把這段時間所有的交易結果上鏈。

除此之外閃電網路還可以支援間接傳遞，比方說A<->B、B<->C之間各有一個閃電支付的通道，那麼即便A與C之間沒有任何通道，但A仍然可以透過抵押BTC的方式要求B利用自身的通道轉給C，也就是說只要你與別人建立了支付通道，那麼就可以如同網路一樣連結到對方所有可用的支付通道，而這些都是不需要支付任何手續費的！所以只要支付通道越多，閃電網路的威力與便利性就會進一步增強。

![Lightning Network_ABC](https://www.lkm543.site/it_iron_man/day27_2.jpg)

圖片擷取自: [Lightning Network Visualizer](https://graph.lndexplorer.com/)

你可以到[Lightning Network Visualizer](https://graph.lndexplorer.com/)這個網站上看目前閃電網路的圖形化介面，只要你與上頭的任何一個節點開啟支付通道，那麼你便可以與節點上連接的所有閃電網路進行無延遲、無手續費的交易！

![Lightning Network](https://www.lkm543.site/it_iron_man/day27_3.JPG)

圖片擷取自: [Lightning Network Visualizer](https://graph.lndexplorer.com/)

在[這裡](https://1ml.com/)你也可以看到閃電網路的支付通道數目，其中又以美國居多。

但閃電網路也有其缺點，為了確保所有人有足夠的資金進行最後的結算，在開啟閃電通道的同時你必須抵押相對應的資產(BTC)才能進行後續的交易，比方說你抵押了3BTC在通道的開啟上，那麼這3BTC在結算前都會被鎖死，而你最多也只能在鏈下的支付通道中支付3BTC，這有點像是你必須事先把悠遊卡儲值後才能夠進行後續的消費。

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。

# Ref:
- [[学习笔记] “付款到多重签名” 和 “付款到脚本哈希”](https://aaron67.cc/2018/12/29/bitcoin-transaction-p2ms-p2sh/)
- [什麼是多重簽名錢包？](https://www.binance.vision/zt/security/what-is-a-multisig-wallet)
- [How exactly does BIP11 work, and how can it be used, particularly with/without P2SH?](https://bitcoin.stackexchange.com/questions/14057/how-exactly-does-bip11-work-and-how-can-it-be-used-particularly-with-without-p)
- [[Mastering Bitcoin 筆記] Standard Transactions](https://medium.com/@wilsonhuang/mastering-bitcoin-%E7%AD%86%E8%A8%98-standard-transactions-undone-bfb9b4ed0ed8)
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook)
- [【三分鐘內就看懂】什麼是Segwit隔離見證？](https://www.blocktempo.com/understand-segwit-in3mins/)
- [不可不知 擴容與隔離見證（SegWit）](https://blockcast.it/2017/04/24/what-is-scalability-issue-and-segregated-witness/)
- [Understanding Segwit Block Size](https://medium.com/@jimmysong/understanding-segwit-block-size-fd901b87c9d4)
- [【動區專題】五分鐘就看懂：圖說閃電網路](https://www.blocktempo.com/lightning-network/)
- [什麼是閃電網路？白話版解釋「閃電網路原理」](https://www.moneybar.com.tw/News/91864)
