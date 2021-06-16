$env:PATH="C:\mingw64\bin;%PATH%"
C:\Users\mjc\AppData\Local\Programs\Python\Python38\python.exe -m `
nuitka `
    --mingw64 `
    --standalone `
    --show-progress `
    --show-modules `
    --output-dir=release `
    --plugin-enable=qt-plugins `
    --plugin-enable=pylint-warnings `
./main.py
Copy-Item config.yml release/main.dist/config.yml
