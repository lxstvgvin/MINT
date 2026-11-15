[app]

title = MINT

package.name = mint
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = __pycache__,.buildozer,bin

version = 0.1.0

requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 0
android.accept_sdk_license = True
android.permissions =
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
