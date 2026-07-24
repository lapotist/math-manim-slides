# Q05 Storyboard: Scaling Hidden in Equal Ratios

目標長度：約 8 分鐘。核心體驗是先看見「同一比例下，附加量放大幾倍，主體也要放大幾倍」，再用交叉相乘把觀察變成證明。畫面中的 `a_n` 長條在正式推導前只作猜想模型；不得把其他項為正當成已知條件。

## Visual grammar

- `a_n` 與所有由它變出的項使用藍色。
- 已知附加量 `2n` 使用黃色。
- 固定比例的外框使用中性灰；嚴格不等號與上限使用紅色。
- 係數 `1,2,...,20` 在相加時保持同一位置與顏色，避免突然換成完成式。
- 除來源短註外，不重播或截取 PDF 內容；題式以專案自己的排版重建。

## Beat plan

## 01 equal_ratio_chain (0:35, loop=false)

- Settled visual: 只顯示從第 1 項到第 20 項的等比值鏈，總和條件與問題答案都先隱藏。
- Animation: 分母中的 `+2,+4,+6,...,+40` 依序亮起，分子暫保持中性。
- Discovery prompt: 問觀眾「這一串式子真正固定的是什麼？」停頓後只圈住等號。
- Boundary: 畫面停在完整但不擁擠的比例鏈。

## 02 focus_first_ratio (0:40, loop=false)

- Settled visual: 其他分式淡出，只留 `a_1/(a_1+2)`。
- Animation: 將分母拆成藍色未知部分 `a_1` 與黃色附加部分 `2`，外框表示整體。
- Teaching point: 這個分式可視為「藍色部分占整體的比例」。先用它建立直覺，不宣稱其他 `a_n` 已知為正。
- Boundary: 第一個比例尺與原分式並列。

## 03 scale_model (0:50, loop=true)

- Loop animation: 一組示意比例尺由 1 倍平滑放大到 2 倍、3 倍，再縮回 1 倍；藍、黃兩段同步縮放，循環端點完全一致。
- Constant: 藍色占整體的比例始終不變。
- Variable: 黃色附加段從 `2` 變成 `4`、`6`；藍段以未知標記跟著放大。
- Purpose: 讓觀眾先猜到「附加段乘 `n`，藍段也應乘 `n`」，但畫面標示「待證」。

## 04 pose_nth_term (0:35, loop=false)

- Settled visual: 將第 1 項與第 `n` 項上下對齊；黃色段由 `2` 對應到 `2n`。
- Prompt: 問「要維持同一比例，第 `n` 個藍段應是多少？」
- Pause: 保留空白答案位置，讓觀眾先說出 `n a_1`。
- Boundary: 猜想 `a_n ?= n a_1` 尚未蓋章。

## 05 derive_nth_term (0:55, loop=false)

- Animation: 停止所有長條運動，從兩個原分式各複製一份進入交叉相乘。
- Algebra staged one cancellation at a time:
  `a_1(a_n+2n)=a_n(a_1+2)`, then cancel the common `a_1a_n`, then obtain `2na_1=2a_n`.
- Conclusion: `a_n=na_1` 落回第 `n` 個藍段，「待證」改成勾號。
- Rigor note: 這個推導不預先假設 `a_n` 的正負，因此也補足前面的示意模型。

## 06 build_sequence (0:40, loop=false)

- Animation: 同一個 `a_1` 方塊被複製成 1、2、3 組，最後快速但有節制地延伸到 20 組。
- On-screen sequence: `a_1, 2a_1, 3a_1, ..., 20a_1`。
- Teaching point: 原來 20 個未知數只有一個自由量。
- Boundary: 整列保持可掃讀，中央項可用省略號壓縮。

## 07 pose_sum_limit (0:35, loop=false)

- Animation: 此時才把 `a_1+...+a_20<2026` 帶入，20 組方塊垂直收攏成一個總量容器。
- Prompt: 問「現在只差哪一個係數總和？」
- Pause: 不立刻顯示 210。
- Boundary: `a_1(1+2+...+20)<2026` 可讀且靜止。

## 08 pair_coefficients (0:50, loop=false)

- Animation: 係數首尾配對：`1+20`, `2+19`, ...；每一對移成同高的 21 方塊列。
- Evidence: 明確顯示共有 10 對，每對 21，而不是直接引用公式。
- Teaching point: 三角數 210 從可見配對得到。
- Boundary: 十列 `21` 與原係數列同時保留。

## 09 sum_coefficients (0:30, loop=false)

- Animation: 十列 21 合併成 `10 x 21 = 210`，再由係數區複製到不等式。
- Result: `210a_1<2026`。
- Boundary: 只保留一行不等式與旁邊縮小的配對圖。

## 10 bound_a1 (0:40, loop=false)

- Animation: 數線先標出 `2026/210` 位於 9 與 10 之間，再顯示 `a_1<2026/210`。
- Teaching point: 嚴格小於號不能在除法後消失。
- Prompt: 問「正整數最大能站在哪一格？」
- Boundary: 9 亮起，10 暫不打叉。

## 11 test_neighboring_integers (0:45, loop=false)

- Animation: 將 9、10 分別代入總和；`210x9=1890<2026` 顯示通過，`210x10=2100>2026` 顯示不通過。
- Proof obligation: 同時證明 9 可行與更大的下一個整數不可行，完成「最大值」而非只有上界。
- Boundary: 9 保持藍色，10 變成灰色並劃除。

## 12 consolidate (0:45, loop=false)

- Return: 從比例鏈到 `a_n=na_1`，再到 `210a_1<2026`，用三個定格畫面依序回顧。
- Final reveal: `a_1` 的最大值 `9` 最後才出現。
- Source footer: `解題來源：正哥愛數學`，並標示第壹部分第 5 題、PDF 第 3 頁。
- End state: 保留推理箭頭，不只留下孤立答案。

## Independent mathematics check

由第一項與第 `n` 項的原式直接得到

`a_1(a_n+2n)=a_n(a_1+2)`,

消去共同項後為 `2na_1=2a_n`，所以 `a_n=na_1`。因此總和是

`(1+2+...+20)a_1=210a_1<2026`。

`a_1=9` 時總和為 1890，符合嚴格不等式；`a_1=10` 時總和為 2100，不符合。因此正整數最大值唯一為 9。

## Implementation cautions for the future deck

- `scale_model` 必須完整回到 1 倍狀態，才可標記為 loop。
- 在 `derive_nth_term` 完成前，示意長條要帶有「待證」訊號，避免視覺上偷渡 `a_n>0`。
- 不得把 210 直接淡入；必須由首尾配對物件轉換而來。
