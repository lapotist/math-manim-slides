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

## Beat map and motion purposes

### 01 meet_unit_hexagon

Draw one fixed regular hexagon, mark its center, and isolate one side of length
1. The motion establishes exactly which object and scale will remain fixed.
Ask when the overlap with a rotating copy is smallest, without showing a copy
or answer.

### 02 rotate_and_watch_overlap

Introduce one blue copy at the same position and rotate only it through 12, 30,
48, and 60 degrees. Keep the green intersection attached to both polygons. The
deliberate states show shrink, recovery, and a full return; they are evidence
for a period, not decorative roaming.

### 03 reduce_one_period_by_reflection

State the 60-degree period only after the return has landed. Then show the
18-degree overlap and its reflected 42-degree copy side by side. The explicit
reflection preserves the fixed hexagon, rotation constraint, and area. Conclude
that only 0 through 30 degrees must be checked.

### 04 find_common_incircle

Return to a generic 18-degree overlap. Draw the circle tangent to every side of
both hexagons, then derive its radius from a visible half-side right triangle.
This motion replaces a moving-boundary problem with one fixed distance `r`.

### 05 read_alternating_normal_gaps

Draw the twelve perpendicular radii to the active support lines. Highlight one
short gap `theta` and the next long gap `60-theta`, then count six of each. The
motion answers what actually changes during rotation.

### 06 balance_the_gaps

Transform the generic configuration to 30 degrees. The alternating radii become
twelve equal 30-degree gaps and the overlap becomes a regular tangential
12-gon. Pause on the question of minimality; do not write the area formula yet.

### 07 measure_one_tangent_corner

Remove the whole diagram and enlarge one pair of adjacent tangent lines. Draw
the two perpendicular radii, angle bisector, right triangles, and tangent leg
in that order. Derive `r^2 tan(delta/2)` from the visible quadrilateral.

### 08 assemble_overlap_area

Return to the generic overlap and fill all twelve tangent-corner pieces. Copy
the six yellow wedges into the first formula term and the six blue wedges into
the second. Only after both contributions exist, combine them into `A(theta)`.

### 09 prove_equal_gaps_minimize

Rename the two half-gaps `x,y`, visibly keep `x+y=30 degrees`, and show an
unequal divider. Use the product identity for `2cos x cos y` to prove its
maximum occurs at `x=y`; then move the divider to equality. The motion answers
why the halfway picture is a global minimum rather than a guess.

### 10 substitute_half_period

Return to the equal-gap 12-gon. Reveal its twelve congruent wedges, substitute
`r^2=3/4`, and reduce the area to `9 tan(15 degrees)`. Every symbol now points
back to a visible radius, gap, or wedge count.

### 11 calculate_tan_fifteen

Show 15 degrees as the visible difference between 45 and 30 degrees. Build the
tangent subtraction identity one line at a time and obtain `2-sqrt(3)`.

### 12 hold_before_expansion

Restore the two hexagons at 30 degrees beside the settled expression
`A_min=9(2-sqrt(3))=?`. Stop before distributing 9. This is the genuine
pre-answer frame.

### 13 reveal_and_return_to_rotation

Expand to the requested exact value, highlight the green overlap, and add the
0-to-30-to-60 rotation route. The final composition reconnects the answer to
the opening motion and remembers 30 degrees as the midpoint of every period.

## Build constraints

- Edit only `lessons/tcfs_112_math_gifted/q12/`; generated media remains under
  ignored `build/` paths.
- Scene class: `CarloTcfs112MathQ12`.
- Thirteen beats, all `loop=false`.
- Traditional Chinese uses `label()`; every `MathTex` string is ASCII math.
- Render through the lesson runner at low quality first and then quality high.
- Inspect all endpoints, the complete fixed-cadence movie sweep, the dynamic
  intersection, reflection transform, gap balancing, enlarged tangent corner,
  wedge-to-formula transforms, equality-divider transform, pre-answer hold,
  and final reveal.
- Stop at `draft_rendered`; do not freeze QA or alter collection state.
