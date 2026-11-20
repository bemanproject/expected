// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// NEGATIVE: or_else on expected<T,E&> must return expected<T, X> for some X
// EXPECT: "F must return expected<T, X> for some X"
#include <beman/expected/expected.hpp>
void test() {
    int                                  err = 0;
    beman::expected::expected<int, int&> e(beman::expected::unexpect, err);
    // F returns expected<double, int&> but must be expected<int, X>
    e.or_else([](int& v) -> beman::expected::expected<double, int&> { return 0.0; });
}
