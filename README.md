# tcptest
tcp flag testing and watching 
TCP Flag Testi (Scapy ile)

Bu proje, hedef makinelere çeşitli TCP bayrakları (flags) göndererek, 
bu bayraklara karşılık gelen yanıtları analiz etmeyi amaçlayan bir 
Python script'idir. Scapy kütüphanesini kullanarak TCP bayraklarını 
test etmek ve hedef makinenin yanıtlarını incelemek için kullanılabilir.
Özellikler

    TCP Bayrakları (Flags) Tespiti: SYN, ACK, FIN, RST, PSH, URG gibi yaygın 
    TCP bayrakları ile paket gönderimi yaparak, hedef makineden gelen yanıtları 
    kontrol eder.
    Yanıt Bekleme: Gönderilen bayrakların her biri için beklenen yanıtlar 
    belirlenmiştir. Script, bu yanıtların alınıp alınmadığını kontrol eder.
    Test Edilen Bayraklar: SYN, ACK, FIN, RST, PSH, URG, XMAS (SYN+FIN+PSH), 
    FIN-PSH, SYN-FIN gibi bayraklar test edilir.
    Yanıtlar ve Özetleme: Gönderilen her bayrak için alınan yanıtların yanı sıra, 
    beklenen yanıtlar ve alınan yanıtlar özetlenebilir.

Kurulum

    Python 3.x yüklü olmalıdır. Eğer yüklü değilse Python'un resmi sitesinden 
    Python'u indirip yükleyebilirsiniz.

    Scapy kütüphanesini yüklemek için aşağıdaki komutu kullanın:

    pip install scapy

Kullanım

    Proje dosyasını indirin veya klonlayın:

git clone https://github.com/enoskom/tcptest.git
cd tcptest

Script'i çalıştırın:

python tcpflag.py

IP ve portları girin: Script çalıştırıldığında, kullanıcıdan hedef 
IP adresi ve port numaraları girilmesi istenecektir. Portlar 
virgülle ayrılmalı, örnek format:

    192.168.1.1:80,443,22

    Çıktıyı özetleyin (isteğe bağlı): Test tamamlandığında, çıktıyı özetleme 
    isteği sunulur. Özetlemenin ardından, gönderilen bayraklar, beklenen 
    yanıtlar ve alınan yanıtlar tablo formatında gösterilecektir.

Örnek Çıktı

➡ Gönderilen bayrak: SYN (0x2) - Port: 80
✔ Beklenen bayrak: SYN-ACK (0x12) - Port: 80
⬅ Alınan bayrak: 0x12 - Port: 80

➡ Gönderilen bayrak: FIN (0x1) - Port: 443
✔ Beklenen bayrak: FIN-ACK (0x11) - Port: 443
⬅ Alınan bayrak: 0x11 - Port: 443
...

Gönderilen bayrak | Port | Beklenen yanıt        | Alınan bayrak
-----------------------------------------------------------------
             SYN   |  80  |    SYN-ACK           |     0x12     
             FIN   |  443 |    FIN-ACK           |     0x11     
...

Bayraklar

    SYN (0x02): Bağlantı başlatmak için gönderilir.
    ACK (0x10): Bağlantıyı doğrulamak için gönderilir.
    RST (0x04): Bağlantıyı sıfırlamak için gönderilir.
    FIN (0x01): Bağlantıyı sonlandırmak için gönderilir.
    PSH (0x08): Verilerin hemen iletilmesini sağlar.
    URG (0x20): Acil veriler için gönderilir.
    XMAS (0x29): SYN+FIN+PSH bayrakları ile gönderilir.
    FIN-ACK (0x11): Bağlantıyı sonlandırmak için gönderilir.
    SYN-FIN (0x03): Geçersiz bayrak kombinasyonu, yanıt alınmaz.
