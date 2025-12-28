[app]
# Oyunun adı
title = Void Runner

# Paket adı (boşluksuz, küçük harf)
package.name = voidrunner

# Kurum adı
package.domain = org.test

# Ana kodun olduğu yer (Genelde aynı klasör olur)
source.dir = .

# Dahil edilecek dosya uzantıları
source.include_exts = py,png,jpg,txt,ttf

# Versiyon
version = 1.0

# GEREKSİNİMLER (En önemli kısım burasıdır)
requirements = python3,pygame

# Ekran yönü (Dikey oyun olduğu için portrait)
orientation = portrait

# Tam ekran olsun mu?
fullscreen = 1

# Android API seviyesi (Genelde 31 veya 33 idealdir)
android.api = 31
android.minapi = 21

# APK'nın mimarisi (Çoğu telefon için armeabi-v7a ve arm64-v8a)
android.archs = arm64-v8a, armeabi-v7a

# Logcat kontrolü (Hata ayıklama için)
log_level = 2

[buildozer]
# Log seviyesi
log_level = 2
warn_on_root = 1
