// tests/beman/expected/expected_ref_or_else_returns_value_fail.cpp   -*-C++-*-
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// NEGATIVE: or_else on expected<T&, E> must not accept expected<T, X>, even
// though its value_type is T: the value path would copy the referent
// EXPECT: "F must return expected<T&, X> for some X"
#include <beman/expected/expected.hpp>
void test() {
    beman::expected::expected<int&, int> e(beman::expected::unexpect, 1);
    e.or_else([](int) -> beman::expected::expected<int, int> { return 0; });
}
