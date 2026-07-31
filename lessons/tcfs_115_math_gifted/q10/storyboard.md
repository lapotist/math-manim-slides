# Q10 Storyboard: One Shared Total Orders Four Variables

目標長度：約 9 分鐘。核心不是逐對硬比 `a,b,c,d`，而是讓四個正數先共用同一把比例尺 `k=a+b+c+d`。觀眾看見每條原式都恰好缺少「另外三項」後，再把四個未知數放到同一條標準化數線上；最後只比較彼此分離的端點。

## Visual grammar

- `a,b,c,d` 固定使用藍、綠、黃、洋紅；共享總量 `k` 使用白色長條。
- 每個未知數的可能範圍用半透明區間帶表示，端點為空心圓，強調全部是不含端點的嚴格不等式。
- 加到不等式三邊的「其餘三項」先以三塊可見積木補入，再收合成 `k`，不直接跳到整理後結果。
- 分數比較只點亮當下需要的一個上界與下一個下界，其餘區間保留為淡色背景。
- 全程使用專案自己的式子排版，不重播來源頁面。

## Beat plan

## 01 meet_four_bounds (0:25, loop=false)

- Settled visual: 四條原不等式分成四列，只給每列的主角變數上色；答案與 `k` 都不出現。
- Animation: 依次圈出第一列中的 `a` 與 `b`、第二列中的 `b` 與 `c`，讓觀眾注意每列都在用另一個變數夾住主角。
- Prompt: 「若直接做六次兩兩比較，會很亂；四列中有沒有同一個可以補齊的整體？」
- Boundary: 四列穩定並列，中間留出一條總量長條的位置。

## 02 name_shared_total (0:25, loop=false)

- Visual construction: `a,b,c,d` 四塊正長條首尾相接，命名為 `k=a+b+c+d`。
- Positivity: 明示四數皆為正，所以 `k>0`；之後除以 `k` 不會翻轉不等號。
- Discovery: 在第一列 `5b-c-d<a<6b-c-d` 的三邊各補上同一組 `b+c+d`，三塊積木落到相應位置。
- Boundary: 中央項剛好收合為 `k`，但兩側係數尚未化簡。

## 03 write_shared_total (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 04 normalize_b (0:25, loop=false)

- Animation: 左側 `5b+(b+c+d)-c-d` 收成 `6b`；右側同理收成 `7b`。
- Staged algebra: `6b<k<7b`，再因 `7,6` 都為正，轉成 `k/7<b<k/6`。
- Object continuity: 從 `b` 的兩個分數複製端點，落到第一條區間帶。
- Boundary: 只保留原第一列的淡影與新區間，讓方法先完整走一次。

## 05 finish_b_normalization (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 06 normalize_c (0:25, loop=false)

- Animation: 第二列三邊加上 `a+c+d`，中央成為 `k`。
- Staged result: `(12/5)c<k<(13/5)c`，再轉成 `5k/13<c<5k/12`。
- Teaching point: 每一列不是做不同技巧，只是補入該列缺少的三項。
- Boundary: `c` 的區間落到第二條帶，與 `b` 共用同一個 `k` 尺度。

## 07 finish_c_normalization (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 08 normalize_d (0:25, loop=false)

- Animation: 第三列三邊加上 `a+b+d`；用顏色追蹤 `d` 的係數從 `7/2,9/2` 各增加 1。
- Staged result: `(9/2)d<k<(11/2)d`，所以 `2k/11<d<2k/9`。
- Boundary: `d` 的區間加入數線，仍不宣告順序。

## 09 finish_d_normalization (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 10 normalize_a (0:25, loop=false)

- Animation: 第四列三邊加上 `a+b+c`，中央再次收成 `k`。
- Staged result: `(19/5)a<k<(21/5)a`，所以 `5k/21<a<5k/19`。
- Pattern: 四個原本互相纏繞的不等式，現在都只剩「某變數位於 `k` 的哪個比例」。
- Boundary: 四條區間全部備齊。

## 11 finish_a_normalization (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 12 place_four_intervals (0:25, loop=false)

- Visual: 因 `k>0`，把水平座標標成「數值除以 `k`」。四條半透明區間依序放在同一刻度上。
- Animation: `b:(1/7,1/6)`、`d:(2/11,2/9)`、`a:(5/21,5/19)`、`c:(5/13,5/12)` 從公式複製到區間帶。
- Prompt: 「不必知道四個數的精確值；要保證誰在誰左邊，只需檢查哪兩個端點？」
- Boundary: 四區間完整可見，但尚未畫出順序箭頭。

## 13 finish_interval_bands (0:20, loop=false)

- Animation: 前兩段落定後，再加入後兩段區間，避免四段同時搶注意力。
- Boundary: 四個範圍全數可見，下一頁才開始比較相鄰端點。

## 14 separate_b_d (0:25, loop=false)

- Focus: 淡化 `a,c`，只留 `b` 的上界 `k/6` 與 `d` 的下界 `2k/11`。
- Exact comparison: 將 `1/6` 與 `2/11` 通分成 `10/60` 與 `10/55`；因 `10/60<10/55`，得到 `b<k/6<2k/11<d`。
- Visual evidence: 在兩區間間畫出清楚空隙，而非只依小數位置判斷。
- Boundary: 第一段順序 `b<d` 落定。

## 15 separate_d_a (0:25, loop=false)

- Focus: 點亮 `d` 的上界 `2k/9` 與 `a` 的下界 `5k/21`。
- Exact comparison: `2/9=10/45`，`5/21=10/42`；同分子下，分母 45 較大，所以前者較小。
- Chain: `d<2k/9<5k/21<a`，接到上一段得到 `b<d<a`。
- Boundary: 第二個空隙與順序箭頭穩定。

## 16 separate_a_c (0:25, loop=false)

- Focus: 點亮 `a` 的上界 `5k/19` 與 `c` 的下界 `5k/13`。
- Exact comparison: 共同正分子 `5k` 下，`19>13`，故 `5k/19<5k/13`。
- Chain: `a<5k/19<5k/13<c`；四個區間現在完全由左至右分離。
- Boundary: 完整順序先以由小到大 `b<d<a<c` 呈現。

## 17 compare_a_and_c (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 18 consolidate (0:25, loop=false)

- Recap: 四塊正數合成 `k`；每列補齊同一總量；四個區間落到共同數線；三對端點留下三個空隙。
- Final reveal: 依題目習慣改寫為 `c>a>d>b`。
- Source footer: `解題來源：正哥愛數學`，第壹部分第 10 題、PDF 第 6 頁。
- End state: 答案保留在四條區間之上，讓結論仍連著可見證據。

## Independent mathematics check

令 `k=a+b+c+d>0`。四列依次整理為

`k/7<b<k/6`, `5k/13<c<5k/12`, `2k/11<d<2k/9`, `5k/21<a<5k/19`。

三個完全分離的端點比較為

`k/6<2k/11`、`2k/9<5k/21`、`5k/19<5k/13`。

因此任何同時滿足原不等式組的四個正數都必有 `b<d<a<c`，也就是 `c>a>d>b`。這個推論只使用必要的端點，不需要假設各區間內的精確位置。

## Source ambiguity

題式、答案與來源推導一致，未發現影響結論的歧義。來源最後一列採用「同分子 10」排列多個分數；本課程改成逐對比較，以免密集長鏈遮住每一步真正需要的上、下界。

## Implementation cautions for the future deck

- 區間端點必須使用空心圓，不能把嚴格不等式畫成含端點。
- 所有分數位置應由精確有理數計算；不得用人工拖曳到近似位置。
- 除以 `k` 前必須先顯示 `k>0`，避免視覺上略過不等號方向的依據。
