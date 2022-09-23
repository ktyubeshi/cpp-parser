import cppParser
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))                 # このスクリプトの格納先ディレクトリを取得する

# メイン関数 ===================================================================================================================
def main():
    p = cppParser.Parser("C:/Program Files/LLVM/bin/libclang.dll")      # cppParserのインスタンスを生成する
    dir_scanner = cppParser.DirScanner
    output_file = "function_list.tsv"
   
    source_extentions = ['.cpp', '.c']                                  # 対象ファイルの拡張子リストを設定する  
    include_paths =[SCRIPT_DIR]                                         # インクルードパスをリストで設定する
    source_files = dir_scanner.scan(SCRIPT_DIR,source_extentions)       # ソースファイルのリストを取得する

    tu_list = p.parse_multiple(source_files, include_paths)             # パースを実行してclang.cindex.TranslationUnitのリストを取得

    for tu in tu_list:    
        errors = p.get_errors(tu)                                       # エラーリストを取得する(実行するとコンソールにもエラーが出力されます。)
            
    writer = cppParser.TSV_Writer(output_file)                          # TSVファイルを作成する
    writer.console_output = True                                        # 出力処理時のコンソール出力を有効にする

    writer.write_header()                                               # ヘッダを出力する
    
    for tu in tu_list:    
        functions = p.get_functions(tu)                                 # 関数リストを取得する
        writer.write_functions(functions)                               # 関数リストをファイルに出力する
    print (output_file + ' is created.')
# ======================================
main ()
