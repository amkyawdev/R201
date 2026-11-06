[app]
# Optional Kivy/buildozer fallback if the Flet Android build is unavailable.
title = Movie Recap Myanmar
package.name = movierecap
package.domain = com.amkyawdev
source.dir = src
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3
version = 1.0.0
requirements = python3,flet,requests,edge-tts
orientation = portrait
fullscreen = 0
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET, RECORD_AUDIO, READ_MEDIA_VIDEO
android.allow_backup = True
