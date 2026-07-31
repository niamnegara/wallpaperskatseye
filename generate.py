import os
import json
from PIL import Image

# ==========================================
# KONFIGURASI REPOSITORY GITHUB ANDA
# ==========================================
GITHUB_USERNAME = "niamnegara"
REPO_NAME = "wallpaperskatseye"
BRANCH_NAME = "main"

# Base URL untuk link raw gambar WebP
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH_NAME}/wallpapers"

# Folder Input & Output
RAW_FOLDER = "raw_images"
OUTPUT_FOLDER = "wallpapers"
JSON_FILE = "wallpapers.json"

# Buat folder jika belum ada
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
if not os.path.exists(RAW_FOLDER):
    os.makedirs(RAW_FOLDER)

wallpapers_list = []
item_id = 1

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

print("🚀 Memulai proses konversi dan pembuatan JSON...\n")

for filename in os.listdir(RAW_FOLDER):
    if filename.endswith(SUPPORTED_EXTENSIONS):
        file_path = os.path.join(RAW_FOLDER, filename)
        name_no_ext = os.path.splitext(filename)[0]
        webp_filename = f"{name_no_ext}.webp"
        webp_path = os.path.join(OUTPUT_FOLDER, webp_filename)

        # 1. Konversi Gambar ke WebP (Kualitas 80%)
        try:
            with Image.open(file_path) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(webp_path, "WEBP", quality=80)
                print(f"✅ Converted: {filename} -> {webp_filename}")
        except Exception as e:
            print(f"❌ Gagal mengonversi {filename}: {e}")
            continue

        # 2. Format Judul (contoh: 'katseye_sophia_story' -> 'Katseye Sophia Story')
        title = name_no_ext.replace('_', ' ').replace('-', ' ').title()

        # 3. Cek Format Story
        is_story = 'story' in filename.lower()
        category = "Story" if is_story else "HD Wallpaper"

        # 4. Tambahkan ke List JSON
        image_url = f"{BASE_URL}/{webp_filename}"
        wallpapers_list.append({
            "id": item_id,
            "title": title,
            "imageUrl": image_url,
            "category": category,
            "isStoryFormat": is_story
        })

        item_id += 1

# 5. Simpan ke wallpapers.json
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(wallpapers_list, f, indent=2, ensure_ascii=False)

print(f"\n🎉 Selesai! Berhasil memproses {len(wallpapers_list)} wallpaper.")
print(f"📄 File '{JSON_FILE}' berhasil diperbarui.")
