# Part 2 Q01 Storyboard: Subtract the Twin Equations

目標長度：約 10 分鐘。三條二次方程看起來密集，但前兩條其實是把 `y` 與 `z` 放進同一個模具。先讓觀眾看見這個交換對稱，再相減；因式分解自然分出 `y=z` 與 `x+y+z=3` 兩條支線。兩支各自走完並驗證存在性，最後公開修正來源答案欄的符號誤植。

## Visual grammar

- `x` 使用藍色、`y` 使用黃色、`z` 使用綠色；第一、二、三式的編號固定為白、青、洋紅圓章。
- 相減時，相同項在原位置成對淡出；留下的差以同一水平基線重組，避免直接淡入完成的因式。
- 分支使用左右兩條清楚路徑：左支 `y=z`，右支 `x+y+z=3`。進入一支時另一支保留為低透明度，完成後回到分岔點。
- 來源誤植以中性「校正」標記呈現，不以來源截圖作畫面，也不隱藏矛盾。
- 答案中的四個 `y` 值必須先由各自分支生成，不能一次顯示。

## Beat plan

## 01 meet_three_equations (0:25, loop=false)

- Settled visual: 三條方程依序編為 `(1),(2),(3)`，只問「所有可能的 `y`」，答案隱藏。
- Animation: 三個變數沿各式出現的位置亮一次，讓觀眾感受直接逐一代入會產生許多交叉項。
- Prompt: 「不必同時解出 `x,y,z`；哪兩條式子最像，適合先相減？」
- Boundary: 方程完整可讀，前兩式尚未被圈選。

## 02 notice_twin_pair (0:25, loop=false)

- Focus: 將 `(1)` 與 `(2)` 上下對齊；共同的 `x^2`、右側係數 3 保持中性。
- Swap: `y` 的三個位置與 `z` 的三個位置用同形彩框對應，顯示第二式只是把第一式的伙伴 `y` 換成 `z`。
- Prompt: 「兩個同模具的式子相減，會留下哪個差？」
- Boundary: `y-z` 的色帶在右側準備出現，但尚未完成因式分解。

## 03 align_twin_equations (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 04 subtract_first_two (0:25, loop=false)

- Animation: `(1)-(2)`；`x^2` 成對消去，剩下 `x(y-z)+(y^2-z^2)=3(y-z)`。
- Factor visually: `y^2-z^2` 先變成 `(y-z)(y+z)`，再和 `x(y-z)` 共用同一塊 `y-z`。
- Result staged: `(y-z)(x+y+z)=3(y-z)`，移到同側後得到 `(y-z)(x+y+z-3)=0`。
- Boundary: 兩個因子以兩扇門呈現，不先選任何一門。

## 05 isolate_first_difference (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 06 split_branches (0:25, loop=false)

- Zero-product: 由兩個因子的乘積為零，依次打開 `y-z=0` 與 `x+y+z-3=0`。
- Branch labels: 左支 `y=z`；右支 `x+y+z=3`。
- Completeness: 明示這兩種情況可以重疊，但聯集已涵蓋所有解，不能漏掉任一支。
- Boundary: 分岔圖停在中央，準備先走左支。

## 07 enter_equal_branch (0:25, loop=false)

- Focus: 左支亮起，`y` 與 `z` 兩張卡合併成同一張。
- Substitution: 將 `z=y` 的物件複製進第三式，三個二次項逐一成為 `y^2`。
- Result: `3y^2=5y+1`，再整理成 `3y^2-5y-1=0`。
- Boundary: 二次式靜止，來源答案不出現。

## 08 compare_equal_branch (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 09 solve_equal_branch (0:25, loop=false)

- Quadratic formula staged: 對 `3y^2-5y-1=0`，標出 `A=3,B=-5,C=-1`。
- Numerator: `-B=5` 先落下，再加入 `plus/minus sqrt(25+12)`；最後化為 `y=(5 plus/minus sqrt(37))/6`。
- Sign emphasis: `5` 保持短暫亮色，為後面的來源校正留下可追蹤證據。
- Boundary: 左支的兩個候選值固定在分支末端。

## 10 derive_equal_branch_sum (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 11 test_equal_branch_values (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 12 enter_sum_branch (0:25, loop=false)

- Return: 回到分岔點，左支淡化但不消失，右支 `S=x+y+z=3` 亮起。
- Visual compression: 三個變數方塊收進一個標有 `S=3` 的總量框。
- Strategy: 第二、三式同時含 `z`，將它們對齊準備相減；先問「這次能否用已知總和壓縮差式？」
- Boundary: `(2)-(3)` 尚未展開。

## 13 derive_x_one (0:25, loop=false)

- Animation: `(2)-(3)` 的左側依結構收成 `(x+y+z)(x-y)=S(x-y)`。
- Right side staged: 收成 `(5/2)(x-y)+(1/2)(x+z)-1`，每組都從原項搬來。
- Substitute: `S=3` 且 `x+z=3-y`，得到 `3(x-y)=(5/2)(x-y)+(1/2)(3-y)-1`。
- Cancellation: 兩邊同乘 2，`y` 項逐一消去，只留下 `x=1`。
- Boundary: 右支中 `x` 被固定，未先求 `y`。

## 14 factor_x_one_relation (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 15 solve_x_one_relation (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 16 solve_sum_branch (0:25, loop=false)

- Substitution: 將 `x=1` 放入第一式，逐步得到 `1+y+y^2=3+3y`，即 `y^2-2y-2=0`。
- Solve: 完成平方或公式得到 `y=1 plus/minus sqrt(3)`。
- Recover z: 由 `x+y+z=3` 得 `z=2-y=1 minus/plus sqrt(3)`，讓兩個候選各有一個實際配對。
- Boundary: 右支的兩個 `y` 值加入分岔圖。

## 17 derive_sum_branch_values (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 18 verify_candidates (0:25, loop=false)

- Right branch: 顯示 `(x,y,z)=(1,1 plus/minus sqrt(3),1 minus/plus sqrt(3))`，三式各得到勾號。
- Left branch existence: 對每個 `y=(5 plus/minus sqrt(37))/6` 取 `z=y`；第一式成為關於 `x` 的二次式，其判別式為 `y+8>0`，所以至少有實數 `x`，第二式與第一式相同。
- Teaching point: 這一步確認四個 `y` 都真的出現在原方程組中，而不只是相減後的必要候選。
- Boundary: 四個值都得到「可達」標記。

## 19 test_first_candidates (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 20 test_remaining_candidates (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 21 correct_source_sign (0:25, loop=false)

- Source note: 顯示專案重排的文字「來源答案欄：第一組分子誤植為 -5；同頁分支方程與最後等號要求 +5」，不顯示來源截圖。
- Fast check: 對 `3y^2-5y-1=0` 使用根和 `5/3`；`(5 plus/minus sqrt(37))/6` 的和是 `5/3`，而帶 `-5` 的兩根和會是 `-5/3`。
- Resolution: 正確答案保留 `+5`，metadata 的 source note 記錄修正依據。
- Boundary: 誤植值淡化並標為「不符合原式」，正確值保持亮色。

## 22 state_corrected_sign (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 23 consolidate (0:25, loop=false)

- Recap: 前兩式的交換結構 -> 相減得零乘積 -> `y=z` 與總和 3 兩支 -> 各產生兩個值 -> 回原系統驗證。
- Final answer: `y=(5 plus/minus sqrt(37))/6` 或 `y=1 plus/minus sqrt(3)`。
- Source footer: `解題來源：正哥愛數學`，第二部分第 1 題、PDF 第 9 頁；旁邊保留精簡校正註記。
- End state: 四個答案分別連回自己的分支，避免看成無來源的列表。

## Independent mathematics check

由 `(1)-(2)` 得

`(y-z)(x+y+z-3)=0`。

若 `y=z`，第三式為 `3y^2=5y+1`，所以 `y=(5 plus/minus sqrt(37))/6`。此時第一式是

`x^2+(y-3)x+(y^2-3y)=0`，

判別式為 `-3y^2+6y+9=y+8>0`，故每個候選都有實數 `x`；第二式因 `z=y` 自動相同。

若 `x+y+z=3`，由 `(2)-(3)` 可得 `x=1`。第一式化成 `y^2-2y-2=0`，所以 `y=1 plus/minus sqrt(3)`，而 `z=2-y`。直接代回三式成立。

## Source ambiguity and correction

PDF 的答案欄印成 `(-5 plus/minus sqrt(37))/6`。同頁解答先寫 `3y^2=5y+1`，其後公式也出現 `-5 plus/minus sqrt(25+12)`，但最後等號又寫回 `(5 plus/minus sqrt(37))/6`。正確二次公式對 `3y^2-5y-1=0` 使用 `-B=5`，因此正確答案必為 `(5 plus/minus sqrt(37))/6`。這是來源中的符號誤植，不是 OCR 歧義。

## Implementation cautions for the future deck

- 不得在因式分解前直接顯示兩條分支；`y-z` 必須由原差式中的項實際收合而來。
- 左支完成後需回到原分岔點，再進入右支，避免看成先後推論。
- 來源校正不能引用或重製頁面截圖；只顯示必要的數學矛盾與專案自己的文字說明。
- 最後答案必須使用正確的 `+5`，並在畫面或講稿明確留下修正記錄。
