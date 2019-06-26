cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

set(APP_NAME testUnits)
project(${APP_NAME})

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/../cmake/Modules/")

#### project sources
FILE(GLOB SRC_SOURCES	${CMAKE_SOURCE_DIR}/src/*.cpp ${CMAKE_SOURCE_DIR}/src/*.c) 
FILE(GLOB SRC_HEADERS	${CMAKE_SOURCE_DIR}/src/*.h ${CMAKE_SOURCE_DIR}/src/*.hpp)
set(SRC_LIST ${SRC_SOURCES} ${SRC_HEADERS}  )


set(PROJECT_INCLUDE_DIRS ${CMAKE_SOURCE_DIR}/include)
set(PROJECT_LIBRARY_DIRS ${CMAKE_SOURCE_DIR}/lib)
set(PYTHON_ROOT_DIR D:/Python/Anaconda)


## find python
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(
  ${PROJECT_INCLUDE_DIRS}
  #${PYTHON_ROOT_DIR}/include
  )
  
link_directories(
  ${PROJECT_LIBRARY_DIRS}
  ${PYTHON_ROOT_DIR}/libs)

add_executable (${APP_NAME}  ${SRC_LIST})
target_link_libraries (${APP_NAME} ${PYTHON_LIBRARIES} )

# set the final binary dir
set(PROJECT_BINARY_DIR ${CMAKE_SOURCE_DIR}/bin)

# copy binary to running director
ADD_CUSTOM_COMMAND(TARGET ${APP_NAME}
          POST_BUILD          
          COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${APP_NAME}> ${PROJECT_BINARY_DIR}
)

set_target_properties(${APP_NAME} PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY 
                      "${CMAKE_SOURCE_DIR}/bin"
)
