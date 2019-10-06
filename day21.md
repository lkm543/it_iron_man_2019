# 傳統的網路架構

![Client–server model](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Client-server-model.svg/1920px-Client-server-model.svg.png)

圖片來源：[Wikipedia](https://en.wikipedia.org/wiki/Client%E2%80%93server_model)

傳統的網路架構是每一張圖片、影片、網站、APP都會有存放的伺服器(`server`)，每個伺服器會有自己像門牌一般的ip位址，當我們(`client`)瀏覽網頁時，其實就是透過ip位址向伺服器發出請求(request)，再由伺服器回傳我們瀏覽網頁上的資源(圖片、影片、html等)給我們。可以說伺服器本身掌控了話語權，也決定了我們能看到甚麼。

因此傳統的架構又稱為`Client–Server model`。

以facebook為例，你在facebook的所有帳戶、照片、好友資料通通都存在facebook的伺服器中，facebook也有權力決定要給你看到/看不到甚麼，所以與其說是你的帳戶，不如說是facebook擁有你自願上傳的資訊，當你有需求時再順道回傳給你一份罷了。

![Centralized](https://www.dcsorg.com/images/centralized-management.jpg)

圖片來源：[Digital Currency Systems](https://www.dcsorg.com/centralized-management.php/)

所以傳統的中心化架構就是所有使用者的請求都會被送到同一個伺服器處理。另一個中心化的例子就是銀行的金流系統，當我們要匯款時便是向銀行的伺服器發出請求，請伺服器驗證我們的身分並且針對我們的請求加以處理，同時我們也信任伺服器的處理結果，整個流程都由銀行端完成。

這種架構的優點就是處理迅速，我們只需要等待單一伺服器的回應就可以知道結果。但其中卻有兩大缺陷：

## Scalability

Scalability代表的是可擴充性，也就是當使用者的數目成長時，系統接收並處理請求的伺服器數目卻是固定的，固定的伺服器規格代表能處理的使用者數目或是單位時間內的請求數是會有上限的，如果想要拉高上限，代表的是營運成本也會跟著上升(但其實近年因為硬體的進步與分散式系統的發達已經很大解決Scalability的問題了)。

## Reliability

Reliability代表的是系統的可靠度，也就是系統的妥善率有多少。傳統的`Client–Server model`仰賴單一伺服器與節點的運行，所以一旦伺服器出錯或是維修，整個服務就會終止，也因如此我們偶爾還是會聽到facebbok斷線或是銀行服務會有固定的停止服務時間等等。

# Peer to Peer(P2P)網路

傳統的網站架構是把所有的資源都放置在同一台伺服器上，有需要的用戶再向伺服器檢索。Peer to Peer(P2P)網路則是網路上的所有人都負責儲存了全部或部分的所有資料，除了向其他IP位址發起請求外，本身也需要負責處理收到的請求，**自身既是Client也是Server**。

但其實P2P網路並非是非常新的概念，在常聽到的[TCP/IP通訊協定](https://zh.wikipedia.org/zh-tw/TCP/IP%E5%8D%8F%E8%AE%AE%E6%97%8F)中其實就是一種終端到終端(end to end)的概念，通訊的兩端是彼此平等不分client與server的！只是因為實務上我們上網幾乎都是在檢索其他網站的資料，為了效率與實務上應用的考量網站經營者才會把所有資源集中存放與處理。

![P2P](https://www.skalex.io/wp-content/uploads/2017/06/p2p-web-model-transparent.png)

圖片來源：[https://www.skalex.io](https://www.skalex.io/blockchain-p2p-web/)

P2P網路在Scalability與Reliability都具有很大的優勢，因為每個獨立的終端都可以視作Server，當終端數目增加，Server數目也隨之增加，所有可運用的硬體資源與網路頻寬也隨之增加，在Scalability會具有很大的優勢。而Reliability的部分因為每個終端都可以獨立運作，所以不存在傳統中心化架構中一旦單一伺服器停擺就會造成整個服務中斷的問題。

除了Scalability與Reliability外，P2P網路也因為沒有中心化的伺服器，而讓資料沒有被中心化機構掌控或修改的可能，也確保了資訊的安全。

## P2P網路的難題

雖然P2P網路可以有效解決傳統中心化網路在Scalability與Reliability的問題，但在技術上因為需要參照與協調許多終端所以技術的複雜度會比傳統Client–Server model複雜。以下簡述幾種P2P網路實作上的難題。

### 工作的分配

雖然P2P網路的硬體資源與頻寬會隨著終端數目的增加而增加，但如何配置與分享彼此間閒置的資源是一大難題，畢竟即便資源增加，若沒有好好地被分配與利用也是徒然。以下簡述幾種工作分配的方式：

#### Opportunistic Load Balancing(OLB)

Opportunistic Load Balancing是將目前的工作隨意分配給一台閒置的電腦，目標是讓所有的電腦都處於工作的狀態，但因為沒有考量每個工作的工作量與每台電腦獨立且不同的運算能力，所以不適用於由異質終端所構成的P2P網路。

#### Minimum Execution Time(MET)

Minimum Execution Time是不考慮電腦目前的工作狀態，直接把這項工作分配給執行時間最短的電腦，但缺點是會造成負載的不平衡，運算能力最強的電腦會被分派到最多工作，運算能力最弱的就會一直閒置，所以同樣不適用於由異質終端所構成的P2P網路。

#### Minimum Completion Time(MET)

Minimum Completion Time是根據電腦的最小完成時間(目前的工作要多久才會結束)來分派工作，越快結束的電腦就會被優先指派然後計算，所以並不保證執行時間(Execution Time)會最短。

#### Min-Min

Min-Min是根據工作在每一台電腦預估可以完成的時間，所以也會將電腦目前的工作狀態列入考量。完成時間的意思便是等待時間加上執行時間(上面的Execution Time)，所以雖然能確保工作能在最短時間內被完成，但預估完成時間也是難事。

### 節點的搜尋

既然P2P網路是由許多獨立的Peer所構成，那要怎麼知道參與網路的節點確切的ip位址呢？你只能透過一些中心化的網站或是上網搜尋其他人提供的節點位置，比方說[這個網站](https://bitnodes.earn.com/)就記錄了Bitcoin網路線上的所有節點(下圖)，找到節點們的資訊後你才能參與整個P2P網路的運作。

![Peer Location](https://www.lkm543.site/it_iron_man/day21_1.JPG)

圖片擷取自：[bitnodes](https://bitnodes.earn.com/)

### 取得Peer間的共識

另一個P2P網路的難題是要取得終端/節點間的共識，P2P網路間必須共享同一份資料與彼此間的資訊才能夠協作，且因為TCP/IP的網路是兩兩連接而成的，由簡單的排列組合可以得知當節點有N個時，所有節點可以組成的連線個數便是CN取2，就是N\*(N-1)，大約取決於N^2，這在節點數一多的狀況下要取得Peer間的共識會非常困難，更何況有時候會有惡意的節點加入並且散步造假過的資訊，我們明日會在根據拜占庭將軍問題詳談如何解決這個問題。

![https://chart.googleapis.com/chart?cht=tx&chl=C%5EN_2%3DN!%2F(k*(N-2)!)%3DN*(N-1)](https://chart.googleapis.com/chart?cht=tx&chl=C%5EN_2%3DN!%2F(k*(N-2)!)%3DN*(N-1))

### 無法徹底去中心化

最後一個問題是P2P網路雖然可以稍微擺脫被單一中心化機構掌控資源的風險，但實際上P2P網路沒有辦法達到完全的去中心化，原因是網路提供商ISP或是[DNS](https://zh.wikipedia.org/zh-tw/%E5%9F%9F%E5%90%8D%E7%B3%BB%E7%BB%9F)還是掌控在中心化機構手中，像是上面節點的搜尋也需要仰賴別人提供的資訊，因此充其也只是最後資訊的儲存與處理是去中心化，底層的通訊還是得仰賴特殊的機構完成。

### 資料的重複儲存與不穩定性

因為P2P網路的節點是可以自由加入與退出的，也就是每個節點的穩定性並無法確認，也無法得知每個節點可存續的時間，為了求取資料的安全便需要在複數個位置上儲存同樣的資料，相較於中心化網路會多耗費許多空間，即便如此在儲存使用者分享的檔案時也無法確保該檔案能存在多久。

## P2P網路的分類

根據P2P網路處理資訊與分配工作的方式大致又可以分成三種：

![P2P Category](https://www.researchgate.net/profile/Taoufik_Yeferny/publication/332539196/figure/fig2/AS:749686013034497@1555750482262/P2P-architectures-at-a-glance-a-Centralized-architecture-b-Pure-P2P-architecture.png)

圖片來源：[P2P architectures at a glance.](https://www.researchgate.net/figure/P2P-architectures-at-a-glance-a-Centralized-architecture-b-Pure-P2P-architecture_fig2_332539196)

### 中央式P2P

也就是上圖的(a)，代表整個P2P有一個中心伺服器專責處理工作的分派與分流，也會記錄節點們的清單與位置，但中心節點並不實際處理資訊或是資料的儲存，只負責節點間的溝通與工作的調度。

### 純P2P

純P2P代表整個P2P網路中的節點都是平等的，彼此並沒有工作或是權力上的分別，也就是上圖的(b)。

### 混合 p2p

混合式P2P很像是中央式P2P，但其跟中央式P2P網路不同的地方是它擁有複數個中心伺服器負責資訊的轉發與協調，[EOS](https://eos.io/)本身就擁有了21個超級節點。

# P2P與區塊鏈

整個Bitcoin全節點可以看作是一種純P2P網路，節點間並沒有先來後到之分，但為了保持資料的一致性(所有節點手上的帳本必須同步)，所以在傳遞或廣播上必須考量到效率與攻擊者假造節點的狀況，因此我們明天就要來介紹究竟在P2P網路中要如何確保節點間的同步與讓正確的共識被形成呢？

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。

# Ref:
- [Peer-to-Peer (P2P) System](https://sls.weco.net/node/12916)
- [P2P-顛覆網際網路傳統觀念](http://bm.nsysu.edu.tw/tutorial/htt/dkl/SearchEngine-nsysu041230.pdf)
- [Wikipedia-Client–server model](https://en.wikipedia.org/wiki/Client%E2%80%93server_model)
- [P2P的網路共享世界](https://dannylin3000.pixnet.net/blog/post/31271397-p2p%E7%9A%84%E7%B6%B2%E8%B7%AF%E5%85%B1%E4%BA%AB%E4%B8%96%E7%95%8C)
- [P2P對等網路技術原理整合](https://www.itread01.com/content/1546608974.html)
- [P2P原理以及如何实现（整理）](https://blog.csdn.net/qq_33850438/article/details/79700133)
- [以兩階段排程演算法提昇動態階層式點對點網路拓樸之負載平衡](http://ir.lib.cyut.edu.tw:8080/bitstream/310901800/6479/1/Two+phases+scheduling+in+P2P.pdf)
- [詳解區塊鏈P2P網路](https://www.itread01.com/content/1545529340.html)
- [Towards Efficient Simulation of Large Scale P2P Networks](https://slideplayer.com/slide/4806764/)
- [點對點網際網路技術(P2P)和軟體之概論](https://www.shs.edu.tw/works/essay/2008/10/2008103101062756.pdf)
