[app]

title = MINT

package.name = mint
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png
source.exclude_dirs = __pycache__,.buildozer,bin

version = 0.2.0

requirements = python3,kivy==2.3.1,charset-normalizer==2.1.1
p4a.branch = develop
orientation = portrait
fullscreen = 0
android.accept_sdk_license = True
android.permissions =
android.archs = armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1
