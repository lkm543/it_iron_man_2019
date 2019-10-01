# 對稱與非對稱加密

在密碼學的領域中，加密法可以根據加密、解密是否用同一把金鑰來決定，如果加解密用的是同一把鑰匙，那麼它便是`對稱式加密`，你也可以發現到目前為止我們所提到的Caesar、Monoalphabetic、Vigenère Cipher、One-Time Pad、Rail-Fence Ciphers、XOR Cipher、SPN、Feistel Cipher都是對稱式加密！如果加密、解密時用的金鑰不同則稱為`非對稱加密`，因為非對稱式加密的算法較為複雜，背後也會牽扯到數學理論，所以我們延後到這裡才做說明。

## 對稱式加密

我們之前所有提到的加密演算法裏利用同一把金鑰就可以做到加密與解密(解密其實就是把加密算法反過來做)。這麼做的好處就是相對容易運算、(~~我們下面非對稱式加密推導完之後你應該就會有感覺~~)、計算量小、所需時間也少。

安全性方面，利用`One-Time Pad`也是唯一一種理論上完全無法被解密的加密算法。但這樣做有甚麼問題跟缺陷呢？

即便演算法本身的安全性無虞，但金鑰呢？你必須先把金鑰傳遞給對方，對方才有辦法解密，但你能夠確保金鑰的傳遞過程是安全的嗎？為了確保金鑰傳遞的安全是不是要再讓金鑰加密一次、又為了確保金鑰的金鑰是安全的，是不是又要把金鑰的金鑰又加密一次變成金鑰的金鑰的金鑰......(~~你真的確定你有個安全的好方法能夠傳遞金鑰不被外洩，你就用那個方法傳遞明文不就好了~~)，所以對稱式加密的癥結點在於：**對稱式加密是安全的，但傳遞過程不是**。

## 非對稱式加密

為了解決對稱式加密傳遞的難處，非對稱式加密每次都會產生兩把鑰匙：公鑰與私鑰。

![symmetric key](https://courses.cs.ut.ee/2015/infsec/fall/uploads/Main/key_generation.png)
圖片來源：[courses.cs.ut.ee](https://courses.cs.ut.ee/)

兩把鑰匙的差別在於：**私鑰可以產出公鑰、公鑰無法產出私鑰**，因此產生的兩把鑰匙中，私鑰會放在身上、公鑰才會在外流通或傳遞，如此一來就可以避免傳遞過程中被竊聽的風險。另外因為兩把鑰匙在加密、解密上彼此可通用，因此又衍伸出兩種主要用法：

1. 公鑰加密、私鑰解密
2. 私鑰加密、公鑰解密

![Bob](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/19DfiKodi3T25Xz7g9EDTyvF9di2SzvJo6JebRJaCN-1P_.width-808.png)
圖片來源：[twillo](https://www.twilio.com/)

公鑰加密、私鑰解密的應用場景就像我們之前提過的：傳私密訊息給別人；利用別人的公鑰加密後，就可以確保持有私鑰的本人有辦法解開(上圖)。

私鑰加密、公鑰解密的就是數位簽章，透過數位簽章我們可以確保該訊息的確是由私鑰的持有人發出的，因此為了確保該筆交易是由本人發起的，每筆交易都必須經過`數位簽章`的確認。

你在[區塊鏈瀏覽器](https://etherscan.io/)上看到的一連串像亂碼般的錢包地址，就是透過非對稱加密產出的`公鑰`，每把公鑰都有相對應的`私鑰`，在必要的時候我們可以利用私鑰對訊息或交易做簽署，讓礦工確認這筆訊息或交易的確是由我們本人發出來的。

回憶一下我們之前所寫的程式碼，在發起交易前必須都必須先用私鑰簽署以證明是本人，送上鏈前礦工會根據公鑰是否能解密來確認該筆交易是否的確由私鑰持有者發出。

```python
def sign_transaction(self, transaction, private_key):
    private_key_pkcs = rsa.PrivateKey.load_pkcs1(private_key)
    transaction_str = self.transaction_to_string(transaction)
    signature = rsa.sign(transaction_str.encode('utf-8'), private_key_pkcs, 'SHA-1')
    return signature

def add_transaction(self, transaction, signature):
    public_key = '-----BEGIN RSA PUBLIC KEY-----\n'
    public_key += transaction.sender
    public_key += '\n-----END RSA PUBLIC KEY-----\n'
    public_key_pkcs = rsa.PublicKey.load_pkcs1(public_key.encode('utf-8'))
    transaction_str = self.transaction_to_string(transaction)
    if transaction.fee + transaction.amounts > self.get_balance(transaction.sender):
        print("Balance not enough!")
        return False
    try:
        # 驗證發送者
        rsa.verify(transaction_str.encode('utf-8'), signature, public_key_pkcs)
        print("Authorized successfully!")
        self.pending_transactions.append(transaction)
        return True
    except Exception:
        print("RSA Verified wrong!")
```

下面就如何產生非對稱式加密的兩大方法(RSA、ECC)做個簡單探討：
# RSA加密

`RSA(Rivest–Shamir–Adleman)加密法`是1977年由Ron Rivest、Adi Shamir、Leonard Adleman共同提出(RSA取名自三個人名字加總)，背後原理是透過一個非常大的質數難以被分解，同時兩個大質數相乘後要拆解回原本的兩質數非常困難。

## RSA公私鑰的產生

在了解RSA加密如何產生公私鑰前，必須先了解兩個名詞：`歐拉函數`與`模反元素`

- 歐拉函數φ(N)指≦N的整數中，跟N互質的個數，如果N是由兩質數p、q構成的，可以滿足：([證明](https://blog.csdn.net/LOI_QER/article/details/52862505))
> φ(N)=φ(p\*q)=(p-1)(q-1)
- 模反元素：整數a對同餘整數N的模反元素b會滿足以下公式
> ab ≡ 1 (mod N)

≡在數學裡是同餘的意思，可以理解成ab跟1除以N的餘數會一樣(也就是1)。因此整數a對同餘整數N的模反元素b又可以理解成對a找到另一個整數b，使a\*b除以N的餘數為1。

公私鑰的產生步驟如下：

1. 選擇兩個大而且相異的質數：p與q，計算N=p\*q
2. 根據[歐拉函數](https://zh.wikipedia.org/wiki/%E6%AC%A7%E6%8B%89%E5%87%BD%E6%95%B0)，求r=φ(N)=φ(p\*q)=(p-1)(q-1)
3. 選一個小於r的整數e，使e與r互質。
4. 求e對r的[模反元素](https://zh.wikipedia.org/wiki/%E6%A8%A1%E5%8F%8D%E5%85%83%E7%B4%A0)d，也就是ed ≡ 1 (mod r)
5. 銷毀p、q

這時候產生的(N、e)與(N、d)就分別是RSA加密的兩把鑰匙

在這裡為了方便舉例我們用一個很小的數來理解：

1. 使p=13、q=17，N=pq=221
2. r=(p-1)(q-1)=12\*16=192
3. 選一個小於192(r)的整數187(e)，使187(e)與192(r)互質。
4. 求187(e)對192(r)的模反元素：115(d)
5. 銷毀p、q

產生的(221、187)與(221、115)就分別是這次RSA加密的公私鑰。(模反元素可以透過[這裡](https://planetcalc.com/3311/)線上運算，integer填e、modulus填r)，現在我們得到(221、187)為公鑰、(221、115)為私鑰

## RSA加密

加密的過程中，先把要加密的訊息編碼成為一個\<N而且>0的整數，如果訊息太長就切割，接著利用下面式子把n加密成密文cipher

> cipher ≡ n^e mod(N)

如果透過公鑰(221、187)加密100這個數，就會得到cipher≡100^187 mod(221)，cipher(密文)就是9

## RSA解密

解密的過程其實就是用另一把鑰匙反過來運算

> n ≡ cipher^d mod(N)
 
如果透過另一把私鑰(221、115)解密9這個數，就會得到n≡9^115 mod(221)，n就是100，原始明文就被解出來了！所以只有在兩把鑰匙相互對應的狀況下可以互相解密，這裡示範的是公鑰加密、私鑰解密，也就是傳私訊給對方，但又確保了只有對方收的到。

## 要如何攻擊RSA?

如果攻擊者想要攻擊RSA的話，他想透過竊得的密文cipher與竊取到的整數N(221)與公鑰e(187)破解另一把私鑰d(115)，他只能透過下面這個公式：

> de ≡ 1 mod(r)

因為r=(p-1)\*(q-1)也就是代換成：

> de ≡ 1 mod((p-1)\*(q-1))

為了破解私鑰，攻擊者必須先求出p與q的值。還記得N=pq嗎？但因為N是一個非常大的數，也是由p與這q兩個非常大的質數相乘而得，這導致了N要運算回p與q非常困難，因此利用**兩個大質數相乘後很難拆解回原本的兩質數來保證了RSA的安全性**，所以N的大小也決定了加密被破解的難易度。

這裡我們就不對RSA加密法的正確性做嚴謹的證明，如果你對數學的證明有興趣可以參考[這裡](http://pajhome.org.uk/crypt/rsa/maths.html)。如果你還不是很熟悉的話，[這個網站](https://www.cryptool.org/en/cto-highlights/rsa-step-by-step)可以幫助你一步步做下來。

# 橢圓公式(Elliptic Curve Cryptography，ECC)

計算完RSA後我們可以得知：非對稱加密是透過數學運算上的不可逆來打造安全性的，同時私鑰可以很容易的產生公鑰、公鑰卻無法反推回私鑰。同樣具有這個特性的還有數學上的橢圓公式(Elliptic Curve)，而且相較於RSA，ECC可以使用更少的位元數達到比RSA更強的安全性，同時在加解密的速度上也比RSA快上許多，在寸土寸金的區塊鏈上這個特性就更加重要，因此目前幾個主流的公鏈像是Bitcoin或Ethereum裡產生公私鑰的非對稱加密主要都是透過橢圓公式來達成了。

## 橢圓公式概論

`橢圓公式`跟我們之前學的橢圓是不一樣的，典型橢圓公式的定義如下：

![https://chart.googleapis.com/chart?cht=tx&chl=y%5E2%3Dax%5E3%2Bbx%5E2%2Bcx%2Bd](https://chart.googleapis.com/chart?cht=tx&chl=y%5E2%3Dax%5E3%2Bbx%5E2%2Bcx%2Bd)

你可以在[這個網站](https://www.desmos.com/calculator)上畫出橢圓公式的圖形，比方說

![https://chart.googleapis.com/chart?cht=tx&chl=y%5E2%3Dx%5E3%2B2x%5E2-5x%2B1](https://chart.googleapis.com/chart?cht=tx&chl=y%5E2%3Dx%5E3%2B2x%5E2-5x%2B1)

就可以畫成：

![Elliptic Curve](https://www.lkm543.site/it_iron_man/day15_1.jpg)

## 橢圓公式的加法定理

這裡我們只看會用到的加法，詳細的數學運算與推導有興趣可以參考[這裡](https://www.cnblogs.com/Kalafinaian/p/7392505.html)。橢圓曲線上加法P+Q=R的定義是連接兩點P、Q的直線，可以得到與該直線相交的曲線另外一點R'，把R'的Y座標取負號得到的點就是R。

![Elliptic Curve](https://www.lkm543.site/it_iron_man/day15_2.jpg)

如果P=Q的情形下，P就代表橢圓切線上的切點，可以得到另外一點2P。同樣的2P可以繼續進行2P+P=3P來計算3P的座標。

![Elliptic Curve](https://www.lkm543.site/it_iron_man/day15_3.jpg)

## 橢圓公式的離散

在電腦科學中，資料的點不若幾何上的連續，資料點是離散的，因此我們在離散化的橢圓公式加入取餘數與同餘的概念，詳細的數學運算與推導有興趣同樣可以參考[這裡](https://www.cnblogs.com/Kalafinaian/p/7392505.html)。

這裡另外定義一個名詞"階"，指的是如果存在一個整數n，可以使np出現在無窮遠處或無法交出第三點，則n為p的"階"，如果不存在就稱p是無限階。

## 橢圓公式的不可逆

如果我們有個式子為nP=Q，P跟Q跟上面的定義一樣都是橢圓曲線上的點，N是P的階，同時n\<N(代表nP必定可以交出Q)，如果給定n與P，透過加法運算nP可以很快地取得Q。但如果反過來給的是Q與P，要計算n相當困難(實際上的p與N都會很大)。

所以對應這時候的P，n其實就是私鑰、Q點就是公鑰，要從私鑰解出公鑰非常容易，但要從公鑰反推私鑰就很困難了！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上。

# Ref:
- [對稱加密與非對稱加密優缺點詳解](https://codertw.com/%E5%89%8D%E7%AB%AF%E9%96%8B%E7%99%BC/246717/)
- [RSA算法原理（一）](https://www.ruanyifeng.com/blog/2013/06/rsa_algorithm_part_one.html)
- [Wikipedia-RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [Proof of the RSA Algorithm](https://sites.google.com/site/danzcosmos/proof-of-the-rsa-algorithm)
- [維基百科-歐拉函數](https://zh.wikipedia.org/wiki/%E6%AC%A7%E6%8B%89%E5%87%BD%E6%95%B0)
- [基礎密碼學(對稱式與非對稱式加密技術)](https://medium.com/@RiverChan/%E5%9F%BA%E7%A4%8E%E5%AF%86%E7%A2%BC%E5%AD%B8-%E5%B0%8D%E7%A8%B1%E5%BC%8F%E8%88%87%E9%9D%9E%E5%B0%8D%E7%A8%B1%E5%BC%8F%E5%8A%A0%E5%AF%86%E6%8A%80%E8%A1%93-de25fd5fa537)
- [區塊鏈中的密碼學（三）-橢圓曲線加密算法分析](https://www.itread01.com/content/1547537909.html)
- [探索橢圓曲線對](https://medium.com/cryptocow/exploring-elliptic-curve-pairings-e322a3f029e8)
- [A (Relatively Easy To Understand) Primer on Elliptic Curve Cryptography](https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/)
- [橢圓曲線加密演算法](https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/43964/)
- [橢圓曲線加密演算法](https://www.itread01.com/content/1546294330.html)
- [ECC椭圆曲线详解(有具体实例)](https://www.cnblogs.com/Kalafinaian/p/7392505.html)
