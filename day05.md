昨天遇到一個問題：如果我們未經驗證就直接把交易紀錄送上區塊鏈，那麼任意人都可以隨意移轉他人帳戶的餘額，很明顯這樣是不可以的，於是今天我們主要處理的便是驗證發起交易者的身分與權限，其中又可以分成以下三個步驟：

1. 利用RSA加密產生公、私鑰與地址
2. 利用產生的公私鑰簽章後發送交易
3. 試著跑起整個鏈並發起交易

# 非對稱式加密
區塊鏈只存在網路上，我們很明顯地無法透過身分證等文件去確認發起者的身分，因此這裡用到的是**非對稱加密**。但非對稱加密因為篇幅較長與理論較深之後會獨立一個章節做進一步的說明，這裡先簡短說明一下非對稱加密的功能。

非對稱加密會得到兩把鑰匙：公鑰與私鑰，功能很簡單就一句話

> *可以公鑰加密私鑰解密，也可以私鑰加密公鑰解密。*

也就是每個人在產生地址的時候同時會得到一把公鑰、一把私鑰，通常公鑰會釋出給對方，私鑰會自己持有以證明自己是該公鑰的持有者。

![Public Private Key](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/19DfiKodi3T25Xz7g9EDTyvF9di2SzvJo6JebRJaCN-1P_.width-808.png)
圖片來源：[twillo](https://www.twilio.com/blog/what-is-public-key-cryptography)

以上圖傳私訊給Bob為例，為了確保我所傳遞的訊息只有Bob能夠收到，因此我們使用非對稱加密來達成，步驟如下：
1. 請Bob給我他的公鑰，即便公鑰被劫走也無妨
2. 透過Bob給的公鑰加密我們要傳的訊息
3. 傳給Bob加密後的文件
4. **只有持有私鑰的Bob有能力解密該文件**

而區塊鏈驗證身分的方法恰恰與上面的例子相反，上面的例子是使用**公鑰加密**而後再用**私鑰解密**。

驗證身分則是透過私鑰把我們的交易紀錄加密，再讓外界使用公鑰解密看看，如果能夠以公鑰解密，就能夠確保這筆交易紀錄是公鑰持有人所簽核的，也就是使用**私鑰加密交易紀錄**、再使用**公鑰解密**，又稱之為**數位簽章**。

# 利用RSA加密產生公、私鑰與地址
在這裡我們使用RSA加密法隨機產生一對公私鑰，並且轉存成pkcs1形式：
```python
import rsa

def generate_address(self):
    public, private = rsa.newkeys(512)
    public_key = public.save_pkcs1()
    private_key = private.save_pkcs1()
    return self.get_address_from_public(public_key), private_key
```

我們的public_key(pkcs1)原本上的內容是這樣的

```
b'-----BEGIN RSA PUBLIC KEY-----\n
MEgCQQCC+FnLB6c50HqIU1+xHmVr2ynahARbCc3/eRFLYSDeWKbVfvpMLnrKqm/qlmOy3QXjjr15ZNSQMO+Cnn0JvnohAgMBAAE=\n
-----END RSA PUBLIC KEY-----\n'
```

我們把其中一些不必要與重複的內容過濾掉，只留下中間有意義的部分：

```python
def get_address_from_public(self, public):
    address = str(public).replace('\\n','')
    address = address.replace("b'-----BEGIN RSA PUBLIC KEY-----", '')
    address = address.replace("-----END RSA PUBLIC KEY-----'", '')
    address = address.replace(' ', '')
    print('Address:', address)
    return address
```

濾完之後剩下的部分便是它的公鑰，這時候我們可以直接把它當作地址來使用！
>MEgCQQCC+FnLB6c50HqIU1+xHmVr2ynahARbCc3/eRFLYSDeWKbVfvpMLnrKqm/qlmOy3QXjjr15ZNSQMO+Cnn0JvnohAgMBAAE=

這就是我們常看到在[Bitcoin](https://www.blockchain.com/explorer)或[Ethereum](https://etherscan.io/)上看到的一連串像是隨機位元組的地址由來了！

但到這裡你可能會有個疑問：產生的公私鑰/帳號會不會有重複的可能？  答案是：會！但是機率~0
這是密碼學中有名的生日碰撞問題(Birthday attack)，詳請可以參考[這裡](http://www.qukuai.top/d/370)還有[這裡](https://medium.com/myethacademy/%E9%8C%A2%E5%8C%85%E5%9C%B0%E5%9D%80%E6%9C%89%E6%A9%9F%E6%9C%83%E9%87%8D%E8%A4%87%E5%97%8E-be1a37337ba0)

總而言之在區塊鏈接納這筆交易前，先試著用地址反推回原本的公鑰，再用公鑰解密當初這筆交易紀錄的簽章看看，如果公鑰解的開就可以代表是公鑰持有人本人所簽核的，這便是剛剛提到的"數位簽章"。

```python
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

# 利用產生的公私鑰簽章後發送交易
產生公私鑰後，先透過`initialize_transaction`初始化一筆交易，這時候可以利用昨天寫好的`get_balance`函式先確定發送者的帳戶餘額是否足夠，初始化之後便可以透過`sign_transaction`簽署。

`initialize_transaction`與`sign_transaction`這兩個動作都是在客戶的本地端做，以避免私鑰外洩的風險。簽署好之後使用`add_transaction`把交易紀錄與簽署發到鏈上去等待礦工確認，因為我們有簽署過，所以礦工使用公鑰對簽署解密便可以確認這筆交易的確是由我們發出的。

```python
def initialize_transaction(self, sender, receiver, amount, fee, message):
    if self.get_balance(sender) < amount + fee:
        print("Balance not enough!")
        return False
    new_transaction = Transaction(sender, receiver, amount, fee, message)
    return new_transaction

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

因此實際使用上可以分成三個步驟
1. 初始化一筆交易紀錄
2. 利用私鑰簽署這筆交易
3. 送上鏈上等待礦工驗證與處理

```python
address, private = block.generate_address()

# Step1: initialize a transaction
transaction = block.initialize_transaction(address, 'test123', 1, 1, 'Test')
if transaction:
    # Step2: Sign your transaction
    signature = block.sign_transaction(transaction, private)
    # Step3: Send it to blockchain
    block.add_transaction(transaction, signature)
```

# 試著跑起整個鏈並發起交易
接著就可以跑起整條鏈了！首先先為我們自己開一個地址，接著創造創世塊。然後便可以不停地挖掘新區塊→調整難度→挖掘新區塊→調整難度→....周而復始，而且中間還可以發起交易！

```python
def start(self):
    address, private = self.generate_address()
    self.create_genesis_block()
    while(True):            
        # Step1: initialize a transaction
        transaction = block.initialize_transaction(address, 'test123', 1, 1, 'Test')
        if transaction:
            # Step2: Sign your transaction
            signature = block.sign_transaction(transaction, private)
            # Step3: Send it to blockchain
            block.add_transaction(transaction, signature)
        self.mine_block(address)
        print(self.get_balance(address))
        self.adjust_difficulty()
```

# 今天的問題
但我們的區塊鏈還少了一個必要的東西：P2P網路，我們的區塊鏈沒辦法接收其他人的請求，只能在本機端跑，因此我們明天就會來透過通訊把我們的區塊鏈區分成：節點端(礦工端)與客戶端！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，至於今天程式碼則放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day05.py)。

# Ref
- [计算：虚拟币详细地址撞击几率](https://www.biboss.com/gonglue/84806.html)
- [錢包地址有機會重複嗎？](https://medium.com/myethacademy/%E9%8C%A2%E5%8C%85%E5%9C%B0%E5%9D%80%E6%9C%89%E6%A9%9F%E6%9C%83%E9%87%8D%E8%A4%87%E5%97%8E-be1a37337ba0)
- [網路安全(1) - 基礎密碼學](https://blog.techbridge.cc/2017/04/16/simple-cryptography/)
- [維基百科-數位簽章](https://zh.wikipedia.org/wiki/%E6%95%B8%E4%BD%8D%E7%B0%BD%E7%AB%A0)
- [不用數學，一張圖了解公鑰加密法原理](https://www.thenewslens.com/article/31591)
- [What is Public Key Cryptography?](https://www.twilio.com/blog/what-is-public-key-cryptography)
