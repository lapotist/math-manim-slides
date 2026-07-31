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

## Beat map

### 01 mirror_three_digits

先不要急著猜五位數。

動作目的：讓「五個位置，其實只有三個選擇」在穩定畫面上單獨成立，再進入下一步。

### 02 fold_outer_digit_pair

先看兩張黃色的 `a`，它們對數字和貢獻 `2a`。

動作目的：讓「先把最外側兩個 a 合成 2a」在穩定畫面上單獨成立，再進入下一步。

### 03 fold_inner_digit_pairs

兩張藍色的 `b` 貢獻 `2b`。中央綠色的 `c` 只出現一次。所以五位數的數字和是

動作目的：讓「再合成 2b 與中央 c」在穩定畫面上單獨成立，再進入下一步。

### 04 state_digit_sum_constraints

題目對這個 `m` 給了三道限制：它是兩位數、它是完全平方數，而且它自己的兩個數字相加後，仍然是完全平方數。

動作目的：讓「列出數字和的三道限制」在穩定畫面上單獨成立，再進入下一步。

### 05 list_digit_sum_squares

五個數字最多都是 9，所以 `m` 不會超過 45；題目又說它是兩位數。

動作目的：讓「列出範圍內平方並先測十六」在穩定畫面上單獨成立，再進入下一步。

### 06 find_the_digit_sum

`2+5=7`，也不行。

動作目的：讓「排除二十五並留下三十六」在穩定畫面上單獨成立，再進入下一步。

### 07 list_terminal_square_digits

回到最外面的黃色數字。它既是最高位，也是整個平方數的個位數。

動作目的：讓「先列平方數可能的末位」在穩定畫面上單獨成立，再進入下一步。

### 08 derive_outer_digit_bound

再看中央三格。即使 `b` 和 `c` 都放到最大，它們的貢獻也只有

動作目的：讓「用中央三格上限推出 a 至少為五」在穩定畫面上單獨成立，再進入下一步。

### 09 retain_outer_digit_branches

總和必須到 36，因此外側兩個 `a` 至少要補足 9。因為 `a` 是整數，得到 `a\ge5`。

動作目的：讓「只留下五、六、九三個分支」在穩定畫面上單獨成立，再進入下一步。

### 10 establish_a_nine_compensation

先從 `a=9` 開始。外側已經貢獻 18，所以中央必須滿足 `2b+c=18`。

動作目的：讓「先用第一個候選建立補償規則」在穩定畫面上單獨成立，再進入下一步。

### 11 enumerate_a_nine

先依序得到 `(6,6)、(7,4)`，讓同一個補償規則只推進兩次。

動作目的：讓「沿同一規則列完 a 等於九」在穩定畫面上單獨成立，再進入下一步。

### 12 finish_a_nine_candidates

再得到 `(8,2)、(9,0)`，完成 `a=9` 的全部五個候選並停在完整清單。

### 13 set_up_a_six_branch

現在把 `a` 固定為 6。外側貢獻 12，所以中央需要 `2b+c=24`。

動作目的：讓「把 a 等於六的方程放到清單旁」在穩定畫面上單獨成立，再進入下一步。

### 14 enumerate_a_six

能成立的只有 `(b,c)=(8,8)` 與 `(9,6)`，分別給出 68886 和 69696。

動作目的：讓「列出兩個合法中央配置」在穩定畫面上單獨成立，再進入下一步。

### 15 set_up_a_five_branch

最後固定 `a=5`。中央需要 `2b+c=26`。

動作目的：讓「建立 a 等於五的最後分支」在穩定畫面上單獨成立，再進入下一步。

### 16 enumerate_a_five

只有 `b=9、c=8` 合法，因此得到 59895。

動作目的：讓「讀出這個分支的唯一候選」在穩定畫面上單獨成立，再進入下一步。

### 17 assemble_eight_candidates

把三個分支排在一起：五個、兩個、一個，總共八個候選。

動作目的：讓「把三個分支整理成八張卡」在穩定畫面上單獨成立，再進入下一步。

### 18 prove_square_residues_mod_four

任何整數不是偶數就是奇數。

動作目的：讓「先證明平方除以四只餘零或一」在穩定畫面上單獨成立，再進入下一步。

### 19 test_mod_four

判斷除以 4 的餘數，只要看最後兩位。現在逐張看標亮的尾端。

動作目的：讓「再替八張卡標餘數並篩選」在穩定畫面上單獨成立，再進入下一步。

### 20 isolate_three_survivors

把三個倖存者單獨放大。

動作目的：讓「必要條件通過後，還要真的驗平方」在穩定畫面上單獨成立，再進入下一步。

### 21 place_first_square_bracket

`310` 的平方是 96100，`311` 的平方是 96721。

動作目的：讓「先放出相鄰平方的兩端」在穩定畫面上單獨成立，再進入下一步。

### 22 bracket_first_false

相鄰整數之間沒有別的整數，所以相鄰平方之間也不可能藏著另一個整數平方。

動作目的：讓「用嚴格夾住排除九六六六九」在穩定畫面上單獨成立，再進入下一步。

### 23 place_second_square_bracket

同樣檢查 98289。

動作目的：讓「先放出第二組相鄰平方」在穩定畫面上單獨成立，再進入下一步。

### 24 bracket_second_false

98289 也嚴格落在兩個相鄰平方之間，所以它不是完全平方數。

動作目的：讓「用嚴格夾住排除九八二八九」在穩定畫面上單獨成立，再進入下一步。

### 25 hold_middle_square_test

中央候選是 69696。最接近的平方根候選是 264。

動作目的：讓「先停在最後一個等號前」在穩定畫面上單獨成立，再進入下一步。

### 26 reveal_square_equality

乘法完成：`264^2=69696`。這一張確實是完全平方數。

動作目的：讓「先確認二六四的平方」在穩定畫面上單獨成立，再進入下一步。

### 27 recheck_palindrome

把它重新展開成五張卡。從右讀回來仍然是 69696，所以它是回文數。

動作目的：讓「把數字展開並核對回文」在穩定畫面上單獨成立，再進入下一步。

### 28 reveal_and_recheck_pair

五個數字相加是

動作目的：讓「核對兩層數字和並寫出數對」在穩定畫面上單獨成立，再進入下一步。

## Build constraints

- Edit only `lessons/tcfs_112_math_gifted/q09/`; generated media stays in the
  lesson's ignored build directories.
- Scene class: `CarloTcfs112MathQ09`.
- Twenty-seven beats, all `loop=false`.
- Traditional Chinese uses `label()`; `MathTex` contains ASCII mathematics.
- Render in an isolated media directory through the lesson runner, first at low
  quality and then at `--quality h`.
- Inspect all endpoints, the complete one-frame-per-second sweep, digit-card
  rearrangements, residue labels, both square brackets, the pre-answer hold,
  and the final return to the palindrome.
- Stop at `draft_rendered`; do not run `freeze-qa` or change collection state.
