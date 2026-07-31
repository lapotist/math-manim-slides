# Q06 Storyboard: Complete the Missing Factor

目標長度：約 9 分鐘。故事先讓七個散開的項成為「八種選擇中少一種」，觀眾看見補 1 的必要性之後才寫因式分解；後半段把乘積候選與三角形條件分開處理，再用最接近平方根的因數對完成有限檢查。

## Visual grammar

- `a,b,c` 三個角色固定使用藍、綠、黃；補上的常數 1 使用洋紅色，之後 `+1` 的平移沿用同色。
- 乘積 480 使用白色或中性亮色；不合三角形的候選淡灰並加短紅線，不能整列突然消失。
- 三角形檢查必須先以可彎折線段表現 `b+c>a`，再轉換成符號。
- 候選表一次只強調一列；表格是檢查工具，不是開場主畫面。
- 題式與圖形全部重新排版，不使用來源 PDF 截圖。

## Beat plan

## 01 original_seven_terms (0:25, loop=false)

- Settled visual: 顯示 `abc, ab, bc, ca, a, b, c` 七張積木牌，先不顯示等號右側與三角形條件。
- Animation: 依三次、二次、一次分成三層，但不立即因式分解。
- Prompt: 問「這七項像是哪一個乘積展開後留下來的？」
- Boundary: 七項按結構排好，中間留一個明顯空位。

## 02 missing_one (0:25, loop=false)

- Visual construction: 三個二選一開關分別為 `{a,1}`、`{b,1}`、`{c,1}`，逐一產生八種乘積。
- Animation: 七種選擇落到原式對應項；最後 `1x1x1` 指向唯一空位。
- Discovery: 觀眾先說出缺少常數 1，再將洋紅色 `+1` 放入兩邊。
- Pause: 在補入之前保留短暫靜止。

## 03 identify_missing_side (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 04 complete_product (0:25, loop=false)

- Animation: 八張積木牌依三個二選一開關收合成 `(a+1)(b+1)(c+1)`。
- Right side: `479+1` 同時變為 `480`，不得先顯示完成式。
- Result: `(a+1)(b+1)(c+1)=480`。
- Boundary: 原七項縮成淡色參考，完成的乘積成為主體。

## 05 shift_sides (0:25, loop=false)

- Animation: 在三條邊 `a>b>c>=1` 的數線標記上各向右平移 1，命名 `x=a+1, y=b+1, z=c+1`。
- Preserve order: 視覺上顯示平移不改變先後，所以 `x>y>z>=2`。
- Product: 將新符號帶入得到 `xyz=480`。
- Boundary: 只留下新變數條件與一個小型回譯標籤。

## 06 bound_z (0:25, loop=false)

- Visual: 三個由小到大的長方柱以 `z<y<x` 排列；若三者都至少是 `z`，乘積就大於 `z^3`。
- Algebra after visual: `z^3<xyz=480`，所以 `z<cube_root(480)<8`。
- Teaching point: 最小因數只能在很小的範圍內，不需要盲目分解所有 480。
- Boundary: 數線只亮出整數 2 到 7。

## 07 list_bounded_candidates (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 08 candidate_divisors (0:25, loop=false)

- Animation: 逐一用 480 的因數檢查數線；2、3、4、5、6 保留，7 因不整除 480 而淡出。
- Exact candidate set: `z in {2,3,4,5,6}`。
- Source clarification: 必須明說 `z` 是 480 的因數；不能只由 `z^3<480` 直接跳到 2 至 6。
- Boundary: 五張候選卡等距排列。

## 09 pose_triangle_filter (0:25, loop=false)

- Visual: 固定最長邊 `a`，把 `b`、`c` 兩線段首尾相接向它靠攏。
- Contrast: 一個剛好碰到的退化情況與一個能真正合攏的三角形。
- Prompt: 問「乘積正確還不夠；哪個條件決定三邊能否合起來？」
- Pause: 等觀眾提出 `b+c>a`。

## 10 state_triangle_filter (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 11 translate_triangle (0:25, loop=false)

- Animation: 從線段圖複製 `b+c>a`，再代入 `a=x-1, b=y-1, c=z-1`。
- Staged simplification: `(y-1)+(z-1)>x-1`, then `x-y<z-1`。
- Visual meaning: `x` 與 `y` 不能相差太遠；`z` 提供允許的差距。
- Boundary: 每張候選卡旁出現自己的門檻 `x-y<z-1`。

## 12 factor_triangle_condition (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 13 nearest_factor_pairs (0:25, loop=false)

- Method reveal: 對固定 `z`，有 `xy=480/z`。以因數矩形向正方形靠近，說明最接近平方根的因數對使 `x-y` 最小。
- Table built row by row:
  `z=2: xy=240, (x,y)=(16,15), gap=1`;
  `z=3: xy=160, (16,10), gap=6`;
  `z=4: xy=120, (12,10), gap=2`;
  `z=5: xy=96, (12,8), gap=4`;
  `z=6: xy=80, (10,8), gap=2`.
- Completeness: 若最接近的因數對都不符合差距，其他更不平均的因數對差距只會更大，因此不必列出每一對。
- Boundary: 五列完整但只強調 gap 欄。

## 14 test_near_factor_pairs (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 15 test_far_factor_pairs (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 16 select_valid_rows (0:25, loop=false)

- Animation: 對每列逐一套入嚴格門檻：`1<1` false、`6<2` false、`2<3` true、`4<4` false、`2<5` true。
- Strictness: `z=5` 的等號邊界代表退化三角形，必須明確淘汰。
- Survivors: 只保留 `(x,y,z)=(12,10,4)` 與 `(10,8,6)`，其他列留淡色痕跡以顯示完整檢查。
- Boundary: 兩列通過標記落定。

## 17 test_candidate_rows (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 18 retain_valid_rows (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 19 restore_sides (0:25, loop=false)

- Animation: 每個存活三元組的三個數都向左平移 1。
- Results: `(12,10,4)->(11,9,3)`；`(10,8,6)->(9,7,5)`。
- Object continuity: 使用數字複本轉換，不重打一份孤立答案。
- Boundary: 兩個原變數序對並排。

## 20 reconstruct_side_triples (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 21 verify_triangles (0:25, loop=false)

- Verify order/positivity: 兩組都逐項顯示正整數且嚴格遞減。
- Verify triangle: `9+3>11` 與 `7+5>9` 由線段真正合攏示範。
- Verify equation: 將各組加 1 後的乘積分別顯示 `12x10x4=480`、`10x8x6=480`，所以原七項和為 479。
- Boundary: 每組得到完整三個勾號。

## 22 check_triangle_witnesses (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 23 consolidate (0:25, loop=false)

- Recap path: 七項少 1 -> 完整乘積 -> 最小因數五個候選 -> 三角形差距篩選。
- Final answer: `(a,b,c)=(11,9,3)` 與 `(9,7,5)`。
- Source footer: `解題來源：正哥愛數學`，第壹部分第 6 題、PDF 第 3 頁。
- End state: 兩個答案連回各自的因數列，不只留下結論。

## 24 reveal_triangle_count (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## Independent mathematics check

原式加 1 後確為 `(a+1)(b+1)(c+1)=480`。令 `x=a+1, y=b+1, z=c+1`，則 `x>y>z>=2` 且 `xyz=480`。因 `z^3<480` 且 `z` 整除 480，故 `z` 只能為 2、3、4、5、6。

三角形條件等價於 `x-y<z-1`。對五個 `z`，最小可能因數差依序為 1、6、2、4、2；與門檻 1、2、3、4、5 比較，只有 `z=4,6` 嚴格通過，得到 `(x,y,z)=(12,10,4),(10,8,6)`，回譯即 `(11,9,3),(9,7,5)`。

## Source ambiguity and resolution

來源在 `z^3<480` 後直接列出 `z=2,3,4,5,6`，少寫了排除 7 所需的理由。這份課程補上：`z` 必須整除 480，而 7 不整除 480。答案本身經完整枚舉驗證無誤。

## Implementation cautions for the future deck

- 因數對表必須由「靠近平方根會縮小差距」的動畫建立，不能作為未解釋的查表結果。
- `4<4` 是錯誤，視覺上不可把退化三角形當成有效邊界。
- 三個變數平移 1 時要保持次序與物件身分，避免觀眾誤以為換了一題。
