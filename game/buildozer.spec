[app]

# Название приложения
title = Snake Game

# Имя пакета
package.name = snakegame

# Доменное имя (обязательно)
package.domain = org.example

# Исходный код
source.dir = game

# Главный файл приложения
source.include_exts = py,png,jpg,kv,atlas

# Версия
version = 0.1

# Требования
requirements = python3,kivy

# Ориентация экрана
orientation = portrait

# iOS настройки (не нужно для Android)
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# Android настройки
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.ndk_api = 21
android.gradle_download = https://services.gradle.org/distributions/gradle-7.6-all.zip

# Разрешения Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Особенности Android
android.features = android.hardware.screen.portrait

# Архитектура
android.arch = arm64-v8a, armeabi-v7a

# Бэкенд
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

[buildozer]

# Логи
log_level = 2

# Каталог сборки
build_dir = buildozer_build
