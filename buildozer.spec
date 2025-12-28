[app]
title = Uzay Savasi Pro
package.name = uzaysavasi
package.domain = org.test

# Ana dosyanın adı
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Gereksinimler (Pygame mutlaka olmalı)
requirements = python3,pygame

# Android API ayarları (Hata aldığın kısım burasıydı)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# Ekran ayarları
orientation = landscape
fullscreen = 1
android.presplash_color = #0A0F23
