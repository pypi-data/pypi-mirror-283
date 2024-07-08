SET(CPACK_RPM_PACKAGE_REQUIRES "python-pip, python-devel")
SET(PY_PACKAGE_NAME "test_cython")
find_program(PYTHON "python3")

set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py")
set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
set(DEPS        "${CMAKE_CURRENT_SOURCE_DIR}/${PY_PACKAGE_NAME}/__init__.py")
set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}")
set(DIST        "${CMAKE_CURRENT_BINARY_DIR}/dist/")

configure_file(${SETUP_PY_IN} ${SETUP_PY})

add_custom_command(OUTPUT ${OUTPUT}
                COMMAND ${PYTHON}
                ARGS setup.py build)

add_custom_target(cython_target ALL DEPENDS ${OUTPUT})

file(COPY ${PY_PACKAGE_NAME} DESTINATION ${OUTPUT})
ADD_CUSTOM_TARGET(cython_packing ALL COMMAND ${PYTHON} ${SETUP_PY} bdist_egg --exclude-source-files --dist-dir=${DIST} WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} DEPENDS test_cython)

install(
        TARGETS
        test_cython
        LIBRARY
        DESTINATION test_cython/lib
        RUNTIME
        DESTINATION test_cython/lib
        PUBLIC_HEADER
        DESTINATION test_cython/include
        RESOURCE
        DESTINATION test_cython
        )