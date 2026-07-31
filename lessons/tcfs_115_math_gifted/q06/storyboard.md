# Q06 Storyboard: Factor 480 Directly

目標長度：約 3 分鐘。這是一題有限因數枚舉，不需要把簡單的因式分解拆成長篇發現活動。課程直接補 1、分解 480、列完候選，再套入三角形條件。

## Teaching basis

- Prerequisites: 乘法公式展開、正整數質因數分解、三角形兩短邊和大於最長邊。
- Likely first misconception: 找到乘積為 480 的三個數就停下來，忘記原來的三角形條件；或把等號的退化情形也算作三角形。
- Concrete object: 依最小因數 `z` 分組的完整有序因數表。
- Boundary case: `(x,y,z)=(12,8,5)` 滿足乘積與次序，但 `8+5=12+1`，回到原邊長後只會攤成一直線。
- Final realization: 質因數分解給出完整候選，三角形條件只留下兩組。

## Source research record

- Canonical source: `數學-115數理資優學科能力評量答案.pdf`。
- Stable checksum: `983f12dbd22aaa7d19c914c4e88c42973faa6d09e32ae036edf15961bbeadcc2`。
- Exact locator: 第壹部分第 6 題，PDF 第 3 頁。
- Permission and release scope: 依 `lesson.toml`、`NOTICE.md` 與相關 provenance 記錄；畫面與文字為專案獨立重述，不複製來源版面。
- Source comparison: 來源答案在限制最小因數時寫得很快；本課保留必要的 `z|480` 理由，但不把它擴張成多頁方法介紹。

## Visual grammar

- `480` 與質因數分解使用亮藍色；三角形條件與通過候選使用綠色。
- 全部 19 組候選留在同一張表中；淘汰時降低不合者透明度，不讓它們突然消失。
- 每個片段只回答一個問題，最多四個動畫階段。

## Beat plan

## 01 complete_product

- Show: `abc+ab+bc+ca+a+b+c=479`。
- Action: 兩邊同時加 1，直接收成 `(a+1)(b+1)(c+1)=480`。
- Purpose: 把七項和轉成整數乘積，不延伸成八種選擇的長篇說明。

## 02 factor_triangle_condition

- Show: `480=2^5·3·5`。
- Purpose: 依使用者回饋，這個片段只直接分解 480，不同時加入變數、條件或額外示範。

## 03 ordered_factor_triples

- Define: `x=a+1, y=b+1, z=c+1`。
- Retain: `x>y>z>=2` 與 `xyz=480`。
- Bound: `z^3<480` 且 `z|480`，故 `z in {2,3,4,5,6}`。
- Complete universe:
  - `z=2`: `(80,3),(60,4),(48,5),(40,6),(30,8),(24,10),(20,12),(16,15)`；
  - `z=3`: `(40,4),(32,5),(20,8),(16,10)`；
  - `z=4`: `(24,5),(20,6),(15,8),(12,10)`；
  - `z=5`: `(16,6),(12,8)`；
  - `z=6`: `(10,8)`。
- Purpose: 先把候選全集定清楚，再做任何篩選。

## 04 filter_triangles

- Translate: `b+c>a` 等價於 `y+z>x+1`。
- Test: 對表中 19 組逐一檢查。
- Survivors: `(12,10,4)` 與 `(10,8,6)`。
- Boundary: `(12,8,5)` 只有 `8+5=12+1`，必須淘汰。
- Purpose: 直接使用原條件，不另立抽象的「最近因數對」方法。

## 05 restore_sides

- Action: 每個值減 1。
- Results: `(12,10,4)->(11,9,3)`；`(10,8,6)->(9,7,5)`。
- Purpose: 明確回到題目所問的 `(a,b,c)`。

## 06 verify_triangles

- Verify order and positivity for both triples.
- Verify triangle inequalities: `9+3>11` and `7+5>9`。
- Verify the original equation through `12·10·4-1=479` and `10·8·6-1=479`。
- Purpose: 將答案完整代回所有原始條件。

## Independent mathematics check

原式加 1 得 `(a+1)(b+1)(c+1)=480`。令 `x=a+1, y=b+1, z=c+1`，則 `x>y>z>=2` 且 `xyz=480`。由 `z^3<480` 及 `z|480`，得到 `z=2,3,4,5,6`。逐一列舉 480 的有序因數三元組，共有 19 組，正如第三片段的完整表。

原三角形條件 `b+c>a` 等價於 `y+z>x+1`。檢查 19 組後，只有 `(x,y,z)=(12,10,4),(10,8,6)` 通過。各自減 1 得 `(a,b,c)=(11,9,3),(9,7,5)`。兩組均滿足嚴格次序、正整數、三角形不等式與原方程。
