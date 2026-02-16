try:
    from google.colab import files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

import os
import shutil
from io import BytesIO
from core.translator import DocumentTranslator

def run_colab_workflow():
    if not IN_COLAB:
        print("Bu betik sadece Google Colab ortamında çalıştırılmak üzere tasarlanmıştır.")
        return

    # --- AYARLAR ---
    OUTPUT_FOLDER = "cevrilmis_belgeler"
    DB_PATH = "data/app_data.db"

    # Klasör temizliği
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER)

    print("🚀 DocTranslate Colab Arayüzüne Hoşgeldiniz!")
    print("1. Google Translate (Ücretsiz)")
    print("2. DeepL API (Pro/Free API Key Gerekir)")
    
    choice = input("\nLütfen çeviri motorunu seçin (1 veya 2): ").strip()
    
    engine = "google"
    api_key = None
    
    if choice == "2":
        engine = "deepl"
        api_key = input("Lütfen DeepL API Key'inizi girin: ").strip()
        if not api_key:
            print("⚠️ API Key girilmedi, Google Translate'e dönülüyor...")
            engine = "google"

    print("\n----------------------------------------------------------------")
    print("Lütfen çevirmek istediğiniz .docx dosyalarını seçin...")
    print("----------------------------------------------------------------")

    # 1. Dosya Yükleme Penceresini Aç
    uploaded = files.upload()

    if not uploaded:
        print("❌ Hiç dosya seçilmedi.")
        return

    print(f"\n✅ Toplam {len(uploaded)} dosya yüklendi. Çeviri işlemi başlıyor...\n")

    # 2. Çeviri İşlemi
    translator = DocumentTranslator(db_path=DB_PATH, engine=engine, api_key=api_key)
    
    translated_files = []
    for filename, content in uploaded.items():
        if filename.endswith(".docx"):
            try:
                print(f"⏳ Çevriliyor: {filename}...")
                
                input_data = BytesIO(content)
                output_data = translator.translate(input_data)

                # Yeni dosya adını belirle
                new_filename = filename.replace(".docx", "_Translated.docx")
                save_path = os.path.join(OUTPUT_FOLDER, new_filename)

                with open(save_path, "wb") as f:
                    f.write(output_data.getvalue())

                translated_files.append(new_filename)
                print(f"  ✓ Tamamlandı: {new_filename}")

            except Exception as e:
                print(f"  X Hata ({filename}): {str(e)}")
        else:
            print(f"  ! Atlandı (Desteklenmeyen format): {filename}")

    if not translated_files:
        print("\n❌ Hiçbir dosya başarıyla çevrilemedi.")
        return

    # 3. Dosyaları Zipleme ve İndirme
    print("\n📦 Dosyalar paketleniyor (ZIP)...")
    archive_name = "DocTranslate_Ceviriler"
    shutil.make_archive(archive_name, 'zip', OUTPUT_FOLDER)

    print("📥 İndirme işlemi başlatılıyor...")
    files.download(f"{archive_name}.zip")
    print("\n✨ İşlem başarıyla tamamlandı!")

if __name__ == "__main__":
    run_colab_workflow()
