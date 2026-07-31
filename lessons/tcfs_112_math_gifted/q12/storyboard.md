# ROC 112 TCFS mathematics gifted assessment, fill-in question 12

## Teaching intent

The audience already knows regular-hexagon symmetry, the 30-60-90 triangle,
right-triangle trigonometry, angle-addition identities, and elementary product
identities. It may not yet see a rotating polygon as a fixed family of support
lines, or know how to prove that an attractive halfway picture is a global
minimum.

The likely first misconception is: **the overlap looks smallest at 30 degrees,
so drawing that position is enough.** The lesson lets that conjecture arise, but
then keeps the rotation domain visible and proves it. The same fixed yellow
hexagon and moving blue hexagon persist through exploration. Their common
incircle turns twelve changing boundary segments into alternating angular gaps;
only after those gaps are visible does the algebra name their area.

The motivating object is one unit regular hexagon and one copy rotating about
the same center. The boundary cases are 0 and 60 degrees, where paired support
lines coincide and the overlap returns to the original six-sided hexagon. The
earned realization is that the complicated moving intersection is controlled
by only two gap sizes whose sum is fixed: equalizing them gives the minimum.

## Source reconstruction

- Canonical page: `https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87%E5%84%AA%E7%8F%AD/112%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87`
- Frozen page SHA-256: `8ef9b13e28c992e21dd874cfeabbb6ad66dcacdeec3c326f058ff561de9ba094`
- Problem asset: Drive `1wZiSE5cZZI9Fr_YJovGP_H3aWoFXxc_H`, PDF page 12,
  SHA-256 `277e49efb3aca44666e17c2c4135b6047922f25adee58952560416996140acbd`
- Solution asset: YouTube `3clUyeUgvOg`, confirmed public stream, exact locator
  `00:00-08:23.75`
- Research stream: 518x360, 504.546395 seconds, SHA-256
  `10a79f8610bbc24723a211d4e67a093bfb0957e34b913e2023203c65bcb7186f`
- Boundary inspection: the complete solution remains unobstructed at 08:23.75;
  a device-control overlay is visible by 08:23.80.

The PDF states that a regular hexagon of side 1 rotates about its center, that
the overlap area varies periodically, and asks for its minimum. The worked area
is blank. The video is therefore the reasoning source. It begins with the
reported answer and a half-period overlap diagram. It proves congruences among
the repeated boundary triangles, labels two adjacent cut lengths `a,b`, uses a
120-degree cosine-rule relation to obtain `ab=2a+2b-1`, bounds `ab` with AM-GM,
and subtracts six maximal exterior triangles from the area of the unit
hexagon. This produces the reported minimum.

Two source presentation details require an explicit note. Its enlarged diagram
uses `A` for the common center although the problem calls that point `G`. Near
the end it rejects the large AM-GM branch with only a brief "impossible" mark;
the missing domain line is `a+b<=1`, hence `sqrt(ab)<=1/2`. These are notation
and exposition gaps, not corrections to the calculation or result.

The source's triangle argument and this lesson's support-line argument agree:
both maximize the pieces removed from one hexagon at the balanced position.
The adaptation does not reproduce the source diagram, handwriting, variable
layout, or early answer. It makes the full rotation domain, periodic reduction,
reflection, coincident-support endpoint, and global equality condition explicit
before evaluating the minimum.

## Independent mathematics check

Let `H_0` be the fixed unit-side regular hexagon and `H_theta` its rotation about
the common center `G`. A regular hexagon is unchanged by a 60-degree rotation,
so `A(theta+60)=A(theta)`. Reflection across a symmetry axis of `H_0` sends
`H_theta` to `H_(-theta)`, which is `H_(60-theta)` within one period. Reflection
preserves area. Therefore every rotation is represented by

```text
0 degrees <= theta <= 30 degrees.
```

The apothem of a unit regular hexagon is

```text
r = sqrt(1-(1/2)^2) = sqrt(3)/2.
```

Every side of both hexagons is tangent to the same circle of radius `r`. For a
generic angle between 0 and 60 degrees, the intersection is a tangential
12-gon. Its consecutive support-line normal gaps alternate

```text
theta, 60-theta, theta, 60-theta, ...
```

six times. At `theta=0`, the two sets of six lines coincide, so adjacent pairs
degenerate and the intersection is the original hexagon. The formula below
extends continuously to that endpoint and gives `3sqrt(3)/2`, the correct
hexagon area.

For consecutive tangent lines with normal gap `delta`, join `G` to both
tangency points and to their line intersection. The angle bisector produces
two right triangles. Each has legs `r` and `r tan(delta/2)`, hence the combined
corner contribution is

```text
r^2 tan(delta/2).
```

The twelve corner pieces partition the overlap, giving

```text
A(theta) = 6r^2[tan(theta/2)+tan((60-theta)/2)].
```

Set `x=theta/2` and `y=(60-theta)/2`, so `x+y=30 degrees`. Then

```text
tan x + tan y = 1/(2 cos x cos y),
2 cos x cos y = cos 30 + cos(x-y) <= sqrt(3)/2 + 1.
```

Equality holds exactly when `x=y=15 degrees`, hence `theta=30 degrees`. The
denominator is then largest and the area is smallest. Therefore

```text
A_min = 12(3/4)tan(15 degrees)
      = 9(2-sqrt(3))
      = 18-9sqrt(3).
```

The scene code independently solves consecutive support-line equations to
construct the actual intersection polygon. Shoelace areas agree with the
closed formula at eight angles spanning a period. Separate assertions verify
reflection samples, the six-sided and twelve-sided endpoint counts, monotone
decrease at every integer angle from 0 to 30 degrees, and the final value.

## Visual grammar

- Yellow is the fixed hexagon and one alternating support-gap family.
- Blue is the rotating hexagon and the other gap family.
- Green is the actual overlap and the final minimum.
- Purple is the common incircle and its apothem.
- Coral is reserved for a failed or excluded condition; it is not needed for
  the successful geometric path.
- The camera stays fixed. Dynamic geometry stops before any long formula is
  read.
- No source scan, frame, handwriting, audio, logo, or channel artwork appears.

## Beat map

### 01 meet_unit_hexagon

先只看一個正六邊形。

動作目的：讓「先固定一個邊長 1 的正六邊形」在穩定畫面上單獨成立，再進入下一步。

### 02 rotate_to_half_period

黃色六邊形完全不動。現在加入藍色六邊形，兩者一開始重合。

動作目的：讓「先觀察重疊縮到週期中點」在穩定畫面上單獨成立，再進入下一步。

### 03 rotate_and_watch_overlap

繼續轉到 48 度，面積開始長回來。到了 60 度，藍色六邊形又和黃色六邊形完全重合。

動作目的：讓「再觀察重疊長回完全重合」在穩定畫面上單獨成立，再進入下一步。

### 04 reflect_half_period

正六邊形每轉 60 度就回到原來的形狀，所以面積以 60 度為一個週期。

動作目的：讓「先把後半週期鏡射到前半」在穩定畫面上單獨成立，再進入下一步。

### 05 reduce_one_period_by_reflection

因此每一個後半週期的位置，都有一個面積相同的前半週期位置。我們只需證明

動作目的：讓「寫出反射關係與保留區間」在穩定畫面上單獨成立，再進入下一步。

### 06 construct_common_incircle

先停在一個普通的 18 度位置。

動作目的：讓「先作出共同內切圓與直角三角形」在穩定畫面上單獨成立，再進入下一步。

### 07 find_common_incircle

由畢氏定理，`r` 的平方加上四分之一等於 1，所以

動作目的：讓「由直角三角形算出內切圓半徑」在穩定畫面上單獨成立，再進入下一步。

### 08 draw_alternating_normal_gaps

從中心向每一條有效邊作垂線。黃色半徑對應固定六邊形，藍色半徑對應旋轉後的六邊形。

動作目的：讓「先畫出交替的短弧與長弧」在穩定畫面上單獨成立，再進入下一步。

### 09 read_alternating_normal_gaps

這兩種間隔交替出現：六個小間隔，六個大間隔。

動作目的：讓「把十二個間隙壓成兩類」在穩定畫面上單獨成立，再進入下一步。

### 10 balance_the_gaps

讓藍色六邊形繼續轉到 30 度。

動作目的：讓「把一大一小，調成一樣」在穩定畫面上單獨成立，再進入下一步。

### 11 construct_tangent_corner

把相鄰的兩條切線放大。它們和圓相切的兩點，到中心的距離都是 `r`，而且半徑都和切線垂直。

動作目的：讓「先完成一個切線角落」在穩定畫面上單獨成立，再進入下一步。

### 12 measure_one_tangent_corner

左右兩個三角形的面積相加，二分之一和乘以二互相抵消，因此這一個角落的面積是

動作目的：讓「把角落面積寫成正切公式」在穩定畫面上單獨成立，再進入下一步。

### 13 collect_small_overlap_wedges

回到 18 度的完整圖形。十二個角落剛好從中心鋪滿整個重疊區，沒有空隙，也沒有重複。

動作目的：讓「先收集較小的一組角落」在穩定畫面上單獨成立，再進入下一步。

### 14 assemble_overlap_area

藍色的六個角落，間隔都是 `60 度減 theta`，得到第二項。

動作目的：讓「加入另一組並合成重疊面積」在穩定畫面上單獨成立，再進入下一步。

### 15 derive_equal_gap_bound

把兩個半角分別叫作 `x` 和 `y`。不論怎麼旋轉，它們的總和永遠是 30 度。

動作目的：讓「先推導固定和下的面積下界」在穩定畫面上單獨成立，再進入下一步。

### 16 prove_equal_gaps_minimize

第一項固定。第二項最大只能是 1，而且只有 `x 減 y等於 0` 時達到。

動作目的：讓「讓兩個間隙相等並達到下界」在穩定畫面上單獨成立，再進入下一步。

### 17 substitute_equal_half_period

回到 30 度的位置。十二個角落現在完全相同，每個角落使用 15 度的半角。

動作目的：讓「把相等間隙代入面積式」在穩定畫面上單獨成立，再進入下一步。

### 18 substitute_half_period

12 和四分之三相乘得到 9，所以整題只剩

動作目的：讓「逐步化簡到正切十五度」在穩定畫面上單獨成立，再進入下一步。

### 19 construct_fifteen_degree_difference

十五度可以看成 45 度減 30 度。

動作目的：讓「先用四十五減三十作出十五度」在穩定畫面上單獨成立，再進入下一步。

### 20 calculate_tan_fifteen

代入並整理，得到

動作目的：讓「再推導正切十五度的精確值」在穩定畫面上單獨成立，再進入下一步。

### 21 hold_before_expansion

左邊是已經證明會取得最小值的 30 度位置。

動作目的：讓「所有幾何都已經回到同一行」在穩定畫面上單獨成立，再進入下一步。

### 22 reveal_minimum_overlap

把 9 分配進去，得到

動作目的：讓「先揭示最小重疊面積」在穩定畫面上單獨成立，再進入下一步。

### 23 reveal_and_return_to_rotation

最後把答案放回旋轉過程：0 度時完全重合；走到週期中點 30 度，兩種間隔完全平均，重疊面積最小；到了 60 度又完全重合。

動作目的：讓「回到旋轉圖並收束路線」在穩定畫面上單獨成立，再進入下一步。

## Build constraints

- Edit only `lessons/tcfs_112_math_gifted/q12/`; generated media remains under
  ignored `build/` paths.
- Scene class: `CarloTcfs112MathQ12`.
- Twenty-three beats, all `loop=false`.
- Traditional Chinese uses `label()`; every `MathTex` string is ASCII math.
- Render through the lesson runner at low quality first and then quality high.
- Inspect all endpoints, the complete fixed-cadence movie sweep, the dynamic
  intersection, reflection transform, gap balancing, enlarged tangent corner,
  wedge-to-formula transforms, equality-divider transform, pre-answer hold,
  and final reveal.
- Stop at `draft_rendered`; do not freeze QA or alter collection state.
