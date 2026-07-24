# Q12 Storyboard: Rotate a Weighted Distance into One Path

目標長度：約 11 分鐘。讓內點 `P` 先移動，觀眾感受三段距離此消彼長；接著只處理最難接入路徑的 `sqrt(2)AP`。將 `P` 繞 `A` 旋轉 90 度後，這個加權長度成為真正線段 `PP'`，三項便能拉直成 `BC'`。先求最小值，再由等號條件精確定位 `P` 並求 `AP`。

## Visual grammar

- 原正三角形與固定點使用中性灰；`P` 與 `AP` 使用藍色，`BP` 使用黃色，`CP` 使用綠色。
- 旋轉後的 `P'、C'` 與對應線段使用洋紅色；同一線段旋轉前後保持色彩連續。
- 三項長度先以畫面中的線段表現，符號只在對應線段可見後加入。
- 直線化時保留原折線淡影，避免觀眾把不等式誤認為任意重排。
- 全部幾何由專案重畫；不使用來源解答圖或其標註。

## Beat plan

## 01 build_equilateral (0:45, loop=false)

- Settled visual: 從邊長 4 的底邊 `BC` 建立正三角形 `ABC`，標出三邊相等。
- Introduce: 一個藍色內點 `P` 落在非特殊位置，依序連接 `AP,BP,CP`。
- Constraint: 只顯示目標 `sqrt(2)AP+BP+CP`，不顯示答案或旋轉提示。
- Boundary: 三段距離和目標式的顏色一一對應。

## 02 explore_p (0:55, loop=true)

- Loop states: `P` 依序移到靠近 `A`、靠近底邊但不在邊上、偏向 `B` 的三個內部位置，再回到初始點。
- Updaters: `AP,BP,CP` 與三段長度條同步變化；不留下軌跡，也不顯示數值最小點。
- Observation: 一段縮短時，另外兩段往往變長，直接逐項猜測不容易。
- Loop boundary: 所有點、線與長度條精確回到初始狀態。

## 03 pose_straightening (0:45, loop=false)

- Freeze: `P` 停在一般位置，三段長度條移成可首尾相接的折線位置，但 `sqrt(2)AP` 仍只有符號、沒有一條可搬的實際線段。
- Prompt: 「`BP` 和 `CP` 本來就是線段；要把三項接成一條路，怎樣把 `sqrt(2)AP` 也變成線段？」
- Pause: 在 `sqrt(2)` 周圍留出 90 度轉角形狀的空位。
- Boundary: 問題聚焦在第一項，不同時處理其餘細節。

## 04 rotate_copy (0:55, loop=false)

- Animation: 以 `A` 為中心，將三角形與 `P` 的一份複本順時針旋轉 90 度；`P` 到 `P'`，`C` 到 `C'`，未使用的 `B'` 淡化。
- Preserved lengths: 旋轉箭頭落定後才標出 `AP'=AP`、`C'P'=CP`。
- Angle: `angle PAP'=90 degrees` 由旋轉弧直接得到。
- Boundary: 原圖與旋轉副本同時可見，對應物件可追蹤。

## 05 earn_sqrt_two (0:50, loop=false)

- Highlight: 三角形 `APP'`，兩腰 `AP=AP'` 且夾角 90 度。
- Construction: 兩條等長直角邊先顯示，再畫斜邊 `PP'`。
- Algebra after geometry: 由畢氏定理 `PP'^2=AP^2+AP'^2=2AP^2`，因長度為正，得到 `PP'=sqrt(2)AP`。
- Transform: 目標式中的藍色 `sqrt(2)AP` 由 `PP'` 的複本取代。
- Boundary: 加權係數已被一條實際線段解釋。

## 06 assemble_broken_path (0:50, loop=false)

- Object continuity: `BP` 保持原位；`sqrt(2)AP` 轉為 `PP'`；`CP` 的複本旋轉為 `P'C'`。
- Equation: `sqrt(2)AP+BP+CP = BP+PP'+P'C'` 一項一項建立。
- Visual: 亮色折線依順序從 `B` 經 `P`、`P'` 到 `C'`，每項與式子同色。
- Boundary: 三項第一次成為有固定起終點的一條完整路徑。

## 07 straighten_path (0:55, loop=false)

- Animation: 保留折線淡影，畫出端點間直線 `BC'`；以三角不等式顯示折線長度至少為 `BC'`。
- Equality condition: 移動到精確等號構形，使 `B,P,P',C'` 依序共線；此時三段無折角地鋪滿 `BC'`。
- Attainability: 明確顯示得到的 `P` 位於原三角形內，故下界確實可以達到，不只是理論下界。
- Boundary: `p=BC'`，但根式值尚未計算。

## 08 measure_bc_prime (0:55, loop=false)

- Geometry: 由旋轉得 `angle CAC'=90 degrees`，原正三角形給 `angle BAC=60 degrees`，所以較小的 `angle BAC'=150 degrees`。
- Construction: 從 `C'` 向直線 `AB` 作垂線，垂足 `D` 落在 `A` 的外側延長線。
- Special triangle: `angle C'AD=30 degrees`、`AC'=4`，逐步得到 `C'D=2`、`AD=2sqrt(3)`。
- Base: 因 `B-A-D` 共線且 `A` 在中間，`BD=BA+AD=4+2sqrt(3)`。
- Boundary: 直角三角形 `BC'D` 的兩股已知。

## 09 compute_minimum (0:50, loop=false)

- Pythagorean build: 從 `BD`、`C'D` 複製長度進入 `BC'^2=(4+2sqrt(3))^2+2^2`。
- Expand slowly: `BC'^2=32+16sqrt(3)`。
- Radical recognition: 將 `(2sqrt(6)+2sqrt(2))^2` 展開核對同一數值，再取正長度。
- Result: `p=BC'=2sqrt(6)+2sqrt(2)`。
- Boundary: 最小值留在一側，接著另外追問等號時的 `AP=q`。

## 10 pin_down_p (0:55, loop=false)

- Retain equality line: 將 `ell=BC'` 保留，並標明等號要求 `P in ell`、`P'=R(P) in ell`，其中 `R` 是順時針 90 度旋轉。
- Inverse construction: 把直線 `ell` 的複本繞 `A` 逆時針旋轉 90 度。因 `P' in ell`，原點 `P` 必在這條逆旋轉直線上。
- Intersection: 兩條線唯一交點就是 `P`；交點精確落在正三角形從 `A` 到 `BC` 的對稱軸上。
- Rigor: 這一步取代來源中未證明的「最小點必在對稱軸」斷言。
- Boundary: `P` 的位置由兩個等號限制決定，而非從外觀猜測。

## 11 read_equality_angles (0:45, loop=false)

- Highlight: 等腰直角三角形 `APP'` 的底角均為 45 度，因此 `angle APP'=45 degrees`。
- Straight line: 因 `B-P-P'` 共線且 `PB` 與 `PP'` 方向相反，得到 `angle APB=180-45=135 degrees`。
- Axis: 由上一 beat 的精確交點，畫出 `A-P-E` 對稱軸，`E` 是 `BC` 中點。
- Boundary: 求 `AP` 所需的 45 度與中點長度均已可見。

## 12 compute_ap (0:55, loop=false)

- Drop/perpendicular: `AE perpendicular BC`，所以三角形 `BPE` 在 `E` 為直角；`PE` 與 `PA` 反向，故 `angle BPE=45 degrees`。
- Isosceles right triangle: `BE=BC/2=2`，因此 `PE=2`。
- Equilateral altitude: `AE=sqrt(4^2-2^2)=2sqrt(3)`，由可見的半邊與斜邊建立。
- Result: `q=AP=AE-PE=2sqrt(3)-2`。
- Boundary: `p` 與 `q` 並列，但答案框仍待最後回顧後出現。

## 13 consolidate (0:55, loop=false)

- Recap: 90 度旋轉把 `sqrt(2)AP` 變成 `PP'`；三段成為 `B-P-P'-C'`；拉直後得到最短 `BC'`。
- Recap equality: 同一條直線與它的逆旋轉線鎖定 `P`，再由 45 度直角三角形算出 `AP`。
- Final answer: `(p,q)=(2sqrt(6)+2sqrt(2), 2sqrt(3)-2)`。
- Source footer: `解題來源：正哥愛數學`，第壹部分第 12 題、PDF 第 8 頁。
- End state: 原正三角形、旋轉副本、直線路徑與數對同時保留。

## Independent mathematics check

取 `A=(0,0)`、`B=(2,-2sqrt(3))`、`C=(-2,-2sqrt(3))`。順時針旋轉 90 度後，`C'=(-2sqrt(3),2)`。因此

`BC'^2=(-2sqrt(3)-2)^2+(2+2sqrt(3))^2=32+16sqrt(3)`，

所以 `BC'=2sqrt(6)+2sqrt(2)`。

直線 `BC'` 的斜率為 `-1`，方程可寫成 `y=-x-(2sqrt(3)-2)`。把這條線逆時針旋轉 90 度後，方程為 `y=x-(2sqrt(3)-2)`。交點是

`P=(0,-(2sqrt(3)-2))`，

確實位於正三角形內且 `AP=2sqrt(3)-2`。其順時針旋轉像 `P'=(-(2sqrt(3)-2),0)` 也在 `BC'` 上，故等號構形可達。

## Source ambiguity and resolution

渲染頁面中的題式與 `sqrt(2)AP` 清楚；文字抽取會漏掉根號，不能依 OCR 讀成 `2AP`。來源解答直接稱最小點必在對稱軸上，但沒有提供理由。本課程使用等號直線與其逆 90 度旋轉線的唯一交點，獨立證明該位置。

## Implementation cautions for the future deck

- `explore_p` 的每個狀態都必須嚴格在三角形內，並完整回到起點才可 loop。
- 只有旋轉完成且 `APP'` 的兩腰與直角可見後，才能顯示 `PP'=sqrt(2)AP`。
- 直線化必須同時顯示等號條件及其可達構形；不能只寫三角不等式下界。
- `D` 在 `AB` 經過 `A` 的延長線上，需明確顯示 `B-A-D` 的順序，才能使用 `BD=BA+AD`。
