import sys
from scapy.all import IP, TCP, sr1

# Bayraklar ve açıklamaları
flags = {
    "SYN": 0x02,
    "ACK": 0x10,
    "RST": 0x04,
    "FIN": 0x01,
    "PSH": 0x08,
    "URG": 0x20,
    "SYN-ACK": 0x12,
    "FIN-ACK": 0x11,
    "XMAS": 0x29,  # XMas bayrağı, SYN+FIN+PSH bayraklarıyla birlikte
    "PSH-URG": 0x28,  # PSH+URG bayrağı
    "FIN-PSH": 0x09,  # FIN+PSH bayrağı
    "SYN-FIN": 0x03  # SYN+FIN bayrağı (Geçersiz kombinasyon)
}

# Beklenen yanıt bayrakları (gerçekleşmesi beklenen durumlar)
expected_flags = {
    0x02: 0x12,  # SYN -> SYN-ACK
    0x12: 0x10,  # SYN-ACK -> ACK
    0x10: 0x04,  # ACK -> RST
    0x04: None,  # RST -> none
    0x01: 0x11,  # FIN -> FIN-ACK
    0x11: 0x11,  # FIN-ACK -> FIN-ACK
    0x29: 0x10,  # XMAS -> ACK (Beklenen yanıt XMAS sonrası ACK'tır)
    0x28: None,  # PSH-URG -> none (Beklenen yanıt yok)
    0x09: None,  # FIN-PSH -> none (Beklenen yanıt yok)
    0x03: None   # SYN-FIN -> none (Geçersiz kombinasyon, yanıt yok)
}

# Gönderilen, beklenen ve alınan bayrakları saklamak için liste
results = []

def send_test_packet(target_ip, target_port, flag_name, flag_value):
    """
    Belirtilen bayrağa sahip bir paket gönderir ve yanıt alır.
    """
    # Paket oluşturma
    ip = IP(dst=target_ip)  # Hedef IP
    tcp_flags = TCP(dport=target_port, flags=flag_value)  # TCP bayrağını belirt
    pkt = ip/tcp_flags  # Paket

    print(f"\n➡ Gönderilen bayrak: {flag_name} ({hex(flag_value)}) - Port: {target_port}")
    sys.stdout.flush()  # Çıktıyı hemen terminalde göster

    # Beklenen bayrağı bir alt satırda yazdır
    expected_response = expected_flags.get(flag_value, None)
    if expected_response is not None:
        expected_flag_name = [name for name, value in flags.items() if value == expected_response][0]
        print(f"✔ Beklenen bayrak: {expected_flag_name} ({hex(expected_response)}) - Port: {target_port}")
    else:
        print(f"✔ Beklenen bayrak: yanıt alınmamalı - Port: {target_port}")

    # Paketi gönder ve yanıt al
    response = sr1(pkt, timeout=2, verbose=0)
    
    received_flag = None

    if response:
        # Yanıt geldiyse, TCP katmanını kontrol et
        if response.haslayer(TCP):
            received_flag = int(response.getlayer(TCP).flags)  # Bayrağı integer'a çevir
            print(f"⬅ Alınan bayrak: {hex(received_flag)} - Port: {target_port}")  # Hex formatında yazdır
        else:
            print(f"⛔ Yanıt TCP katmanında değil - Port: {target_port}")
    else:
        # Timeout durumunda bilgilendirme
        print(f"⏱ Yanıt alınmadı - Port: {target_port}")
    
    # Sonuçları kaydet
    results.append({
        "Gönderilen bayrak": flag_name,
        "Port": target_port,
        "Beklenen yanıt": expected_flag_name if expected_response is not None else "yanıt alınmamalı",
        "Alınan bayrak": hex(received_flag) if received_flag is not None else "Yanıt alınmadı"
    })

def main():
    # Kullanıcıdan IP adresi ve port bilgilerini al
    target = input("IP adresi ve portları gir (IP:PORT1,PORT2,...): ")

    # IP adresi ve portları ayırma
    try:
        target_ip, ports = target.split(":")
        target_ports = [int(port) for port in ports.split(",")]  # Portları integer'a dönüştürme
    except ValueError:
        print("Hata: IP adresi ve portları 'IP:PORT1,PORT2,...' formatında gir.")
        sys.exit(1)

    # Tüm bayraklar ve portlar için test yapma
    for target_port in target_ports:
        for flag_name, flag_value in flags.items():
            send_test_packet(target_ip, target_port, flag_name, flag_value)

    # Kullanıcıya çıktıyı özetlemek isteyip istemediğini sor
    summarize = input("\nÇıktıyı özetle ? (e/h): ").strip().lower()
    if summarize == "e":
        # Tabloda sonuçları göster
        print("\nGönderilen bayrak | Port | Beklenen yanıt        | Alınan bayrak")
        print("-" * 65)
        for result in results:
            print(f"{result['Gönderilen bayrak']:>15} | {result['Port']:>4} | {result['Beklenen yanıt']:>20} | {result['Alınan bayrak']:>15}")
    else:
        print("Özetleme yapılmadı.")

if __name__ == "__main__":
    main()
