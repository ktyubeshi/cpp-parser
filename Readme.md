# Cpp Parser

libclang + Python でC/C++のソースコードをパースするスクリプトです。

関数リストをテキストファイルに出力することができます。

# 依存関係

* [LLVM](https://clang.llvm.org)
* [Python](https://www.python.org)
    * Clang Python Bindings [libclang](https://pypi.org/project/libclang/)

※ 動作確認は Win64版の LLVM 14.0.6 、libclang 14.0.6 、Python 3.10 で行いました。

# 使い方

* LLVMのページからLLVMをダウンロードしてインストールしてください。
* Pythonをインストールしてlibclangをインストールしてください。

```
pip install libclang
```

* src/example.py を環境に合わせて修正して実行してください。

## ファイルの説明

| ファイル/フォルダ              | 説明                                                                     |
|-------------------------------|-------------------------------------------------------------------------|
| /src/cppParser.py             | 本体のモジュールです。                                                    |
| /src/example.py               | 使用例を示すサンプルコードです                                             |
| /src/example.c                | 使用例を示すためのｃのサンプルコードです。                                  |
| /CMakeLists.txt               | このプロジェクトではdoxygen-python.cmakeを呼び出すためだけに使われています。 |
| /doxygen/doxygen-python.cmake | Pythonのドキュメント生成用に設定したCMakeファイルです。                     |
| /doxygen-output/html          | Cmakeを実行するとHTML形式でドキュメントが生成されます。(git管理外)           |
| /build                        | Cmakeの構成を実行すると生成されます。(git管理外)                           |






