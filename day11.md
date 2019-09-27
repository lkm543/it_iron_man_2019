# 比昨天稍微現代一點的加密
奠定現代密碼學的兩大基柱分別是取代-重排網路與費斯妥密碼：

- 取代-重排網路(Substitution-Permutation Network)
- 費斯妥密碼(Feistel Cipher)

這兩者可說是現在密碼學的扛霸子，幾乎所有現代密碼學的演算法裡或多或少都可以看到他們的足跡，而未來幾天要介紹的區塊加密法(block cipher)則利用了這兩者的精神加以延伸，雖然感覺我們跟區塊鏈離得越來越遠，但實際上區塊鏈就是區塊加密法(block cipher)的一種變體，所以要了解區塊鏈裏頭的各種名詞，不可不從加密開始。

首先我們先來簡單聊聊現代幾種加密的標準。

## Data Encryption Standard(DES)

DES使用7個8位元大小的位元組共56位元作為金鑰內容，也屬於區塊式密碼(block cipher，意即每次加密的長度是固定的，我們之後會再提及)，每次的輸入能夠加密64位元的明文，加密過程共有16輪，每輪都使用演算法從金鑰產生不同的子金鑰(subkey)來加密，也在1977年被美國國家標準局製定為標準，下面是DES加密的大概流程。

![DES](https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/DES-key-schedule.png/250px-DES-key-schedule.png)

圖片來源：[維基百科](https://zh.wikipedia.org/wiki/%E8%B3%87%E6%96%99%E5%8A%A0%E5%AF%86%E6%A8%99%E6%BA%96)

### Triple DES(3DES)

但隨著電腦硬體的飛速進步，早在1997年6月，Rocke Verser、Matt Curtin、Justin Dolske團隊就能透過暴力運算所有金鑰的2^56次方種可能來破解DES加密，1999年甚至有人能夠在一天內的時間就破解DES加密。DES此時非常需要一個替代方案來取代，但新方案的出現需要經過密碼學者的驗證與研究，產生新演算法的標準耗時而緩不濟急，因此過渡方案便是透過重複利用三次的DES加密、同時也把金鑰長度變成三倍，藉此在過渡階段避免對DES的攻擊。

## Advanced Encryption Standard加密(AES)

因為過往的標準DES已無法提供足夠的安全性，國家標準暨技術研究院(National INstitute of Standards and Technology，NIST)在1997年9月12日向密碼學界徵求能夠替代DES的加密演算法，經過3年的驗證以後，Rijndael演算法最後入選成為進階加密標準(Advanced Encryption Standard，AES)。

也因為AES採用Rijndael演算法，所以AES有兩意義：標準或演算法。如果AES指的是演算法時，那麼AES演算法就是Rijndael演算法。

### Rijndael演算法

Rijndael演算法由比利時學者Joan Daemen和Vincent Rijmen提出，因此Rijndael演算法的名稱就來自於兩位學者名字的融合，其特色是基於明天我們會詳細提到的`代換-置換網路(Substitution-permutation network，SPN)`的加密演算。也就是原始的明文會透過多次的加密與轉換後生成密文，大部分的加密演算法也都會透過重複多輪的加密與轉換來增加加密的安全性。

## XOR Cipher

在之後講到現代加密的`Substitution-Permutation Network`與`Feistel Cipher`前，不可不提到兩者都會用到的XOR加密，XOR加密法利用的就是任何一段文字被另一段文字XOR運算兩次後會得到原本的文字，這種加密法的好處就是因為只有XOR運算，容易運算、運算快速、電路上容易實現、成本也小，下面的公式描述了這個現象，我們可以把裏頭的A看作是要傳遞的明文、B是加解密用的金鑰、C是加密後的密文

> A⊕B=C           C⊕B=A

用實際例子來看的話就是下面這張圖，每次加密我們都隨機產生一個金鑰，再利用金鑰與原始文字作XOR運算得到加密後的密文。傳遞之後接收端可以再讓密文與金鑰作另一次XOR運算得到原本的明文。

![XOR Cipher](https://www.lkm543.site/it_iron_man/day11_1.png)

在這裡金鑰可以粗分成兩種：金鑰長度小於訊息、金鑰長度與訊息等長，如果金鑰長度小於訊息長度，代表我們會重複利用該筆金鑰作XOR運算，這時候利用字頻的分析就可以破解XOR加密，但如果金鑰與訊息等長，那其實就跟我們昨天提到的`One-Time Pad`一樣，理論上是不可被破解的。

下面是XOR加密法的簡單實作：這裡我們為了之後顯示位元組的方便，先準備兩個函式可以把字串轉換成位元組01構成的字串。

```python
def string_to_bytes(input):
    input = bytearray(input, 'utf-8')
    result = ""
    for byte in input:
        for i in range(7, -1, -1):
            result += str((byte >> i) & 1)
    return result

def bytes_to_string(input):
    result = ""
    for idx in range(0, int(len(input)/8)):
        binary = input[8*idx:8*(idx+1)]
        result += chr(int(binary, 2))
    return result
```

接著產生金鑰，金鑰的產生由簡單的0跟1所構成，根據需要的長度產生。接著便可以進行XOR的運算，如果兩個輸入不同，則輸出1，兩個輸入值相同則輸出0。最後就可以用XOR來加解密了！注意這裡因為金鑰的長度有可能小於訊息長度，所以一旦處理到超出金鑰的長度，就從金鑰的頭開始重新使用金鑰。

```python
import random

def generate_key(length):
    key = ""
    for i in range(0, length):
        key += str(random.randint(0, 1))
    return key

def xor_operation(text, key):
    if text == key:
        return "0"
    else:
        return "1"

def xor_en_decrypt(text, key):
    result = ""
    len_txt = len(text)
    len_key = len(key)
    for idx in range(0, len_txt):
        if idx >= len_key:
            key_idx = idx % len_key
        else:
            key_idx = idx
        xor_result = xor_operation(text[idx], key[key_idx])
        result += xor_result
    return result
```

最後就可以來實作看看啦，先隨意給定一個我們想加密的訊息，接著根據訊息長度產生金鑰，再讓訊息與金鑰進行XOR運算便可以得到密文。要解密的話也是一樣，讓密文與金鑰作XOR運算，就可以得到原本的密文。

```python
if __name__ == "__main__":
    message = "XOR Cipher!"
    print(f"Origin message: {message}")
    message = string_to_bytes(message)
    print(f"Message in binary: {message}")

    key = generate_key(len(message))
    print(f"Key: {key}")

    encryption = xor_en_decrypt(message, key)
    print(f"Encryption: {encryption}")

    decryption = xor_en_decrypt(encryption, key)
    print(f"Decryption: {decryption}")

    text = bytes_to_string(decryption)
    print(f"Text: {text}")
```

實際運行結果如下：

![XOR Demo](https://www.lkm543.site/it_iron_man/day11_2.jpg)

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，至於今天的程式碼則放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day11.py)。
# Ref:
- [維基百科-互斥或密碼](https://zh.wikipedia.org/wiki/%E5%BC%82%E6%88%96%E5%AF%86%E7%A0%81)
- [維基百科-3DES](https://zh.wikipedia.org/wiki/3DES)
- [Chapter 2: 密碼學基礎](http://140.125.45.29/courses/files/network%20security/network%20security%20ch%202.pdf)
- [DES 数据加密标准 结构详解](https://blog.csdn.net/jerry81333/article/details/78091145)
- [AES標準及Rijndael演算法解析](https://www.itread01.com/content/1541892089.html)
- [ 你的網路資訊真的安全嗎？美國政府公定「資料加密標準」首度被破解](https://panx.asia/archives/51155)
