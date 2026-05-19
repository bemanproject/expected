# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

find_package(Catch2 3 REQUIRED)

add_executable(beman.expected.tests.todo)
target_sources(
    beman.expected.tests.todo
    PRIVATE bad_expected_access.test.cpp expected.test.cpp unexpected.test.cpp
)
target_link_libraries(
    beman.expected.tests.todo
    PRIVATE beman::expected Catch2::Catch2WithMain
)
if(BEMAN_EXEMPLAR_USE_MODULES)
    set_target_properties(
        beman.expected.tests.todo
        PROPERTIES CXX_MODULE_STD ON
    )
endif()

list(APPEND CMAKE_MODULE_PATH ${Catch2_SOURCE_DIR}/extras)

include(Catch)
catch_discover_tests(beman.expected.tests.todo)
