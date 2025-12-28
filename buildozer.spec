[app]
# Oyun Bilgileri
title = Void Runner
package.name = voidrunner
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,txt,ttf
version = 1.1

# Gereksinimler (Pygame mutlaka ekli olmalı)
requirements = python3,pygame

# Ekran Ayarları
orientation = portrait
fullscreen = 1

# Android Ayarları (Hata almamak için sabitlendi)
android.api = 31
android.minapi = 21
android.sdk = 31
android.build_tools_version = 31.0.0
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# --- KRİTİK AYARLAR ---
# Lisansları otomatik kabul et (AIDL hatasını önler)
android.accept_sdk_license = True
# Log seviyesini yükselt (Hata olursa anlamamızı sağlar)
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
