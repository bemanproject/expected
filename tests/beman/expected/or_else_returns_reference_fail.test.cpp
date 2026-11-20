// tests/beman/expected/or_else_returns_reference_fail.cpp            -*-C++-*-
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// NEGATIVE: or_else on expected<T, E> must not accept expected<T&, X>, even
// though expected<T&, X>::value_type is T
// EXPECT: "F must return expected<T, X> for some X"
#include <beman/expected/expected.hpp>
namespace {
int fallback = 0;
} // namespace
void test() {
    beman::expected::expected<int, int> e(beman::expected::unexpect, 1);
    e.or_else([](int) -> beman::expected::expected<int&, int> { return fallback; });
}
