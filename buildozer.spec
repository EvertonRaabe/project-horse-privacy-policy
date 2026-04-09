[app]
title = Project Horse
package.name = projecthorse
package.domain = com.terknautgames

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3,ogg,json

version = 1.3.2

# ── Dependências ───────────────────────────────────────────────────────────────
# plyer adicionado para notificações push locais
requirements = python3,kivy,pyjnius,android,https://github.com/kivymd/KivyMD/archive/master.zip

orientation = portrait
fullscreen = 0

# ── Android SDK ────────────────────────────────────────────────────────────────
android.minapi = 21
android.api = 35
android.ndk = 25b
android.sdk = 34
android.archs = arm64-v8a, armeabi-v7a

# ── Ícone ──────────────────────────────────────────────────────────────────────
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png

# ── Permissões ─────────────────────────────────────────────
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# ── AdMob ─────────────────────────────────────────────────
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-1629730681290593~2169149407
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0
android.enable_androidx = True
android.use_androidx = True

android.add_manifest_xml = """
<uses-permission android:name="com.google.android.gms.permission.AD_ID"/>
"""
# ── Assinatura (AAB para Play Store) ──────────────────────────────────────────
android.release_artifact = aab
android.keystore = project-horse.keystore
android.keystore_passwd = 721023
android.keyalias = project-horse
android.keyalias_passwd = 721023

# Evita incluir arquivos desnecessários no APK
source.exclude_dirs = tests, bin, .buildozer, __pycache__, .git
source.exclude_exts = pyc, pyo, spec

[buildozer]
log_level = 2
warn_on_root = 1
