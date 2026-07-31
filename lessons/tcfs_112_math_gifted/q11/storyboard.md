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
- 專案原創課程內容採 CC BY 4.0，程式碼採 MIT；來源素材不納入本專案授權。

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

## Beat map

### 01 meet_square_and_inner_point

這是一個正方形 `ABCD`。黃色的 `P` 確定在正方形內部。

動作目的：讓「先只看固定圖形」在穩定畫面上單獨成立，再進入下一步。

### 02 test_two_valid_positions

題目給的距離關係現在出現：

動作目的：讓「同一條件不只一個位置」在穩定畫面上單獨成立，再進入下一步。

### 03 ask_for_target_angle

題目要找的是 `P` 點的這個珊瑚色角，也就是 `\angle APB`。

動作目的：讓「真正要找的是這個角」在穩定畫面上單獨成立，再進入下一步。

### 04 demonstrate_quarter_turn

從 `B` 指向 `A` 的邊，繞 `B` 轉九十度，正好落在 `BC`。

動作目的：讓「先用探針確認四分之一圈」在穩定畫面上單獨成立，再進入下一步。

### 05 rotate_point_about_b

現在讓三角形 `ABP` 的副本做完全相同的旋轉。`A` 落到 `C`；同一個 `P` 的副本落到正方形外的新點 `E`。

動作目的：讓「再把整個三角形旋轉到 E」在穩定畫面上單獨成立，再進入下一步。

### 06 match_rotated_lengths

藍色的 `AP` 旋轉後就是藍色的 `CE`，所以兩段一樣長。

動作目的：讓「旋轉保留哪些資料」在穩定畫面上單獨成立，再進入下一步。

### 07 construct_rotated_diagonal

`BP` 轉到 `BE`，所以它們互相垂直，而且長度相等。三角形 `BPE` 是直角等腰三角形。

動作目的：讓「先作出旋轉後的新斜邊」在穩定畫面上單獨成立，再進入下一步。

### 08 measure_the_new_diagonal

由畢氏定理，

動作目的：讓「用等腰直角關係量出斜邊」在穩定畫面上單獨成立，再進入下一步。

### 09 match_condition_lengths

先把題目的式子移項：

動作目的：讓「把原條件中的長度搬到新圖」在穩定畫面上單獨成立，再進入下一步。

### 10 translate_the_condition

所以同一個條件變成

動作目的：讓「寫成新三角形的畢氏關係」在穩定畫面上單獨成立，再進入下一步。

### 11 earn_the_right_angle

先只看三角形 `CEP`。`CP` 的平方等於另外兩邊平方和。

動作目的：讓「逆畢氏定理落在哪一點」在穩定畫面上單獨成立，再進入下一步。

### 12 show_forty_five_and_ninety

再把黃色的直角等腰三角形 `BPE` 放回來。

動作目的：讓「先並列四十五度與九十度」在穩定畫面上單獨成立，再進入下一步。

### 13 assemble_preanswer_angles

旋轉又告訴我們 `\angle APB=\angle CEB`。畫面先停在最後一次加法；請在心裡完成它。

動作目的：讓「把兩角接成答案前的合角」在穩定畫面上單獨成立，再進入下一步。

### 14 reveal_the_angle

現在才揭示相加的結果。

動作目的：讓「揭示合角並送回原來的 P」在穩定畫面上單獨成立，再進入下一步。

### 15 name_quarter_turn_insight

關鍵不是先猜這個鈍角，而是先把係數二看成旋轉後的斜邊平方。

動作目的：讓「留下四分之一圈的關鍵提示」在穩定畫面上單獨成立，再進入下一步。

### 16 set_up_interior_vectors

再用另一套方法核對一次，而且這次不使用剛才的旋轉證明。

動作目的：讓「建立內點座標與兩支向量」在穩定畫面上單獨成立，再進入下一步。

### 17 derive_negative_dot_product

從 `P` 指向 `A`、`B` 的向量分別是 `(u-s,v)` 與 `(u,v)`。用上方的關係整理，內積是 `-sv`。

動作目的：讓「算出負內積並鎖定鈍角」在穩定畫面上單獨成立，再進入下一步。

### 18 verify_with_interior_vectors

行列式的絕對值是 `sv`。`-sv<0` 先證明夾角是鈍角；兩個絕對值相等，再說明正弦等於負餘弦。鈍角範圍內只有剛才的 `135` 度。

動作目的：讓「比較行列式後核對一百三十五度」在穩定畫面上單獨成立，再進入下一步。

### 19 return_to_original_square

最後回到同一個正方形與同一個內點 `P`。

動作目的：讓「回到原正方形並標回答案」在穩定畫面上單獨成立，再進入下一步。

### 20 summarize_quarter_turn_route

第一個畫面：正方形的直角讓 `ABP` 轉四分之一圈。

動作目的：讓「依序重播三個關鍵畫面」在穩定畫面上單獨成立，再進入下一步。

## Build constraints

- 只編輯 `lessons/tcfs_112_math_gifted/q11/`；渲染媒體寫入專屬 ignored build 目錄。
- 場景類別為 `CarloTcfs112MathQ11`，共 20 個 beat，全部 `loop=false`。
- 中文只使用 `label()`；`MathTex` 只放 ASCII 數學內容。
- 先做 Python compile/import 與低畫質 smoke，再以 `--quality h` 隔離渲染。
- 必須檢查 20 個 endpoint、完整每秒 sweep，以及 `test_two_valid_positions` 的條件移動、`rotate_point_about_b` 的旋轉、`translate_the_condition` 的式子替換、`assemble_preanswer_angles` 的答案前停點、`reveal_the_angle` 的答案揭示與向量核對的中間影格。
- lesson worker 停在 `draft_rendered`，不執行 `freeze-qa`，不建立 human-reviewed attestation，也不修改 collection state。
