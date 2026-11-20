// tests/beman/expected/expected_ref_or_else_wrong_value_type_fail.cpp -*-C++-*-
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// NEGATIVE: or_else on expected<T&,E> must return expected<T&, X> for some X
// EXPECT: "F must return expected<T&, X> for some X"
#include <beman/expected/expected.hpp>
namespace {
using E = beman::expected::expected<int&, int>;
using G = beman::expected::expected<double&, int>;
} // namespace
void test() {
    double d = 0;
    E      e = beman::expected::unexpected(0);
    // F returns expected<double&, int>, but e is expected<int&, int>
    e.or_else([&](int) -> G { return d; });
}
