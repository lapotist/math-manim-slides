# ROC 113 Proof Question 1 storyboard

## Teaching intent

本課要處理三個逐步擴張的問題：來源圖中的五步閉合角、七步閉合角，以及奇數
步的乘積猜想。教學順序必須從真正的等步長移動開始；不先顯示
\(36^\circ\)、\(180^\circ/7\) 或 \(mn=180\)。觀眾先看同一個點走完整條
之字路徑，再從相鄰兩步等長所形成的等腰三角形，看見底角依序為
\(\theta,2\theta,3\theta,\ldots\)。

五步時，最外三角形的角是 \(\theta,2\theta,2\theta\)，所以
\(5\theta=180^\circ\)。七步時，最外三角形的角是
\(\theta,3\theta,3\theta\)，所以 \(7\theta=180^\circ\)。一般奇數
\(n=2h+1\) 時，第 \(h\) 層底角是 \(h\theta\)，所以最外三角形給出
\((2h+1)\theta=n\theta=180^\circ\)。若 \(\theta=m^\circ\)，則
\(mn=180\)。

這個一般化必須和來源圖的構形綁在一起：除了起終點 \(O\) 之外，所有落點都
留在從 \(O\) 出發的兩條指定射線上，而且討論的是第一次回到 \(O\) 的交替
之字路徑。原題文字允許完整直線上的任意方向；若不加這個構形限制，會有其他
閉合角。因此本課不得把 \(mn=180\) 稱為完整直線問題的普遍定理。

預估 11 分鐘。二十三個 beat 全部不循環；每一個停點都落在靜止且可朗讀的
構圖。`mark_scope_boundary` 與 `verify_full_line_counterexample` 只用一個反例標示適用範圍，隨即在 `consolidate_scoped_invariant` 回到主線，
避免範圍校正淹沒原本的等腰三角形發現過程。

## Source and provenance

- 典藏頁面：`https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87%E5%84%AA%E7%8F%AD/113%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87`。
- 題目來源：`113中一中資優班解析.pdf`，Drive ID
  `1QQhuf8PqZMVyCdF9s9LHR8Q3y8RmAk3M`，SHA-256
  `c4c5c0d834f7ef8f423d21265c6a69cadcaedfc5f2de290a79d0bc61b3844273`，
  第 14 到 16 頁計算證明第 1 題。
- 解題來源：正哥愛數學公開影片
  `https://www.youtube.com/watch?v=rw7Z1rw7gYA`，影片標題
  `113中一中資優班計算證明1`，存取狀態 `public_stream`，精確定位
  `00:00-04:34`。
- 來源以五步的 \(\theta+2\theta+2\theta=180^\circ\)、七步的
  \(\theta+3\theta+3\theta=180^\circ\)，以及一般式
  \(m+2((n-1)m/2)=180^\circ\) 解題。本課保留這個可驗證的角度骨架，
  但以原創射線、點、等步長線段、角弧與遞推動畫重建。
- 不使用 PDF 或影片畫面、手寫字、聲音或原文。專案原創課程內容採 CC BY 4.0，程式碼採 MIT；來源素材不納入本專案授權。

## Scope audit

集合中的 `solution_scope_note` 是本課的硬性數學邊界：

> The source's mn=180 generalization follows the displayed same-ray zigzag
> family. If signed positions on the full lines are allowed without that
> configuration restriction, additional closure angles exist.

在課內使用的精確中文定義是：

「同射線首次閉合之字構形」指 \(P_0=P_n=O\)，\(P_1,\ldots,P_{n-1}\)
交替落在從 \(O\) 出發的兩條指定射線上、每個相鄰距離皆相等，而且在第
\(n\) 步之前不回到 \(O\)。

這句話必須在 `meet_two_rays`、`name_general_scope`、`state_scoped_product`、
`restate_scoped_results` 可見，講者稿也必須同步朗讀。顯示完整直線反例後，
必須明說它不屬於這個定義。

## Independent mathematics check

令兩條指定射線的夾角為 \(0<\theta<\pi/2\)，步長標準化為 1。對來源圖中的
同射線構形，設

\[
r_k=\frac{\sin(k\theta)}{\sin\theta},\qquad
P_k=\begin{cases}
(r_k,0),&k\text{ 為奇數},\\
r_k(\cos\theta,\sin\theta),&k\text{ 為偶數}.
\end{cases}
\]

恆等式

\[
r_k^2+r_{k-1}^2-2r_kr_{k-1}\cos\theta=1
\]

證明每一個相鄰距離都是 1。若 \(\theta=\pi/n\)，則
\(r_n=0\)，而 \(1\le k<n\) 時 \(r_k>0\)，所以所有中間點都在指定射線
上並於第 \(n\) 步首次回到 \(O\)。

幾何上，令 \(\alpha_j\) 為向外第 \(j\) 個等腰三角形的底角。第一個三角形
有 \(\alpha_1=\theta\)。同射線上的點序與平角，加上下一對相等步長，給出
\(\alpha_{j+1}=\alpha_j+\theta\)，所以 \(\alpha_j=j\theta\)。若
\(n=2h+1\)，最外三角形的三角為 \(\theta,h\theta,h\theta\)，故

\[
\theta+2h\theta=(2h+1)\theta=n\theta=180^\circ.
\]

因此 \(n=5\) 時 \(\theta=36^\circ\)；\(n=7\) 時
\(\theta=180^\circ/7\)；若 \(\theta=m^\circ\)，則限定構形內
\(mn=180\)。

完整直線反例取 \(n=5\)、\(\theta=72^\circ=2\pi/5\)。同一座標式仍有
\(r_5=0\) 且每步長 1，但 \(r_3<0,r_4<0\)，所以第三、第四個落點跑到
相反延長線。這條路徑閉合而 \(mn=5\cdot72=360\)。它證明拿掉同射線限制
後 \(mn\) 不是定值，也說明來源結論為何只能以限定圖族呈現。

`deck.py` 匯入時使用 `Fraction` 精確核對五步、七步及一般奇數的角度和與
乘積；另以座標檢查同射線家族的正半徑、單位步長、首次閉合與完整直線反例的
負半徑。這些檢查不依賴動畫畫面座標。

## Visual grammar

- 中性白灰色固定代表兩條射線與最外參考三角形；藍色代表每一段相同的步長。
- 黃色代表正在移動的機器人與目前被追蹤的角；綠色代表合法的同射線範圍與
  限定結論。
- 紫色用於逐層長出的等腰三角形；珊瑚色只用於完整直線反例與範圍警告。
- 同一條路徑必須由同一個黃色點依序走出，不能把五個或七個不同點同時淡入
  當作移動。
- 等角必須先由兩條可見的等長邊產生，再顯示角標；長公式只能在動態幾何停止
  後出現。
- 一般化時保留內部路徑作低透明度背景，隔離最外三角形後才建立
  \(n\theta=180^\circ\)。
- `verify_full_line_counterexample` 的負半徑點必須畫在 \(O\) 背後的延長線上，並以珊瑚色標成
  「範圍外」；不得把它和前面的綠色合法家族混為一圖。
- 所有中文使用 `label()`；`MathTex` 只放 ASCII 字元與數學符號。

## Beat map

### 01 meet_two_rays

只畫兩條指定射線、夾角與步長尺，先固定同射線的構形範圍。

### 02 walk_five_steps

黃色點先走前兩個等步長，步數與落點同時落定。

### 03 finish_five_step_walk

再走第三到第五步並首次回到 \(O\)，停在只問 \(\theta\) 的完整路徑。

### 04 seed_equal_angles

隔離第一個等腰三角形，先把已知角複製到對應底角。

### 05 mark_first_equal_sides

補上第一組等長記號，讓等角的理由在圖上保持可查。

### 06 propagate_five_step_angles

沿出發端的相鄰等腰三角形傳遞角度，得到一側的 \(2\theta\)。

### 07 complete_five_step_propagation

從閉合端反向完成同一傳遞，停在外三角形的 \(\theta,2\theta,2\theta\)。

### 08 reveal_thirty_six

由外三角形建立 \(\theta+2\theta+2\theta=180^\circ\)，先化成 \(5\theta=180^\circ\)。

### 09 solve_five_step_angle

最後才解出並揭示 \(\theta=36^\circ\)。

### 10 walk_seven_steps

清除五步圖，使用同一規則先走七步構形的前兩步。同射線範圍條保留。

### 11 continue_seven_step_walk

走第三到第五步，停在尚未閉合的中間構形。

### 12 finish_seven_step_walk

走完第六、七步並回到 \(O\)，再顯示七段等長記號。

### 13 grow_three_layers

從出發端依序建立第一、第二層，停在 \(\theta,2\theta\) 的具體增長。

### 14 complete_three_layer_growth

完成第三層並從終點反向傳遞，停在外三角形的 \(\theta,3\theta,3\theta\)。

### 15 reveal_seven_step_angle

由可見三角建立 \(\theta+3\theta+3\theta=180^\circ\)，先得到 \(7\theta=180^\circ\)。

### 16 solve_seven_step_angle

將七步關係解成 \(\theta=180^\circ/7\)。

### 17 name_general_scope

以九步圖作一般奇數的代表，明示 \(n=2h+1\)、\(h=(n-1)/2\)，並再次完整
顯示「同射線、首次閉合」範圍。

### 18 build_angle_recurrence

先建立 \(\alpha_1=\theta\) 與逐層增加 \(\theta\) 的遞迴。

### 19 propagate_general_angles

先讓代表三角形走過第二、第三層，具體呈現逐層增加 \(\theta\)。

### 20 complete_general_propagation

走到代表圖最外層，才一般化為第 \(h\) 層的 \(h\theta\)。

### 21 close_outer_triangle

淡化內部路徑，只保留最外三角形及三個已知角。

### 22 state_scoped_product

由外三角形逐行建立 \(n\theta=180^\circ\) 與限定構形內的 \(mn=180\)。

### 23 mark_scope_boundary

切換到兩條完整直線，先明示這已越出同射線構形的適用範圍。

### 24 verify_full_line_counterexample

顯示負半徑落點與 \(n=5,\theta=72^\circ\) 的閉合例，核對其乘積為 360。

### 25 consolidate_scoped_invariant

回到同射線九步圖與原先的限定敘述，重新取得主線脈絡。

### 26 restate_scoped_results

依序重述五步、七步與一般奇數的結果，最下方永久保留限定範圍。

## Build constraints

- 只可在 `lessons/tcfs_113_math_gifted/p2q01/` 編輯來源檔；媒體輸出使用專屬
  ignored `build/media/carlo_tcfs_113_math_gifted_p2q01`。
- 二十三個 beat、TOML、講者稿與 Slides manifest 必須完全同序，全部
  `loop=false`；講者稿必須有 22 個 `[NEXT]`、0 個 `[LOOP]`。
- 匯入期必須檢查角度和、同射線正半徑、每步等長、首次閉合，以及完整直線
  反例的負半徑與乘積 360。
- 必須以 1920x1080 原尺寸檢查五步移動、第一個等腰三角形、五步外三角形、
  七步三層角、一般遞推、限定乘積、反例與最終範圍；另以固定頻率加密檢查
  所有移動與三角形轉場。
