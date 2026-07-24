# Part 2 Q02 Storyboard: Two Similarities Build the Identity

目標長度：約 10 分鐘。先從三角形、角平分線與外接圓逐層建立圖形。觀眾先看見兩組角被同一條弧或對頂角固定，才把三個三角形抽出並對齊。後半段讓兩個相似比各產生一個乘積，最後沿著 `AE=AD+DE` 把它們拼成角平分線長度公式。

## Visual grammar

- 原三角形與外接圓使用中性灰；角平分線 `AD` 使用藍色。
- 第一組相似 `ABD~AEC` 的對應角使用黃色；第二組 `ABD~CED` 使用綠色；對頂角使用洋紅色短弧。
- 對應邊在三個抽出三角形中保持同色與同線寬；重排方向可旋轉，但不可鏡射後不加提示。
- 兩個乘積關係分列為藍、綠「收據」，代入時由圖中線段複本移動，不直接顯示完成公式。
- 所有圖形與排版重新建構，不使用來源圓圖。

## Beat plan

## 01 build_triangle (0:40, loop=false)

- Settled visual: 建立一般的不等邊三角形 `ABC`，不先畫圓或任何輔助線。
- Prompt: 「若想量從 `A` 到對邊的一條特殊線，哪些局部形狀可能把它和三邊長連起來？」
- Boundary: 只保留三角形與頂點名稱，公式隱藏。

## 02 place_angle_bisector (0:45, loop=false)

- Animation: 從 `A` 畫角平分線交 `BC` 於 `D`。
- Evidence: `angle BAD` 與 `angle DAC` 的兩個等角弧依序出現，`D` 在 `BC` 上的共線關係清楚。
- Question: 顯示目標線段 `AD`，但不顯示待證公式。
- Boundary: 角平分線的定義已被圖形確認。

## 03 add_circle_and_e (0:50, loop=false)

- Animation: 作過 `A,B,C` 的外接圓，再沿同一條射線延長 `AD`，與圓第二次交於 `E`。
- Add chord: 連接 `CE`；保留 `A-D-E` 與 `B-D-C` 的交叉結構。
- Discovery prompt: 「新增的點 `E` 不是為了多一條線；它讓哪些角由同一段圓弧鎖定？」
- Boundary: 完整構形穩定，三個待比較三角形只以淡色輪廓提示。

## 04 pose_hidden_similarity (0:45, loop=false)

- Animation: 依次著色三角形 `ABD`、`AEC`、`CED`，一次一個，其餘降透明度。
- Prompt: 「這三個大小不同、方向不同的三角形，會不會其實有相同形狀？」
- Pause: 在角標位置留空，不先寫 `AA`。
- Boundary: 三個候選同時以輪廓保留。

## 05 prove_first_similarity (0:55, loop=false)

- First angle: 因 `A,D,E` 共線且 `AD` 平分 `angle BAC`，從兩個原等角弧轉移得到 `angle BAD=angle CAE`。
- Second angle: `angle ABD=angle ABC`；`angle ABC` 與 `angle AEC` 同對弧 `AC`，所以 `angle ABD=angle AEC`。弧 `AC` 在圓上亮起後才標等角。
- Conclusion: 兩組角足夠，顯示 `triangle ABD ~ triangle AEC`。
- Correspondence: 頂點配對 `A<->A, B<->E, D<->C` 保留在小表中。
- Boundary: 第一組相似得到黃色勾號。

## 06 prove_second_similarity (0:55, loop=false)

- First angle: `angle BAD=angle BAE`，而 `angle BAE` 與 `angle BCE` 同對弧 `BE`，所以 `angle BAD=angle BCE`。
- Second angle: 直線 `AE` 與 `BC` 在 `D` 相交，`angle ADB` 與 `angle CDE` 是對頂角。
- Conclusion: 顯示 `triangle ABD ~ triangle CED`。
- Correspondence: 頂點配對 `A<->C, B<->E, D<->D`。
- Boundary: 第二組相似得到綠色勾號；兩組證明並列。

## 07 align_three_triangles (0:55, loop=false)

- Object continuity: 從原圖各複製 `ABD`、`AEC`、`CED`，旋轉與縮放後排成相同方向；原圓圖淡化保留。
- Match: 每一對對應角疊上同色弧；對應邊依配對表上色。
- Conclusion: 因後兩者都與 `ABD` 相似，形成 `ABD~CED~AEC` 的完整鏈。
- Prompt: 「哪一個相似比能產生 `AB*AC`？哪一個能產生 `BD*DC`？」
- Boundary: 三角形與兩個空白乘積框並列。

## 08 build_first_product (0:50, loop=false)

- Focus: 只亮 `ABD~AEC`。
- Ratio: 從對應邊複製得到 `AB/AE=AD/AC`。
- Cross product: 兩條對角配對線交叉後，式子變成 `AB*AC=AD*AE`。
- Meaning: 左邊正是目標根號中的第一個乘積；右邊含有要研究的 `AD`。
- Boundary: 藍色第一張收據固定。

## 09 build_second_product (0:50, loop=false)

- Focus: 轉到 `ABD~CED`。
- Ratio: 由配對邊得到 `AD/CD=BD/DE`。
- Cross product: `AD*DE=BD*DC`，左右兩側由實際線段標籤複製形成。
- Teaching point: 這個乘積也可視為交弦關係，但此處已直接由第 (1) 小題的相似三角形得到。
- Boundary: 綠色第二張收據固定在第一張下方。

## 10 split_ae (0:50, loop=false)

- Return to geometry: 點亮共線順序 `A-D-E`，將整段 `AE` 拆成藍色 `AD` 與綠色 `DE`。
- Transform: 第一張收據中的 `AE` 由線段複本展開成 `AD+DE`。
- Build one term at a time: `AB*AC=AD(AD+DE)=AD^2+AD*DE`。
- Boundary: `AD*DE` 以綠框等待第二張收據代入。

## 11 isolate_ad_square (0:50, loop=false)

- Substitution: 將第二張收據的 `BD*DC` 移入綠框，取代 `AD*DE`。
- Equation: `AB*AC=AD^2+BD*DC`。
- Rearrangement: 把 `BD*DC` 作為同一物件移到左側並改變符號，得到 `AD^2=AB*AC-BD*DC`。
- Boundary: 平方形式落定，尚未取根號。

## 12 take_positive_root (0:40, loop=false)

- Positivity: 回到圖上的實際線段 `AD`，標明 `AD>0`。
- Root: 對平方式取根時只保留正根，得到 `AD=sqrt(AB*AC-BD*DC)`。
- Rigor: 根號內非負性不是額外假設，而由左側本來就是 `AD^2` 得到。
- Boundary: 完整待證式第一次顯示。

## 13 consolidate (0:50, loop=false)

- Recap: 角平分線與弧給第一組相似；弧與對頂角給第二組相似；兩組各交出一個乘積。
- Assembly: `AE=AD+DE` 把兩張乘積收據接在一起，留下 `AD^2`。
- Final statement: `AD=sqrt(AB*AC-BD*DC)`。
- Source footer: `解題來源：正哥愛數學`，第二部分第 2 題、PDF 第 10 頁。
- End state: 圓圖、兩張相似配對表與最後公式同時可追溯。

## Independent mathematics check

第一組相似的對應為

`triangle ABD ~ triangle AEC`, with `(A,B,D)<->(A,E,C)`，

故 `AB/AE=AD/AC`，即 `AB*AC=AD*AE`。

第二組相似的對應為

`triangle ABD ~ triangle CED`, with `(A,B,D)<->(C,E,D)`，

故 `AD/CD=BD/DE`，即 `AD*DE=BD*DC`。

又 `A-D-E` 共線且 `D` 在 `AE` 內部，所以

`AB*AC=AD*AE=AD(AD+DE)=AD^2+BD*DC`。

移項得 `AD^2=AB*AC-BD*DC`。因 `AD` 是正長度，`AD=sqrt(AB*AC-BD*DC)`。

## Source ambiguity

題式、圖形與結論清楚，未發現影響結論的歧義。Collection 的摘要答案記成平方形式 `AD^2=...`，而 PDF 題目最後要求並證得的是正根形式 `AD=sqrt(...)`；lesson metadata 以實際題目要求的正根形式為 expected answer。來源第 (2) 小題以圓內冪得到 `AD*DE=BD*DC`；本課程改由第 (1) 小題已證的 `ABD~CED` 直接導出同一關係，更明確回應「利用第 (1) 小題」。

## Implementation cautions for the future deck

- 圓周角必須在對應弧亮起後才標等角，不能只靠看起來相近。
- 三角形抽出重排時保留頂點配對表；相似式中的順序必須與表一致。
- `AE=AD+DE` 依賴 `A-D-E` 的順序，延長線構形必須清楚顯示 `D` 位於 `A,E` 之間。
- 取根號前必須顯示 `AD>0`，不能從平方等式無條件省略正負號。
