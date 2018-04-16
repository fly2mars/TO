cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

set(APP_NAME simp)
project(${APP_NAME})

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/")

##########################################
# Specify the 3d-party library directory #
##########################################
INCLUDE(${PROJECT_SOURCE_DIR}/cmake/UseEigen.cmake)

#### project sources
FILE(GLOB SRC_SOURCES	${CMAKE_SOURCE_DIR}/src/*.cpp ${CMAKE_SOURCE_DIR}/src/*.c) 
FILE(GLOB SRC_HEADERS	${CMAKE_SOURCE_DIR}/src/*.h ${CMAKE_SOURCE_DIR}/src/*.hpp)
set(SRC_LIST ${SRC_SOURCES} ${SRC_HEADERS}  )


set(PROJECT_INCLUDE_DIRS ${CMAKE_SOURCE_DIR}/include)
set(PROJECT_LIBRARY_DIRS ${CMAKE_SOURCE_DIR}/lib)

include_directories(
  ${PROJECT_INCLUDE_DIRS})
  
link_directories(
  ${PROJECT_LIBRARY_DIRS})


#############
# Test Unit #
#############
FILE(GLOB SRC_SOURCES_TEST_UNIT	${CMAKE_SOURCE_DIR}/src/testUnit/*.cpp ${CMAKE_SOURCE_DIR}/src/testUnit/*.c) 
FILE(GLOB SRC_HEADERS_TEST_UNIT	${CMAKE_SOURCE_DIR}/src/testUnit/*.h ${CMAKE_SOURCE_DIR}/src/testUnit/*.hpp)
add_executable (TestUnit  ${SRC_LIST} ${SRC_SOURCES_TEST_UNIT} ${SRC_HEADERS_TEST_UNIT})


# target_link_libraries (TestUnit)

########
# SIMP #
########
FILE(GLOB SRC_SOURCES_SIMP	${CMAKE_SOURCE_DIR}/src/simp/*.cpp ${CMAKE_SOURCE_DIR}/src/simp/*.c) 
FILE(GLOB SRC_HEADERS_SIMP	${CMAKE_SOURCE_DIR}/src/simp/*.h ${CMAKE_SOURCE_DIR}/src/simp/*.hpp)
add_executable (${APP_NAME}  ${SRC_LIST} ${SRC_SOURCES_SIMP} ${SRC_HEADERS_SIMP})

