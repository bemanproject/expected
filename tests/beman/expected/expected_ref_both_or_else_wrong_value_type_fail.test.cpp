// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// NEGATIVE: or_else on expected<T&, E&> must return expected<T&, X> for some X
// EXPECT: "F must return expected<T&, X> for some X"
#include <beman/expected/expected.hpp>
namespace {
using E = beman::expected::expected<int&, int&>;
using G = beman::expected::expected<double&, int&>; // double& is not int&
} // namespace
void test() {
    double d   = 0;
    int    err = 0;
    E      e   = E(beman::expected::unexpect, err);
    // F returns expected<double&, int&>, but e is expected<int&, int&>
    e.or_else([&](int&) -> G { return d; });
}
