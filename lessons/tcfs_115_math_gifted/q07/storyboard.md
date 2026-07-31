# Q07 Storyboard: The Hidden Product of Radical Partners

目標長度：約 8 分鐘。先用可變的數值對與固定面積矩形發現 `A+a`、`A-a` 的乘積不變，再把同一觀察搬到第二組。直到「影子乘積」已經可見，才展開兩式並相減，讓目標交叉項自然被留下。

## Visual grammar

- 第一組 `A,a` 使用藍色，第二組 `B,b` 使用綠色；加號版本為亮色，減號版本為較淡但仍清楚的同色。
- 固定乘積 4 與 9 用兩個面積不變的矩形表現，合併後的 36 用黃色。
- 目標 `aB+bA` 從題目開始使用洋紅色，展開後相同兩項保持洋紅色。
- 共通項 `AB+ab` 使用中性灰，只有在兩式相減時才淡出。
- 不以「背共軛公式」開場；名稱可在不變量已經被觀察和證明後才補充。

## Beat plan

## 01 given_product (0:25, loop=false)

- Settled visual: 顯示已知乘積 7；目標式放在右下但以問號遮住數值。
- Animation: 只圈出兩個大括號，暫不展開四項。
- Prompt: 問「我們不知道 `a,b`，為什麼目標仍可能被唯一決定？」
- Boundary: 7 與目標問號同時可見。

## 02 expand_given_product (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 03 isolate_radical_pairs (0:25, loop=false)

- Definitions: 令 `A=sqrt(a^2+4)`、`B=sqrt(b^2+9)`，原式變成 `(A+a)(B+b)=7`。
- Positivity guard: 以數線短示意顯示 `A>|a|`、`B>|b|`，因此 `A+/-a`、`B+/-b` 都是正數，後續矩形與除法合法。
- Visual split: 將第一組 `A+a` 與尚未使用的夥伴 `A-a` 上下排列。
- Boundary: 第一組成為畫面主角，第二組淡化。

## 04 vary_first_pair (0:25, loop=true)

- Loop states: `a=-3/2,0,3/2`；相應 `A=5/2,2,5/2`，故 `(A+a,A-a)` 依序為 `(1,4),(2,2),(4,1)`。
- Animation: 兩個數作為矩形邊長，矩形由瘦高變正方形、再變扁寬，最後回到起點。
- Observation: 外形改變但面積一直是 4；畫面只顯示實例，尚未寫一般證明。
- Boundary/loop: 循環必須回到 `(1,4)`，無跳格。

## 05 discover_first_invariant (0:25, loop=false)

- Prompt: 從三個實例問「為什麼面積總是 4？」
- Algebra after observation: `(A+a)(A-a)=A^2-a^2=(a^2+4)-a^2=4`。
- Naming: 此時才將兩因子標成一對根式夥伴；不需強迫使用術語。
- Boundary: 固定面積 4 落在第一個矩形中央。

## 06 compare_first_pair (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 07 state_first_invariant (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 08 mirror_second_pair (0:25, loop=false)

- Animation: 將第一組的視覺結構複製到 `B+b`、`B-b`。
- Derivation staged: `(B+b)(B-b)=B^2-b^2=(b^2+9)-b^2=9`。
- Teaching point: 變數部分消失，留下根號內的固定常數。
- Boundary: 面積 4 與 9 的兩矩形並列。

## 09 state_second_invariant (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 10 combine_invariants (0:25, loop=false)

- Animation: 兩個固定面積由物件複本相乘，得到四個因子的總乘積 36。
- Equation: `(A+a)(A-a)(B+b)(B-b)=36`。
- Preserve grouping: 亮色的兩個加號因子仍被括成已知的一組，淡色兩個減號因子括成未知的一組。
- Boundary: 畫面像一個已知總量 36 被分成兩塊乘積。

## 11 collect_invariant_sum (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 12 pose_target (0:25, loop=false)

- Return: 目標 `aB+bA` 放大，對應到原乘積展開時會出現的兩個交叉位置。
- Prompt: 問「若只展開已知的加號乘積，哪些項會和目標混在一起？」
- Pause: 不立即展開，讓觀眾預期需要一個能消掉共通項的第二式。
- Boundary: 目標洋紅色，其他位置灰色問號。

## 13 build_shadow_product (0:25, loop=false)

- Animation: 從總乘積 36 中取出已知亮色乘積 7，剩下的淡色乘積由除法形成。
- Equation: `(A-a)(B-b)=36/7`。
- Object identity: 減號因子必須由先前夥伴複製過來，不可突然出現。
- Boundary: `7` 與 `36/7` 上下對齊，準備比較。

## 14 name_shadow_product (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 15 expand_known_product (0:25, loop=false)

- Animation: 四個乘積格逐一展開 `(A+a)(B+b)`。
- Grouping: `AB+ab` 收進灰色框；`aB+bA` 收進洋紅色框 `T`。
- Result: `7=(AB+ab)+T`。
- Boundary: 只完成上式，下式仍保持因式型態。

## 16 collect_known_terms (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 17 expand_shadow_product (0:25, loop=false)

- Animation: 以相同四格位置展開 `(A-a)(B-b)`，保持項的位置與上式一致。
- Signs: 共通項仍為 `AB+ab`，兩個交叉項同時變號。
- Result: `36/7=(AB+ab)-T`。
- Boundary: 兩式垂直對齊，共通框與正負 `T` 一眼可比。

## 18 collect_shadow_terms (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 19 subtract_to_isolate (0:25, loop=false)

- Animation: 上式減下式；灰色共通框成對消去，`T-(-T)` 合成 `2T`。
- Equation earned from objects: `7-36/7=2T`。
- Teaching point: 不求 `a`、`b`，因為兩個乘積的差已經只留下題目所求。
- Boundary: `2T` 位於中央，原式淡作背景。

## 20 isolate_requested_product (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 21 final_value (0:25, loop=false)

- Arithmetic staged: `7=49/7`，所以 `2T=(49-36)/7=13/7`；再除以 2。
- Final: `T=13/14`，由洋紅色 `T` 轉回完整目標式。
- Boundary: 完整等式 `a sqrt(b^2+9)+b sqrt(a^2+4)=13/14`。

## 22 reveal_product_value (0:25, loop=false)

- Boundary: 保留目前落定的構形，下一頁再加入新的關係。

## 23 consolidate (0:25, loop=false)

- Recap path: 可變矩形面積固定 4、9 -> 加號乘積 7 決定減號乘積 `36/7` -> 相減留下交叉項。
- Source footer: `解題來源：正哥愛數學`，第壹部分第 7 題、PDF 第 4 頁。
- End state: 4、9、7、`36/7` 與 `13/14` 保持一條清楚的因果箭頭。

## Independent mathematics check

令 `A=sqrt(a^2+4)`、`B=sqrt(b^2+9)`。由 `A>|a|`、`B>|b|`，四個夥伴因子都為正。且

`(A+a)(A-a)=4`, ` (B+b)(B-b)=9`。

因此已知 `(A+a)(B+b)=7` 立刻推出 `(A-a)(B-b)=36/7`。若 `T=aB+bA`，兩式分別為

`7=AB+ab+T`, `36/7=AB+ab-T`。

相減得 `2T=7-36/7=13/7`，所以 `T=13/14`。推導不需要也沒有假設 `a,b` 為正。

## Source ambiguity

題式、答案與來源推導清楚，未發現影響結論的歧義。課程額外明示四個夥伴因子為正，以保證固定面積模型和除法步驟在任意實數 `a,b` 下都成立。

## Implementation cautions for the future deck

- `vary_first_pair` 的三個狀態必須使用精確值，並回到初始 `(1,4)` 才能循環。
- 展開兩式時四個項的位置必須完全對齊；否則相減的理由會被動畫遮蔽。
- 目標的兩個交叉項從題目到最後一律使用同一洋紅色，不讓 `Ab` 與 `bA` 看似不同角色。
