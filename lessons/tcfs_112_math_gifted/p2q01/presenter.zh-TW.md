# 計算證明第 1 題講者稿：面積如何跟著邊長變化

預估時間：12 分鐘

解題來源：正哥愛數學

題目定位：`112中一中資優班解析.pdf` 第 14–17 頁；公開解題影片 `JisNVawr1NM`，`00:00–07:19.25`。

## 01 introduce_area_notation｜先把面積符號放回三角形

`T(a,b,c)` 表示三邊長是 `a、b、c` 的三角形。

`Delta(a,b,c)` 不是新的邊長；它指的是這個三角形內部的面積。 [PAUSE] [NEXT]

## 02 meet_area_notation｜停在三四五三角形的面積問題

第一小題給我們三邊 `3、4、5`。畫面上這塊區域到底多大？先不急著代公式。 [PAUSE] [NEXT]

## 03 derive_three_four_five_area｜先確認直角並寫出面積式

`3` 的平方加 `4` 的平方，剛好是 `5` 的平方。所以這裡是直角。

現在底 `4` 和高 `3` 已經在圖上垂直。面積是二分之一乘底乘高：

\[
\frac12\cdot4\cdot3.
\] [PAUSE] [NEXT]

## 04 earn_three_four_five｜揭示第一個面積答案

所以第一個答案是 `6`。 [PAUSE] [NEXT]

## 05 build_doubled_triangle｜先把三邊與高都放大兩倍

現在不限定 `3、4、5`。左邊是任意三角形，底是 `b`，對應高是 `h`。

右邊的三邊全部乘二。它和原圖相似，所以底變成 `2b`，高也變成 `2h`。 [PAUSE] [NEXT]

## 06 double_one_triangle｜比較兩個方向的倍率並保留問題

注意有兩個獨立的方向同時放大。那麼面積是原來的多少倍？ [PAUSE] [NEXT]

## 07 earn_scale_factor｜面積會收到兩個倍率

放大後的面積是

\[
\frac12(2b)(2h).
\]

底帶來一個 `2`，高又帶來一個 `2`。合起來就是 `4` 倍的 `bh/2`。

因此

\[
\Delta(2a,2b,2c)=4\Delta(a,b,c),
\]

第二個答案 `k=4`。 [PAUSE] [NEXT]

## 08 introduce_medians｜三條中線是下一個三角形的邊

接下來這個三角形故意畫得不對稱，免得我們把偶然的圖形當成證明。

每一條中線，都是從頂點連到對邊中點。我們把三條長度記成 `l_a、l_b、l_c`。

題目要用這三個長度再組一個三角形。它的面積和原來有什麼穩定關係？ [PAUSE] [NEXT]

## 09 derive_one_third_centroid_area｜先證明重心三角形占三分之一

三條中線交在重心 `G`。

先只看底邊 `AB`。重心把中線 `CM_c` 分成 `2:1`，所以 `G` 到 `AB` 的垂直距離，是 `C` 到 `AB` 的三分之一。

`AGB` 和原三角形共用底 `AB`，高是三分之一，因此面積是 `K/3`。 [PAUSE] [NEXT]

## 10 split_six_equal_wedges｜再把三條中線分成六個等面積塊

`M_c` 又把 `AB` 平分；`AGM_c` 和 `BGM_c` 共高、底相等，所以各是 `K/6`。對另外兩邊循環同一個論證，才得到六塊都等於 `K/6`。

這個三分之一，等一下會搬到右邊的新三角形。 [PAUSE] [NEXT]

## 11 start_centroid_vector_chain｜先畫三支重心向量與第一段平移

從重心 `G` 分別指向 `A、B、C`。這三支箭頭的和是零。

先不旋轉、不伸縮，只把第一支箭頭平移到右邊；它的方向與長度都保留。 [PAUSE] [NEXT]

## 12 translate_centroid_vectors｜閉合向量三角形並核對面積

再依序接上另外兩支箭頭。因為三支向量的和是零，最後一支正好回到起點，形成一個三角形。

為什麼面積仍是 `K/3`？取 `GA` 當底；平移 `GB` 不改變它對 `GA` 的垂直分量。兩個 `h_\perp` 等長，所以閉合三角形和左邊 `AGB` 同底、同高。

因此這個閉合三角形的面積是 `K/3`。不過它的三邊還是 `GA、GB、GC`，不是完整中線。 [PAUSE] [NEXT]

## 13 scale_centroid_triangle_to_medians｜把重心向量放大成完整中線

重心把每條中線分成 `2:1`。從頂點到重心是中線的 `2/3`，所以完整中線是 `GA、GB、GC` 的 `3/2` 倍。

把右邊三邊一起放大 `3/2`，它們就變成 `l_a、l_b、l_c`。面積因此要乘上 `3/2` 的平方： [PAUSE] [NEXT]

## 14 earn_median_area_factor｜平方倍率得到四分之三規則

\[
\frac K3\left(\frac32\right)^2=\frac34K.
\]

每做一次「用中線當新邊」，面積就變成原來的四分之三。 [PAUSE] [NEXT]

## 15 set_up_first_median_step｜先放出十六乘四分之三的問號

題目的起始面積是 `16`。

第一次把三條中線拿來當新三邊，面積乘 `3/4`： [PAUSE] [NEXT]

## 16 apply_first_median_step｜算出第一次中線面積十二

\[
16\cdot\frac34=12.
\]

現在畫面上的 `12` 是第一個中線三角形，還不是題目問的第二次結果。 [PAUSE] [NEXT]

## 17 hold_second_median_step｜停在十二乘四分之三

現在對面積 `12` 的三角形，再取一次中線。規則沒有變，所以又乘 `3/4`。

請先看著問號，把最後一步算完。 [PAUSE] [NEXT]

## 18 reveal_second_median_step｜再揭示第二次面積九

\[
12\cdot\frac34=9.
\]

第三個答案是 `9`。 [PAUSE] [NEXT]

## 19 construct_side_altitude_pair｜先作出邊 a 與對應高

最後一小題改用三條高當新邊。先只看原三角形的邊 `a`。

從對面頂點垂直落到 `a`，這一段是 `h_a`。如果原面積記成 `K`，那麼 [PAUSE] [NEXT]

## 20 introduce_altitude_triangle｜補齊邊名並寫出面積配對

\[
K=\frac12a h_a.
\]

對 `b` 和 `c` 也有完全同樣的配對。 [PAUSE] [NEXT]

## 21 construct_second_altitude｜把原高搬成新三角形的底

先把左邊那一條 `h_a` 原長搬到右邊，作為新三角形的底。右邊三邊長是原圖的 `h_a、h_b、h_c`。

右邊又有自己的高。對應邊 `h_a` 的高記成 `h'_a`。 [PAUSE] [NEXT]

## 22 compare_two_area_units｜標出兩個面積並提出比例問題

題目告訴我們，左邊原面積 `K=45`，右邊面積 `H=30`。

我們要用 `h'_a、h'_b、h'_c` 再組一個三角形。先別猜它的面積；先找新高和原邊的比例。 [PAUSE] [NEXT]

## 23 derive_one_second_altitude｜先由兩個面積式求出 h'a

左邊面積式是 `K=a h_a/2`。右邊把 `h_a` 當底，對應高是 `h'_a`，所以 `H=h_a h'_a/2`。

兩式相除，共用的 `h_a` 與二分之一同時消去：

\[
\frac{h'_a}{a}=\frac HK=\frac{30}{45}=\frac23.
\] [PAUSE] [NEXT]

## 24 derive_second_altitudes｜循環得到另外兩條第二高

循環更換字母，還有 `h'_b=2b/3`、`h'_c=2c/3`。新三角形的三邊，全部是原三邊的 `2/3`。 [PAUSE] [NEXT]

## 25 build_second_altitude_similarity｜把第二高三角形縮放到原圖旁

現在左右三對邊已經同色對齊。第二高邊三角形與原三角形相似，長度比是 `2/3`。

不要把面積也直接乘 `2/3`。底與高都縮成 `2/3`，所以面積要乘 [PAUSE] [NEXT]

## 26 hold_altitude_area_preanswer｜停在四十五乘比例平方

\[
\left(\frac23\right)^2.
\]

原面積是 `45`。畫面現在停在 `45(2/3)^2=?`。 [PAUSE] [NEXT]

## 27 reveal_altitude_area｜最後才把縮放面積算完

二分之三的平方是九分之四。

\[
45\cdot\frac49=20.
\]

所以以 `h'_a、h'_b、h'_c` 為三邊的三角形，面積是 `20`。這是第四個答案。 [PAUSE] [NEXT]

## 28 collect_four_area_results｜先收集四個小題答案

第一小題從 `3-4-5` 直角三角形得到 `6`。

第二小題看到長度乘二，面積乘四，所以 `k=4`。

第三小題的中線操作每次乘 `3/4`，兩次後得到 `9`。

第四小題先從兩個面積式得邊比 `2/3`，平方後得到 `20`。 [PAUSE] [NEXT]

## 29 consolidate_four_results｜用長度比平方收束四題

四個答案是

\[
(6,4,9,20).
\]

真正需要記住的不是四個零散公式，而是：先找長度比，再把它平方成面積比。 [PAUSE]
