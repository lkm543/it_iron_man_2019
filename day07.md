# 節點的建置

我們昨天已經能夠讓使用者端與節點端彼此溝通，而且能夠讓使用者在不需要儲存所有交易明細的狀況下向節點查詢餘額或是發起交易，但我們的節點也只有一個，在這個狀況下其實運作方式跟傳統中心化的方式並無差異。

因此今天的目的是要讓外界的人可以自由加入節點的運作與挖掘新區塊，在這過程中也牽涉到區塊或交易的廣播(必須把收到的新資訊廣播給彼此，區塊鏈裡的資料才會一致)，這一步完成後我們的簡易區塊鏈也就大功告成了！

## 同步區塊

為了與已經上線運作的區塊鏈同步，需要向已知的節點發起請求，要求節點將目前所有的資料都傳遞過來。因為我們選用的是Stream Socket，接收到的資料是連續的，為了避免資料流斷開因此直到讀到`len(response) % 4096`不為零才停止。(但其實會有Bug，但因為機率很小只有1/4096這裡先忽略)。接收到資料後就把目前鏈上的資料同步。

```python
def clone_blockchain(self, address):
    print(f"Start to clone blockchain by {address}")
    target_host = address.split(":")[0]
    target_port = int(address.split(":")[1])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    message = {"request": "clone_blockchain"}
    client.send(pickle.dumps(message))
    response = b""
    print(f"Start to receive blockchain data by {address}")
    while True:
        response += client.recv(4096)
        if len(response) % 4096:
            break
    client.close()
    response = pickle.loads(response)["blockchain_data"]

    self.adjust_difficulty_blocks = response.adjust_difficulty_blocks
    self.difficulty = response.difficulty
    self.block_time = response.block_time
    self.miner_rewards = response.miner_rewards
    self.block_limitation = response.block_limitation
    self.chain = response.chain
    self.pending_transactions = response.pending_transactions
    self.node_address.update(response.node_address)
```

實務上也是如此，你可以到[這裡](https://bitnodes.earn.com/nodes/?q=Satoshi:0.18.0)查閱Bitcoin所有節點的資料，並且向這些節點發出請求！

## 接受並判別訊息

接收資訊那裏，我們也需要新增收到其他節點的資訊後應該要做的處置，分別有下面四種：

1. 接收到同步區塊的請求─把目前的區塊鏈上的資料都dump一份給對方
2. 接收到挖掘出的新區塊─確認是否有符合Hash的規則，有的話就把它加入鏈上，改挖掘下一區塊
3. 接收到廣播的交易─把交易置入等待中的交易`pending_transactions`
4. 接收到新增節點的請求─把位置加到之後要廣播的清單中

```python
# 接收到同步區塊的請求
elif parsed_message["request"] == "clone_blockchain":
    print(f"[*] Receive blockchain clone request by {address}...")
    message = {
        "request": "upload_blockchain",
        "blockchain_data": self
    }
    connection.sendall(pickle.dumps(message))
    continue
# 接收到挖掘出的新區塊
elif parsed_message["request"] == "broadcast_block":
    print(f"[*] Receive block broadcast by {address}...")
    self.receive_broadcast_block(parsed_message["data"])
    continue
# 接收到廣播的交易
elif parsed_message["request"] == "broadcast_transaction":
    print(f"[*] Receive transaction broadcast by {address}...")
    self.pending_transactions.append(parsed_message["data"])
    continue
# 接收到新增節點的請求
elif parsed_message["request"] == "add_node":
    print(f"[*] Receive add_node broadcast by {address}...")
    self.node_address.add(parsed_message["data"])
    continue
```

## 接收並驗證廣播的區塊

一旦接收到新區塊，必須對區塊的內容與哈希加以驗證，確認資料格式是正確的！同時也要把裏頭被打包好的交易從自身等待中的交易`pending_transactions`移除，否則該筆交易就會被執行兩次！

```python
def receive_broadcast_block(self, block_data):
    last_block = self.chain[-1]
    # Check the hash of received block
    if block_data.previous_hash != last_block.hash:
        print("[**] Received block error: Previous hash not matched!")
        return False
    elif block_data.difficulty != self.difficulty:
        print("[**] Received block error: Difficulty not matched!")
        return False
    elif block_data.hash != self.get_hash(block_data, block_data.nonce):
        print(block_data.hash)
        print("[**] Received block error: Hash calculation not matched!")
        return False
    else:
        if block_data.hash[0: self.difficulty] == '0' * self.difficulty:
            for transaction in block_data.transactions:
                self.pending_transaction.remove(transaction)
            self.receive_verified_block = True
            self.chain.append(block_data)
            return True
        else:
            print(f"[**] Received block error: Hash not matched by diff!")
            return False
```

## 如果廣播的區塊驗證通過，改挖掘下一塊

如果通過上一步的驗證，則本地端的挖掘工作必須暫停，直接挖掘下一個新區塊。在這裡我們也修改nonce的產生方式，不再是統一由1開始逐漸+1，否則永遠都會是算力最高的節點會挖到。

```python
def mine_block(self, miner):
    start = time.process_time()

    last_block = self.chain[-1]
    new_block = Block(last_block.hash, self.difficulty, miner, self.miner_rewards)

    self.add_transaction_to_block(new_block)
    new_block.previous_hash = last_block.hash
    new_block.difficulty = self.difficulty
    new_block.hash = self.get_hash(new_block, new_block.nonce)
    new_block.nonce = random.getrandbits(32)

    while new_block.hash[0: self.difficulty] != '0' * self.difficulty:
        new_block.nonce += 1
        new_block.hash = self.get_hash(new_block, new_block.nonce)
        if self.receive_verified_block:
            print(f"[**] Verified received block. Mine next!")
            self.receive_verified_block = False
            return False

    self.broadcast_block(new_block)

    time_consumed = round(time.process_time() - start, 5)
    print(f"Hash: {new_block.hash} @ diff {self.difficulty}; {time_consumed}s")
    self.chain.append(new_block)
```

## 挖掘到新區塊，廣播給其他節點

如果是自身挖到新區塊的話，就要把這個新區塊廣播給其他節點囉！

```python
def broadcast_block(self, new_block):
    self.broadcast_message_to_nodes("broadcast_block", new_block)

def broadcast_message_to_nodes(self, request, data=None):
    address_concat = self.socket_host + ":" + str(self.socket_port)
    message = {
        "request": request,
        "data": data
    }
    for node_address in self.node_address:
        if node_address != address_concat:
            target_host = node_address.split(":")[0]
            target_port = int(node_address.split(":")[1])
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((target_host, target_port))
            client.sendall(pickle.dumps(message))
            client.close()
```

## 執行我們的區塊鏈與雙節點

首先我們運行第一個節點，並指明它的port為1111

> python .\Blockchain.py 1111

接著可以運行第二個節點，並指明它的port為1112、請它去連接與同步127.0.0.1:1111。

> python .\Blockchain.py 1112 127.0.0.1:1111

接著就可以看到兩邊不停地交換挖掘到的新區塊了！

![Demo](https://www.lkm543.site/it_iron_man/day7_1.JPG)

# 現實中的網路

雖然我們透過socket來模擬現實網路的通訊，但與真正的網路還是有些差距，以下稍微敘述一下其中較大的差異與挑戰，我們之後會再有幾天專門介紹網路的相關資訊(特別是P2P的網路)，在加入網路後，更多問題會接踵而來：網路延遲如何處理？共識如何決定、分岔等等的。


## 網路的延遲

在網路交換訊息的過程中延遲是不可避免的，也就是自廣播到接收會有一段時間落差、甚至資訊的遺失，這些落差與資訊遺失會造成礦工間的異議與區塊鏈的分岔，分岔的產生主要有兩種原因：

1. 沒有完整收到別人廣播的區塊，自然就會繼續自己挖自己的而跟其他節點脫節
2. 在區塊傳播過程中恰巧自己剛好挖到新區塊！

分岔產生後就像下圖一樣：

![Fork Demo](https://www.lkm543.site/it_iron_man/day7_2.jpg)

因此我們之後也會需要來探討如何融合礦工間的異議！

## 節點不全然可信(reliable)

真實世界中的節點不全然是可信的，攻擊者可能會混入節點或帳戶的行列之中對外界發出錯誤的訊息，這種攻擊方式又稱為[女巫攻擊(Sybil Attack)](https://www.binance.vision/zt/security/sybil-attacks-explained)。為了避免假節點與帳戶混充，因此我們需要求得節點間的共識，也需要了解在何種狀況下才能保障區塊鏈免受女巫攻擊的威脅。

# 完成簡易的區塊鏈了！

到目前為止，我們第一部分─打造一個簡易的區塊鏈就完成了喔！但其實我們的區塊鏈還是有很多不足的地方，比方說無法處理以下這些事情：

1. 預期外的輸入、例外處理
2. 單獨驗證過去的某一筆交易
3. 要求同步特定的區塊
4. 在上面發行代幣
5. 進行多重簽名等交易

但至少我們這幾天透過一步步刻出一個簡單的區塊鏈而確定在這裡頭有三個必備的知識領域：

1. 密碼學(Hash與非對稱式加密)
2. 挖礦演算法
3. P2P網路與共識

因此明天後我們會再來逐步探討與研究這三個領域，在簡易應用後也需要把我們的基礎知識補足並且才能持續優化區塊鏈！最後幾天有時間的話再來研究一下區塊鏈的發展方向與這兩年很夯的智能合約！

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，今天節點端的程式碼放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day07.py)。

# Ref:
- [網路的延遲（Latency）與頻寬（Bandwidth）是什麼？](https://blog.gtwang.org/web-development/network-lantency-and-bandwidth/)
- [區塊鏈的冷暖系列之：數據同步技術的鬼畜型圖解](https://kknews.cc/zh-tw/tech/r3o6vnv.html)
- [女巫攻擊(Sybil Attack)](https://www.binance.vision/zt/security/sybil-attacks-explained)
