cd release
pyinstaller --noupx -y -p ../ ../main.py
rm dist/main/MSVCP140.dll
rm dist/main/VCRUNTIME140.dll
CP ../config.yml dist/main/
upx dist/main/Qt5WebEngineCore.dll
upx dist/main/opengl32sw.dll
upx dist/main/Qt5Gui.dll
upx dist/main/main.exe
cd ..