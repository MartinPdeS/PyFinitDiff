#CREDENTIALS------------------------------------------------------------------------
set(Token    "$ENV{PyPiUsername}")
set(Password "$ENV{PyPiPassword}")

#COMPILE_CONFIGURATION--------------------------------------------------------------
set(CMAKE_Fortran_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS     1)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD          17)
#set(CMAKE_CXX_FLAGS_DEBUG    " -static-libgcc -static-libstdc++ -Wall -Wextra -pedantic -Werror -fopenmp -D MS_WIN64")
#set(CMAKE_CXX_FLAGS_DEBUG     " -static-libgcc -static-libstdc++ -Wall -Wextra -pedantic -Werror -fopenmp -D")

#set(CMAKE_CXX_FLAGS_RELEASE  " -static-libgcc -static-libstdc++ -Wall -Wextra -march=native -O3 -fopenmp -D MS_WIN64")
#set(CMAKE_CXX_FLAGS_RELEASE   " -static-libgcc -static-libstdc++ -Wall -Wextra -march=native -O3 -fopenmp -D")

set(CMAKE_CXX_FLAGS_RELEASE "-fopenmp -O3 -march=native")

set(CMAKE_Fortran_FLAGS_DEBUG    " -fPIC")
set(CMAKE_Fortran_FLAGS_RELEASE  " -fPIC")


#INCLUDE_&_PACKAGES_DIRECTORY--------------------------------------------------------------
find_package(OpenMP REQUIRED)
add_subdirectory(extern/pybind11)
include_directories("${CMAKE_SOURCE_DIR}/PyMieSim/Cpp")



#PYTHON_VERSION----------------------------------------------------------------------------
IF (DEFINED PYTHON_VERSION_STRING)
    #set(Python_VERSION ${PYTHON_VERSION_STRING})
    find_package(Python ${py} COMPONENTS Interpreter Development REQUIRED)
    include_directories(${PYTHON_INCLUDE_DIRS})
ELSE()
    find_package(Python COMPONENTS Interpreter Development)
    include_directories(${PYTHON_INCLUDE_DIRS})
ENDIF()
