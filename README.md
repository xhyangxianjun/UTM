# 测温仪上位机

## 编译

### 编译前端文件

```cmd
pyrcc5 -o .\asserts\__init__.py .\asserts\charts.qrc
```

### 打包为exe

```cmd
cd release
pyinstaller --noupx ../main.py
```
