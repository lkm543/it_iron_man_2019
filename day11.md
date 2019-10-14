# 比昨天稍微現代一點的加密
奠定現代密碼學的兩大基柱分別是取代-重排網路與費斯妥密碼：

- 取代-重排網路(Substitution-Permutation Network)
- 費斯妥密碼(Feistel Cipher)

這兩者可說是現在密碼學的扛霸子，幾乎所有現代密碼學的演算法裡或多或少都可以看到他們的足跡，而明天要介紹的區塊加密法(block cipher)則利用了這兩者的精神加以延伸，雖然感覺我們跟區塊鏈離得越來越遠，但實際上區塊鏈就是區塊加密法(block cipher)的一種變體，所以要了解區塊鏈裏頭的各種名詞，不可不從加密開始。

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

# Substitution-Permutation Network(SPN)
SPN是Claude Shannon在1949年提出，Claude Shannon認為一個好的加密方法必須有這兩種特色：

> Diffusion：將密文中有可能出現的統計結構消除，同時明文的一點小改變會讓密文產生很大的變化
> Confusion：複雜化密文與金鑰間的關係

我們昨天提到的One-Time Pad有這兩個特色，所以`One-Time Pad`也是唯一在金鑰安全的狀態下無法被解密的加密方法。至於為什麼要`Diffusion`與`Confusion`呢？

Diffusion是為了避免密文可以透過詞頻等分析被解出來，就像是昨日我們提到的Monoalphabetic，即便Monoalphabetic在金鑰的複雜度上幾不可能被破譯，但是詞頻的統計結構可以逐步解開我們的轉換表，為了避免攻擊者可以透過語言中會出現的統計結構來破譯，所以在密文中出現的統計結構必須被消除。同時為了避免傳遞兩段類似文字的情形中被猜出加密方式與密鑰，也期望即便明文只有一些小變動也會使密文產生很大的變化。

Confusion是為了讓密文看起來更像隨機、無法被讀取，同時在金鑰洩漏的狀況下能夠有多一層保障，只要密文與金鑰間夠複雜，攻擊者只能不斷嘗試各種加密方式來是突破譯。

Diffusion跟Confusion兩者都是為了避免攻擊者在知道密文與明文的狀態下可以解出加密方式與金鑰，這種情形又可以稱之為[known-plaintext attack](https://en.wikipedia.org/wiki/Known-plaintext_attack)。

下面是一個基本的SPN算法，其中主要有代換、置換和輪金鑰混合三個步驟，在這裡我們先簡介一下代換、置換：

- 代換：把明文的字母用另一個字母替換，我們昨日提到的Monoalphabetic就是代換法的應用。

- 置換：調動字母的順序，我們昨日提到的Rail-Fence Ciphers就是置換法的應用。

SPN的想法其實很好理解，既然單次的代換與置換都很容易被破譯，那麼代換跟置換都用總行了吧？單輪不夠的話，那重複加密很多輪，那如何解密呢？其實一樣解密很多輪就可以把最原始的明文解出來。

![SPN](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/SubstitutionPermutationNetwork2.png/540px-SubstitutionPermutationNetwork2.png)

## SPN演算法實作

SPN演算法每次的輸入明文是固定的，為了簡化與方便後續的運算與表達，我們這裡把輸入SPN算法的位元數設定在16個位元。流程大概跟上圖顯示的一樣：

> 明文→XOR Cipher(→S-boxes→P-boxes→XOR Cipher)*n→S-boxes→P-boxes→XOR Cipher→密文

其中(→S-boxes→P-boxes→XOR Cipher)\*n代表的是我們要重複做幾輪加密

### XOR Cipher

在`XOR Cipher`這裡我們可以直接把昨天寫好的函式拿過來使用。分別處理：產生金鑰、XOR運算、XOR加解密。只是因為SPN會做多組的XOR Cipher，所以SPN金鑰的產生方式是透過一組最初始的金鑰產生另外(回合數+1)組16bits的金鑰。

```python
def generate_key(key, rounds):
    key += key
    keys = []
    for idx in range(rounds):
        key_this_round = key[4*idx+4:4*idx+20]
        keys.append(key_this_round)
    return keys

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

### S-boxes(替換盒)

替換盒這裡我們可以先產生一個隨機數列`s_box`，這個數列裏頭有0-15隨機散布而且不重複，它看起來會長成這樣：

> s_box = [4, 6, 15, 12, 5, 1, 3, 11, 14, 13, 0, 7, 9, 10, 8, 2]

這個數列的意思是：1用5替換掉、2用7替換掉、3用16替換掉....(記得索引值從0開始)，於是我們就可以進行替換了！實作方法如下：

```python
def substitution(input, s_box):
    output = ""
    for idx in range(4):
        data = input[4*idx:4*(idx+1)]
        number = int(data, 2)
        number_substitution = s_box[number]
        # Convert to binary string
        # ex: 9 -> "1001"
        binary_number = ""
        for i in range(3, -1, -1):
            binary_number += str((number_substitution >> i) & 1)

        output += binary_number
    return output
```

### P-boxes(排列盒)

排列盒這裡我們跟s_box用同樣方法產生一個隨機數列`p_box`：

> p_box = [13, 3, 12, 1, 9, 8, 15, 4, 6, 5, 10, 14, 2, 0, 11, 7]

這代表：第1個bit要移動到第14個bit、第2個bit要移動到第4個bit、第3個bit要移動到第13個bit....實作方法如下

``` python
def permutation(input, p_box):
    output = list("0" * 16)
    for idx, value in enumerate(p_box):
        output[value] = input[idx]
    return "".join(output)
```

### 加密：重複XOR Cipher→S-boxes→P-boxes的步驟

加密的過程中就不斷重複XOR Cipher→S-boxes→P-boxes的過程，每次進入XOR-Cipher的金鑰都不一樣，但每次s_box、p_box的參數都相同，注意這裡會因為XOR的步驟會因為頭尾都作而比s_box與p_box多進行一次。

```python
def spn_encrypt(text, rounds, key, s_box, p_box):
    output = text
    for idx in range(rounds):
        output = xor_en_decrypt(output, key[idx])
        output = substitution(output, s_box)
        output = permutation(output, p_box)
    output = xor_en_decrypt(output, key[rounds])
    return output
```

### 解密：把加密的過程倒置過來

這裡有兩點需要注意：xor_cipher使用的key必須倒置、s_box與p_box的參數也必須互換(原本如果是1替換成4，現在必須把4替換回1)，把加密的過程反過來作就可以解密了！

```python
def spn_decrypt(text, rounds, key, s_box, p_box):
    output = text
    s_box_inverse = [0]*16
    p_box_inverse = [0]*16
    for idx in range(16):
        s_box_inverse[s_box[idx]] = idx
        p_box_inverse[p_box[idx]] = idx
    for idx in range(rounds):
        output = xor_en_decrypt(output, key[rounds-idx])
        output = permutation(output, p_box_inverse)
        output = substitution(output, s_box_inverse)
    output = xor_en_decrypt(output, key[0])
    return output
```

### 測試一下加解密

到這裡就可以測試我們的代換─置換網路是否可以正常運作了！

```python
if __name__ == '__main__':
    rounds = 3
    key = "1011101000111110"
    keys = generate_key(key, rounds + 1)
    print(f"初始金鑰： {key}")
    print(f"產生金鑰： {keys}")

    s_box = random.sample(range(0, 16), 16)
    print(f"s_box： {s_box}")
    p_box = random.sample(range(0, 16), 16)
    print(f"p_box： {p_box}")

    message = "1001001110100101"
    print(f"原始明文： {message}")
    encryption = spn_encrypt(message, rounds, keys, s_box, p_box)
    print(f"加密密文： {encryption}")
    decryption = spn_decrypt(encryption, rounds, keys, s_box, p_box)
    print(f"原始明文： {decryption}")
```

![SPN Demo](https://www.lkm543.site/it_iron_man/day12_1.jpg)

## 那SPN有滿足Diffusion跟Confusion嗎？

首先回憶一下Diffusion跟Confusion這兩個詞代表的意思：

> Diffusion：將密文中有可能出現的統計結構消除，同時明文的一點小改變會讓密文產生很大的變化
> Confusion：複雜化密文與金鑰間的關係

首先是Diffusion，想像一下如果我們僅改變輸入明文的其中一個bit，則這個bit會被餵到s-box做替換，使跟這個bit同一組的數個bits通通被換掉，而後被傳入p-box做重新排序，等於所有的bit都有機會被更動到，而後又進到下一輪開始的s-box，如果其中只有一個位元被更動，那麼輸出的位元仍然會有相當大的變化！光說沒證據，那麼我們簡單用上面的程式碼做個實驗：

> 原始明文： 1001001110100101
> 加密密文： 0010000011101100
> 原始明文： 1001001110100111
> 加密密文： 1101110001110000

這裡我們對明文只做了一個bit的更動：1001001110100101→1001001110100111，但密文卻從0010000011101100→1101110001110000整整改變了10個bit！

Confusion的理由跟Diffusion類似，因為裏頭的bit通通被替換與重新排序了，密文與金鑰間的關係對外界來說自然是幾不可考了！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，至於今天的程式碼則放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day12.py)。

# SPN與區塊鏈

到這裡我們可以發現SPN每次能夠加密的長度都是固定的！而且SPN透過了多輪重複的加密來大幅提升破譯難度，這兩種特色也會在明天區塊加密中的介紹被提及，屆時就可以發現區塊鏈並不是一夕之間被發明出來的新技術，背後是由許多傳統的技術積累而構成的！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，至於今天的XOR程式碼則放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day11_XOR.py)，SPN程式碼則放[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day11_SPN.py)。
# Ref:
- [維基百科-互斥或密碼](https://zh.wikipedia.org/wiki/%E5%BC%82%E6%88%96%E5%AF%86%E7%A0%81)
- [Chapter 2: 密碼學基礎](http://140.125.45.29/courses/files/network%20security/network%20security%20ch%202.pdf)
- [維基百科-代換-置換網路](https://zh.wikipedia.org/wiki/%E4%BB%A3%E6%8D%A2-%E7%BD%AE%E6%8D%A2%E7%BD%91%E7%BB%9C)
- [密码学入门（一）：用Python实现对称加密算法](https://zhuanlan.zhihu.com/p/36262011)
