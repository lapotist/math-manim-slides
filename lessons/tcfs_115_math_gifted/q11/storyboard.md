# Q11 Storyboard: Following One Plane Across a Cube

目標長度：約 11 分鐘。先把「截面」理解成同一平面在每一個正方形面上留下的一條直線，再讓這條線從上表面、右表面一路走到前表面。找到 `N` 之後才把三個面攤平，用三組相似三角形傳遞長度比例。

## Visual grammar

- 立方體參考邊使用中性灰；截面內已確認的直線使用亮青色。
- 原題點 `P,Q,R` 使用黃色；為延伸而新增的 `L,I,J` 使用洋紅色；目標點 `N` 使用綠色。
- 每次只強調正在工作的立方體表面，其餘面降至低透明度，但保持空間方向可辨。
- 展開三個正方形面時，點和線從立方體複製移動到平面圖，保持物件身分與邊長標記。
- 來源圖只作核對，不作畫面素材；所有立方體、截線與標記重新建構。

## Beat plan

## 01 build_cube (0:45, loop=false)

- Settled visual: 逐邊建立正立方體 `ABCD-EFGH`，先只標八個頂點。
- Orientation: 明確保留四條直立邊 `AE,BF,CG,DH`，讓後續的「上、右、前」三個面可追蹤。
- Prompt: 「一個斜平面穿過立方體時，在每一個正方形面上會留下什麼？」
- Boundary: 立方體穩定，截面尚未出現。

## 02 place_pqr (0:50, loop=false)

- Animation: `P` 落在 `EF` 中點，`R` 落在 `HD` 中點；兩條邊各以 `1:1` 刻痕確認。
- Ratio: `Q` 沿 `EH` 從 `E` 移到 `EQ:QH=2:3` 的精確位置。
- Constraint: 三點同時亮起，旁邊出現一張透明平面片的淡影，但不先畫完整截面。
- Boundary: `P,Q,R` 和三個已知比例可讀。

## 03 trace_known_section (0:45, loop=false)

- Visual fact: 同一截平面與一個立方體面相交時，交痕是一條直線。
- Animation: 上表面 `EFGH` 亮起，連接同在此面的 `P,Q`；後表面 `AEHD` 接著亮起，連接 `Q,R`。
- Teaching point: 已知同一面上的兩個截點，就已經知道該面上的整條截線方向。
- Boundary: `PQ`、`QR` 成為兩條已確認的青色線段。

## 04 extend_top_line (0:55, loop=false)

- Animation: 在上表面延長 `PQ`；向 `FG` 一側交其延長線於 `L`，向 `GH` 一側交其延長線於 `I`。
- Definitions on screen: `L=PQ cap extended FG`，`I=PQ cap extended GH`，逐一出現，避免來源輔助圖中的未定義跳躍。
- Spatial meaning: `L,I` 雖在正方形外，仍同時位於上表面所在平面與截平面中。
- Boundary: `L-P-Q-I` 共線可見。

## 05 extend_right_line (0:50, loop=false)

- Focus: 只亮右表面 `CDHG`。
- Animation: `I` 與 `R` 都在這個面的延伸平面中，連成直線；直線向下交 `CD` 於題目給定的 `M`，並交 `CG` 延長線於新增點 `J`。
- Definitions: `J=IR cap extended CG`。保留 `M` 作方向核對，但後續計算只需要 `J`。
- Boundary: `I-R-M-J` 的同一直線關係穩定。

## 06 locate_n (0:55, loop=false)

- Focus: 轉到前表面 `BCGF`。
- Membership proof: `L` 位於 `FG` 延長線，`J` 位於 `CG` 延長線，所以兩者都在前表面所在平面；前面又已證明兩者都在截平面。
- Animation: 連接 `LJ`，它就是兩平面在此面的交痕；與 `FB` 的交點亮成綠色 `N`。
- Section: 以 `P-Q-R-M-J-N` 的關聯短暫回顧截面如何跨面延續，答案比例仍隱藏。
- Boundary: `N=LJ cap FB` 已由兩個面共同決定。

## 07 unfold_three_faces (0:55, loop=false)

- Animation: 複製上表面、右表面、前表面，依序旋開成三張並排正方形；原立方體縮小保留在角落作方向參考。
- Stable labels: `L,P,Q,I` 留在上面圖；`I,R,G,J` 留在右面圖；`L,F,N,G,J` 留在前面圖。
- Scale: 統一標示立方體邊長為 `a`。
- Prompt: 「接下來只需讓比例從第一張正方形，一張一張傳到 `FN`。」
- Boundary: 三張平面圖均無透視變形。

## 08 top_left_ratio (0:55, loop=false)

- Highlight: 上表面的直角三角形 `PEQ` 與 `PFL`。
- Similarity: 兩者有一對對頂角，且各有一個直角，所以相似；又 `PE=PF=a/2`，相似比為 1。
- Transfer: `LF=EQ=2a/5` 從 `EQ` 的已知黃色長度複製到 `LF`。
- Boundary: 前表面稍後要用的 `LF` 已被精確測得。

## 09 top_right_ratio (0:55, loop=false)

- Highlight: 同一上表面的三角形 `PEQ` 與 `IHQ`。
- Ratio: `EQ:QH=2:3`，相似三角形給出 `PE:HI=2:3`。
- Staged lengths: `PE=a/2`，所以 `HI=3a/4`；再由 `IG=IH+HG` 得 `IG=3a/4+a=7a/4`。
- Boundary: 右表面所需的 `HI`、`IG` 同時可見。

## 10 right_face_ratio (0:55, loop=false)

- Highlight: 右表面的三角形 `IHR` 與 `IGJ`。兩者共用 `I` 的方向，`HR`、`GJ` 平行，因此相似。
- Known length: `R` 是 `HD` 中點，所以 `HR=a/2`。
- Staged proportion: `HI/IG=HR/GJ`，代入 `(3a/4)/(7a/4)=(a/2)/GJ`。
- Result: `GJ=7a/6`，從比例式轉到線段標籤。
- Boundary: 右面將長度傳到前面的共同邊 `GJ`。

## 11 front_face_ratio (0:55, loop=false)

- Highlight: 前表面的三角形 `LFN` 與 `LGJ`；兩者共用 `L` 的角，`FN` 與 `GJ` 平行，所以相似。
- Build denominator: `LG=LF+FG=2a/5+a=7a/5`，從兩段實際合併形成。
- Proportion: `LF/LG=FN/GJ`；將 `2a/5`、`7a/5`、`7a/6` 逐一由圖形複製進式子。
- Result: `FN=a/3`。
- Boundary: 綠色 `FN` 在原立方體和展開面上同步更新。

## 12 finish_ratio (0:45, loop=false)

- Visual: 回到直立邊 `FB=a`；把它分成上段 `FN=a/3` 與下段 `NB`。
- Staged arithmetic: `NB=a-a/3=2a/3`。
- Ratio: 由兩段實體長條收成 `(a/3):(2a/3)=1:2`，最後顯示 `FN/NB=1/2`。
- Boundary: 不只保留分數，也保留 `FB` 上的 1 對 2 分割。

## 13 consolidate (0:55, loop=false)

- Recap construction: `PQ` 延伸找 `L,I`；`IR` 延伸找 `J`；`LJ` 交 `FB` 找 `N`。
- Recap ratios: 上表面得到 `LF=2a/5`、`IG=7a/4`；右表面得到 `GJ=7a/6`；前表面得到 `FN=a/3`。
- Final answer: `FN/NB=1/2`。
- Source footer: `解題來源：正哥愛數學`，第壹部分第 11 題、PDF 第 7 頁；標明原題頁碼範圍在 collection metadata 為 `[7,8]`。
- End state: 小立方體、三張展開面與答案同時可掃讀。

## Independent mathematics check

取座標

`A=(0,0,0), B=(a,0,0), C=(a,a,0), D=(0,a,0)`,

`E=(0,0,a), F=(a,0,a), G=(a,a,a), H=(0,a,a)`。

則 `P=(a/2,0,a)`、`Q=(0,2a/5,a)`、`R=(0,a,a/2)`。三點決定的平面為

`4x+5y+6z=8a`。

邊 `FB` 上有 `x=a,y=0`，代入得到 `z=2a/3`。這是從 `B` 向上的 `NB`，故 `NB=2a/3`、`FN=a/3`，比例確為 `1/2`。此座標檢查獨立於 storyboard 的相似三角形推導。

## Source ambiguity and resolution

- 來源解答的輔助圖使用 `L,J`，正文在使用前未逐一定義。本課程明確定義 `L=PQ` 與 `FG` 延長線的交點，`J=IR` 與 `CG` 延長線的交點。
- PDF 文字層在一處把 `EQ` 誤辨為 `EG`；渲染圖、題目比例與相似三角形關係都支持正確讀法 `EQ:QH=2:3`。
- Collection 將 source pages 記為 `[7,8]`；實際第 11 題完整解答在 PDF 第 7 頁，第 8 頁從第 12 題開始。metadata 保留 catalog 的頁碼範圍，source locator 說明實際位置。

## Implementation cautions for the future deck

- 3D 投影只用於建立空間關係；所有比例計算切換到無透視的正方形面。
- `L,I,J` 在出現時必須立即顯示交點定義，不能依賴觀眾猜延長線。
- 展開表面時保持共享邊與點的顏色一致；不要複製出看似不同的 `G` 或 `I`。
- 相似比例需依線段方向配對，特別避免把 `HI/IG` 或 `LF/LG` 寫反。
