# 第 3 題講者稿：六個面心圍出的八面體

預估時間：7 分鐘
解題來源：正哥愛數學
題目頁：https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/中一中資優班/114中一中資
公開解題影片：https://www.youtube.com/watch?v=MUhQmAz9OvE

## 01 place_face_centers｜先找到六個面心

先不要急著想體積。我們只看一個立方體。六個面可以先整理成三對相對的面，接著逐對放入面心。 [PAUSE] [NEXT]

## 02 place_opposite_side_centers｜先放側面的兩對中心

左右兩面是一對，前後兩面是一對。畫面先放入這四個側面中心；它們會形成中間的一圈。 [PAUSE] [NEXT]

## 03 complete_six_face_centers｜補上上下兩個中心

上下兩面是第三對。每一對各有兩個點，所以現在一共是六個面心。這六個點接下來都會保留在畫面上。 [PAUSE] [NEXT]

## 04 connect_octahedron｜先連中間四個點

現在把位在相鄰兩個面上的中心連起來。先只連中間四點，得到一個共同的底面輪廓。 [PAUSE] [NEXT]

## 05 connect_upper_and_lower_apices｜再連上下兩個頂點

從上方中心連到中間四點，再從下方中心連到同一圈四點。十二條候選邊現在全部可見。 [PAUSE] [NEXT]

## 06 name_regular_octahedron｜等邊證據落定後再命名

立方體可以旋轉，把任何一組相鄰的面帶到另一組，因此這十二條邊的長度相同。六個面心圍出的，正是一個正八面體。 [PAUSE] [NEXT]

## 07 establish_scale_invariance｜先讓內外立體同步縮放

如果整個立方體縮小，裡面的八面體也跟著一起縮小；如果放大，也會一起放大。

畫面回到原尺寸時，兩個立體的相對形狀完全沒有改變。 [PAUSE] [NEXT]

## 08 confirm_scale_invariance｜用體積因子確認比值不變

邊長乘上 (k) 時，兩個體積都乘上 (k^3)。相除以後，這個共同因子會消掉，所以體積比不受原來大小影響。

我們可以放心挑一個最好算的尺度：把立方體邊長取成 2。這樣從中心到任何一個面的距離都剛好是 1。 [PAUSE] [NEXT]

## 09 isolate_middle_square｜先只看中間一圈

整個八面體同時看，線很多。我們先把上下的線淡掉，只保留四個側面中心連成的藍色四邊形。

它在斜視圖裡看起來像菱形，但那只是投影。它究竟是什麼形狀？ [PAUSE] [NEXT]

## 10 turn_to_top_view｜換一個能回答問題的視角

我們不換點，只把視線慢慢轉到正上方。

現在外框是邊長 2 的正方形。四個藍點分別落在四邊中點；相鄰兩條藍邊形成直角，所以中間確實是一個正方形。

這次轉動不是裝飾，而是把斜視圖藏住的直角顯示出來。 [PAUSE] [NEXT]

## 11 measure_square_base｜先建立一個可量的直角三角形

挑左下角這一小塊直角三角形。兩條直角邊都是大正方形邊長的一半，因此都是 1。

藍色斜邊就是中間正方形的一邊。圖形與兩股長度先落定，下一步才開始計算。 [PAUSE] [NEXT]

## 12 derive_square_base_area｜從一條邊得到整個底面積

由畢氏定理，

\[
d^2=1^2+1^2=2,
\]

所以 (d=\sqrt2)。中間正方形的面積便是

\[
B=(\sqrt2)^2=2.
\]

[PAUSE] [NEXT]

## 13 calculate_one_pyramid｜先把上半部的底與高看清楚

回到斜視圖。先把下半部留在暗處，只看上方這一個正方錐。

它的底就是剛才量好的藍色正方形，底面積是 2。頂點位在上面的面心；到中間平面的高度，是立方體邊長的一半，也就是 1。

底面積 2 與高度 1 都已經可見。下一步才把它們放進正方錐體積公式。 [PAUSE] [NEXT]

## 14 calculate_upper_pyramid_volume｜逐項算出一半的體積

因此上半部體積是

\[
V_1=\frac13\times2\times1=\frac23.
\]

先把這個一半的結果停在這裡。 [PAUSE] [NEXT]

## 15 reflect_and_double｜鏡射落地後才乘二

沿著中間的藍色正方形鏡射。上方頂點落到下方頂點，底面完全不動，高度 1 也保持不變。

所以剛剛的正方錐會完整落到下半部，兩半體積相同。現在才可以乘上 2：

\[
a=2\times\frac23=\frac43.
\]

[PAUSE] [NEXT]

## 16 calculate_cube｜再算外面的立方體

八面體已經算完。現在把外框重新亮起來。

立方體邊長是 2，所以

\[
b=2^3=8.
\]

到這裡，(a) 和 (b) 都是在同一個尺度下算出的實際體積。 [PAUSE] [NEXT]

## 17 form_final_ratio｜先寫出要比較的比值

現在才寫出 (a/b)。兩個數值都還從原來的圖與公式保留著，下一步再把它們送進比值。 [PAUSE] [NEXT]

## 18 substitute_visible_volumes｜代入兩個已知體積並化簡

把兩個已知體積相除：

\[
\frac ab=\frac43\div8=\frac16.
\]

[PAUSE] [NEXT]

## 19 consolidate_volume_ratio｜回到六個面心與完整立體

因此，六個面心圍出的正八面體，體積正好是原立方體的六分之一。 [PAUSE]
