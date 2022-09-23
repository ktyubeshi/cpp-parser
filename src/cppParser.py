import clang.cindex
import os
from enum import Enum
from typing import List



def replace_none_to_empty_string(string: any) -> str:
    """入力された文字が有効な場合は文字列を返し、Noneの場合は空文字を返します。
    
    引数:
        string (str): 処理対象の文字列
    戻り値:
        str: 処理結果の文字列

    """
    
    if string is None:
        return ''
    else:
        return string
            
class DirScanner:
    def scan(source_dir:str,extentions:List[str]) -> List[str]:
        source_files =[]
        
        for root, dirs, files in os.walk(source_dir):
            
            for file in files:
                if os.path.splitext(file)[1] in extentions:  # 対象ファイルの拡張子なら
                    source_file = os.path.join(root, file)   # ファイルパスを取得する
                    source_files.append(source_file)         # ソースファイルリストに追加する
                    
        return source_files

# 出力項目を定義するための列挙体       
class OutputItem(Enum):
    """出力する項目を定義する"""
    SOURCE_ABS_PATH = 0     # ソースコードの絶対パス
    SOURCE_REL_PATH = 1     # ソースコードの相対パス
    SOURCE_FILE     = 2     # ソースファイル名
    PROTOTYPE       = 3     # 関数のプロトタイプ宣言文
    RETURN_TYPE     = 4     # 関数の戻り値の型
    FUNCTION_NAME   = 5     # 関数名
    PARAMETER_NAMES = 6     # 関数の引数名リスト(カンマ区切り)
    PARAMETER_TYPES = 7     # 関数の引数の型リスト(カンマ区切り)
    BRIEF_COMMENT   = 8     # Doxygenフォーマットの@briefコメント
    RAW_COMMENT     = 9     # Doxygenフォーマットのコメントの全て
    
# 引数オブジェクト=========================================================================================
class FunctionArg:
    """関数の引数を表すクラス
    """
    def __init__(self, name:str, type:str) -> None:
        """引数オブジェクトのコンストラクタ

        Args:
            name (str): 引数の名前
            type (str): 引数の型名
        """
        self.name:str = name
        """引数の名前"""
        
        self.type:str = type
        """引数の型名"""

    def get_name(self)->str:
        """引数名を返す

        戻り値:
            str: 引数名
        """
        return self.name

    def get_type(self)->str:
        """引数の型を返す

        戻り値:
            str: 引数の型名
        """
        return self.type
# 関数オブジェクト=========================================================================================
class CppFunction:
    """関数を表すクラス"""

    def __init__(self, name:str) -> None:
        """パースした関数の情報を格納するクラスです。

        Args:
            name (str): 関数名
        """
        self.name:str = name
        """関数名"""
        self.args:List[FunctionArg] = []
        """引数オブジェクトのリスト"""
        self.return_type:str = 'Void'
        """戻り値のタイプ"""
        self.brief:str = ''
        """関数の説明(Doxygenフォーマットの@briefコメント)"""
        self.raw_comment:str = ''
        """関数の説明(Doxygenフォーマットの全てのコメント)"""
        self.source_path:str = ''
        """関数が定義されているソースファイルのパス"""
        
    
    def add_arg(self, arg) -> None:
        """引数オブジェクトを追加する関数

        引数:
            arg (Argument): 引数オブジェクト
        """
        self.args.append(arg)

    # 引数オブジェクトを返す関数
    def get_args(self) -> List[any]:
        """引数オブジェクトのリストを取得します。

        Returns:
            List[cp]: 引数オブジェクトのリスト
        """
        return self.args
    

    def set_return(self, return_type:str) -> None:
        """戻り値の型名をセットします。"""
        
        self.return_type = return_type
            
    
    def get_return(self)->str:
        """戻り値の型名を取得します。

        戻り値:
            str: 戻り値の型名
        """
        return self.return_type
    
    
    def set_brief(self, brief:str)->None:
        """Briefコメントをセットします。

        引数:
            brief (str): Briefコメント
        """
        self.brief = replace_none_to_empty_string(brief)
        
    def get_brief(self,escape_eol:bool = False)->str:            
        """Doxygenフォーマットで@briefに書かれたコメントをします。

        戻り値:
            str: Briefコメント
        """
        
        if (escape_eol == True):
            return self.brief.replace('\r','\\r').replace('\n','\\n')
        else:
            return self.brief
    
    def set_raw_comment(self, raw_comment) -> None:
        self.raw_comment = replace_none_to_empty_string(raw_comment)
            
    def get_raw_comment(self,escape_eol:bool = False)->str:            
        """ Doxygenフォーマットで記述されたコメントの全てを取得します。    
        引数:
            escape_eol (bool, optional): 改行文字を\でエスケープします。(デフォルト値=False)

        戻り値:
            str: コメント
        """
        
        if (escape_eol == True):
            return self.raw_comment.replace('\r','\\r').replace('\n','\\n')
        else:
            return self.raw_comment
    def get_file_name (self)-> str:
        """ファイル名を取得します"""
        return os.path.basename(self.source_path)
    
    def get_function_name(self)->str:
        """関数名を取得します。"""
        return self.name

    
    def get_prototype(self)->str:
        """関数のプロトタイプ宣言を取得します。
        
        戻り値:
            str: プロトタイプ宣言文字列
        """
        
        prototype = self.return_type + ' ' + self.name + '('
        for arg in self.args:       # 引数リストの作成
            prototype += arg.get_type() + ' ' + arg.get_name()
            if arg != self.args[-1]:
                prototype += ', '   # 最後の引数でない場合はカンマを付ける
        prototype += ');'
        return prototype
    
    def get_return_type(self):
        return self.return_type
    
    def get_parameter_list(self):
        parameter_list = ''
        for arg in self.args:       # 引数リストの作成
            parameter_list += arg.get_name()
            if arg != self.args[-1]:
                parameter_list += ','
        return parameter_list
    
    def get_parameter_type_list(self):
        parameter_type_list = ''
        for arg in self.args:       # 引数リストの作成
            parameter_type_list += arg.get_type()
            if arg != self.args[-1]:
                parameter_type_list += ','
        return parameter_type_list

# パースエラーオブジェクト ================================================================================
class ParseError:
    """エラーを表すクラス"""
    def __init__(self, file_path:os.PathLike, line:str, column:str, message:str):
        """エラー情報を基にエラーオブジェクトを作成します。"""
        self.file_path:os.PathLike = file_path
        """エラーが発生したファイル名"""
        self.line:str = line
        """エラーが発生した行番号"""
        self.column:str = column
        """エラーが発生した列番号"""
        self.message:str = message
        """エラーメッセージ"""
    def get_file_name(self)->str:
        return os.path.basename(self.file_path.name)

# パーサー ===============================================================================================
class Parser:
    # コンストラクタ
    def __init__(self, clang_dll_path):
        clang.cindex.Config.set_library_file(clang_dll_path) # libclang.dllのパスを設定する

    def get_errors(self,tu:clang.cindex.TranslationUnit) -> List[ParseError]:
        """エラーオブジェクトのリストを取得します。

        Args:
            tu (clang.cindex.TranslationUnit): エラーを取得する対象のTranslationUnit

        Returns:
            List[error]: エラーオブジェクト(cppParser.ParseError)のリスト
        """
        errors:List[ParseError] = []    # エラーを格納するリスト
        
        # エラーを取得する(ファイル名、行番号、列番号、エラーメッセージ)    
        for diagnostic in tu.diagnostics:       
            file_name = replace_none_to_empty_string(diagnostic.location.file)
            line = diagnostic.location.line
            column = diagnostic.location.column
            message = diagnostic.spelling
            
            errors.append(ParseError(file_name, line, column, message))      # エラーリストにエラーオブジェクトを追加する


        if(len(errors) == 0):
            print ('')
            print ('Num of errors: ' + str(len(errors)) )
        else:
            print ('')
            print ('Num of errors: ' + str(len(errors)) )
            print ('=========================================================================')
            for error in errors:
                    print(error.get_file_name() + '\tL:' +  str(error.line) + '\t' + error.message)
            print ('=========================================================================')
            
        print ('')
        
        return errors   # エラーリストを返す


    # パーサーを実行する
    def parse(self,source_file, include_paths) -> clang.cindex.TranslationUnit:
        """パースを実行します

        引数:
            source_file (str): 単一のソースファイルの絶対パスを指定します。
            include_paths (List[str]): インクルードディレクトリのリストを指定します。

        戻り値:
            clang.cindex.TranslationUnit: パース結果のオブジェクトを返します。
        """
        index = clang.cindex.Index.create()
        
        args = ['-x', 'c++', '-std=c++14', '-D__CODE_GENERATOR__']                              # パーサーに渡す引数リストを作成する
        for include_path in include_paths: args.append('-I' + include_path)                     # 全てのインクルードパスを引数に追加する
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()              # 前処理のため、ソースコードを文字列として読み出す
        source_code = source_code.replace('DLLEXPORT ', '')                                     # ソースコードの"DLLEXPORT"を削除する
        return index.parse(source_file, args=args, unsaved_files=[(source_file, source_code)])  # パースを実行

    def parse_multiple(self,source_files:List[os.PathLike], include_paths:List[os.PathLike]) -> List[clang.cindex.TranslationUnit]:
        tu_list = []
        for source_file in source_files:
            tu=self.parse(source_file, include_paths)
            tu_list.append(tu)
        return tu_list
    
    def get_functions(self,tu:clang.cindex.TranslationUnit) -> List[CppFunction]:
        """関数リストを取得します。

        Args:
            tu (clang.cindex.TranslationUnit): _description_

        Returns:
            List[CppFunction]: _description_
        """
        source_file_path = tu.spelling
        functions:List[CppFunction] = []
        
        
        for child in tu.cursor.get_children():                  # ルート直下の子要素を走査
            
            # 関数で且つ、対象ファイル内に記述されている関数の場合
            if child.kind == clang.cindex.CursorKind.FUNCTION_DECL and\
            child.location.file.name == source_file_path:                        

                function = CppFunction(child.spelling)             # 関数名を取得して関数オブジェクトを作成する
                function.source_path = source_file_path
                #Doxygen形式のコメントを取得する
                function.set_brief(child.brief_comment)             # @briefのみ
                function.set_raw_comment(child.raw_comment)         # 全てのコメント

                function.return_type = child.result_type.spelling   # 戻り値の型を取得する
                
                for arg in child.get_arguments():                   # 引数名とデータ型を取得する
                    arg_name = arg.spelling
                    arg_type = arg.type.spelling
                    
                    function.add_arg(FunctionArg(arg_name,arg_type))  # 関数オブジェクトに引数オブジェクトを追加する
                
                functions.append(function)                            # 関数リストに関数オブジェクトを追加する

        # 関数リストを返す
        return functions

    # ===============================================================================

    def get_enum_list(self,source_file, include_paths):

        # インデックスを作成する
        index = clang.cindex.Index.create()
        
        # パーサーに渡す引数リストを作成する
        args = ['-x', 'c++', '-std=c++14', '-D__CODE_GENERATOR__']
        for include_path in include_paths:
            args.append('-I' + include_path)

        # 前処理のため、ソースコードを文字列として読み出す
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # ソースコードの"DLLEXPORT"を削除する
        source_code = source_code.replace('DLLEXPORT ', '')

        # ソースコードをパースする
        tu = index.parse(source_file, args=args, unsaved_files=[(source_file, source_code)])

        # Enumリストを作成する
        enum_list = []

        # ソースコードのトップレベルのノードを取得する
        for child in tu.cursor.get_children():
            # Enumで且つソースコードに記述されているEnumの場合
            if child.kind == clang.cindex.CursorKind.ENUM_DECL and child.location.file.name == source_file:
                # Enum名を取得する
                enum_name = child.spelling

                # Enumオブジェクトを作成する
                enum = Enum(enum_name)

                # 要素を取得する
                for element in child.get_children():
                    # 要素名を取得する
                    element_name = element.spelling

                    # 要素の値を取得する
                    element_value = element.enum_value

                    # 要素オブジェクトを作成する
                    enum_element = self.EnumElement(element_name, element_value)

                    # Enumオブジェクトに要素オブジェクトを追加する
                    enum.add_element(enum_element)
                
                # EnumリストにEnumオブジェクトを追加する
                enum_list.append(enum)

        # Enumリストを返す
        return enum_list

# ファイル出力のためのクラス
class FileWriter:
    def __init__(self, output_file:os.PathLike,overwrite:bool = True) -> None:
        self.output_file = output_file
        self.console_output = False
        self.output_items:List[OutputItem] =[
            OutputItem.SOURCE_FILE,
            OutputItem.PROTOTYPE,
            OutputItem.RETURN_TYPE,
            OutputItem.FUNCTION_NAME,
            OutputItem.PARAMETER_NAMES,
            OutputItem.PARAMETER_TYPES,
            OutputItem.BRIEF_COMMENT,
            OutputItem.RAW_COMMENT
        ]  
    def get_item_name(self,output_item:OutputItem) -> str:
        match output_item:
            case OutputItem.SOURCE_ABS_PATH:
                return 'Abusolute Path'
            case OutputItem.SOURCE_REL_PATH:
                return 'Relative Path'
            case OutputItem.SOURCE_FILE:
                return 'File Name'
            case OutputItem.PROTOTYPE:
                return 'Prototype'
            case OutputItem.RETURN_TYPE:
                return 'Return Type'
            case OutputItem.FUNCTION_NAME:
                return 'Function Name'
            case OutputItem.PARAMETER_NAMES:
                return 'Parameter List'
            case OutputItem.PARAMETER_TYPES:
                return 'Parameter Type List'
            case OutputItem.BRIEF_COMMENT:
                return 'Brief comment'
            case OutputItem.RAW_COMMENT:
                return 'Raw comment'
            case _:
                return 'not implemented'
    def get_item_value(self,output_item:OutputItem,cpp_function:CppFunction) ->str:
        match output_item:
            
            #function.get_prototype() + '\t' + function.return_type + '\t' + function.name + '\t' + function.get_parameter_list() + '\t' + function.get_parameter_type_list() + '\t' + function.get_brief() + '\t' + function.get_raw_comment(True)
            
            case OutputItem.SOURCE_ABS_PATH:
                return cpp_function.source_path
            case OutputItem.SOURCE_REL_PATH:
                raise Exception("OutputItem.SOURCE_REL_PATH not implemented")
                return ''
            case OutputItem.SOURCE_FILE:
                return cpp_function.get_file_name()
            case OutputItem.PROTOTYPE:
                return cpp_function.get_prototype()
            case OutputItem.RETURN_TYPE:
                return cpp_function.get_return_type()
            case OutputItem.FUNCTION_NAME:
                return cpp_function.get_function_name()
            case OutputItem.PARAMETER_NAMES:
                return cpp_function.get_parameter_list()
            case OutputItem.PARAMETER_TYPES:
                return cpp_function.get_parameter_type_list()
            case OutputItem.BRIEF_COMMENT:
                return cpp_function.get_brief(True)
            case OutputItem.RAW_COMMENT:
                return cpp_function.get_raw_comment(True)
            case _:
                raise Exception('OutputItem = ' + output_item + ' not implemented')
                return ''
        
# TSV ファイル出力のためのクラス(FileWriterを継承)
class TSV_Writer(FileWriter):
    
    # コンストラクタ
    def __init__(self, output_file:os.PathLike,overwrite = True) -> None:
        FileWriter.__init__(self,output_file,overwrite)  # 継承元のコンストラクタを実行
        f = open(output_file, 'w', encoding='utf-8')     # ファイルを作成して閉じる
        f.close()
        
    def set_console_output(self,console_output:bool):
        self.console_output = console_output
        
    def write_header(self):
        column_names = []
        for output_item in self.output_items:
            column_names.append (self.get_item_name(output_item))

        output_string = '\t'.join(column_names)
        if (self.console_output == True): print(output_string)          # コンソール出力        
        with open(self.output_file, 'a', encoding='utf-8') as f:        # 追記モードで開く
            f.write(output_string + '\n')                               # ファイルに書き込む
        f.close()                                                       # ファイルを閉じる        
        
    def write_functions(self,cpp_functions:List[CppFunction]):
        
        with open(self.output_file, 'a', encoding='utf-8') as f:        # 追記モードで開く
            for cpp_function in cpp_functions:
                
                output_values = [] #ループの反復ごとに出力用のリストを初期化
                for output_item in self.output_items:                    # 出力項目のリストを生成
                    output_values.append(self.get_item_value(output_item,cpp_function))

                output_string = '\t'.join(output_values)                        # タブ区切りで連結

                if (self.console_output == True): print(output_string)          # コンソール出力
                f.write(output_string + '\n')                                   # ファイルに書き込む
                
        f.close()
