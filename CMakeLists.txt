cmake_minimum_required(VERSION 3.14 FATAL_ERROR)

# プロジェクト名を設定します。
# このCMakeLists.txtはDoxygenのドキュメント生成のみに使用しているため、言語はNONEに設定しています。
project(cpp-parser LANGUAGES NONE)

include (${CMAKE_SOURCE_DIR}/doxygen/doxygen-python.cmake)
