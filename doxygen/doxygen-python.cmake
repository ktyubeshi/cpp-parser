find_package(Doxygen
             REQUIRED dot
             OPTIONAL_COMPONENTS mscgen dia)

# Doxygen の設定
# DOXYGEN_<TAG> という形式のCMake変数は、<TAG>の部分がDoxyfileの設定項目名と対応します。
# プロジェクト名など、一部の変数はCMakeによって自動的に設定されます。
#   https://cmake.org/cmake/help/latest/module/FindDoxygen.html
#   https://www.doxygen.nl/manual/config.html
#   http://www.doxygen.jp/config.html

# 出力言語設定
    set(DOXYGEN_OUTPUT_LANGUAGE "Japanese")

# 外観設定
    set(DOXYGEN_DISABLE_INDEX "YES")                        # ページ上部のインデックスを表示しない
    set(DOXYGEN_GENERATE_TREEVIEW "YES")                    # ツリー表示を有効にする

    set(DOXYGEN_OPTIMIZE_OUTPUT_FOR_C "NO")                 # C言語のソースだけで構成されている場合、"YES" にすることで出力がC言語に最適化されます。
    set(DOXYGEN_OPTIMIZE_OUTPUT_JAVA "YES")                 # pythonの場合は、JAVAに最適化した出力を使用することが推奨されています。
                                                            # http://www.doxygen.jp/config.html#cfg_optimize_output_java

    set(DOXYGEN_MARKDOWN_SUPPORT "YES")                     # コメントをMarkdownフォーマットに従って前処理し、より読みやすいドキュメントを作成します。
        set(DOXYGEN_TOC_INCLUDE_HEADINGS "5")               # TOCに含める見出しレベルを指定します。(0～99,Default:5)

#  set(DOXYGEN_HTML_STYLESHEET  "${CMAKE_CURRENT_LIST_DIR}/doxygen.css")
#  set(DOXYGEN_HTML_FOOTER      "${CMAKE_CURRENT_LIST_DIR}/footer.html" )
#  set(DOXYGEN_HTML_HEADER      "${CMAKE_CURRENT_LIST_DIR}/header.html" )
#  set(DOXYGEN_HTML_INDEX_FILE  "${CMAKE_CURRENT_LIST_DIR}/index.html"  )

# set(USE_MDFILE_AS_MAINPAGE "${CMAKE_CURRENT_LIST_DIR}/index.md") #トップページにMarkdownファイルを使用する場合は.mdファイルを指定する

# 処理対象
    set(DOXYGEN_INPUT_ENCODING UTF-8)
    set(DOXYGEN_FILE_PATTERNS *.py *.md)        # 処理対象のファイルパターン
    set(DOXYGEN_EXCLUDE_PATTERNS "*.cmake")     # 除外するファイルパターン

    
# Build related configuration options
# https://www.doxygen.nl/manual/config.html#config_build

    set(DOXYGEN_EXTRACT_ALL "YES")                        # 全ての実体をドキュメントに出力します。
                                                          # このオプションをYESにした場合、WARNINGS = YES は無視され、文書化されていないメンバーに関する警告が無効化されます。

    # set(DOXYGEN_EXTRACT_PRIVATE "YES")                  # privateメンバーをドキュメントに出力します。
    # set(DOXYGEN_EXTRACT_STATIC "YES")                   # staticメンバーをドキュメントに出力します。
    

# 出力
    set(DOXYGEN_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/doxygen-output)  # 出力先ディレクトリ

doxygen_add_docs(doxygen
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/docs
    ALL
    COMMENT comment
)

message("DOXYGEN_OUTPUT_DIRECTORY ${DOXYGEN_OUTPUT_DIRECTORY}")

