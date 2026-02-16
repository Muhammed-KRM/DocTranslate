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

### 1. Yerel Kullanım (Bilgisayar)
Programı kendi bilgisayarınızda çalıştırmak için:
1.  Çevirmek istediğiniz belgeyi `D:\doc\` klasörüne koyun.
2.  `translate_main_doc.py` dosyasını çalıştırın:
    ```bash
    python translate_main_doc.py
    ```

### 2. Google Colab Kullanımı (Hızlı & Kolay)
Hiçbir teknik kurulumla uğraşmadan, doğrudan tarayıcı üzerinden birden fazla dosyayı çevirmek için:
1.  Projeyi Colab'e yükleyin veya bir hücreye kopyalayın.
2.  `colab_translator.py` dosyasını çalıştırın:
    ```python
    python colab_translator.py
    ```
3.  Açılan ekranda **"Dosyaları Seç"** butonuna basarak bilgisayarınızdan bir veya birden fazla `.docx` dosyası seçin.
4.  İşlem bittiğinde, çevrilen tüm dosyalar otomatik olarak bir **ZIP** dosyası içinde bilgisayarınıza indirilecektir.

## 📦 Toplu İşlem (Batch Processing)
Yeni Colab arayüzü sayesinde:
- Birden fazla dosyayı aynı anda yükleyebilirsiniz.
- Dosyalar sırayla çevrilir.
- Sonuçlar tek bir paket (ZIP) halinde sunulur.

## ⚙️ Yapılandırma

- **Ana Belge:** `translate_main_doc.py` dosyasını açarak `INPUT_FILE` değişkeninden giriş dosyasını değiştirebilirsiniz.
- **Sözlük:** `data/app_data.db` dosyası, programın koruduğu veya zorunlu çevirdiği kelimeleri saklar.

## 👨‍💻 Geliştirici
Muhammed-KRM (ustunmuhammed09@gmail.com)
