cmake_minimum_required (VERSION 2.6)
# Projektname
project(Uebung5)
# F�ge Source-Files hinzu
set(SRC_FILES object.cpp)
set(SRC_FILES program.cpp ${SRC_FILES})
set(SRC_FILES dynamicobjectlist.cpp ${SRC_FILES})
set(SRC_FILES dynamicobjectlist.hpp ${SRC_FILES})
set(SRC_FILES object.h ${SRC_FILES})
# Erzeuge Binary
add_executable(Uebung5 ${SRC_FILES})