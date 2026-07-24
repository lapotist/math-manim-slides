# ROC 114 TCFSH gifted mathematics, fill-in 13

The source prompt asks for a positive parameter, but its stated sum of solutions
is inconsistent. The lesson therefore treats the contradiction as the result,
then clearly labels the sum-420 computation as a corrected variant. It never
presents the corrected answer as the answer to the printed question.

| Beat | Visual question | Evidence earned on screen |
| --- | --- | --- |
| `meet_claim` | Can the requested sum 345 actually occur? | Only the equation and the claimed sum appear; no answer is previewed. |
| `split_number` | What do floor and fractional part measure? | A moving number is split into its integer step `n` and remainder `r`. |
| `sign_filter` | Where can a nonzero solution live? | Negative `x` has incompatible signs; `0<x<1` has zero left side; `x=0` contributes nothing. |
| `normalize_strip` | How can all integer strips share one equation? | With `n=floor(x)` and `y=n/x`, the equation becomes `a=y(1-y)`. |
| `choose_branch` | Which of the two symmetric roots fits its strip? | The `x=n/t` branch lies beyond `n+1`; only `x_n=cn` remains. |
| `march_candidates` | Why are the solutions consecutive? | The offset `(c-1)n` grows steadily until it first reaches the next integer boundary. |
| `sum_candidates` | What does a total of 345 force? | The consecutive candidates sum to `cN(N+1)/2=345`. |
| `build_two_bounds` | What must the last candidate satisfy? | `c>1` bounds `N` above, while `x_N<n+1` bounds the same `N` below. |
| `meet_contradiction` | Can one integer pass both bounds? | `N<=25` gives `(N+1)^2<=676`, contradicting `690<(N+1)^2`. |
| `separate_correction` | Why does the source later compute another value? | The printed sum 345 and corrected sum 420 are placed in separate columns. |
| `solve_corrected` | Does the corrected variant close consistently? | `N=28`, `c=210/203`, `t=1/30`, `a=29/900`, and the next candidate lands exactly at 30 and is excluded. |

## Review traps

- Include `x=0` in the logic: it is always a solution but contributes zero to
  the sum.
- The larger quadratic branch must be rejected with the half-open strip
  condition, not by visual plausibility.
- The candidate indices are consecutive because `(c-1)n<1` is monotone in
  positive integer `n`.
- Keep the source correction neutral and visible. The deck must not force the
  corrected `29/900` onto the printed sum-345 problem.
