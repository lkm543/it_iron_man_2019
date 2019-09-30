在講解完昨天的2種加密法─XOR Cipher與Substitution-Permutation Network(SPN)後，我們今天要來講解Feistel Cipher與區塊加密，講解完區塊加密後，你就可以發現區塊加密其實跟區塊鏈架構是一樣的！

# Feistel Cipher
Feistel在1973所提出Feistel Cipher，幾乎被應用在所有區塊加密的演算法上(區塊加密是甚麼以下會再說明)，Feistel Cipher跟昨天提到的Substitution Permutation Network的精神很類似：用各種算法算很多輪來打散密文與明文間的關係，下圖是Feistel Cipher的演算法流程：

![Feistel Cipher](https://www.tutorialspoint.com/cryptography/images/feistel_structure.jpg)

圖片來源：[tutorialspoint](https://www.tutorialspoint.com/cryptography/)

Feistel Cipher首先會跟SPN一樣利用一把原始金鑰生成(回合數)個金鑰，隨後把明文切割成左右兩部分(L0與R0)，接著在每一回合中，依序在第N回合中對左右兩部分做：

1. 把右邊(RN)的的部分跟第N把金鑰作F函數的轉換(RN')
2. 第一步驟轉換出來的結果(RN')再和這一回合的左邊做XOR運算便是新產生的右邊(RN+1=LN⊕RN')
3. 接著再把此輪的右邊的原始資料直接當作下一輪的左邊(LN+1=RN)

與SPN相同，加解密都是利用相同的編碼方法，因此密文解密的過程即是把加密的過程反過來，即可。要注意的是F函數應該要有取代的功能(因為左右兩邊交換的過程中其實已經有置換，但沒有取代，取代應該要在F函數中被實做出來)，此外，F函數的設計也會影響到攻擊的難度，F函數越複雜，由密文拆解出明文就會越困難。

如果F函數用的是跟SPN同樣的s_box呢?這樣的話就很像我們昨天提到的SPN網路，但SPN網路在實務上比較容易被平行運算，在GPU或ASIC的運算上能夠很輕易的實現，但在嵌入式或是智慧卡上頭SPN就不太適用了。另外用s_box當作F函數其實就是我們之前提到的Data Encryption Standard(DES)。


# 串流加密 vs 區塊加密

我們到目前為止提到的加密法都是對稱式加密，對稱式加密指的是加解密用的是同一把金鑰，而對稱式加密裏頭又可以分成：串流加密(stream cipher)與區塊加密(block cipher)。

串流加密是透過固定的算法與金鑰，對明文的位元逐個做加解密，也就是同一套模式從第一個字元運算到最後一個字元，好處是運算速度快，可以隨時隨著資料的輸入而加密，通常運用在通訊上。

區塊加密則不然，每個區塊加密都有**固定長度的輸入**，也就是區塊加密每次只能加密固定長度的資料，如果要加密的資料超出區塊加密法能夠加密的上限，就把原始資料切割成許多子資料後再分別加密；如果資料長度不足則需要補齊到區塊加密法能接收的長度。我們介紹的SPN或是Feistel Cipher因為都有固定長度的輸入，因此兩者都屬於區塊加密。

目前主流的加密方法都是區塊加密了，因此我們接下來對幾種區塊加密的方法做個簡介：

## Electronic codebook(ECB)

在Electronic codebook(ECB)的模式中會根據區塊加密法每次能夠加密的資料大小把資料切割成許多獨立的區塊，每個區塊再獨立地被加解密，下面是它的流程圖：

加密
![CBC Encryption](https://upload.wikimedia.org/wikipedia/commons/c/c4/Ecb_encryption.png)

圖片來源：[Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#ECB)

解密
![CBC Decryption](https://upload.wikimedia.org/wikipedia/commons/6/66/Ecb_decryption.png)

圖片來源：[Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#ECB)

但ECB的缺陷就是包含同樣資訊的區塊會被加密成同樣的密文，使得Diffusion不足(無法保障密文與明文間的複雜)。

### 重放攻擊 

另外一個ECB模式的缺陷就是容易被**重放攻擊**(應念二聲ㄔㄨㄥˊ，重複的重)，意即因為每一個區塊都有獨立的訊息，即使攻擊者不知道加密方式與金鑰，只要攻擊者知道區塊的功能後也只需要重複傳遞該區塊，接收端便會誤認接收了多次相同的訊息，比方說其中一個區塊是匯款給他人，那麼攻擊者可以透過不斷傳遞該區塊的方式把使用者的餘額給提領光。

## Cipher-block chaining(CBC)

ECB模式的問題在於當我們紀錄連續資料時，容易被重放攻擊，同時也很難逐一驗證每個區塊資訊是否有被竄改過，因此Cipher-block chaining(CBC)便應運而生，在CBC模式中，每區塊的明文會先跟前一個密文區塊進行XOR運算後再加密。因為此時每個區塊的加密都會使用到前面所有區塊的參數，因此只要中間其中一個區塊被更改過，那麼便會輕易地被發現，下圖是它概要的加解密流程。

加密
![CBC Encryption](https://upload.wikimedia.org/wikipedia/commons/d/d3/Cbc_encryption.png)

圖片來源：[Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#ECB)

解密
![CBC Decryption](https://upload.wikimedia.org/wikipedia/commons/6/66/Cbc_decryption.png)

圖片來源：[Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#ECB)

到這裡你也可以發現：**CBC**加密其實就是Blockchain的前身，這也給我們一個線索，既然中本聰知道CBC加密，那麼中本聰自己應該就是從事密碼學相關領域的工作！

### 區塊鏈上的重放攻擊

但在區塊鏈上也有所謂的重放攻擊，因為主鏈硬分岔之後的加密演算法、私鑰、公鑰通通都相同，所以攻擊者可以重現在另一條鏈上的交易(因為簽署或密文都可以在另外一條鏈找到，找到後就可以在其他鏈上發起同樣的交易)。避免重放攻擊的方法就是讓分岔後的每條鏈有自己獨立的ID，這樣就可以讓交易只在某特定ID的鏈上能夠被廣播。

可以點選[這裡](https://www.binance.vision/zt/security/what-is-a-replay-attack)了解相關資訊，也因此**了解區塊鏈之前必須先了解密碼學**。

# 編碼、壓縮、哈希、加密的比較

終於把加密的內涵與幾個重要算法講解完畢，今日的最後讓我們簡單複習一下密碼學裏頭這四種詞彙代表的意涵：

- 編碼：**雙向轉換**資料的儲存形式或內容
- 壓縮：轉換後使資料的**儲存空間變小**，也可以解開回原先的檔案
- 哈希：**單向**把不定長度的輸入變成固定長度的輸出
- 加密：可以雙向轉換，但**只有特定的對象有辦法反向解開**而得到原本的資料

![Example](https://www.lkm543.site/it_iron_man/day10_3.jpg)

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。

# Ref:
- [維基百科-費斯妥密碼](https://zh.wikipedia.org/wiki/%E8%B4%B9%E6%96%AF%E5%A6%A5%E5%AF%86%E7%A0%81)
- [Feistel Block Cipher](https://www.tutorialspoint.com/cryptography/feistel_block_cipher.htm)
- [維基百科-資料加密標準](https://zh.wikipedia.org/wiki/%E8%B3%87%E6%96%99%E5%8A%A0%E5%AF%86%E6%A8%99%E6%BA%96)
- [<Feistel Cipher> 費斯特密文](https://wiki.kmu.edu.tw/index.php/Feistel_cipher)
- [AES五种加密模式（CBC、ECB、CTR、OCF、CFB）](https://www.cnblogs.com/starwolf/p/3365834.html)
- [区块链中，什么是重放攻击，什么是重放保护呢？](http://blockgeek.com/t/topic/1518)
