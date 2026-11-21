// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// NEGATIVE: or_else Mandates G is expected<T, X> for some X
// EXPECT: "F must return expected<T, X> for some X"
#include <beman/expected/expected.hpp>
void test() {
    beman::expected::expected<int, int> e(beman::expected::unexpect, 1);
    e.or_else([](int v) -> beman::expected::expected<long, int> { return static_cast<long>(v); });
}
