# 智能合約

在講解完Ethereum的架構、手續費機制與基本語法後，今天我們來試著在一般網頁上使用簡單的合約，我們的重點會放在智能合約如何使用與運作、以及智能合約在使用時有哪些需要特別注意的地方。

## 如何觸發智能合約

觸發智能合約的方式跟一般交易相當類似，使用者會發出一筆交易到智能合約的地址，而這筆交易通常不帶任何ETH(其實有需求要帶也可以，照昨天所說的加入`
payable修飾即可`)。跟一般交易不同的是該筆交易的`input data`欄位會指定要執行的函式與欲帶入的引數(下圖紅框處)，礦工打包到這筆交易後便會執行相對應的函式。比方說下圖這筆交易便是觸發`transfer`(轉移餘額，就是匯款的意思)

![Input Data](https://www.lkm543.site/it_iron_man/day30_1.jpg)

圖片擷取自: [etherscan](https://etherscan.io/tx/0x43cd813f9a838c300338f6973d103ca660fc0519f160b01d1de6b6f7abb680ed)

你也可以點選Etherscan中Decode input data的按鈕來看編碼後的輸入值，可以看到這筆匯款是匯給   725f78217f20784ccd723be44abe39fc03fd855c、金額則是420348314(換算時記得除以1000000)。

![Input Data](https://www.lkm543.site/it_iron_man/day30_2.JPG)

圖片擷取自: [etherscan](https://etherscan.io/tx/0x43cd813f9a838c300338f6973d103ca660fc0519f160b01d1de6b6f7abb680ed)

## Application Binary Interface(ABI)

前幾天我們有提到智能合約編譯成可以被EVM執行的Bytecode後才會被送上鏈，送上鏈之後便會產生一個特定的合約地址，日後有人想要使用這個合約也只要向這個合約地址發起交易便可以了！但我們要怎麼知道合約有哪些函式、這些函式又需要那些引數呢？

這時候就需要`Application Binary Interface(ABI)`來告訴我們智能合約的介面了。

如果你也寫過標頭檔(.hpp)或是API文件的話就會很好理解ABI，ABI向標頭檔一樣是個程式介面，其中詳盡規範與說明了合約中每一個函式的使用方式，如果你沒有相關經驗的話，你可以把ABI想像成是該智能合約的操作說明書，你可以到Etherscan上看到某些合約的程式碼與ABI(下圖)。

![ABI](https://www.lkm543.site/it_iron_man/day30_3.JPG)

圖片擷取自: [etherscan](https://etherscan.io/address/0xdac17f958d2ee523a2206206994597c13d831ec7#code)

另外注意一件事，實際上智能合約編譯成Bytecode後就很難反編譯回原本的程式碼，同時也無法直接從Bytecode推算出合約的ABI，你可以在[Etherscan](https://etherscan.io/)上看到某些智能合約的程式碼與ABI是因為合約持有方對Etherscan提供了合約的原始碼，經過Etherscan編譯後可以編譯出一模一樣的Bytecode，藉此證明該原始碼與合約內容是相符的，同時Etherscan也可以幫助你公開合約的程式碼與ABI供外界檢視與使用。

Solidity的[官方文件](https://solidity.readthedocs.io/en/v0.5.3/abi-spec.html)中便有規範ABI裏頭的格式，節錄一段在下面可以參考。

> `type`: "function", "constructor", or "fallback" (the unnamed “default” function);
> `name`: the name of the function;
> `inputs`: an array of objects, each of which contains:
> `name`: the name of the parameter;- 
> `type`: the canonical type of the parameter (more below).
> `components`: used for tuple types (more below).
> `outputs`: an array of objects similar to inputs, can be omitted if function doesn’t return anything;
> `stateMutability`: a string with one of the following values: pure (specified to not read - blockchain state), view (specified to not modify the blockchain state), nonpayable (function does not accept Ether) and payable (function accepts Ether);
> `payable`: true if function accepts Ether, false otherwise;
> `constant`: true if function is either pure or view, false otherwise.

# 網頁與Ethereum的互動

智能合約目前最大的痛點就是相較一般網頁與APP來說使用門檻極高─區塊鏈上都是以地址為身份辨識進行，所以使用智能合約你必須先安裝/擁有Ethereum的錢包地址才能夠跟智能合約互動。

## Metamask

目前最主流的網頁錢包就是Chrome的擴充套件[metamask](https://metamask.io/)，你可以到[這裡](https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn?hl=zh-TW)安裝下載，安裝上Metamask後就等於擁有了網頁錢包，也可以透過Metamask對智能合約發起交易。。

![Metamask](https://www.ledger.com/wp-content/uploads/2019/06/assets_logo_metamask.jpg)

圖片來源: [ledger](https://www.ledger.com/metamask/)

## Web3.js

至於要如何讓使用者可以透過網頁與Metamask直接操作錢包呢?目前最主流跟Ethereum溝通的toolkit是由Javascript所撰寫的`Web3.js`，因為Web3.js由Javascript所撰寫，所以可以直接嵌入網頁的前端中，使用者只需要點選網頁就可以跟智能合約或是Ethereum互動。

如果你不會寫JS的話，到[codecademy](https://www.codecademy.com/)可以先學一些javascript語法。下面我簡單列舉了幾項Web3.js的寫法來讓你理解Web3.js是如何工作的。

### 初始化並連接節點

要連接節點後我們才能查詢資料或發出交易請求，因此這裡我們需要透過API的協助，目前最主流的服務商是[infura](https://infura.io/)，你可以到他們的網頁申請帳號後就可以申請到一組API_KEY並且使用他們的服務。

```js
var Web3 = require('web3');

if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    // set the provider you want from Web3.providers
    web3 = new Web3(new Web3.providers.HttpProvider("https://mainnet.infura.io/v3/YOUR_API_KEY"));
}
```


### 取得錢包餘額

如果要取得錢包餘額的話，可以使用`web3.eth.getBalance()`來獲取特定地址的ETH餘額，並起透過`web3.fromWei(balance, 'ether')`換算成ETH，並且取到小數點後三位。

```js
var balance = web3.eth.getBalance(YOUR_ADDRESS);
balance = web3.fromWei(balance, 'ether').toFixed(3);
```

### 匯款

匯款的話可以使用`web3.eth.sendTransaction()`，需要帶入的引數為一個紀錄交易明細的Json，注意匯款的單位是Wei喔。交易完後就可以得到該筆交易的Hash值。

```js
var transaction_obj = {
    "from": sender,
    "to": receipt,
    "value": web3.toWei(1.5, 'ether'),
    "gas": optional,
    "gasPrice": optional,
    "data": optional,
    "nonce": optional
};
web3.eth.sendTransaction(transaction_obj, function(error, result){
    if(error) {
        // 例外處理
    } else {
        var transaction_hash = result;
    }
});
```


### 使用智能合約

智能合約的使用你必須先匯入上面我們提到的ABI，接著透過合約地址與ABI就可以接上智能合約在Ethereum上的對口。

```js
const abi = require('./abi.json');
const contract_address = 'CONTRACT_ADDRESS';
contract_instance = new web3.eth.Contract(abi, contract_address);
```

使用上有兩種方式`call`、`send`，如果你只需要讀取合約上的資料，那麼使用call就可以了，使用call時不需要任何費用，但該函式必須是我們昨天寫的pure、view或是public變數，但如果你想要更動合約上的資料，那麼就必須用send來跟上面一樣發出一筆交易，也會耗去部分的手續費。

```js
contract_instance.FUNCTION_NAME.call(function(error, result) {
    if (error) {
        // 例外處理
    } else {
        // 實際執行
    }
});
```

或是你也可以直接透過地址與METHOD_ID來查詢合約裡的變數。

```js
var result = web3.eth.call({
    to: CONTRACT_ADDRESS,
    data: METHOD_ID
});
```

如果想要更動合約上的資料，就必須使用`web3.eth.sendRawTransaction()`來發起一筆交易對合約動作。

# 推薦的學習資料

上面只是簡單列舉實際在使用時會需要知道的基本知識，如果你想要更進一步了解的話，下面幾個是我接觸過也相當推薦的學習網站。另外[Truffle](https://www.trufflesuite.com/)與[Ganache](https://www.trufflesuite.com/ganache)也是必學的開發環境。


## Smart contract開發

- [Solidity官方文件](https://solidity.readthedocs.io/en/latest/)
- [Ethereum Builder's Guide](https://ethereumbuilders.gitbooks.io/guide/content/en/solidity_tutorials.html)
- [cryptozombies](https://cryptozombies.io/)

## Web3.js開發

- [Web3.js官方文件](https://web3js.readthedocs.io/en/v1.2.1/)
- [Dapp University](https://www.dappuniversity.com/articles/web3-js-intro)
- [Truffle Tutorial](https://www.trufflesuite.com/tutorials)

## Udemy影音推薦

- [Practical Blockchain & Smart Contracts : Ethereum & Solidity](https://www.udemy.com/course/blockchain-and-smart-contracts-a-complete-practical-guide/)
- [Ethereum and Solidity: The Complete Developer's Guide](https://www.udemy.com/course/ethereum-and-solidity-the-complete-developers-guide/)
- [web3.js Documentation Release 1.0.0](https://buildmedia.readthedocs.org/media/pdf/web3js/1.0/web3js.pdf)

# 後記─鐵人賽心得

三十天的鐵人賽終於告一段落了\~在今天與鐵人賽的最後來分享這段時間的感想。

## 進度配置

鐵人賽最重要的部分莫過於進度配置，我習慣先用Evernote把這三十天的主題大致先決定好，在9/17(二)開賽前剛好遇到三天的中秋連假，利用中秋連假大概用一篇4~6小時的速度在開賽前完成了快10篇的摳打，但遇到考試、實習與打工，其實到後面這些庫存量是完全不夠用的，在平均一篇要寫4~6小時的狀況下等於整個晚上都會被寫文章耗費掉，在區段考前頂多也只能抽出每天1~2小時來撰寫，幸好結束前又遇到了四天國慶連假補了大概5~6篇進來才能夠順利完賽，如果沒有連假應該會直接GG。

強烈建議如果事前知道自己有哪些天會比較忙碌的話，可以事先把這些天的內容準備好，或是多庫存幾天以免突發狀況(朋友邀約、生病之類的)產生，像是考量到區段考的時間所以我先留了10篇的庫存讓我在這段時間可以專心準備考試。

## 內容安排

內容的考驗的是對領域的掌握程度─你要先知道這個領域有甚麼可以談、要談多深、談多久都需要底子，另外粗細的掌握非常重要，我一開始很有衝勁的想把所有東西都講很細很清楚，結果密碼學入門那裏就寫的太多導致壓縮到後面的內容與空間。內容的掌握與安排真是一項藝術呀。

除了入門教學的系列外，鐵人賽可以看作是一年來的學習成果與加深，會選區塊鏈這個題目也是因為過去一兩年來對這個領域接觸比較多，除了強迫自己歸納與統整這段日子的所學外，也可以順便透過查詢資料與規劃內容的過程知道自己有哪些方面的知識有所不足並且可以趁機加以填補。

## 強迫自己閱讀與真正理解

寫文章的好處是強迫自己真正理解一個領域，而不是只有處在一知半解的狀態。但寫文章難的部分是要怎麼樣有動力去扎扎實實地寫好一個系列......而鐵人賽就給了一個強烈的動機去完成。此外是對寫作能量的提升，以我為例這30天內寫了7萬個字左右，從第一天的舉筆不定到後來可以流暢地直接打完一整段文字自己的感覺最深刻。

## 時限壓力

與平常工作或Side Project相比，鐵人賽有每天要完成一定工作的時間壓力，在壓力賀爾蒙的協助下可以大幅度的提升工作表現與治療拖延病，但偶爾一個月這樣可以，太久就會有點傷身了。

這次大約用了一個半月的空閒時間產出了30篇文章，說真的CP值還蠻高的，明年見習時或許可以再來挑戰看看，至於要寫甚麼就看未來這一年會學到甚麼了。

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。

# Ref:

- [Contract ABI Specification](https://solidity.readthedocs.io/en/v0.5.3/abi-spec.html)
- [【Ethereum 智能合約開發筆記】深入智能合約 ABI](https://medium.com/taipei-ethereum-meetup/ethereum-%E6%99%BA%E8%83%BD%E5%90%88%E7%B4%84%E9%96%8B%E7%99%BC%E7%AD%86%E8%A8%98-%E6%B7%B1%E5%85%A5%E6%99%BA%E8%83%BD%E5%90%88%E7%B4%84-abi-268ececb70ae)
- [在區塊鏈上建立可更新的智慧合約(二)](https://medium.com/@twedusuck/%E5%9C%A8%E5%8D%80%E5%A1%8A%E9%8F%88%E4%B8%8A%E5%BB%BA%E7%AB%8B%E5%8F%AF%E6%9B%B4%E6%96%B0%E7%9A%84%E6%99%BA%E6%85%A7%E5%90%88%E7%B4%84-%E4%BA%8C-24f07206d033)
- [Ethereum Dapp初心者之路(5): 簡介Web3 Javascript API及常用操作](https://medium.com/@ksin751119/ethereum-dapp%E5%88%9D%E5%BF%83%E8%80%85%E4%B9%8B%E8%B7%AF-5-%E7%B0%A1%E4%BB%8Bweb3-javascript-api%E5%8F%8A%E5%B8%B8%E7%94%A8%E6%93%8D%E4%BD%9C-253c468450c0)
- [Truffle - 以太坊Solidity编程语言开发框架](https://truffle.tryblockchain.org/truffle3.0-integrate-nodejs.html)
- [利用工具加速Dapp建置和測試](https://medium.com/taipei-ethereum-meetup/%E5%88%A9%E7%94%A8%E5%B7%A5%E5%85%B7%E5%8A%A0%E9%80%9Fdapp%E5%BB%BA%E7%BD%AE%E5%92%8C%E6%B8%AC%E8%A9%A6-fb08e77f208e)
- [The DCS Triangle](https://blog.bigchaindb.com/the-dcs-triangle-5ce0e9e0f1dc)
