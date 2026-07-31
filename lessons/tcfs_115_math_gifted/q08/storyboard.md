# Q08 Storyboard: Counting Collisions Across Shifted Parabolas

目標長度：約 9 分鐘。先在五條拋物線的小模型上讓水平線移動，觀眾看見「每條兩點」與「不同拋物線的點會重合」之間的差別；接著把圖形壓成左右兩排數線點，才引入 `t=sqrt(k)` 並完成一般計數。

## Visual grammar

- 拋物線本身使用不同明度的中性灰；頂點與水平位移 0、2、4...使用白色小標。
- 水平線 `y=k` 使用黃色；每條拋物線的左交點為藍色、右交點為綠色。
- 藍綠重合時改成洋紅色同心點，且保留兩個來源連線，清楚表示「兩個標記、一個相異點」。
- 小模型只顯示五條拋物線；擴展到 51 條時轉成數線序列，不把 51 條曲線全塞在同一畫面。
- 題式與所有圖形由程式重建，不使用來源 PDF 截圖。

## Beat plan

## 01 parabola_family (0:25, loop=false)

- Settled visual: 依序長出五條同形拋物線，頂點在 `0,2,4,6,8`，先不顯示一般公式。
- Animation: 用同一條基準拋物線平移 2 單位的複本建立家族，強調形狀不變、頂點等距。
- Prompt: 問「同一條水平線切過它們時，每條會提供幾個點？」
- Boundary: 五條曲線與頂點標記清楚，沒有水平線。

## 02 sweep_horizontal_line (0:25, loop=true)

- Loop animation: 黃色水平線從一個非碰撞高度平滑升到另一個非碰撞高度，再回到起點；所有交點沿曲線更新。
- Evidence: 每條拋物線始終各有左、右兩個交點，五條共有十個帶來源的交點標記。
- Constraint: 選擇不造成跨曲線重合的端點高度，循環回程完全重合。
- Boundary/loop: 顯示「每條 2 個」但不宣稱十個位置永遠相異。

## 03 count_nominal_hits (0:25, loop=false)

- Boundary cases first: `k<0` 沒有交點，`k=0` 只有 51 個頂點；題設為 76，因此後續可確定 `k>0`、每條都有兩個交點。
- Animation: 五條的 `5x2=10` 向右延伸成 51 條的 `51x2=102` 標記計數。
- Language: 稱為「標記數」或「最多相異點數」，避免尚未處理重合就叫作答案。
- Prompt: 題目只有 76 個相異點，比 102 少了什麼？
- Boundary: `102 labels` 與 `76 distinct` 分列，中間留問號。

## 04 observe_collision (0:25, loop=false)

- Return to five: 將水平線精確移到離每個頂點水平距離 1 的高度。
- Animation: 左邊拋物線的右交點與右邊相鄰拋物線的左交點，在兩頂點中點相撞。
- Counting lesson: 十個來源標記仍在，但四組成對重合，所以只有六個相異位置。
- Boundary: 一個重合點放大，兩條來源導線仍可見。

## 05 compare_collision_times (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 06 name_first_collision (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 07 compress_to_number_line (0:25, loop=false)

- Animation: 拋物線淡化，每個頂點垂直投影到數線；每條曲線的左右交點沿水平線滑到兩排點。
- Top row: 所有左交點；bottom row: 所有右交點。相同水平座標上下對齊。
- Teaching point: 只要數兩排位置的聯集，就不必同時看 51 條曲線。
- Boundary: 小模型的兩排點與頂點間距 2 保留。

## 08 define_offset_t (0:25, loop=false)

- Algebra introduced from picture: 設從頂點到交點的水平距離為 `t>=0`。由 `(x-h)^2=k`，得到 `t=sqrt(k)`。
- General rows for centers `h=2j`: 左排 `2j-t`，右排 `2j+t`，其中 `j=0,...,50`。
- Visual continuity: `+t/-t` 標籤直接從小模型水平距離複製到一般式。
- Boundary: 兩個等差數列顯示首、次、末項。

## 09 pose_76_count (0:25, loop=false)

- Arithmetic prompt: 若完全不重合有 102 個，而實際是 76 個，必須合併掉 `102-76=26` 個重複標記。
- Pause: 問「哪一個 `t` 會讓兩排剛好重疊出這種數量？」
- Boundary: 26 以洋紅色顯示，但不先對應到 `t=25`。

## 10 derive_collision_condition (0:25, loop=false)

- Pick arbitrary collision: 藍點 `2j-t` 與綠點 `2i+t` 對齊。
- Staged equation: `2j-t=2i+t`, then `t=j-i`。
- Consequence: `j-i` 是整數，所以只要 `t` 不是整數，兩排完全不重合，仍有 102 個相異點；前面已排除 `t=0`，故 76 強迫 `t` 為正整數。
- Range: 因確有重合，且共有 51 個中心，故 `1<=t<=50`。
- Boundary: 整數格點尺亮起。

## 11 solve_collision_congruence (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 12 state_collision_period (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 13 count_overlap (0:25, loop=false)

- Rows: 左排 `-t,2-t,...,100-t`；右排 `t,2+t,...,100+t`。
- Animation: 將右排向左對齊；當 `t` 是整數時，重疊從索引 0 到 `50-t`，共有 `51-t` 個位置。
- Inclusion-exclusion: 相異點數 `=51+51-(51-t)=51+t`。
- Boundary: 三段計數由實際點列轉換成公式，不直接淡入完成式。

## 14 count_shared_positions (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 15 solve_offset (0:25, loop=false)

- Animation: 將題目 76 放入 `51+t=76`，數線上的可變間距同步停在 25。
- Result: `t=25`。
- Interpretation: 每個交點離自己的頂點水平 25 單位。
- Boundary: 不顯示 `k`，先讓幾何距離落定。

## 16 recover_k (0:25, loop=false)

- Animation: 從先前標籤 `t=sqrt(k)` 取複本，平方得到 `k=t^2=25^2=625`。
- Equation timing: 625 最後出現。
- Boundary: 黃色水平線落在 `y=625`。

## 17 substitute_overlap_count (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 18 solve_for_k (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 19 verify_full_count (0:25, loop=false)

- Exact rows at `t=25`: 左排 `-25,-23,...,75`，右排 `25,27,...,125`。
- Overlap check: 共同部分 `25,27,...,75` 有 `(75-25)/2+1=26` 點，故 `51+51-26=76`。
- Geometric reconnect: 特別標出 `y=x^2` 與 `y=(x-50)^2` 在 `x=25, y=625` 相交，對應來源解法的代表碰撞。
- Boundary: 76 得到驗證勾號，非整數與 `k=0` 邊界以短註排除。

## 20 recheck_union_count (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 21 consolidate (0:25, loop=false)

- Recap path: 水平線每條兩點 -> 相異點減少來自左右排重合 -> `t` 必為整數 -> 聯集大小 `51+t`。
- Final answer: `k=625`。
- Source footer: `解題來源：正哥愛數學`，第壹部分第 8 題、PDF 第 4 頁。
- End state: 小型拋物線碰撞圖、兩排數線和最終計數三者保持連線。

## 22 reveal_k_value (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## Independent mathematics check

若 `k<0`，無交點；若 `k=0`，只有 51 個頂點，所以題設 76 迫使 `k>0`。令 `t=sqrt(k)>0`。第 `j` 條拋物線的兩個交點橫坐標為 `2j-t` 與 `2j+t`，`j=0,...,50`。

每排內部各有 51 個不同位置。跨排重合需 `2j-t=2i+t`，即 `t=j-i`，所以相異點少於 102 時 `t` 必為整數。重合存在也給出 `1<=t<=50`。此時兩排交集有 `51-t` 點，聯集大小為 `102-(51-t)=51+t`。令它等於 76 得 `t=25`，故 `k=625`。代回時交集 26 點，聯集確為 76。

## Source ambiguity and resolution

來源答案用碰撞數列直接走到第 26 個重合，但未明說非整數 `sqrt(k)` 時兩排不會重合，也未分別排除 `k<=0`。這些是解釋完整度的缺口，不影響來源答案；本課以兩排等差數列補上唯一性證明。

## Implementation cautions for the future deck

- 不要同時畫滿 51 條拋物線；小模型建立直覺後必須轉成數線點列。
- 重合點必須保留兩個來源連線，否則觀眾看不出為何「少一點」。
- `sweep_horizontal_line` 只使用不碰撞的端點高度並回到起點；碰撞高度留給下一個非循環 beat。
- `count_overlap` 要以實際索引對齊顯示 `51-t`，不能只報公式。
