# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

beman.expected is a C++ library in the Beman Project ecosystem. It implements a reference for `std::expected` (or a related proposal). The library is header-only (INTERFACE target) by default, with an optional C++23 modules mode (`BEMAN_EXPECTED_USE_MODULES=ON` makes it a STATIC target).

License: Apache-2.0 WITH LLVM-exception. All source files must have an SPDX license header.

## Build Commands

### Using CMake presets (preferred)

```bash
cmake --workflow --preset gcc-debug      # configure + build + test
cmake --workflow --preset gcc-release
cmake --workflow --preset llvm-debug
cmake --workflow --preset llvm-release
```

List all presets: `cmake --list-presets=workflow`

### Using the Makefile

The Makefile uses Ninja Multi-Config with `uv run cmake`/`uv run ctest`. It requires `uv` to be installed.

```bash
make              # default target: compile + test (Asan config)
make compile      # build only
make test         # compile then run tests
make ctest        # run tests without rebuilding
make lint         # run pre-commit hooks (clang-format, gersemi, codespell, beman-tidy)
make coverage     # build with Gcov config, run tests, process coverage
```

The Makefile builds into `.build/build-system/` (or `.build/build-<TOOLCHAIN>/`). Config defaults to `Asan`; override with `CONFIG=Debug`, `CONFIG=RelWithDebInfo`, etc.

To use a specific toolchain: `make TOOLCHAIN=gcc-14 compile`

### Running a single test

After building, use ctest with a filter:
```bash
ctest --test-dir .build/build-system --output-on-failure -C Asan -R "test_name_regex"
```

Or from presets:
```bash
ctest --test-dir build/gcc-debug --output-on-failure --preset gcc-debug -R "test_name_regex"
```

## Code Layout

- `include/beman/expected/` — public headers. `expected.hpp` is the main include; `todo.hpp` has the actual declarations (placeholder). `config.hpp` + `config_generated.hpp.in` handle module vs. header-only configuration.
- `tests/beman/expected/` — tests using Catch2 (fetched via FetchContent or vcpkg). Single test executable `beman.expected.tests.todo` built from multiple `.test.cpp` files.
- `examples/` — example programs linked against `beman::expected`.
- `cmake/` — local toolchain files for various compiler versions (gcc-12 through gcc-16, clang-16 through clang-22, etc.).
- `infra/cmake/` — shared Beman infrastructure (install helpers, toolchains, FetchContent config, build telemetry).

## Conventions

- Namespace: `beman::expected`
- CMake target: `beman::expected` (alias of `beman.expected`)
- Headers are included with the `beman/expected/` prefix: `#include <beman/expected/expected.hpp>`
- C++20 minimum standard. The project is a "passive project" — `CMAKE_CXX_STANDARD` must be set externally (presets set it to 20).
- Formatting: clang-format with 119-column limit, 4-space indent, no tab, pointers left-aligned (`int* p`). Run via pre-commit or `clang-format -i`.
- CMake formatting: gersemi (run via pre-commit).
- Test files follow the pattern `<name>.test.cpp` and include the header twice to verify idempotency.
- Project-specific CMake options are prefixed with `BEMAN_EXPECTED_`.
- Beman Standard compliance is checked by `beman-tidy` (configured in `.beman-tidy.yaml`, run via pre-commit).
