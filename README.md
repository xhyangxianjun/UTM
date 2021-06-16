# UTM

![screenshot_2](https://github.com/ma6254/UTM/raw/master/doc/screenshot_2.png)
![screenshot_1](https://github.com/ma6254/UTM/raw/master/doc/screenshot_1.png)

原为usb测温仪（usb temperature monitor），后扩展为多种设备上位机，通讯协议公开，易扩展

包括以下机型：

- USB测温仪（未公开）
- 牛牛FOC驱动器 CowDrive（未公开）
- 用于公司产品调试（未公开）
- 电参（T8775）

已实现：

- 支持同时查看设备多协议
- 支持可屏蔽不需要字段
- 支持主动下发数据
- 支持载入、导出CSV、JSON格式

未实现：

- 不支持字段数值缩放（需要手动改源代码缩放）
- TODO 暂时没有新需求



## 依赖库

```cmd
PyQt5==5.14.2
PyQt5-sip==12.7.2
PyQtWebEngine==5.14.0
pyserial==3.4
pywin32-ctypes==0.2.0
PyYAML==5.3.1
```

## 编译

### 编译前端文件

```cmd
pyrcc5 -o .\asserts\__init__.py .\asserts\charts.qrc
```

## 调试web

```bash
--remote-debugging-port=9223
```

### 打包为exe

```cmd
cd release
pyinstaller --noupx -p ../ ../main.py
rm dist/main/MSVCP140.dll
rm dist/main/VCRUNTIME140.dll
CP ../config.yml dist/main/
upx dist/main/Qt5WebEngineCore.dll

```
