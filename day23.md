# 升級之路上的岔路口

![Fork Road](https://www.danblewett.com/wp-content/uploads/2012/12/fork-in-the-road1-640x426.jpg)

圖片來源：[danblewett](https://www.danblewett.com/the-necessity-of-failure-the-fork-in-the-road/)

昨天我們提到網路廣播的延遲會產生不可避免的`暫時性分岔`，而今天要提的分岔則跟整個P2P網路的軟體升級有關。一般網站或APP升級都會由中心化伺服器負責軟體更新，或是派送新版本的軟體到用戶端要求用戶安裝。但去中心化的P2P網路則不同，因為每個節點都是獨立平等的存在，所以如果要更新目前運作的軟體版本，節點也有可能拒絕或是選擇另一個版本繼續運作，因此根據新版本在原本P2P網路中是否會互相排斥或是相容就會分成`軟分岔(Soft Fork)`與`硬分岔(Hard Fork)`。

軟分岔(Soft Fork)與硬分岔(Hard Fork)跟暫時性分岔有一個很大的不同：暫時性分岔不牽涉到程式碼或是協定的更動，只是因為網路延遲造成短期間無法同步所有資料的現象，而軟分岔(Soft Fork)與硬分岔(Hard Fork)則會**永久更動現行運作的程式碼**。更動程式碼的原因有很多，最常見的幾種分別是：

1. 新增過去沒有的功能：

    2012年3月份Bitcoin根據BIP16新增了[多重簽名](https://www.binance.vision/zt/security/what-is-a-multisig-wallet)的付款方式，詳情可以參考[這裡](https://en.bitcoin.it/wiki/Pay_to_script_hash)。

2. 回溯過去的資料：

    2016年DAO(the Decentralized Autonomous Organization)被盜走了360萬顆ETH，為了追回被盜取的ETH，採取硬分岔的方式回溯到資產轉移之前，相關[新聞報導](https://www.ithome.com.tw/news/107405)。

3. 修改某部分運行的參數：

    XMR為了對抗ASIC固定每半年會更新一次挖礦的參數。

既然軟分岔(Soft Fork)與硬分岔(Hard Fork)都跟節點運行的軟體升級有關，那麼首先來談談節點們又是如何決定升級的方向與內容呢？

## 從社群提案到接受

去中心化的區塊鏈並沒有權威的中心機構來決定未來升級的方向與內容，因此未來升級方向的提案、討論、決定都是仰賴社群意見的協助，為了凝聚社群共識與方便大家提案，社群也會在Github上開啟專門的Repository來標示各提案的內容，有意參與討論的人都可以在下自由留言。

### BIP(Bitcoin Improvement Proposals)

Bitcoin的改善協議稱為`Bitcoin Improvement Proposals(BIP)`，你可以到[Github](https://github.com/bitcoin/bips)上看到Bitcoin至今的所有BIP與社群的意見。BIP是社群間彼此溝通想法的方式，一旦議題被社群廣泛接受就會被收入BIP，下圖便是BIP收入後大致的運作流程與可能結果。

![BIP](https://en.bitcoin.it/w/images/en/e/ea/BIP_Workflow.png)

圖片來源：[Bitcoin Wiki](https://en.bitcoin.it/wiki/Bitcoin_Improvement_Proposals)

每個BIP在被當作草稿(`Draft`)提出後會有四種可能：被廣泛接受後被實作在鏈上(`Accepted`)、被社群拒絕(`Rejected`)、發起者自己撤銷提案(`Withdrawn`)、推遲提案(`Deferred`)。值得一提的是或許是開源社群的習慣，社群很少直接拒絕(Reject)某個提案，而通常以推遲(Deferred)或自行撤回(Withdrawn)的方式結束，少數幾個被Rejected例外就是想把區塊容量依照中本聰原本的想法擴容至2MB的[BIP109](https://github.com/bitcoin/bips/blob/master/bip-0109.mediawiki)，提出BIP109的是與中本聰一起參與過的Gavin Andresen，該次Reject也間接導致後續Bitcoin社群的分裂與BCH的分岔，甚至還有專人架設[網站](http://bip109.com/)聲援Bitcoin應該要照原本中本聰理想的實行BIP109。

### EIP(Ethereum Improvement Proposals)

與Bitcoin的BIP類似，社群經過提案後會產生相對應的`Ethereum Improvement Proposals(EIP)`，Ethereum主要由乙太坊基金會在開發與維持社群，因此與Bitcoin不同的是在營運上較為中心化，官方對於EIP會發出相應的ERC討論。

ERC的全名是`Ethereum Request for Comments`，就是徵求社群間的意見，此時ERC的編號與EIP通常會一致，最有名的EIP與ERC莫過於[ERC20](https://medium.com/myethacademy/%E5%88%B0%E5%BA%95%E4%BB%80%E9%BA%BC%E6%98%AFerc-20-49d052e8d290)成為代幣的標準並引發2017-2018年間的ICO熱潮，在[這裡](https://eips.ethereum.org/)你也可以看到所有的EIP列表。

## 軟分岔(Soft Fork)與硬分岔(Hard Fork)

在P2P網路中每個節點對於是否要接受新提案都是自由的，也就是每個節點所運行的區塊鏈版本不一定一致，在P2P網路中也可能會有多個版本共存，根據**是否要接受過去版本的資訊可以分成軟分岔(Soft Fork)與硬分岔(Hard Fork)**。

- 軟分岔(Soft Fork)─更新後仍然可以接受與過去版本間形成部份的共識
- 硬分岔(Hard Fork)─更新後完全無法與舊版本形成共識

如果你對軟體有點概念的話，軟體開發中所講到的**向後相容**的概念(對過去的版本相容)就是軟分岔！

## 軟分岔(Soft Fork)

軟分岔(Soft Fork)的定義是舊節點不升級也可以相容於部分的共識，因為共識可以在新舊版本間形成，所以**新舊版本可以共存在同一條鏈之上**。

![Soft Fork](https://bitcoin.org/img/dev/en-soft-fork.svg)

圖片來源：[mycryptopedia](https://www.mycryptopedia.com/hard-fork-soft-fork-explained/)

軟分岔以**功能的更新**居多，亦即雖然可以相容在同一條鏈上，但舊版本會沒有辦法使用新版本所推出的功能，就像是你可以使用Word2017去開啟Word2013的檔案，但如果你仍然在使用Word2013就會沒辦法使用某些Word2017才有的新功能了。

## 硬分岔(Hard Fork)

硬分岔(Hard Fork)的定義是舊節點不升級就無法相容於新節點產生的共識，因為共識不能在新舊版本間形成，所以**新舊版本不能共存在同一條鏈之上**，所以一旦網路中還有兩種版本在運行，則兩種版本就會岔開分成兩條獨立的鏈，各走各的路。

![Soft Fork](https://bitcoin.org/img/dev/en-hard-fork.svg)

圖片來源：[mycryptopedia](https://www.mycryptopedia.com/hard-fork-soft-fork-explained/)

之所以新舊版本不能共存的原因通常在於**共識規則的更新**，如果未更新成新的共識規則會導致舊版本無法驗證新版本所產生的區塊。

### IFO(Initail Fork Offering)

因為P2P網路可自由進出的關係，單一節點也可以採取自行開發的新硬分岔版本而跟多數節點脫離。任何人也都可以分岔出屬於自己的區塊鏈，因此有一陣子因為ICO被法令限制的關係，IFO成為某些人手中的印鈔機─你可以可以輕易的分岔出一條區塊鏈然後把部分的挖礦所得直接配給自己(在[這裡](https://medium.com/@jordan.baczuk/how-to-fork-bitcoin-part-1-397598ef7e66)及[這裡](https://medium.com/@jordan.baczuk/how-to-fork-bitcoin-part-2-59b9eddb49a4)你可以學到如何岔出一條自己的Bitcoin)，雖然硬分岔在技術上是容易的，但分岔出的幣種市場是否能接受則仰賴市場上的共識了！實際上這些幣多半會因為流通量太低而成為一攤死水沒人理睬。

![XMR Fork](https://steemitimages.com/640x0/https://steemitimages.com/DQmZ7MngHG9gQm46of2CSfQTf71KbFC2CaYwFgdhUJLhELG/MoneroCoins.jpg)

圖片來源：[steemit](https://steemit.com/monero/@cryptocurrencyhk/monero-monero)

像是為了因應XMR修改演算法對抗比特大陸的ASIC，許多社群與礦機商分岔出了Monero Classic(XMC)、Monero-Classic(XMC)、Monero 0(XMZ)及Monero Original(XMO)，不過這些分岔出的幣多半都在一攤死水的狀態了。在[這裡](https://steemit.com/monero/@cryptocurrencyhk/monero-monero)你可以看到更多進一步的消息。

### 歷史上知名的硬分岔

歷史上最知名的兩次硬分岔莫過於[Ethereum Classic(ETC)](https://ethereumclassic.github.io/)自Ethereum分岔出與[Bitcoin Cash(BCH)](https://www.bitcoincash.org/)自Bitcoin分岔出的這兩段故事了。

#### ETC的分岔

ETC的分岔起因於Ethereum為了拯救在2016年6月17日[DAO被駭走的360萬顆ETH](https://www.ithome.com.tw/news/106614)而採取硬分岔回溯的行為，ETC的支持者認為這違反了區塊鏈不可竄改的精神，於是拒絕了Ethereum的提案留在舊鏈形成了Ethereum Classic(ETC)，真的說起來的話Ethereum Classic(ETC)才是真正的Ethereum。

#### BCH的分岔

BCH的分岔則是因為不認同目前把持Bitcoin發展方向的Core所規劃的未來藍圖([閃電網路](https://www.blocktempo.com/lightning-network/)、[隔離驗證](https://www.blocktempo.com/understand-segwit-in3mins/)等方向)，認為透過增加區塊容量到8MB就可以很容易解決目前TPS(Transactions per Second)過低的問題，也因此BCH新的共識規則便是8MB的區塊大小，但既然共識規則改變了，BCH新的共識規則自然無法相容於舊Bitcoin的1MB容量，於是兩者就分岔出不同鏈各走各的路了！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。

# Ref:

- [BlockchainHard ForkSoft Fork Blockchain Soft Fork & Hard Fork Explained](https://www.mycryptopedia.com/hard-fork-soft-fork-explained/)
- [什麼是區塊鏈分叉? 什麼又是硬分叉/軟分叉?](https://medium.com/@crypto.peng/%E4%BB%80%E9%BA%BC%E6%98%AF%E5%8D%80%E5%A1%8A%E9%8F%88%E5%88%86%E5%8F%89-%E4%BB%80%E9%BA%BC%E5%8F%88%E6%98%AF%E7%A1%AC%E5%88%86%E5%8F%89-%E8%BB%9F%E5%88%86%E5%8F%89-2246d1d28d84)
- [【硬塞科技字典】區塊鏈的分叉是什麼？還分為軟的和硬的？](https://www.inside.com.tw/article/13733-fork-soft-hard)
- [How to Fork Bitcoin — Part 1](https://medium.com/@jordan.baczuk/how-to-fork-bitcoin-part-1-397598ef7e66)
- [How to Fork Bitcoin — Part 2](https://medium.com/@jordan.baczuk/how-to-fork-bitcoin-part-2-59b9eddb49a4)
- [Complete Guide on How to Create a New Alt Coin](https://bitcointalk.org/index.php?topic=225690.0)
- [Wikipedia-List of bitcoin forks](https://en.wikipedia.org/wiki/List_of_bitcoin_forks)
- [一文讀懂BIP、EIP、ERC等相關概念](https://kknews.cc/zh-tw/finance/mkbayb6.html)
