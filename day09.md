我們昨天提到了四個下面名詞，並且已經解釋完編碼與壓縮：

1. 編碼
2. 壓縮
3. 哈希(湊雜)
4. 加密

在正式進入密碼學之前我們接著介紹：**哈希**

# 哈希(湊雜)
我們在[Day03|打造一個簡易的區塊鏈(2)：產生創世塊與挖掘新區塊](https://ithelp.ithome.com.tw/articles/10215088)中有稍微介紹一下哈希數：

![Hash](https://www.lkm543.site/it_iron_man/day3_1.jpg)

簡而言之哈希可以把**任意長度的輸入轉換成固定長度的輸出，而且無法被逆轉換**，跟昨天我們提到的編碼做比較：編碼可以完全轉換回原本的詞彙，但是哈希不行，**哈希數的轉換是單向的**！

## 哈希在區塊鏈上的功能

### 工作量證明(Proof of Work，POW)

回憶一下我們之前是這樣挖掘新區塊的：透過不斷修改nonce值後重新計算hash數，直到我們找出來的hash數符合當下的難度為止。

```python
while new_block.hash[0: self.difficulty] != '0' * self.difficulty:
    new_block.nonce += 1
    new_block.hash = self.get_hash(new_block, new_block.nonce)
```

利用哈希函數的單向性，讓礦工只能不停地去產生新的輸入(`nonce`)後，期望能夠找到一個能夠符合的解；並無法透過已知的難度去反推符合的nonce值。

### 驗證區塊

因為哈希函式單向轉換的特性，我們可以把區塊哈希數生成的其中一個參數仰賴於前一個區塊，像鎖鏈般把所有區塊結合在一起(回憶一下之前出現過的下圖)，這樣只要某一個區塊被攻擊或竄改，透過很快的計算哈希數與驗證，我們就可以輕易揪出是哪個區塊被攻擊了！而且因為工作量證明(POW)的機制，如果攻擊者想要重新計算哈希鏈來讓驗證可以通過，因為哈希函式單向運算的保障，攻擊者需要耗費龐大的運算資源才能做到。

![Hash Chain](https://www.lkm543.site/it_iron_man/day2_3.jpg)

回憶一下我們之前可以這樣驗證鏈上的資料是否有被竄改過：

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

### 驗證單筆交易

為了驗證單筆交易的真偽，我們可以把該筆交易的明細也透過哈希函式轉換成一個哈希數，接著只要向節點索取區塊內的交易哈希數便可以驗證該筆交易的真偽，而不需要向節點同步所有資料。關於如何改進單筆交易的驗證效率，我們之後提到Merkle Tree時會更進一步地說明Bitcoin的交易驗證機制。

## 哈希的其他功能

除了區塊鏈之外，在電腦科學的領域中也會大量使用到哈希函式。

### 確保下載的資料沒有被竄改

![Ubuntu Hash](https://www.lkm543.site/it_iron_man/day9_1.jpg)

網路上我們常常會互傳檔案，或是直接從網站上把資料下載下來，於是有心人士可以故意把惡意軟體包裝成正常軟體供人在網路上流傳，為了避免這類事情發生，開發者可以把軟體事先利用哈希函式轉換出一個哈希數：

> f800c84a4fac2ee698d1b8ec49c3c6dd13c3cca4

如此一來如果有人造假軟體在其他地方流傳，它所提供的檔案算出來的哈希數就會是不同的哈希數，像是：

> ea010ee53036c72c7932dad62065a292f3226bf5

於是就可以很輕易的被發現這個檔案是被造假過，並非原始檔案。例如你可以到[Ubuntu的下載頁面](https://releases.ubuntu.com/bionic/)，會發現許多MD5、SHA開頭的檔案：

![Ubuntu Hash](https://www.lkm543.site/it_iron_man/day9_2.jpg)

要檢測/驗證的話，可以到[這裡](https://briian.com/6457/)下載檢測器，或是到[這裡](https://vitux.com/how-to-verify-download-in-ubuntu-with-sha256-hash-gpg-key/)有完整的驗證教學。

### 保護原始資料

平時登入網站所使用的帳號密碼都應該要被網站管理者好好保存，其中一個必備的條件是：密碼的儲存永遠不該是明文儲存，如果以明文儲存的話一旦資料庫被竊取則所有使用者的密碼都會被看光光，然後通常....大部分使用者在各個網站使用的密碼都是一樣的，所以一旦資料庫被竊取，駭客便可以輕鬆地拿著竊取到的帳號跟密碼到各個網站去登入了。

比方說我們的密碼如果是*a1Sna6!g2*，那麼**網站的資料庫永遠不應該直接儲存明文***a1Sna6!g2*！

而是儲存透過哈希函式像是SHA-256轉換出的哈希數，像是

> 7e5a1428400e9c5576ef9ff7538ee6257ebecaede29d5e0bd48237f5ef05cd1d

把這段文字儲存進資料庫裏頭，即便資料庫被竊取，駭客手上也只能拿到這段加密後的文字，也無法得知原本的密碼是多少。你可能會有個疑問，那麼我要怎麼驗證使用者輸入的密碼就是當初的密碼呢？其實我們只要再次把使用者登入當下輸入的密碼再轉換一次哈希數，如果轉出來的哈希數一樣，幾乎就可以代表使用者輸入的是正確的密碼了(還記得不同輸入值，輸出成同一個哈希數的機率\~0嗎?)！

不過因為通常哈希數都會遠遠比使用者的密碼還長，所以網路上也很多利用常見的文字或密碼轉換出哈希數後再記錄下來的資料庫，例如你可以在[這個網站](https://hashkiller.co.uk/Cracker/MD5)輸入MD5的值，它會幫你找是否有相對應的原始資料存在。如果你輸入下面這個MD5密文：

> 827ccb0eea8a706c4c34a16891f84e7b

你會發現轉出來是12345，因為12345太多人用啦！所以本身密碼的複雜度也是相當重要！另一個小技巧是加鹽：

![Salt](https://i.imgur.com/RKTIIUX.jpg)
圖片來源：[imgur圖床](https://imgur.com/)

喔，不是這種加鹽。密碼學中的加鹽(salt)指的是在把使用者的密碼轉換成密文前多做一些小改變，比如說我們在使用者輸入的密碼前後各加上!a!，變成!a!12345!a!再丟進去算哈希，算出來的哈希數就會完全不一樣了！變成：

> 5b839893d2ad60d14de1102151f0381d

就可以發現即便使用者用一個很簡單的密碼，經過我們的加鹽之後，在[這個網站](https://hashkiller.co.uk/Cracker/MD5)又解不出來了，於是使用者的密碼又多一層保障！

### 哈希表(Hash Table)

![Hash table](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Hash_table_3_1_1_0_1_0_0_SP.svg/315px-Hash_table_3_1_1_0_1_0_0_SP.svg.png)
圖片來源：[維基百科](https://en.wikipedia.org/wiki/Hash_table)

如果你有學過演算法的話~~這裡就可以跳過~~，打個比方來說，Facebook上頭假設有100億個帳號(畢竟現在網軍或分身氾濫)，如果帳號密碼是用陣列儲存的話，那麼我們每次登入都要從第一個帳號往下找直到找到我們的帳號對應到的密碼為止，平均要找50億次，很明顯的效率不佳。

而哈希函數可以幫助你直接把使用者的帳號轉換成一個數字，這個數字就代表它在陣列中的索引值，因此就不需要一個個往下找了！關於哈希表的詳情可以參考[這裡](https://blog.techbridge.cc/2017/01/21/simple-hash-table-intro/)。

## 自製一個簡單的哈希函式

我們簡單製作一個哈希函式，這裡我們哈希函式的定義與步驟是：

1. 哈希數從512開始
2. 哈希數乘上逐個字元的ascii碼
3. 哈希數加上3
4. 哈希數除以1024取餘數
5. 重複步驟2~4直到每個字元都處理完
6. 哈希數乘上字串長度
7. 哈希數除以1024取餘數

```python
def hash(input):
    hash_number = 512
    for char in input:
        hash_number *= ord(char)
        hash_number += 3
        hash_number %= 1024
    hash_number *= len(input)
    hash_number %= 1024
    return hash_number

if __name__ == "__main__":
    print(hash("Hello World!"))
    print(hash("Bill Gates"))
    print(hash("100000000"))
```

於是三種字串的輸入"Hello World!"、"Bill Gates"、"100000000"，分別會得到哈希數280、610、43了！而且哈希數280、610、43並沒有辦法反推回原本的輸入！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，今天哈希函式的程式碼放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day09.py)。
# Ref:
- [資訊與網路安全概論-粘添壽](http://www.tsnien.idv.tw/Security_WebBook/%E7%AC%AC%E5%9B%9B%E7%AB%A0%20%E9%9B%9C%E6%B9%8A%E8%88%87%E4%BA%82%E6%95%B8%E6%BC%94%E7%AE%97%E6%B3%95.html)
- [維基百科-雜湊函式](https://zh.wikipedia.org/wiki/%E6%95%A3%E5%88%97%E5%87%BD%E6%95%B8)
- [What Is Hashing?](https://blockgeeks.com/guides/what-is-hashing/)
