# Question 1 storyboard

## Teaching intent

讓觀眾先「看見」內、外角平分線其實互相垂直，再讓長度比把直角三角形鎖成 \(30\text{-}60\text{-}90\) 的形狀。角度代數放在最後，作為幾何觀察的整理，而不是開場就堆公式。

預估 8 分鐘。畫面一次只保留一個新問題；所有結論都在對應的圖形證據出現後才顯示。

## Source and verification

- 解題來源：正哥愛數學
- 原始題目：`數學-115數理資優學科能力評量答案.pdf`，第 1 頁。
- PDF 文字層把根號漏掉，會抽成 `AE=3AD`；頁面影像清楚顯示 \(AE=\sqrt3\,AD\)。本課以頁面影像為準。
- 獨立驗算：設 \(\angle CAD=\angle DAB=x\)。內、外角平分線垂直；由 \(AE/AD=\sqrt3\) 得 \(\angle ADE=60^\circ\)。因此 \(C=60^\circ-x\)、\(B=120^\circ-x\)、\(A=2x\)，代入得 \(0^\circ\)。

## Visual grammar

- 三角形與延長線：白色；已知條件：淡灰。
- \(x\) 角弧：黃色；\(60^\circ\) 與直角記號：綠色；最後消去的項：藍色與紅色成對。
- 點位固定採 `E--B--D--C` 的水平順序，符合 \(B>C\) 所選出的構形。
- 不用整頁文字卡。每個式子都靠近它所描述的角或邊，再在最後匯入同一條算式。

## Beat map

### 01 build_triangle (0:25, loop=false)

先畫底邊 \(BC\)，再長出 \(A\) 與兩腰。只顯示 \(B>C\) 及目標式 \(4C-2B+A\)；不顯示答案。鏡頭停一拍，讓觀眾辨認三個頂角。

### 02 place_bisectors (0:25, loop=false)

從 \(A\) 畫內角平分線 \(AD\)，以兩個相同黃色小弧表示；再把 \(BC\) 向左延長至 \(E\)，畫外角平分線 \(AE\)，以另一組相同小弧表示。畫面角落保留點的順序 `E--B--D--C`。

### 03 mark_bisected_angles (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

### 04 see_right_angle (0:25, loop=false)

把內角半角標成 \(x\)，先逐一亮起兩個內角半角。

### 05 inspect_exterior_bisectors (0:20, loop=false)

再逐一亮起兩個外角半角，四角落定後才顯示 \(2x+2y=180^\circ\)。

### 06 derive_perpendicular_bisectors (0:20, loop=false)

把直線角化成 \(x+y=90^\circ\)，最後在 \(A\) 放上 \(AD\perp AE\) 的直角記號。

### 07 complete_special_triangle (0:25, loop=false)

其餘圖形淡出，只保留直角三角形 \(ADE\)。以 \(AD=u\)、\(AE=\sqrt3u\) 標邊，逐步用畢氏定理得到 \(DE=2u\)。接著才標示斜邊一半所對的角 \(\angle ADE=60^\circ\)。避免只背誦特殊三角形比例。

### 08 measure_special_triangle (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

### 09 name_sixty_degree_angle (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

### 10 transfer_sixty (0:25, loop=false)

恢復全圖。讓 \(DE\) 與 \(DB\) 的同一射線閃一次，把 \(60^\circ\) 搬到 \(\angle ADB\)；再沿直線 \(BC\) 展開鄰補角，得到 \(\angle ADC=120^\circ\)。

### 11 transfer_sixty_to_base (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

### 12 derive_c (0:25, loop=false)

只強調三角形 \(ACD\)。依序亮起 \(x\)、\(120^\circ\)、\(C\)，沿三角形內角和排成 \(x+120^\circ+C=180^\circ\)，整理為 \(C=60^\circ-x\)。

### 13 derive_b_and_a (0:25, loop=false)

切換強調三角形 \(ABD\)，用 \(x+60^\circ+B=180^\circ\) 得 \(B=120^\circ-x\)。鏡頭回到頂角，兩個 \(x\) 合併成 \(A=2x\)。三個結果並排但仍以顏色連回圖中的角。

### 14 solve_segment_lengths (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

### 15 cancel_expression (0:25, loop=false)

目標式移到中央。把三個結果各自複製進去，而非憑空換式：

### 16 substitute_length_relations (0:25, loop=false)

\[
4(60-x)-2(120-x)+2x.
\]

### 17 cancel_common_terms (0:25, loop=false)

先讓常數 \(240-240\) 成對消去，再讓 \(-4x+2x+2x\) 成對消去，最後才顯示 \(0^\circ\)。

### 18 simplify_target_expression (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

### 19 consolidate (0:25, loop=false)

回到乾淨全圖；依序短暫脈衝「垂直」、「\(60^\circ\)」、「三個角的表示式」，最後停在 \(4C-2B+A=0^\circ\)。這一頁供口頭回顧，不增加新推導。

### 20 reveal_final_value (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## Build constraints

- 以 `Slide.next_slide()` 對應九個 beat；切頁前所有 updater 必須清乾淨。
- 長度標籤與角弧跟著圖形變換，但本題不需要連續拖曳或循環頁。
- MathTex 使用 `\sqrt{3}`，不可沿用 PDF 文字層的錯誤抽取。
- 等式替換使用 `TransformMatchingTex`；不要以整張新算式直接淡入覆蓋舊式。
