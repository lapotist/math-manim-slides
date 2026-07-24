# 第二部分第 2 題｜講者稿

解題來源：正哥愛數學
來源定位：115 學年度數學學科能力評量答案，第二部分第 2 題，PDF 第 10 頁。
預計時間：約 10 分鐘。

## 01 build_triangle｜先保留最簡單的物件

先看一個一般三角形 `ABC`。

我們最後想把從 `A` 到對邊的一條特殊線，寫成三邊上幾段長度的關係。

現在先不畫圓，也不顯示公式，只保留這個基本物件。

[NEXT]

## 02 place_angle_bisector｜AD 的第一個身分

從 `A` 作 `angle BAC` 的角平分線，交 `BC` 於 `D`。

所以 `angle BAD=angle DAC`。

藍色線段 `AD` 就是題目要研究的長度。眼前只有一個等角條件，還不足以直接得到長度公式。

[NEXT]

## 03 add_circle_and_e｜讓同弧角進場

作三角形 `ABC` 的外接圓。

再沿著 `AD` 的同一方向延長，第二次交圓於 `E`，並連接 `CE`。

現在有兩條共線關係：`A、D、E` 共線，`B、D、C` 共線。

更重要的是，圓上的角可以由同一段弧鎖定。

[NEXT]

## 04 pose_hidden_similarity｜三個方向不同的三角形

依序看 `ABD`、`AEC` 與 `CED`。

它們大小不同、朝向也不同，但題目提示這三個三角形應該有相同形狀。

我們不先宣告相似，先逐組找兩對確定相等的角。

[PAUSE]

[NEXT]

## 05 prove_first_similarity｜ABD 與 AEC

先比較 `ABD` 和 `AEC`。

因為 `A、D、E` 共線，加上 `AD` 是角平分線，`angle BAD=angle CAE`。

接著，`angle ABD` 就是原三角形的 `angle ABC`。`angle ABC` 與 `angle AEC` 都對著同一段弧 `AC`，所以兩角相等。

有兩組角分別相等，因此 `triangle ABD` 相似於 `triangle AEC`。

頂點依序配對為 `A` 對 `A`、`B` 對 `E`、`D` 對 `C`。

[NEXT]

## 06 prove_second_similarity｜ABD 與 CED

再比較 `ABD` 和 `CED`。

`angle BAD` 也就是 `angle BAE`。它與 `angle BCE` 都對著弧 `BE`，所以相等。

另外，直線 `AE` 與 `BC` 在 `D` 相交，`angle ADB` 與 `angle CDE` 是對頂角。

因此 `triangle ABD` 也相似於 `triangle CED`。

這次配對是 `A` 對 `C`、`B` 對 `E`、`D` 對 `D`。

[NEXT]

## 07 align_three_triangles｜把相同形狀排在一起

把三個三角形從原圖各複製一份，旋轉並縮放到相同方向。

同色角一一重合，對應邊也排到相同位置。

因為 `AEC` 和 `CED` 都與 `ABD` 相似，所以三者形成完整的相似鏈。

接下來，我們不需要所有邊的比例，只挑能產生目標中兩個乘積的兩組。

[NEXT]

## 08 build_first_product｜第一組相似交出 AB 乘 AC

從 `ABD` 相似 `AEC`，依照剛才的頂點配對，得到

`AB/AE=AD/AC`。

交叉相乘後是 `AB*AC=AD*AE`。

左邊已經出現目標根號中的 `AB*AC`；右邊則把它連到角平分線 `AD`。

[NEXT]

## 09 build_second_product｜第二組相似交出 BD 乘 DC

從 `ABD` 相似 `CED`，得到

`AD/CD=BD/DE`。

交叉相乘後是 `AD*DE=BD*DC`。

這個關係也可以用交弦理解，但我們現在是直接使用第 (1) 小題已經證明的相似三角形。

[NEXT]

## 10 split_ae｜把兩張乘積關係接起來

回到共線的 `A、D、E`。

整段 `AE` 正好由 `AD` 加上 `DE` 組成。

所以第一個關係變成

`AB*AC=AD(AD+DE)=AD^2+AD*DE`。

最後一項，正好可以用第二個相似關係替換。

[NEXT]

## 11 isolate_ad_square｜留下角平分線的平方

把 `AD*DE` 換成 `BD*DC`。

得到 `AB*AC=AD^2+BD*DC`。

將 `BD*DC` 移到另一側，便有

`AD^2=AB*AC-BD*DC`。

兩組看似分開的相似，現在正好在這一行接起來。

[NEXT]

## 12 take_positive_root｜長度只取正根

最後從平方回到線段長度。

`AD` 是一條實際線段，所以 `AD>0`。因此取平方根時保留正根。

得到 `AD=sqrt(AB*AC-BD*DC)`。

根號內必為非負，也不是額外猜測；它本來就等於 `AD^2`。

[NEXT]

## 13 consolidate｜兩組相似，各提供一塊

最後回看證明的結構。

角平分線與同弧角證出第一組相似，給我們 `AB*AC=AD*AE`。

同弧角與對頂角證出第二組相似，給我們 `AD*DE=BD*DC`。

再沿著 `AE=AD+DE` 展開，兩塊關係恰好拼成 `AD^2`。

所以 `AD=sqrt(AB*AC-BD*DC)`。

[PAUSE]
