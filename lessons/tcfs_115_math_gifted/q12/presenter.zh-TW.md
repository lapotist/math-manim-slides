# 第壹部分第 12 題｜講者稿

解題來源：正哥愛數學
來源定位：115 學年度數學學科能力評量答案，第壹部分第 12 題，PDF 第 8 頁。
預計時間：約 13 分鐘。

## 01 build_equilateral｜先建立固定三角形

先只看固定資料。`ABC` 是邊長 4 的正三角形，三邊相等。

移動點和最小值都先不出現，讓這個參考圖形保持清楚。

[NEXT]

## 02 introduce_interior_point｜再放入 P 與三段距離

現在把內點 `P` 放進來，依序連上 `AP`、`BP`、`CP`。

題目要讓 `sqrt(2)AP+BP+CP` 最小。三種顏色正好對應三段距離。

先不要猜答案，只記住這三項都會跟著 `P` 改變。

[NEXT]

## 03 explore_p｜只移動 P 看三項拉扯

[LOOP]

當 `P` 靠近 `A`，`AP` 變短，但到 `B`、`C` 的距離一起變長。

靠近底邊或偏向 `B` 時，另外兩項又要付出代價。三段距離彼此拉扯，直接猜位置並不容易。

[NEXT]

## 04 pose_straightening｜先提出拉直問題

最短路徑常把幾段線首尾相接，再嘗試拉直。

眼前有三項。哪一項還不是一條可以直接搬進路徑的線段？

[PAUSE]

[NEXT]

## 05 isolate_weighted_term｜找出難接的第一項

`BP` 和 `CP` 本來就是線段。

第一項卻是 `sqrt(2)` 倍的 `AP`，它只有符號，還沒有一條等長的可見線段。

什麼幾何圖形的斜邊，會是直角邊的 `sqrt(2)` 倍？

[PAUSE]

[NEXT]

## 06 rotate_copy｜先完成九十度旋轉

以 `A` 為中心，把整個構形的一份複本順時針旋轉 90 度。

先看物件怎麼移動：`P` 到 `P'`，`C` 到 `C'`。等旋轉完全落定，再讀它保留了什麼。

[NEXT]

## 07 record_rotation_invariants｜讀出旋轉保留的資料

旋轉保持距離，所以 `AP'=AP`，而且 `C'P'=CP`。

同時，`AP` 與 `AP'` 的夾角正好是 90 度。

這三項資料一起把 `APP'` 準備成等腰直角三角形。

[NEXT]

## 08 earn_sqrt_two｜先畫出真正的斜邊

兩條直角邊 `AP`、`AP'` 等長，而且互相垂直。

把 `P` 和 `P'` 連起來，眼前這條 `PP'` 才是我們要找的實際線段。

[NEXT]

## 09 derive_weighted_segment｜用畢氏定理確認長度

由畢氏定理，`PP'^2=AP^2+AP'^2=2AP^2`。

長度取正值，所以 `PP'=sqrt(2)AP`。

題目最難處理的第一項，現在確實變成了斜邊 `PP'`。

[NEXT]

## 10 assemble_broken_path｜先接前兩段

把畫面整理一下。第一段從 `B` 到 `P`，第二段從 `P` 到 `P'`。

也就是先得到折線的前半段 `B-P-P'`。固定終點還沒有接上來。

[NEXT]

## 11 complete_broken_path｜接上 C' 並核對原式

最後接上 `P'C'`。旋轉保持長度，所以它就是原來的 `PC`。

因此原式正好等於折線 `B-P-P'-C'` 的總長。現在三項第一次有了共同的起點和終點。

[NEXT]

## 12 straighten_path｜先得到下界

固定起點 `B` 和終點 `C'` 後，任何折線都不會比直線 `BC'` 更短。

所以這個總和至少是 `BC'`。什麼時候等號成立？

[PAUSE]

[NEXT]

## 13 attain_straight_path｜再證明下界可以達到

把 `P`、`P'` 移到等號位置。此時 `B、P、P'、C'` 依序共線，三段不再轉彎。

而且這個 `P` 確實在原正三角形內，所以直線下界真的可以達到。

因此最小值就是 `BC'`。

[NEXT]

## 14 measure_bc_prime｜只留下固定端點

最小路徑已經確定，現在暫時移走動點構形，只量固定的 `BC'`。

旋轉後的 `C'` 與線段 `AC'` 保留下來；接著要先找 `AB` 和 `AC'` 的夾角。

[NEXT]

## 15 derive_endpoint_angle｜合併六十度與九十度

正三角形給 `angle BAC=60 degrees`，旋轉給 `angle CAC'=90 degrees`。

兩個角相接，所以 `angle BAC'=150 degrees`。

等價地，`AC'` 與 `AB` 的反向延長線夾 30 度。

[NEXT]

## 16 measure_thirty_sixty_triangle｜量出兩條直角邊

從 `C'` 向直線 `AB` 作垂線，垂足記作 `D`，而順序是 `B-A-D`。

在 30-60-90 三角形 `AC'D` 中，斜邊 `AC'=4`，所以 `C'D=2`、`AD=2sqrt(3)`。

因此 `BD=BA+AD=4+2sqrt(3)`。

[NEXT]

## 17 compute_minimum｜先算 BC' 的平方

現在在直角三角形 `BC'D` 中使用畢氏定理。

`BC'^2=(4+2sqrt(3))^2+2^2=32+16sqrt(3)`。

先停在平方值，下一步再辨認它是哪一個正根。

[NEXT]

## 18 recognize_positive_radical｜辨認正根得到 p

把 `(2sqrt(6)+2sqrt(2))^2` 展開，正好也是 `32+16sqrt(3)`。

因為 `BC'` 是長度，取正值，得到 `p=2sqrt(6)+2sqrt(2)`。

最小值已經求出；接著要找等號發生時的 `AP=q`。

[NEXT]

## 19 pin_down_p｜保留等號直線並逆旋轉

保留等號時的直線 `ell=BC'`。等號要求 `P` 在 `ell` 上，也要求旋轉後的 `P'` 在 `ell` 上。

把整條 `ell` 逆時針轉回 90 度。旋轉前的 `P` 也必須落在這條轉回來的直線上。

[NEXT]

## 20 intersect_equality_lines｜兩條限制唯一定位 P

現在 `P` 同時要在原直線和逆旋轉直線上，所以只能是兩線的唯一交點。

交點精確落在正三角形的對稱軸上。這是等號條件推出的結果，不是看圖猜到的。

[NEXT]

## 21 read_equality_angles｜先讀出四十五度

回到等腰直角三角形 `APP'`。它在 `P` 與 `P'` 的底角都是 45 度。

先把這個 45 度留在畫面上，下一頁再把它轉到原三角形裡。

[NEXT]

## 22 derive_straight_line_angle｜利用共線轉回原圖

等號時 `B、P、P'` 共線，而且 `PB` 與 `PP'` 方向相反。

因此 `angle APB=180-45=135 degrees`。

把對稱軸延長到 `BC`，交點記作 `E`；它同時是底邊中點。

[NEXT]

## 23 compute_ap｜先建立 BPE 的直角與四十五度

`AE` 垂直 `BC`，而 `PE` 與 `PA` 方向相反。

所以三角形 `BPE` 在 `E` 為直角，在 `P` 為 45 度。這是一個等腰直角三角形。

[NEXT]

## 24 read_half_base｜由底邊中點得到 PE

`E` 是底邊中點，因此 `BE=BC/2=2`。

等腰直角三角形的兩股相等，所以 `PE=BE=2`。

[NEXT]

## 25 calculate_altitude_and_ap｜最後求出 q

正三角形的高 `AE=sqrt(4^2-2^2)=2sqrt(3)`。

`P` 位在 `A` 與 `E` 之間，所以 `q=AP=AE-PE=2sqrt(3)-2`。

[NEXT]

## 26 consolidate｜旋轉、拉直、再回到答案

最後把路徑連起來。

九十度旋轉把 `sqrt(2)AP` 變成 `PP'`；三段接成 `B-P-P'-C'`；拉直後得到最短的 `BC'`。

同一個等號條件又唯一定位 `P`，讓我們算出 `AP`。

因此 `(p,q)=(2sqrt(6)+2sqrt(2), 2sqrt(3)-2)`。

[PAUSE]
