# Question 10 storyboard

## Teaching intent

本課把最短路徑當成一個可以親手拉直的幾何問題。開場只畫長方形、對角線與
折線 (Q\to P\to B)，讓 (P) 在 (AC) 上、(Q) 在 (AB) 上移動；觀眾先看見
兩個點都能動，而且折線長度會跟著改變。此時不顯示任何座標或最短公式。

接著把 (B) 對 (AC) 鏡射到 (B')。畫面保留中垂線、直角與等長記號，先建立
鏡射身分 (PB=PB')，才把原目標改寫成 (PQ+PB')。然後才出現三角不等式；
移動 (P) 讓 (Q,P,B') 共線，把折線真的拉直，讓等號條件不是一句抽象規則。

拉直後先暫時隱去 (P)，只讓 (Q) 沿著 (AB) 滑動。每一個 (Q) 都對應一條
(QB')，最短的一條自然停在垂直 (AB) 的方向。直到這個幾何結論已經看懂，
才給四個頂點座標，算出 (B')、垂足 (Q) 與直線交點 (P)。倒數第二頁完整
檢查 (Q) 確實落在邊 (AB) 上、(P) 確實落在線段 (AC) 上，而且
(Q,P,B') 的次序正確。該頁停在 (QB'=8-(-24/5))，最後一頁才化簡成
(64/5)。

預估 9 分鐘。十一個 beat 全部不循環；每個停點只新增一個主要想法，並保留
足夠時間讓講者慢速指認線段與等號條件。

## Source and verification

- 典藏頁面：`https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87%E5%84%AA%E7%8F%AD/113%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87`。
- 題目來源：頁面嵌入的 `113中一中資優班解析.pdf`，Drive ID
  `1QQhuf8PqZMVyCdF9s9LHR8Q3y8RmAk3M`，SHA-256
  `c4c5c0d834f7ef8f423d21265c6a69cadcaedfc5f2de290a79d0bc61b3844273`，
  第 10 頁填充第 10 題。
- 題意：長方形 (ABCD) 中 (AB=16)、(BC=8)，(P) 在線段 (AC) 上、
  (Q) 在線段 (AB) 上，求 (PQ+PB) 的最小值。
- 解題來源：正哥愛數學公開影片
  `https://www.youtube.com/watch?v=X6Cabjm94eY`，影片標題為
  `113中一中資優班填充9-10`，存取狀態 `public_stream`。逐格檢視固定 Q10
  定位為 `01:26-05:50`。
- 來源使用鏡射、拉直與面積／比例關係計算。本課保留鏡射與拉直的核心數學，
  但以原創動態圖形重建；末段獨立採用座標，明確核對垂足與交點都在指定線段
  上。不使用來源影片或 PDF 的畫面、手寫字、聲音或原文。
- 專案原創課程內容採 CC BY 4.0，程式碼採 MIT；來源素材不納入本專案授權。

## Independent mathematics check

取

\[
D=(0,0),\quad C=(16,0),\quad B=(16,8),\quad A=(0,8).
\]

對角線 (AC) 的方程為 (x+2y=16)。令
(L(x,y)=x+2y-16)，法向量 (\mathbf n=(1,2))，則
(L(B)=16) 且 (\mathbf n\cdot\mathbf n=5)。把 (B) 對此直線鏡射：

\[
B'=B-2\frac{L(B)}{\mathbf n\cdot\mathbf n}\mathbf n
=(16,8)-\frac{32}{5}(1,2)
=\left(\frac{48}{5},-\frac{24}{5}\right).
\]

因 (P\in AC)，鏱射保持到鏡面的距離，故 (PB=PB')，所以

\[
PQ+PB=PQ+PB'\ge QB'.
\]

等號發生於 (Q,P,B') 共線且 (P) 位於兩者之間。從 (B') 到水平直線
(AB:y=8) 的最短線段為垂線，垂足

\[
Q=\left(\frac{48}{5},8\right).
\]

因 (0<48/5<16)，垂足確實在線段 (AB) 上。垂直線 (x=48/5) 與 (AC)
相交於

\[
P=\left(\frac{48}{5},\frac{16}{5}\right).
\]

又 (8>16/5>-24/5)，所以 (Q,P,B') 依序共線，且 (P) 位於線段 (AC)
上，等號確實可達。最後

\[
QB'=8-\left(-\frac{24}{5}\right)=\frac{64}{5}.
\]

`deck.py` 匯入時使用 `Fraction` 獨立核對鏡射點、垂足、交點、兩段鏡射長度
與最後總長，不依賴畫面座標或浮點近似。

## Visual grammar

- 黃色固定代表 (P)，珊瑚色固定代表 (Q) 與原始線段 (PB)。
- 藍色代表對角線 (AC) 與最後的直線距離；綠色代表鏡射構造與 (PB')；
  紫色代表折線的第一段 (PQ)。
- 鏡射時保留 (BB'\perp AC)、中點與等長記號，先讓 (PB=PB') 可見，再改寫
  路徑。三角不等式不可在鏡射身分之前出現。
- 座標只在第 8 beat 之後出現；此前只靠移動、鏡射、共線與垂直來建立直覺。
- 最終答案 (64/5) 在第 11 beat 前不得出現。第 10 beat 必須以
  (QB'=8-(-24/5)) 作為完整的 pre-answer 停點。
- 所有中文用 `label()`；`MathTex` 只放 ASCII 字元與數學符號。點標籤避開
  動線，尤其不能壓在線段 (QP) 或 (PB') 上。

## Beat map

### 01 meet_broken_path

先畫長方形與對角線，再放入 (P)、(Q) 與折線 (Q\to P\to B)。只提出
(PQ+PB) 要最小化，不顯示策略。

### 02 explore_two_movers

讓 (P) 沿 (AC) 走過幾個位置，再讓 (Q) 沿 (AB) 移動。折線持續跟隨，
使兩個自由度與長度變化可見，最後停在一個非最優的一般位置。

### 03 reflect_b_across_diagonal

將 (B) 跨過 (AC) 鏡射到 (B')。顯示鏡射線 (BB')、中點 (H)、直角與
(BH=HB')，但還不改寫目標。

### 04 replace_equal_leg

連結 (P) 與 (B')，以等長記號和 (P\in AC) 得到 (PB=PB')，再把
(PQ+PB) 改寫為 (PQ+PB')。淡出原本的 (PB)，留下鏡射後折線。

### 05 straighten_reflected_path

先畫直線段 (QB')，這時才寫三角不等式 (PQ+PB'\ge QB')。移動 (P)
直到 (Q,P,B') 共線，展示等號發生時折線被拉直。

### 06 slide_q_along_top_edge

暫時隱去 (P) 與兩段折線，只保留 (QB')。讓 (Q) 沿 (AB) 左右滑動，觀察
所有候選直線段，最後停在垂足位置。

### 07 settle_perpendicular_foot

加上直角記號，指出從固定點到直線的最短距離垂直於該直線；視覺確認垂足
落在 (AB) 這一段內。仍不使用座標。

### 08 introduce_coordinates

把四個頂點標成 (D=(0,0),C=(16,0),B=(16,8),A=(0,8))，由截距式得到
(AC:x+2y=16)。

### 09 compute_reflected_point

使用直線法向量公式計算鏡射點，得到
(B'=(48/5,-24/5))，並在圖上標出這個座標。

### 10 verify_attainable_configuration

算出垂足 (Q=(48/5,8)) 並用 (0<48/5<16) 確認它在線段上；再求
(P=(48/5,16/5))，用高度次序確認 (Q,P,B') 共線且 (P\in AC)。停在
(QB'=8-(-24/5))。

### 11 reveal_minimum_length

只做最後化簡，得到 (64/5)，並框住 (\min(PQ+PB)=64/5)。

## Build constraints

- 只可在 `lessons/tcfs_113_math_gifted/q10/` 編輯來源檔；媒體輸出使用專屬
  ignored `build/media/carlo_tcfs_113_math_gifted_q10`。
- 十一個 beat、TOML、講者稿與 Slides manifest 必須完全同序，全部
  `loop=false`；講者稿必須有 10 個 `[NEXT]`、0 個 `[LOOP]`。
- 匯入期必須用有理數核對鏡射點、垂足、交點、線段包含關係與答案。
- 必須以 1920x1080 原尺寸檢查鏡射直角／等長記號、移動標籤、座標推導、
  pre-answer 與答案畫面；另以固定頻率檢查完整影片，並加密抽查反射、拉直、
  滑動 (Q) 與座標轉場的中間影格。
