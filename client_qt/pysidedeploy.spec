[app]

# Title of your application
title = pyside_app_demo

# Project root directory. Default: The parent directory of input_file
project_dir = .

# Source file entry point path. Default: main.py
input_file = main.py

# Directory where the executable output is generated
exec_directory = android_bin

# Path to the project file relative to project_dir
project_file =

# Application icon
icon =

[python]

# Python path
python_path = /home/noah/code/pyside-setup/.python311_venv/bin/python3.11

# Python packages to install
packages = Nuitka==2.7.11

# Buildozer: for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# Paths to required QML files. Comma separated
# Normally all the QML files required by the project are added automatically
# Design Studio projects include the QML files using Qt resources
qml_files = ./qml/Login.qml, ./qml/App.qml, ./qml/MainWindow.qml, ./qml/LoginForm.ui.qml, ./qml/MessageBox.ui.qml, ./qml/ContactElement.ui.qml, ./qml/MainWindowForm.ui.qml

# Excluded qml plugin binaries
excluded_qml_plugins =

# Qt modules used. Comma separated
modules =

# Qt plugins used by the application. Only relevant for desktop deployment
# For Qt plugins used in Android application see [android][plugins]
plugins =

[android]

# Path to PySide wheel
wheel_pyside = /home/noah/.cache/qtpip/QtForPython/6.10.1/PySide6-6.10.1+commercial-6.10.1-cp311-cp311-android_aarch64.whl

# Path to Shiboken wheel
wheel_shiboken = /home/noah/.cache/qtpip/QtForPython/6.10.1/shiboken6-6.10.1+commercial-6.10.1-cp311-cp311-android_aarch64.whl

# Plugins to be copied to libs folder of the packaged application. Comma separated
plugins =

[nuitka]

# Usage description for permissions requested by the app as found in the Info.plist file
# of the app bundle. Comma separated
# eg: NSCameraUsageDescription:CameraAccess
macos.permissions =

# Mode of using Nuitka. Accepts standalone or onefile. Default: onefile
mode = onefile

# Specify any extra nuitka arguments
# eg: extra_args = --show-modules --follow-stdlib
extra_args = --quiet --noinclude-qt-translations

[buildozer]

# Build mode
# Possible values: [release, debug]
# Release creates a .aab, while debug creates a .apk
mode = debug

# Path to PySide6 and shiboken6 recipe dir
recipe_dir =

# Path to extra Qt Android .jar files to be loaded by the application
jars_dir =

# If empty, uses default NDK path downloaded by buildozer
ndk_path =

# If empty, uses default SDK path downloaded by buildozer
sdk_path =

# Other libraries to be loaded at app startup. Comma separated.
local_libs =

# Architecture of deployed platform
# Possible values: ["aarch64", "armv7a", "i686", "x86_64"]
arch = aarch64
