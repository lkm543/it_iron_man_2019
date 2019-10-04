# 如何開始挖礦

今天我們來簡單談一下如何挖礦，以及如果有興趣要挖礦的話該怎麼開始以及有那些眉角需要注意！

## 選擇幣種/演算法

參與挖礦的第一步就是選擇想要挖的幣種，現在主流可以挖的幣有BTC、ETH、ZEC、ZCL、XMR、DASH、DCR等，雖說幣種繁多，但只要想挖的幣種使用的演算法是相同的，便可以隨意切換而且算力不會受到任何影響，用演算法區分會比較適當。其中又可以分成三種主流的挖礦方式：ASIC挖礦、Nicehash挖礦以及GPU挖礦。

### ASIC挖礦

首先是ASIC挖礦，這類幣種代表礦機廠商已經開發出ASIC，而且官方沒有要對抗(修改演算法或參數)的打算，因此已經都被ASIC攻陷，普通家用電腦或已經沒有競爭的空間。而且ASIC買來也只有挖礦的用途，並無法挪作他用，所以一旦礦機商推陳出新，舊機台也只能直接報廢。

如果是ASIC的話，你可以到[Asicminervalue](https://www.asicminervalue.com/)查看每種機台的報酬率(像下圖)，沒意外的話報酬率都十分低。即便看起來每月利潤相當豐厚的幣種，也只是因為ASIC還沒大舉進入市面的假象，一旦礦機大舉入市，帳面上的收益會直接崩盤，所以大部分的情況下都應該直接避免購買ASIC，我身邊買ASIC的人通常賺錢的比例....非常低。

![ASIC Demo](https://www.lkm543.site/it_iron_man/day19_2.JPG)

### GPU挖礦

另一種方式是透過家用的顯示卡來挖礦，這種挖礦方式的好處是假使不挖了，GPU還是能夠拿來使用，這類幣種所採用的演算法便是我們昨天提到的Proof by bandwidth或是利用多種演算法交錯來抵禦ASIC，也因為尚未被ASIC大舉進攻，通常個體挖礦也還能夠保持一定的收益，你可以在[Whattomine](https://whattomine.com/)裡查看每一張顯卡或算力的收益，比方說一張[AMD RX570](https://www.amd.com/zh-hant/products/graphics/radeon-rx-570)就可以在[這裡](https://whattomine.com/coins?utf8=%E2%9C%93&adapt_q_380=0&adapt_q_fury=0&adapt_q_470=0&adapt_q_480=0&adapt_q_570=1&adapt_570=true&adapt_q_580=0&adapt_q_vega56=0&adapt_q_vega64=0&adapt_q_vii=0&adapt_q_1050Ti=0&adapt_q_10606=0&adapt_q_1070=0&adapt_q_1070Ti=0&adapt_q_1080=0&adapt_q_1080Ti=0&adapt_q_1660=0&adapt_q_1660Ti=0&adapt_q_2060=0&adapt_q_2070=0&adapt_q_2080=0&adapt_q_2080Ti=0&eth=true&factor%5Beth_hr%5D=27.9&factor%5Beth_p%5D=120.0&zh=true&factor%5Bzh_hr%5D=19.0&factor%5Bzh_p%5D=100.0&cnh=true&factor%5Bcnh_hr%5D=640.0&factor%5Bcnh_p%5D=110.0&cng=true&factor%5Bcng_hr%5D=640.0&factor%5Bcng_p%5D=110.0&cnr=true&factor%5Bcnr_hr%5D=730.0&factor%5Bcnr_p%5D=120.0&cnf=true&factor%5Bcnf_hr%5D=1250.0&factor%5Bcnf_p%5D=110.0&eqa=true&factor%5Beqa_hr%5D=85.0&factor%5Beqa_p%5D=100.0&cc=true&factor%5Bcc_hr%5D=0.0&factor%5Bcc_p%5D=0.0&cr29=true&factor%5Bcr29_hr%5D=0.0&factor%5Bcr29_p%5D=0.0&ct31=true&factor%5Bct31_hr%5D=0.2&factor%5Bct31_p%5D=100.0&eqb=true&factor%5Beqb_hr%5D=13.0&factor%5Beqb_p%5D=110.0&ns=true&factor%5Bns_hr%5D=700.0&factor%5Bns_p%5D=140.0&bcd=true&factor%5Bbcd_hr%5D=8.6&factor%5Bbcd_p%5D=110.0&tt10=true&factor%5Btt10_hr%5D=11.5&factor%5Btt10_p%5D=110.0&x16r=true&factor%5Bx16r_hr%5D=6.5&factor%5Bx16r_p%5D=110.0&phi2=true&factor%5Bphi2_hr%5D=0.0&factor%5Bphi2_p%5D=0.0&xn=true&factor%5Bxn_hr%5D=0.0&factor%5Bxn_p%5D=0.0&hx=true&factor%5Bhx_hr%5D=6.6&factor%5Bhx_p%5D=110.0&zlh=true&factor%5Bzlh_hr%5D=12.5&factor%5Bzlh_p%5D=100.0&ppw=true&factor%5Bppw_hr%5D=6.7&factor%5Bppw_p%5D=130.0&x25x=true&factor%5Bx25x_hr%5D=0.7&factor%5Bx25x_p%5D=75.0&mtp=true&factor%5Bmtp_hr%5D=0.0&factor%5Bmtp_p%5D=0.0&lrev3=true&factor%5Blrev3_hr%5D=33.5&factor%5Blrev3_p%5D=120.0&factor%5Bcost%5D=0.1&sort=Profitability24&volume=0&revenue=24h&factor%5Bexchanges%5D%5B%5D=&factor%5Bexchanges%5D%5B%5D=binance&factor%5Bexchanges%5D%5B%5D=bitfinex&factor%5Bexchanges%5D%5B%5D=bitforex&factor%5Bexchanges%5D%5B%5D=bittrex&factor%5Bexchanges%5D%5B%5D=cryptobridge&factor%5Bexchanges%5D%5B%5D=dove&factor%5Bexchanges%5D%5B%5D=exmo&factor%5Bexchanges%5D%5B%5D=gate&factor%5Bexchanges%5D%5B%5D=graviex&factor%5Bexchanges%5D%5B%5D=hitbtc&factor%5Bexchanges%5D%5B%5D=hotbit&factor%5Bexchanges%5D%5B%5D=ogre&factor%5Bexchanges%5D%5B%5D=poloniex&factor%5Bexchanges%5D%5B%5D=stex&dataset=Main&commit=Calculate)看到它的算力與利潤分別為多少，評估後再決定要不要下去。

![RX 570 Demo](https://www.lkm543.site/it_iron_man/day19_1.JPG)


### Nicehash挖礦

另一種挖礦方式是持有硬體，但不直接參與特定的礦池挖礦，而是透過[Nicehash](https://www.nicehash.com/)這個算力租賃平台把自身的算力售予別人，Nicehash在接受到你的算力後，會直接結算BTC給你，對於想要直接獲取BTC的人實在方便許多，同時也提供了一種利用GPU來獲取BTC的方式。Nicehash比較特殊的作法是它會檢測你每一張顯示卡對於各個演算法下的效能，接著根據購買者對於每個演算法的出價決定我們的顯示卡究竟要採用哪個演算法。

![Nicehash](https://fsmedia.imgix.net/3a/09/0f/04/ec2e/41e1/b991/22ce07a8f5e2/logobiglightpng.png?auto=format%2Ccompress&dpr=2&w=650)

圖片來源：[inverse.com](https://www.inverse.com/article/39221-nicehash-robbed-of-78-million-worth-of-bitcoin)

Nicehash的另一種使用方式就是購買別人的算力，通常是礦池在剛始建立時缺乏算力而無法穩定出塊與吸引其他人加入時會使用到，[這裡](https://justhodl.blogspot.com/2018/03/nicehash-buy-hashrate-mining.html)有詳細的買算力教學，有興趣的話可以閱讀，不過另一種用法就是被攻擊者拿來租借後進行51%攻擊了(之後會再詳述)。

### Ethereum的算力預估

目前主流的個體挖礦都是Ethereum了，因此下面的教學主要都是以ETH為主，這裡提供一個簡單的方式去粗略預估每種顯卡的算力：把顯卡的`記憶體頻寬除以8000Bytes`便是大概的算力值(h/s，每秒可以算幾個hash)。原理就是我們昨天說的─Dagger-Hashimoto演算法是Proof by bandwidth，因此根據顯卡的頻寬就能夠大概把算力估計出來(但只有在軟體已經針對硬體優化過的狀況下適用)。

以RX570為例，你可以在[這裡](https://www.techpowerup.com/gpu-specs/radeon-rx-570.c2939)看到RX570的頻寬大約是224GB/s，除以8000 Bytes後便大約是28 Mh/s，跟實際上超頻後的最大值31Mh/s相距不遠。

![570 Spec](https://www.lkm543.site/it_iron_man/day19_3.JPG)

至於另一張家用神卡[1050ti](https://www.geforce.com/hardware/desktop-gpus/geforce-gtx-1050-ti/specifications)的記憶體頻寬約在112GB/s上下，換算出的算力大約14Mh/s。

## 選擇硬體

選擇好欲挖掘的幣種與演算法後，接著就可以來選擇要添購的硬體，這裡我們以Ethereum為例，組成礦機的過程大致上跟組裝一台電腦一樣，但在同一台主機上我們可能會插上十幾張顯卡！

### CPU、RAM、SSD、網路

為了讓礦機能夠順利運行，因此一般電腦的零組件是不可少的，但又為了節省成本，因此在CPU、RAM、SSD、網路選擇最基本/廉價的硬體即可，也就是通常只會搭配4GB的RAM與128GB的SSD(建議不要用HDD，不然等待重開機的過程會讓你想死)，CPU大部分人都選用便宜堪用的[G3930](https://ark.intel.com/content/www/tw/zh/ark/products/97452/intel-celeron-processor-g3930-2m-cache-2-90-ghz.html)，只要1000出頭便可以入手。網路的部分也是一樣，因為現今的挖礦幾乎都採用了我們前幾天提到的Stratum協定，因此一台礦機只需要幾KB的上下載速度便足夠了！

### 主機板

主機板的使用就一個要點：能夠接上GPU的PCIE插槽越多越好，因為主機零件(CPU、RAM、SSD)是有成本的，如果能夠在一台主機上插上越多的GPU，就代表每張GPU需要攤提的主機成本就越低也越有競爭力，主流八卡機是採用[B250H Gaming](https://www.asus.com/tw/Motherboards/ROG-STRIX-B250H-GAMING/)這張主機板，但其實上面只有六個PCIE插槽，其餘兩個需要從M.2轉接。專業或想要挑戰的人可以選用[ASUS Mining Expert](https://www.asus.com/us/Motherboards/B250-MINING-EXPERT/)，上頭甚至有19個PCIE插槽！雖然說插槽數一多成本也下降，但隨之而來除錯上的困難也是必須考慮的。

### PSU(電源供應器)

PSU(電源供應器)的使用只有兩個要點：務必足瓦、請使用金牌以上認證的PSU。足瓦是為了保證供電是有餘裕的避免突波造成電器的損壞，如果瓦數不足有時候會透過雙電源啟動線(下圖)來提供足夠的供電(畢竟如果你真的用了19張顯示卡在Mining Expert那張板子上，光靠一台電源供應器一定是推不動的。)，金牌以上的電源供應器是為了保證電源使用的效率，畢竟電費是開始挖礦後最大的開支，因此電源的轉換效率會直接決定日後的電費多寡。

補充說明一下：80PLUS的認證依序可以分成：銅牌、銀牌、金牌、白金、鈦金，通常越往上電源轉換效率越好、越省電，但價格也會越高。

![雙電源啟動線](http://www.armygroup.com.tw/shop/images/201002/goods_img/3598_G_1265084554965.jpg)
圖片來源：[改裝軍團](https://www.armygroup.com.tw/shop/goods-3598.html)

### GPU

在確保你的GPU有辦法提供你想要的算力與性價比後(通常是RX570、RX580、GTX 1060、GTX1070)，GPU的選用主要有兩點：保固期與記憶體廠牌，保固期決定了你的顯示卡能夠被使用多久，即便損壞你還是能夠跟原廠換一張新的過來，而記憶體的製造商主要有三大廠，一般而言：`三星>美光>海力士`。因為對於Ethereum的算法而言，記憶體的頻寬是重要的，而在實測上三星與美光能夠超頻並提供高一點的算力(其中三星又>美光)，而海力士則幾乎不能超頻。

## 選擇作業系統

作業系統的選用除了常見的Windows與Linux外，目前也有許多開發出專門應用在挖礦上的作業系統，像是[Hiveos](https://hiveos.farm/)、[ETHOS](http://ethosdistro.com/)、SparkOS等作業系統，如果是專門挖礦、平常不會拿來使用的主機強烈建議安裝挖礦專用的作業系統，裏頭整合了驅動程式與挖礦控制等軟體，可以避免安裝驅動程式不合或是難以監控的問題。另外一點是隨著時間過去，DAG也會增加，AMD預設的顯示卡架構會印為DAG的增加造成大幅度的算力下降，選擇挖礦的作業系統能夠幫助你輕鬆解決這個問題而不需要另外設定。(一般Windows你安裝AMD的驅動後必須在驅動程式介面啟動運算模式以避免DAG增大帶來的負面影響)。

## 選擇挖礦軟體

Ethereum主要的挖礦軟體有Claymore、Ethminer、Phoenix Miner等，其中臺灣最多人使用的就是Claymore，即使它會抽取你1%不等的算力(你可以指定不要讓Claymore抽1%，但Claymore會讓你算力減少2%)，但因為Claymore目前仍是主要公認效能最好的挖礦軟體(沒有之一)，因此還是最主流的挖礦軟體。你可以到[bitcoin talk](https://bitcointalk.org/index.php?topic=1433925.0)下載最新的Claymore來使用。

# 實際畫面

這裡我用家裡的電腦(Win10)搭配[RX460](https://www.techpowerup.com/gpu-specs/radeon-rx-460.c2849)做示範，RX 460擁有112GB/s的頻寬，理論上能夠跑到約14Mh/s，但因為這裡我沒有超頻與優化，而只有看到11~12Mh/s的算力。也可以在畫面中看到DAG的載入，這就是我們昨天所說的Dagger-Hashimoto演算法裏頭的DAG！

![Miner Demo](https://www.lkm543.site/it_iron_man/day19_4.JPG)

# Ref:
- [Asicminervalue](https://www.asicminervalue.com/)
- [Whattomine](https://whattomine.com/)
- [bitcointalk](https://bitcointalk.org/)
- [維基百科-80PLUS](https://zh.wikipedia.org/wiki/80_PLUS)

