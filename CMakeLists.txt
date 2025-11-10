cmake_minimum_required(VERSION 3.25.1)
project(RECHERCHE_DOCUMENTAIRE LANGUAGES CXX)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

add_executable(recherche_documentaire
    src/main.cpp
)
target_compile_features(recherche_documentaire PRIVATE cxx_std_17)
