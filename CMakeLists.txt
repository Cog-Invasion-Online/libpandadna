cmake_minimum_required(VERSION 2.8.8 FATAL_ERROR)
project(libpandadna)

### Panda3D dir ###
if (DEFINED LINK_ALL_STATIC)
    set(P3BUILT built_x64_static)
else()
    set(P3BUILT built_x64)
endif ()
SET(PANDA_DIR ..\\cio-panda3d\\${P3BUILT})
SET(PYTHON2_EXECUTABLE "${PANDA_DIR}\\python\\ppython")
SET(BUILD_STATIC_LIB OFF CACHE BOOL "If true, will build a static lib")
SET(PYTHON_LIBRARY "python27")
execute_process(COMMAND ${PYTHON2_EXECUTABLE} "${CMAKE_SOURCE_DIR}/src/run_interrogate.py" "${PANDA_DIR}")

### Define core components ###
set(BASE_FILES
    src/base/DNALoader.h
    src/base/DNALoader.cxx
    src/base/DNAStorage.h
    src/base/DNAStorage.cxx
    src/base/dnabase.h
    src/base/config_dna.h
    src/base/config_dna.cxx
)

set(SUIT_FILES
    src/suit/DNASuitPath.h
    src/suit/DNASuitPath.cxx
    src/suit/DNASuitEdge.h
    src/suit/DNASuitEdge.cxx
    src/suit/DNASuitPoint.h
    src/suit/DNASuitPoint.cxx
    src/suit/SuitLeg.h
    src/suit/SuitLeg.cxx
    src/suit/SuitLegList.h
    src/suit/SuitLegList.cxx
)

set(COMPONENTS_FILES
    src/components/DNAAnimBuilding.cxx
    src/components/DNAAnimBuilding.h
    src/components/DNAAnimProp.cxx
    src/components/DNAAnimProp.h
    src/components/DNABattleCell.cxx
    src/components/DNABattleCell.h
    src/components/DNACornice.cxx
    src/components/DNACornice.h
    src/components/DNADoor.cxx
    src/components/DNADoor.h
    src/components/DNAFlatBuilding.cxx
    src/components/DNAFlatBuilding.h
    src/components/DNAFlatDoor.cxx
    src/components/DNAFlatDoor.h
    src/components/DNAGroup.cxx
    src/components/DNAGroup.h
    src/components/DNAInteractiveProp.cxx
    src/components/DNAInteractiveProp.h
    src/components/DNALandmarkBuilding.cxx
    src/components/DNALandmarkBuilding.h
    src/components/DNANode.cxx
    src/components/DNANode.h
    src/components/DNAProp.cxx
    src/components/DNAProp.h
    src/components/DNASign.cxx
    src/components/DNASign.h
    src/components/DNASignBaseline.cxx
    src/components/DNASignBaseline.h
    src/components/DNASignGraphic.cxx
    src/components/DNASignGraphic.h
    src/components/DNAStreet.cxx
    src/components/DNAStreet.h
    src/components/DNAVisGroup.cxx
    src/components/DNAVisGroup.h
    src/components/DNAWall.cxx
    src/components/DNAWall.h
    src/components/DNAWindows.cxx
    src/components/DNAWindows.h
)

set(IGATE_FILES
    src/base_igate.cxx
    src/suit_igate.cxx
    src/components_igate.cxx
    src/libpandadna_module.cxx
)

include_directories(src/base)
include_directories(src/suit)
include_directories(src/components)
include_directories(${PANDA_DIR}/include)
include_directories(${PANDA_DIR}/python/include)
include_directories(../../rpbmStudios/panda_cxx_projs/libpandabsp/include)
link_directories(${PANDA_DIR}/lib)
link_directories(${PANDA_DIR}/python/libs)
link_directories(../../rpbmStudios/panda_cxx_projs/libpandabsp/Release)

set(LIBPFX "")
if(WIN32)
    set(LIBPFX "lib")
    add_definitions(/wd4275)
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    execute_process(COMMAND "${CMAKE_C_COMPILER}" -dumpversion OUTPUT_VARIABLE GCC_VERSION)
    message(STATUS "GCC Version: ${GCC_VERSION}")
    if(GCC_VERSION VERSION_GREATER 4.7 OR GCC_VERSION VERSION_EQUAL 4.7)
        add_definitions(-std=c++11) # Enable the new C++ standard
    else()
        add_definitions(-std=c++0x) # Enable the new C++ standard
    endif()
endif()

add_definitions(-DBUILDING_DNA)

if (NOT BUILD_STATIC_LIB)
    set(PANDA_LIBS
        ${LIBPFX}p3framework
        ${LIBPFX}panda
        ${LIBPFX}pandafx
        ${LIBPFX}pandaexpress
        ${LIBPFX}p3dtool
        ${LIBPFX}p3dtoolconfig
        ${LIBPFX}p3direct
		${LIBPFX}p3pystub
    )

    # Add p3interrogatedb, if it exists
    find_library(HAVE_P3INTERROGATEDB
                 ${LIBPFX}p3interrogatedb
                 HINTS ${PANDA_DIR}/lib)
                 
    if (HAVE_P3INTERROGATEDB)
        message(STATUS "libp3interrogatedb found")
        LIST(APPEND PANDA_LIBS ${LIBPFX}p3interrogatedb)
    else()
        message(STATUS "libp3interrogatedb not found")
    endif()

    # Add p3pandatoolbase, if it exists
    find_library(HAVE_P3PANDATOOLBASE
                 ${LIBPFX}p3pandatoolbase
                 HINTS ${PANDA_DIR}/lib)

    if (HAVE_P3PANDATOOLBASE)
        message(STATUS "libp3pandatoolbase found")
        LIST(APPEND PANDA_LIBS ${LIBPFX}p3pandatoolbase)
    else()
        message(STATUS "libp3pandatoolbase not found")
    endif()

    if(WIN32)
        if (DEFINED LINK_ALL_STATIC)
            set(LIB_TYPE STATIC)
            set(OUT_EXT .lib)
            add_definitions(-DLINK_ALL_STATIC)
        else ()
            set(LIB_TYPE SHARED)
            set(OUT_EXT .pyd)
        endif ()
        add_library(libpandadna ${LIB_TYPE}
            ${BASE_FILES}
            ${SUIT_FILES}
            ${COMPONENTS_FILES}
            ${IGATE_FILES}
        )
        SET_TARGET_PROPERTIES(libpandadna PROPERTIES SUFFIX ${OUT_EXT})
        target_link_libraries(libpandadna ${PANDA_LIBS} ${PYTHON_LIBRARY} bsp.lib)
        add_custom_command(TARGET libpandadna
                           PRE_BUILD
                           COMMAND ${PYTHON2_EXECUTABLE} "${CMAKE_SOURCE_DIR}/src/run_interrogate.py" "${PANDA_DIR}"
                           COMMENT "Interrogate")
        if (DEFINED LINK_ALL_STATIC)
            add_custom_command(TARGET libpandadna POST_BUILD COMMAND copy /Y Release\\libpandadna.lib ${PANDA_DIR}\\lib\\libpandadna.lib)
        else()
            add_custom_command(TARGET libpandadna POST_BUILD COMMAND copy /Y Release\\libpandadna.pyd ${PANDA_DIR}\\bin\\libpandadna.pyd)
            #add_custom_command(TARGET vifparser POST_BUILD COMMAND copy /Y ${CMAKE_BUILD_TYPE}\\libvif.pdb ${PANDA_DIR}\\bin\\libvif.pdb)
        endif()

    else()
        add_library(pandadna MODULE
            ${BASE_FILES}
            ${SUIT_FILES}
            ${COMPONENTS_FILES}
            ${IGATE_FILES}
        )
        target_link_libraries(pandadna ${PANDA_LIBS} ${PYTHON_LIBRARY})
        add_custom_command(TARGET pandadna
                           PRE_BUILD
                           COMMAND ${PYTHON2_EXECUTABLE} "${CMAKE_SOURCE_DIR}/src/run_interrogate.py" "${PANDA_DIR}"
                           COMMENT "Interrogate")
    endif()

else()

    if(WIN32)
        add_library(libpandadna STATIC
            ${BASE_FILES}
            ${SUIT_FILES}
            ${COMPONENTS_FILES}
            ${IGATE_FILES}
        )
        add_custom_command(TARGET libpandadna
                           PRE_BUILD
                           COMMAND ${PYTHON2_EXECUTABLE} "${CMAKE_SOURCE_DIR}/src/run_interrogate.py" "${PANDA_DIR}"
                           COMMENT "Interrogate")

    else()
        add_library(pandadna STATIC
            ${BASE_FILES}
            ${SUIT_FILES}
            ${COMPONENTS_FILES}
            ${IGATE_FILES}
        )
        add_custom_command(TARGET pandadna
                           PRE_BUILD
                           COMMAND ${PYTHON2_EXECUTABLE} "${CMAKE_SOURCE_DIR}/src/run_interrogate.py" "${PANDA_DIR}"
                           COMMENT "Interrogate")
    endif()

endif()



### Setup source groups and defines for configurables ###
source_group("base" FILES ${BASE_FILES})
source_group("suit" FILES ${SUIT_FILES})
source_group("components" FILES ${COMPONENTS_FILES})
source_group("interrogate_files" FILES ${IGATE_FILES})

