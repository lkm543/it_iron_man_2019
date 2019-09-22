# 前置作業
我們今天的目標是模擬節點(礦工)端與使用者端的互動，節點端儲存了自創世塊以來的所有交易明細，同時也負責接受交易、打包交易至區塊、挖掘區塊、廣播挖掘到的區塊等等；而使用者端通常只會讀取鏈上的資料與發起交易，因為交易紀錄動輒數十GB起跳，為了效率與經濟的考量，使用者端通常不會儲存交易紀錄。

為了方便模擬我們把兩端的程式都跑在同一台電腦上，這裡選用的通訊方式是`socket`；也因為加入通訊後程式必須同時處理多樣的工作，所以使用`thread`來讓程式能夠順利執行監聽與挖礦這兩件事情。以下先就socket與thread做個簡單介紹後再開始。

## Socket

在UNIX系統下所有的I/O(輸入及輸出)都可以看做是file descriptors，因此socket就是利用`UNIX file descriptors`來與其他程式構通。它也同時提供了良好的介面與API，讓使用這可以在不具備網路底層知識的狀況下讓程式間透過網路進行溝通。一般而言socket主要可以分成下面兩種：

1. Stream Socket
2. Datagram Sockets

Stream Socket是利用TCP(Transmission Control Protocol)協定的傳輸，特色是會確保資料傳遞的完整性(不會東掉一個西掉一個)、次序性(誰先傳就會先到)，但缺點就是為了檢核傳遞的狀況，傳遞的延遲也較長。

Datagram Sockets是利用UDP(User Datagram Protocol)協定，不會去檢查資料的完整性、也無法保障傳地上的次序性，但因為節省了許多檢核的作業，傳遞的延遲非常短。

這裡因為我們需要保障資料傳遞的完整性，選用的是Stream Socket。這裡我們把區塊鏈區分成Server端與Client端，其中Server端負責處理Client連接後發出的訊息，並給予相對應的回饋；可以把Server看作是節點(礦工)端、Client看作是一般使用者。

## Thread

程式在運行時一般一次只能做一件事情，但我們的節點在打包交易與挖掘新區塊外同時也需要接收外界同步區塊或交易的請求，因此這裡我們導入`Thread`的概念讓我們的區塊鏈有能力同時處理不同工作。

`Thread`又稱為執行緒，在理解上可以把單一程式(`Program`)開始運行並載入記憶體後看作是處理程序`Process`，常見的作業系統像是Windows或Linux等也可以看做是Process的載具，而且CPU每顆核心同時也只能進行一個Process的運算。

而Process則是Thread的載具，同一個`Process`裏頭可以同時運行許多`Thread`來達到同時處理不同工作的目的。下圖是作業系統、Process、Thread的大概運作架構。

![Thread](https://www.lkm543.site/it_iron_man/day6_1.jpg)

但其實Process中的所有Thread並非是同時執行，只是Thread間以相當快的速度交錯執行讓人感受不到之間的延遲而已，就像是日光燈管每秒會因為交流電亮暗交錯60次但我們感覺不出一樣。

## Bitcoin中也有用到Socket與Thread喔！

以Bitcoin為例，中本聰一開始的版本也是使用socket與thread的概念來完成資料的接收與處理，有一個thread專門處理socket的連接，另一個thread專門處理接受後的資訊([來源](https://en.bitcoin.it/wiki/Satoshi_Client_Sockets_and_Messages))。下面是bitcoin中使用到的socket與thread的原文介紹，大抵上而言跟我們等等要寫的節點架構相當類似！

> The original bitcoin client uses a multithreaded approach to socket handling and messages processing. There is one thread that handles socket communication (ThreadSocketHandler) and one (ThreadMessageHandler) which handles pulling messages off sockets and calling the processing routines. 

# 節點與客戶端的功能

在這裡我們先簡單區分一下節點端與客戶端分別需要那些功能：

## 節點的功能

節點的功能與我們之前所撰寫的並無差異，也就是需要：

   - 產生公私鑰(錢包地址)
   - 儲存交易紀錄
   - 確認帳戶餘額
   - 驗證交易上面的數位簽章
   - 打包交易並挖掘新區塊

### 使用者端的功能

使用者端至少需要能夠**產生公私鑰**與**簽署交易**，簡單說就是為了避免私鑰外洩的風險，所有跟私鑰有關的作業(產生公私鑰或簽署數位簽章時)通通都由使用者端完成，不需要仰賴外界或是將私鑰傳至節點即可完成。

   - 產生公私鑰(錢包地址)
   - 向節點查詢資料
   - 發起並簽署交易

# 節點端
在節點端這裡首先我們需要準備socket的端口讓外界可以連入，因為測試時節點端與使用者端都在本機上，所以IP地址給的是本機的`127.0.0.1`，至於Port則因為每一個節點所用的Port不同，因此在執行程式時再透過命令列的參數給定。

## 準備socket連線的端口

```python
class BlockChain:
    def __init__(self):
        # For P2P connection
        self.socket_host = "127.0.0.1"
        self.socket_port = int(sys.argv[1])
        self.start_socket_server()
```

下圖是Socket的簡單運作流程，我們等待連接、接收資訊的步驟跟圖裡是一致的。

![Socket](https://files.realpython.com/media/sockets-tcp-flow.1da426797e37.jpg)
圖片來源：[Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)

## 開thread監聽新連線與傳入訊息

為了在打包交易與挖礦的同時能夠接收外界的資訊，我們開一個thread在`bind`之後等待外界的新連線`s.accept()`，同時在每次新連線建立之後，又為每一個獨立的連線開一個thread去接收並且處理資訊。

```python
def start_socket_server(self):
    t = threading.Thread(target=self.wait_for_socket_connection)
    t.start()

def wait_for_socket_connection(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((self.socket_host, self.socket_port))
        s.listen()
        while True:
            conn, address = s.accept()

            client_handler = threading.Thread(
                target=self.receive_socket_message,
                args=(conn, address)
            )
            client_handler.start()
```

## 接收訊息後處理

這裡我們根據使用者傳遞過來的資料，判別使用者想要做

1. 取得帳戶餘額
2. 發起交易

並且根據使用者想做的事情分別去接收不同的參數，並且回傳結果給使用者。

```python
def receive_socket_message(self, connection, address):
    with connection:
        print(f'Connected by: {address}')
        while True:
            message = connection.recv(1024).decode('utf8')
            print(f"[*] Received: {message}")
            parsed_message = ast.literal_eval(message)

            if message:
                if parsed_message["request"] == "get_balance":
                    print("Start to get the balance for client...")
                    address = parsed_message["address"]
                    balance = self.get_balance(address)
                    response = {
                        "address": address,
                        "balance": balance
                    }
                elif parsed_message["request"] == "transaction":
                    print("Start to transaction for client...")
                    address = parsed_message["address"]
                    new_transaction = self.initialize_transaction(
                        parsed_message["address"], 
                        parsed_message["receiver"],
                        int(parsed_message["amount"]),
                        int(parsed_message["fee"]),
                        parsed_message["comment"]
                    )
                    result, result_message = self.add_transaction(
                        new_transaction,
                        parsed_message["signature"]
                    )
                    response = {
                        "result": result,
                        "result_message": result_message
                    }
                else:
                    response = {
                        "message": "Unknown command."
                    }
                response_bytes = str(response).encode('utf8')
                connection.sendall(response_bytes)
```

## 啟動節點

完成上面接收並且處理資訊的過程後，便可以啟動節點、打包新交易、挖掘新區塊、調節難度，同時我們也可以根據外界的請求做相對應的處置。在這裡為了測試轉帳，我們同時產出一組礦工的公私鑰來使用(轉帳的前提是帳戶裡必須有足夠的餘額，在一開始也只有礦工有，因此我們只能用礦工的公私鑰來發起交易)。

```python
def start(self):
    address, private = self.generate_address()
    print(f"Miner address: {address}")
    print(f"Miner private: {private}")
    self.create_genesis_block()
    while(True):
        self.mine_block(address)
        self.adjust_difficulty()
```
# 客戶端

客戶端這裡的工作相對單純，首先建立與節點間的socket聯繫，這裡節點的IP因為同在本地端因此也為`127.0.0.1`，節點端的Port的部分則在啟動程式碼時再帶入。之後就可以開一個Thread不停去接收socket傳過來的資訊。

## 接收訊息

```python
def handle_receive():
    while True:
        response = client.recv(4096)
        if response:
            print(f"[*] Message from node: {response}")

if __name__ == "__main__":
    target_host = "127.0.0.1"
    target_port = int(sys.argv[1])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    receive_handler = threading.Thread(target=handle_receive, args=())
    receive_handler.start()
```

## 產生錢包地址與公私鑰

為了避免私鑰外洩，強烈建議公私鑰都在使用者的本地端產生，在利用RSA加密法產生一對鑰匙後，再把裏頭的前綴與後綴字濾掉後便是我們的公私鑰。比方說公鑰是：
> -----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANrG/HiSL6M41EaDsmpVKW+E4QZKaiW2
KZD2RR7If7f9jMZiojoS1/uM0N6AQ2G8TUkPHjBuAnS1Dn4PJZAUysMCAwEAAQ==
-----END PUBLIC KEY-----

產生的地址便是

>MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANrG/HiSL6M41EaDsmpVKW+E4QZKaiW2
KZD2RR7If7f9jMZiojoS1/uM0N6AQ2G8TUkPHjBuAnS1Dn4PJZAUysMCAwEAAQ==

私鑰原本是：

> -----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBANrG/HiSL6M41EaDsmpVKW+E4QZKaiW2KZD2RR7If7f9jMZiojoS
1/uM0N6AQ2G8TUkPHjBuAnS1Dn4PJZAUysMCAwEAAQJBAKWsPHKd2X9UQMQpZQnK
9fbifHmEDsACI5YIOK2oDbfo3mzW+gfxHtS1YVZz5TlymUAwm+qxBnwjTPEm+Jqn
9ukCIQD1pl7vOofGdAiPBM0M2mJpOh7/b82XSCO/LCyRaP8pPwIhAOP+wxujrxRe
BwzZmH6rqpKuuK2ueEVY/eVxpnHfaZl9AiAlT2mn6DnrGICcSFxkkV7VILDIl1Cg
o6JaTPlP9KScvQIhAIMFft49XHnZ5zdNPMNep7GP0vWMk/VWROI8Q6ig+TCJAiBF
ug2F+uZz3Gma5ySWBN49eH95o1PqYkDcoATkZ90skQ==
-----END RSA PRIVATE KEY-----

過濾後產生的私鑰便是：

> MIIBOwIBAAJBANrG/HiSL6M41EaDsmpVKW+E4QZKaiW2KZD2RR7If7f9jMZiojoS
1/uM0N6AQ2G8TUkPHjBuAnS1Dn4PJZAUysMCAwEAAQJBAKWsPHKd2X9UQMQpZQnK
9fbifHmEDsACI5YIOK2oDbfo3mzW+gfxHtS1YVZz5TlymUAwm+qxBnwjTPEm+Jqn
9ukCIQD1pl7vOofGdAiPBM0M2mJpOh7/b82XSCO/LCyRaP8pPwIhAOP+wxujrxRe
BwzZmH6rqpKuuK2ueEVY/eVxpnHfaZl9AiAlT2mn6DnrGICcSFxkkV7VILDIl1Cg
o6JaTPlP9KScvQIhAIMFft49XHnZ5zdNPMNep7GP0vWMk/VWROI8Q6ig+TCJAiBF
ug2F+uZz3Gma5ySWBN49eH95o1PqYkDcoATkZ90skQ==

同時這裡的程式碼節點端也會用到喔!

```python
def generate_address():
    public, private = rsa.newkeys(512)
    public_key = public.save_pkcs1()
    private_key = private.save_pkcs1()
    return get_address_from_public(public_key), extract_from_private(private_key)

def get_address_from_public(public):
    address = str(public).replace('\\n','')
    address = address.replace("b'-----BEGIN RSA PUBLIC KEY-----", '')
    address = address.replace("-----END RSA PUBLIC KEY-----'", '')
    address = address.replace(' ', '')
    return address

def extract_from_private(private):
    private_key = str(private).replace('\\n','')
    private_key = private_key.replace("b'-----BEGIN RSA PRIVATE KEY-----", '')
    private_key = private_key.replace("-----END RSA PRIVATE KEY-----'", '')
    private_key = private_key.replace(' ', '')
    return private_key
```

## 初始化交易

接著就可以來初始化一筆交易了！依序填入這筆交易的匯款方、收款方、匯款金額、手續費與備註後生成一筆交易。

```python
class Transaction:
    def __init__(self, sender, receiver, amounts, fee, message):
        self.sender = sender
        self.receiver = receiver
        self.amounts = amounts
        self.fee = fee
        self.message = message

def initialize_transaction(sender, receiver, amount, fee, message):
    # No need to check balance
    new_transaction = Transaction(sender, receiver, amount, fee, message)
    return new_transaction
```

## 簽章交易

為了讓礦工驗證這筆交易的確是由我們親自發出的，因此發出去交易前我們先透過私鑰對交易的內容做簽署，完成後就得到這筆交易的數位簽章，礦工可以透過數位簽章確認是由我們發出的。

```python
def transaction_to_string(transaction):
    transaction_dict = {
        'sender': str(transaction.sender),
        'receiver': str(transaction.receiver),
        'amounts': transaction.amounts,
        'fee': transaction.fee,
        'message': transaction.message
    }
    return str(transaction_dict)

def sign_transaction(transaction, private):
    private_key = '-----BEGIN RSA PRIVATE KEY-----\n'
    private_key += private
    private_key += '\n-----END RSA PRIVATE KEY-----\n'
    private_key_pkcs = rsa.PrivateKey.load_pkcs1(private_key.encode('utf-8'))
    transaction_str = transaction_to_string(transaction)
    signature = rsa.sign(transaction_str.encode('utf-8'), private_key_pkcs, 'SHA-1')
    return signature
```

## 控制流程

接著便是控制整個流程了！在使用者端總共有三件事情可以做：

1. 產生地址與公私鑰
2. 向節點詢問帳戶的餘額
3. 發起並簽署交易後送到節點端等待礦工確認與上鏈

```python
if __name__ == "__main__":
    target_host = "127.0.0.1"
    target_port = int(sys.argv[1])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    receive_handler = threading.Thread(target=handle_receive, args=())
    receive_handler.start()

    command_dict = {
        "1": "generate_address",
        "2": "get_balance",
        "3": "transaction"
    }

    while True:
        print("Command list:")
        print("1. generate_address")
        print("2. get_balance")
        print("3. transaction")
        command = input("Command: ")
        if str(command) not in command_dict.keys():
            print("Unknown command.")
            continue
        message = {
            "request": command_dict[str(command)]
        }
        if command_dict[str(command)] == "generate_address":
            address, private_key = generate_address()
            print(f"Address: {address}")
            print(f"Private key: {private_key}")

        elif command_dict[str(command)] == "get_balance":
            address = input("Address: ")
            message['address'] = address
            client.send(str(message).encode('utf8'))

        elif command_dict[str(command)] == "transaction":
            message['address'] = input("Address: ")
            private_key = input("Private_key: ")
            message['receiver'] = input("Receiver: ")
            message['amount'] = input("Amount: ")
            message['fee'] = input("Fee: ")
            message['comment'] = input("Comment: ")
            new_transaction = initialize_transaction(
                message["address"], 
                message["receiver"],
                int(message["amount"]),
                int(message["fee"]),
                message["comment"]
            )
            signature = sign_transaction(new_transaction, private_key)
            message["signature"] = signature

            client.send(str(message).encode('utf8'))

        else:
            print("Unknown command.")
        time.sleep(1)
```
# 實際操作
## 運行節點

首先透過`python 節點的py檔 port位置`指定節點端的port並啟動。

```shell
python .\blockchain_server.py 1111
```

![Node](https://www.lkm543.site/it_iron_man/day6_2.jpg)

啟動後便可以看到礦工的公私鑰與挖掘中的情形，稍後我們就可以透過礦工的公私鑰來發起交易！

## 運行使用者端

透過`python 用戶的py檔 port位置`指定欲連接的節點端port後啟動。

```shell
python .\blockchain_client.py 1111
```

接著就可以看到選單，輸入1、2、3便可以執行相對應的工作。

![Node](https://www.lkm543.site/it_iron_man/day6_3.jpg)

## 創建新地址

輸入1後便可以透過RSA加密法得到一組公私鑰！

![Node](https://www.lkm543.site/it_iron_man/day6_4.jpg)

## 查詢餘額

輸入2與要查詢的地址後便可以查詢該帳戶的餘額，這裡我們查詢礦工地址的餘額：

![Node](https://www.lkm543.site/it_iron_man/day6_5.jpg)

發現裏頭現在有620元！

## 發起交易

接著我們利用一開始產生礦工的公私鑰，轉移50元到我們自己的地址上，手續費給1元：

![Node](https://www.lkm543.site/it_iron_man/day6_6.jpg)

## 確認是否有收到

最後查閱我們被轉帳的帳戶裏頭是不是有出現50元。

![Node](https://www.lkm543.site/it_iron_man/day6_7.jpg)

咦？怎麼還是0元？別緊張，這是因為我們的交易還沒被打包並且挖掘出來，稍微等新區塊被礦工挖掘出來後：

![Node](https://www.lkm543.site/it_iron_man/day6_8.jpg)

順利收到50元！

今天的目標達成了：讓使用者可以查閱節點的資料、並透過數位簽章發起交易，但是我們的節點目前只有一個，似乎不是理想中的去中心化。因此明天的目標就是讓有意願的人也可以一起自由地加入節點紀錄並且挖掘新區塊，同時完成我們簡易區塊鏈的最後一步─去中心化。

到目前為止的文章都會放置在[Github](https://github.com/lkm543/it_iron_man_2019)上，至於今天節點端的程式碼放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day06_server.py)、使用者端的程式碼則放在[這裡](https://github.com/lkm543/it_iron_man_2019/blob/master/code/day06_client.py)。

# Ref:
- [Beej's Guide to Network Programming 正體中文版](http://beej-zhtw.netdpi.net/02-what-is-socket)
- [Satoshi Client Sockets and Messages](https://en.bitcoin.it/wiki/Satoshi_Client_Sockets_and_Messages)
- [Python基於socket實現簡單的即時通訊功能示例](https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/360741/)
- [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)
- [TCP Socket Programming 學習筆記](http://zake7749.github.io/2015/03/17/SocketProgramming/)
- [Thread 的概念](http://ccckmit.wikidot.com/thread)
- [Program/Process/Thread 差異](https://medium.com/@totoroLiu/program-process-thread-%E5%B7%AE%E7%95%B0-4a360c7345e5)
