# DocTranslate

DocTranslate, Microsoft Word (.docx) belgelerini, içindeki tüm görsel formatları (renkler, tablolar, linkler, resimler) koruyarak yüksek doğrulukla çeviren profesyonel bir araçtır.

## 🚀 Özellikler

- **Format Koruma:** Yazı tipi, boyutu, rengi, kalınlık/italik/altı çizili gibi tüm özellikleri korur.
- **Link Desteği:** Belge içindeki hyperlinkleri (bağlantıları) bozmadan çevirir ve tıklanabilir tutar.
- **Gelişmiş Renk Yönetimi:** "Heading" stillerinden gelen otomatik renkleri ve "Shading" (gölgelendirme) arkaplan renklerini doğru şekilde işler.
- **Sözlük Sistemi:** SQLite tabanlı bir veritabanı kullanarak özel terimlerin hatalı çevrilmesini önler (Tam kelime eşleşmesi desteği ile).
- **Hata Kontrolü:** API sınırlarını ve çeviri hatalarını otomatik algılayıp orijinal metni koruma altına alır.

## 🛠️ Kurulum

1.  **Python Yükleyin:** Bilgisayarınızda Python 3.10 veya üzeri bir sürümün yüklü olduğundan emin olun.
2.  **Bağımlılıkları Kurun:** Terminale şu komutu yazın:
    ```bash
    pip install -r requirements.txt
    ```

## 📖 Kullanım

Programı çalıştırmak için aşağıdaki adımları izleyin:

1.  Çevirmek istediğiniz belgeyi `D:\doc\` klasörüne (veya `translate_main_doc.py` içindeki yol ile aynı yere) koyun.
2.  Terminalden projeye gidin ve çalıştırın:
    ```bash
    python translate_main_doc.py
    ```
3.  Çevrilmiş dosya otomatik olarak `output/` klasörü altına kaydedilecektir.

## ⚙️ Yapılandırma

- **Ana Belge:** `translate_main_doc.py` dosyasını açarak `INPUT_FILE` değişkeninden giriş dosyasını değiştirebilirsiniz.
- **Sözlük:** `data/app_data.db` dosyası, programın koruduğu veya zorunlu çevirdiği kelimeleri saklar.

## 👨‍💻 Geliştirici
Muhammed-KRM (ustunmuhammed09@gmail.com)
