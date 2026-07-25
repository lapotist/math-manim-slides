# ROC 112 TCFS mathematics gifted assessment, fill-in question 9

## Teaching intent

The audience already knows decimal place value, digit sums, small perfect
squares, and division with remainder. It may not yet be comfortable using a
necessary congruence condition as a filter, or proving that a finite candidate
list is complete.

The likely first misconception is to begin testing every five-digit square, or
to write a few attractive palindromes and hope one works. The lesson instead
asks: **which condition removes the most uncertainty before any large square is
tested?** A palindrome is kept as one concrete five-card object throughout.
The cards first fold into a digit sum, then unfold into the complete candidate
set, and finally return after the surviving square is verified.

The motivating object is the mirrored row `a b c b a`. The boundary case is
the largest possible inner contribution `2b+c=27`, which forces the outer
digit to be at least 5. The earned realization is that four apparently tangled
conditions become three small gates: one digit sum, eight palindromes, and
three exact square checks.

## Source reconstruction

- Canonical page: `https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87%E5%84%AA%E7%8F%AD/112%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87`
- Frozen page SHA-256: `8ef9b13e28c992e21dd874cfeabbb6ad66dcacdeec3c326f058ff561de9ba094`
- Problem asset: Drive `1wZiSE5cZZI9Fr_YJovGP_H3aWoFXxc_H`, PDF page 9,
  SHA-256 `277e49efb3aca44666e17c2c4135b6047922f25adee58952560416996140acbd`
- Solution asset: YouTube `E8hGcX6oQO4`, confirmed public stream, exact locator
  `00:00-08:52.40`
- Research stream: 518x360, 533.153379 seconds, SHA-256
  `876802b78b7197c47e2c984fc31dc71f0591d70fe704bfceab0803dbebc17ff3`
- Boundary inspection: the complete solution remains readable at 08:52.40;
  a device-control overlay obscures it by 08:52.45.

The PDF page identifies the problem but its worked region is blank. The video
is therefore the reasoning source. It writes `n=abcba=y^2`, restricts `a` by
possible final digits of a square, and writes `m=2a+2b+c=x^2<45`. It checks
`16,25,36` and keeps `36` because their digit sums are `7,7,9`. It uses
`2b+c<=27` to discard `a=1,4`, enumerates the eight remaining palindromes,
then applies the square residues modulo 4. The source displays `(36,69696)` in
the margin before finishing the working and ultimately marks `69696` among the
three modulo-4 survivors.

The adaptation preserves that mathematical route but does not reproduce the
source handwriting or early answer. It adds a proof of the modulo-4 rule and
exact consecutive-square brackets for `96669` and `98289`, so the final choice
is verified rather than selected by appearance.

## Independent mathematics check

Let

```text
n = abcba = 10001a + 1010b + 100c,
1 <= a <= 9,  0 <= b,c <= 9.
```

Its digit sum is `m=2a+2b+c`. Since five decimal digits have sum at most 45,
and `m` is a two-digit square, only `16,25,36` are possible. Their own digit
sums are `7,7,9`; only `9=3^2` is a square. Thus `m=36`.

The first and last digits are both `a`. A decimal square can end only in
`0,1,4,5,6,9`, and `a` is nonzero, so `a` belongs to `{1,4,5,6,9}`. Meanwhile
`2b+c<=2*9+9=27`. From `36=2a+(2b+c)`, `2a>=9`, and the integer digit bound
gives `a>=5`. Hence `a` belongs to `{5,6,9}`.

For each remaining `a`, solve `c=36-2a-2b` under `0<=b,c<=9`:

```text
a=5: (b,c)=(9,8)                         -> 59895
a=6: (b,c)=(8,8),(9,6)                   -> 68886,69696
a=9: (b,c)=(5,8),(6,6),(7,4),(8,2),(9,0) -> 95859,96669,97479,98289,99099
```

This is exhaustive because every allowed `a` is handled and every integer `b`
whose resulting `c` is a digit is listed. For any integer `k`, either
`k=2r` and `k^2` is `0 mod 4`, or `k=2r+1` and `k^2` is `1 mod 4`. Reading the
last two decimal digits therefore leaves exactly `69696`, `96669`, and `98289`.
The condition is necessary, not sufficient.

Exact checks finish the search:

```text
310^2 = 96100 < 96669 < 96721 = 311^2,
264^2 = 69696,
313^2 = 97969 < 98289 < 98596 = 314^2.
```

Finally `6+9+6+9+6=36=6^2` and `3+6=9=3^2`. Thus the unique pair is
`(m,n)=(36,69696)`. A separate exhaustive computation over all 900 digit
triples `(a,b,c)` gives this same single solution.

## Visual grammar

- Yellow means the mirrored outer digit `a` and later the selected result.
- Blue means the mirrored inner digit `b`.
- Green means the center digit `c` and valid constraints.
- Purple means a surviving square test.
- Coral means a rejected candidate or failed condition.
- The five digit cards remain a spatial palindrome; formulas are always built
  from highlighted card groups and then translated back to digit cards.
- No source scan, handwriting, channel artwork, logo, or video frame appears in
  the lesson.

## Beat map and motion purposes

### 01 mirror_three_digits

Reveal `a,b,c` from left to center, then copy `b` and `a` into their reflected
positions. The copying motion answers why a five-digit palindrome has only
three independent digits. End with `n=abcba`, but no numerical candidate.

### 02 fold_digit_sum

Highlight the two `a` cards, the two `b` cards, and the center `c` card in
sequence. Copy those groups into `m=2a+2b+c`, then reveal the three conditions
on `m`. The motion translates the same object from positions to contributions.

### 03 find_the_digit_sum

Place `m` on the visible interval from 10 to 45 and reveal only the square
stops `16,25,36`. Open each two-digit card into its own digit sum; cross the two
sevens and retain `9=3^2`. Only after that check settles, state `m=36`.

### 04 filter_outer_digit

Return to the palindrome and highlight its shared leading/trailing digit.
Generate the possible nonzero terminal digits of a square. Then fill the inner
three positions to their maximum `9+9+9=27`; the visible capacity bound forces
`a>=5`, crossing `1,4` and retaining `5,6,9`.

### 05 enumerate_a_nine

Freeze `a=9` and vary only `b,c` while `2b+c=18` remains fixed. Each deliberate
state `(5,8),(6,6),(7,4),(8,2),(9,0)` creates its corresponding five-card
palindrome. The motion shows where all five candidates come from.

### 06 enumerate_a_six

Dim the first branch, freeze `a=6`, and vary the only two valid inner states
`(8,8),(9,6)` under `2b+c=24`. Keep both new palindromes visible beside the
first branch.

### 07 enumerate_a_five

Freeze `a=5`; only `(b,c)=(9,8)` satisfies `2b+c=26`. Create `59895`, then
rearrange the three branches into one settled eight-card search set. The
rearrangement answers the completeness question, not a new arithmetic step.

### 08 test_mod_four

Prove the two square residues using even and odd roots. Highlight the final two
digits on every candidate, attach its actual remainder, and cross only those
with remainder 2 or 3. Keep all rejected cards dimly visible until the three
survivors have been accounted for.

### 09 isolate_three_survivors

Move `96669`, `69696`, and `98289` into three large test positions. Restore the
condition `n` is a square and explicitly label modulo 4 as only a first gate.
No survivor is selected yet.

### 10 bracket_first_false

Place `96669` on a number line between `310^2=96100` and `311^2=96721`.
Its position strictly between consecutive squares visibly rejects it.

### 11 bracket_second_false

Apply the same exact construction to `98289`, between `313^2=97969` and
`314^2=98596`. Reusing the construction adds a second proof case rather than
decorative repetition.

### 12 hold_middle_square_test

Return to the three candidate cards with the two false ones crossed. Place
`264^2 ? 69696` beneath the untouched middle card and stop on a settled frame.
The equality and requested pair are not yet shown.

### 13 reveal_and_recheck_pair

Compute `264^2=69696` in the pre-answer position, clear the completed test, then
rebuild the surviving number as five colored digits beside the fixed equality.
Pair the mirrored digits to recover `36`, check `36=6^2` and `3+6=9=3^2`, and
only after every check lands reveal `(m,n)=(36,69696)`.

## Build constraints

- Edit only `lessons/tcfs_112_math_gifted/q09/`; generated media stays in the
  lesson's ignored build directories.
- Scene class: `CarloTcfs112MathQ09`.
- Thirteen beats, all `loop=false`.
- Traditional Chinese uses `label()`; `MathTex` contains ASCII mathematics.
- Render in an isolated media directory through the lesson runner, first at low
  quality and then at `--quality h`.
- Inspect all endpoints, the complete one-frame-per-second sweep, digit-card
  rearrangements, residue labels, both square brackets, the pre-answer hold,
  and the final return to the palindrome.
- Stop at `draft_rendered`; do not run `freeze-qa` or change collection state.
