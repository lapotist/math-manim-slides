# Question 11 storyboard

## Teaching intent

這是一個教師帶領的幾何 worked example。預備知識是正方形的直角與等邊、全等變換會保留長度與角度、畢氏定理及其逆定理，以及向量內積判斷銳鈍角。學生最可能先產生的誤解是把

\[
2BP^2=CP^2-AP^2
\]

當成只能硬展開的三段距離；另一個常見錯誤是看見圖中的 `P` 靠近對角線，就自行假設 `A,P,C` 共線。課程始終不使用這個圖像假設。

開場只建立正方形、同一個內點 `P` 和三段距離。接著讓 `P` 沿著條件本身的一小段精確參數路徑移動，再回到容易觀看的代表位置。這個動作只回答一個問題：條件不是某張特殊比例圖偶然成立，而目標角在不同合法位置仍值得追問。畫面不留下軌跡，也不標角度數值。

核心動機來自正方形已經提供的四分之一圈。以 `B` 為中心，`BA` 旋轉 `90` 度會落在 `BC`；把整個三角形 `ABP` 同步旋轉，`P` 落到新點 `E`。同一個變換立刻給出

\[
BE=BP,\qquad CE=AP,\qquad \angle CEB=\angle APB.
\]

新出現的三角形 `BPE` 是直角等腰三角形，所以 `PE^2=2BP^2`。原條件現在不再是三段互不相干的平方，而是可見三角形 `CEP` 的

\[
CP^2=CE^2+PE^2.
\]

逆畢氏定理讓 `E` 點的直角真正落下。另一邊，直角等腰三角形給 `45` 度。第 9 段只把兩塊角拼成 `90+45`，並停在問號；第 10 段才把旋轉後的角送回原來的 `P`，揭示 `135` 度。

揭示後再做一次獨立核對。座標段不重演旋轉，而用 `P` 在正方形內部所保證的 `u>0,v>0`，算出

\[
\overrightarrow{PA}\cdot\overrightarrow{PB}=-sv,
\qquad
\left|\det(\overrightarrow{PA},\overrightarrow{PB})\right|=sv.
\]

內積為負先鎖定鈍角；正弦與負餘弦等大再鎖定 `135` 度。最後回到原圖，保留「四分之一圈把係數 2 變成一條可量的斜邊」這個可記憶的 realization。

## Source reconstruction

- 典藏頁面：`https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87%E5%84%AA%E7%8F%AD/112%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87`。
- 凍結頁面 SHA-256：`8ef9b13e28c992e21dd874cfeabbb6ad66dcacdeec3c326f058ff561de9ba094`。
- 題目資產：`112中一中資優班解析.pdf`，Drive ID `1wZiSE5cZZI9Fr_YJovGP_H3aWoFXxc_H`，catalog 存取狀態 `public`，17 頁，本題在第 11 頁。
- PDF SHA-256 為 `277e49efb3aca44666e17c2c4135b6047922f25adee58952560416996140acbd`，檔案大小 `1122169` bytes；此值與 catalog source registry 及目前本地研究檔一致。
- PDF 第 11 頁實際題意是：`P` 為正方形 `ABCD` 內一點，滿足 `2BP^2=CP^2-AP^2`，求 `\angle APB`。頁面 `解析` 區域空白，因此 PDF 只能定位題目，不能驗證解法。
- 解題資產：公開影片 `https://www.youtube.com/watch?v=WHaIgarL3nM`，provider ID `WHaIgarL3nM`，catalog 存取狀態 `public_stream`，驗證標題 `112中ㄧ中資優班填充11`。
- 本地研究串流長 `167.740952` 秒、解析度 `208x144`，SHA-256 `bf297c3f85804a54ac57f951d443f492624397eb100335c12592400211cb955c`。`00:02:46.85` 仍是完整且無遮擋的最後結論；`00:02:46.90` 開始出現裝置介面，所以解題定位固定為 `00:00-02:46.85`。
- 來源令 `AP=a`、`BP=b`、`CP=c`，再把 `P` 繞 `B` 旋轉四分之一圈到外部點 `E`，旋轉方向同時把 `A` 送到 `C`。所以 `BE=b`、`CE=a`，而直角等腰三角形 `BPE` 給 `PE=\sqrt2 b`。條件成為 `PE^2+CE^2=CP^2`，來源再用逆畢氏定理得到 `\angle CEP=90` 度，以 `\angle PEB=45` 度與旋轉保角完成 `\angle APB=135` 度。
- 來源結論與獨立重建一致。來源圖中的 `P` 靠近 `AC`，但推理不需要且沒有權利假設 `A,P,C` 共線。本課保留旋轉構想，改用原創動畫逐步維持物件身分，並新增條件保留的兩個合法位置、完整內點符號檢查與外部反例。
- 權利狀態維持 `pending_cc0_scope`。課程不重用 PDF 頁面、影片畫面、手寫筆跡、聲音、標誌或來源措辭。

## Independent mathematics check

令正方形邊長為 `s>0`，取

\[
D=(0,0),\quad A=(0,s),\quad B=(s,s),\quad C=(s,0),
\]

且 `P=(x,y)` 在內部，所以 `0<x,y<s`。設

\[
u=s-x>0,\qquad v=s-y>0.
\]

三段平方長為

\[
BP^2=u^2+v^2,
\]

\[
CP^2=u^2+(s-v)^2,
\]

\[
AP^2=(s-u)^2+v^2.
\]

代入題設並除以 2：

\[
u^2+v^2=s(u-v).
\]

從 `P` 出發的兩支向量為

\[
\overrightarrow{PA}=(u-s,v),
\qquad
\overrightarrow{PB}=(u,v).
\]

因此

\[
\overrightarrow{PA}\cdot\overrightarrow{PB}
=u^2-su+v^2
=-sv,
\]

而二維行列式為

\[
\det(\overrightarrow{PA},\overrightarrow{PB})
=(u-s)v-vu
=-sv.
\]

因 `P` 在內部，`sv>0`。故內積為負，`\angle APB` 必為鈍角；同時行列式絕對值與內積絕對值相等。若 `0<\theta<180` 度表示兩向量的夾角，則

\[
\sin\theta=-\cos\theta>0,
\qquad
\cos\theta<0.
\]

唯一可能是

\[
\theta=135\text{ degrees}.
\]

兩個精確內部樣本也直接核對條件。令 `s=1`：

\[
P_1=\left(\frac25,\frac45\right),
\qquad
P_2=\left(\frac35,\frac45\right).
\]

兩點分別對應 `(u,v)=(3/5,1/5)` 與 `(2/5,1/5)`，都滿足 `u^2+v^2=u-v`；兩者的內積都等於 `-v`，行列式絕對值都等於 `v`。

「內部」不能刪掉。令 `s=1` 且取外部點 `P=(0,2)`，則

\[
BP^2=2,\quad CP^2=5,\quad AP^2=1,
\]

所以同一個距離式仍成立；但

\[
\overrightarrow{PA}=(0,-1),
\qquad
\overrightarrow{PB}=(1,-1)
\]

的夾角是 `45` 度。這個精確反例證明答案依賴題目明訂的內部條件，而不是無限制的距離恆等式。

`deck.py` 在匯入時以 `Fraction` 精確檢查兩個內部樣本、一般展示路徑的數個有理參數、四分之一圈構造中的全部距離等式、直角內積，以及外部反例。這些斷言不依賴 Manim 畫面座標。

## Visual grammar

- 正方形與非作用中的邊固定用中性墨白或灰色；同一個 `P` 從開場到答案揭示都保持黃色。
- `AP` 及其旋轉像 `CE` 固定用藍色；`BP` 及其旋轉像 `BE` 固定用黃色；`CP` 固定用紫色；新斜邊 `PE` 固定用綠色。
- 目標角與最後答案固定用珊瑚色。`90` 度用綠色，`45` 度用黃色，讓 `90+45` 的來源可從圖形直接回讀。
- 第 2 段的移動由 `t` 的有理圓參數控制：`u=(1-t)/(1+t^2)`、`v=tu`。畫面由 `t=1/3` 移到 `1/2` 再回來，全程精確滿足條件；不留下軌跡，以免誤認為課程正在宣告完整軌跡。
- 旋轉不是用新線段替換舊線段：三角形 `ABP` 的副本繞固定點 `B` 真正轉過 `90` 度，讓 `A` 落到 `C`、`P` 落到 `E`。原物件保留為淡色背景，學生可同時比對像與原像。
- 第 9 段的穩定畫面只出現 `90+45` 與問號，沒有 `135`。第 10 段才用獨立動畫揭示答案並把角標示送回原來的 `P`。
- 座標核對採新的兩欄版面，不疊在旋轉證明上。先突出 `u>0,v>0`，再出現內積與行列式，避免兩套論證在同一畫面互相競爭。

## Beat map and motion purposes

### 01 meet_square_and_inner_point

依序建立固定正方形、內點 `P`、三段 `AP`、`BP`、`CP`；動作只回答題目有哪些物件，不出現條件、輔助點或角度答案。

### 02 test_two_valid_positions

條件式出現後，`P` 與三段相依線沿精確條件路徑移到第二個合法位置，再回到代表位置；動作只提供「不是單一特例」的證據，不畫完整軌跡。

### 03 ask_for_target_angle

在原點 `P` 長出珊瑚色角弧與問號，其他線段略暗；動作把注意力從三個平方距離收束到唯一待求量。

### 04 rotate_point_about_b

先讓 `BA` 的副本繞 `B` 轉到 `BC`，再讓整個三角形 `ABP` 的彩色副本做同一個四分之一圈並落成 `BCE`；動作說明輔助點 `E` 為何自然出現。

### 05 match_rotated_lengths

相同顏色與刻痕依序連起 `AP=CE`、`BP=BE`，最後顯示 `\angle APB=\angle CEB`；動作只記錄旋轉保留的資料，不先做角度加法。

### 06 measure_the_new_diagonal

在 `B` 落下直角記號，連接 `P,E`，再由兩條相等直角邊逐項建立 `PE^2=PB^2+BE^2=2BP^2`；動作讓係數 2 變成一條可見線段。

### 07 translate_the_condition

由原條件移項得到 `CP^2=AP^2+2BP^2`，先依序突出同色的旋轉像與新斜邊，再寫出 `CP^2=CE^2+PE^2`；顏色連結讓每項都能回讀到已可見的線段。

### 08 earn_the_right_angle

只保留三角形 `CEP` 為亮色，等式落定後才在 `E` 顯示直角；動作回答逆畢氏定理在圖上究竟給了哪一個角。

### 09 assemble_preanswer_angles

恢復三角形 `BPE`，先標 `\angle PEB=45` 度，再把它與 `\angle CEP=90` 度拼成 `\angle CEB=90+45`；最後把旋轉保角關係寫成帶問號的目標式並停頓。

### 10 reveal_the_angle

問號單獨變成 `135` 度，珊瑚色角弧由 `E` 的合角對應回原來的 `P`；這是全課第一個出現答案數值的事件。

### 11 verify_with_interior_vectors

旋轉證明退場，換成座標正方形、`u,v` 內部距離與從 `P` 出發的兩支向量。內積與行列式分兩行落下，先用負號判斷鈍角，再用等大關係核對 `135` 度。

### 12 return_to_original_square

回到原正方形與同一個 `P`，以三個短句卡重新對應「四分之一圈、`2BP^2=PE^2`、直角加 `45` 度」，最後保留原目標角和答案；動作只做整體鞏固，不引入新結論。

## Build constraints

- 只編輯 `lessons/tcfs_112_math_gifted/q11/`；渲染媒體寫入專屬 ignored build 目錄。
- 場景類別為 `CarloTcfs112MathQ11`，十二個 beat 全部 `loop=false`。
- 中文只使用 `label()`；`MathTex` 只放 ASCII 數學內容。
- 先做 Python compile/import 與低畫質 smoke，再以 `--quality h` 隔離渲染。
- 必須檢查十二個 endpoint、完整每秒 sweep，以及第 2 段條件移動、第 4 段旋轉、第 7 段式子替換、第 9 段答案前停點、第 10 段答案揭示與第 11 段向量式的中間影格。
- lesson worker 停在 `draft_rendered`，不執行 `freeze-qa`，不建立 human-reviewed attestation，也不修改 collection state。
