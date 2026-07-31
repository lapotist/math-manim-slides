# 第二部分第 1 題講者稿

解題來源：正哥愛數學。題目在 `113中一中資優班解析.pdf` 第 14 到 16 頁；公開解題影片 `rw7Z1rw7gYA` 的定位是 00:00 到 04:34。

範圍聲明：最後的 `mn=180` 只討論來源圖中「除了 O 以外，所有落點都留在從 O 出發的兩條指定射線上」的同射線首次閉合之字構形。若放寬成兩條完整直線，結論不一定成立。

## 01 meet_two_rays｜先固定我們研究的構形

眼前有兩條從 O 出發的射線，夾角是 theta。機器人每一步一樣長，而且落點在兩條射線之間交替。

請先注意綠色範圍條件：今天做一般化時，除了 O 以外，所有落點都要留在這兩條指定射線上，也就是不能穿過 O 跑到背後的延長線。

我們先從來源圖中的五步路徑開始，不先猜角度。 [PAUSE] [NEXT]

## 02 walk_five_steps｜親眼走完五個等步長

從 O 出發，第一步到 A，第二步到 B。

先停在前兩段，確認黃色點和步數計數器都落在同一個狀態。

[NEXT]

## 03 finish_five_step_walk｜補完三步並閉合

第三步到 C，第四步到 D，第五步才回到 O。

每一段都是同一個步長；A、C 留在下方射線，B、D 留在上方射線。

現在路徑閉合了。只靠這些等長線段，能不能把 theta 找出來？ [PAUSE] [NEXT]

## 04 seed_equal_angles｜第一個等腰三角形

先只看最前面兩步。OA 和 AB 都是一個步長，所以三角形 OAB 是等腰三角形。

兩條相等的邊已經標好。接下來只追蹤它們對面的兩個底角。 [PAUSE] [NEXT]

## 05 mark_first_equal_sides｜把 theta 傳到另一個底角

O 點的底角就是兩條射線的夾角 theta。等腰三角形的兩個底角相等，因此 B 點這一個角也等於 theta。

這是角度往外傳的第一顆種子。 [PAUSE] [NEXT]

## 06 propagate_five_step_angles｜先從出發端推到二 theta

先從出發端看下一對相等步長 AB 和 BC。O、A、C 在同一條指定射線上，A 點的平角配合等腰三角形，把 C 點的外層底角推成二 theta。

出發端這一側已經完成。另一側還要獨立核對。 [PAUSE] [NEXT]

## 07 complete_five_step_propagation｜再從終點端倒著推

但這只得到一邊。我們再從終點 O 倒著看：OD 等於 DC，接著 DC 等於 CB；同樣的平角與等腰關係，把 B 點的外層底角也推成二 theta。

所以最外面的三角形 OBC 才真正有三個角：theta、二 theta、二 theta。現在只差把三角形內角和寫下來。 [PAUSE] [NEXT]

## 08 reveal_thirty_six｜先寫五步外三角形的角和

把三個角相加，theta 加二 theta 再加二 theta等於一百八十度。

先停在這條完整角和。下一步才解出 theta。 [PAUSE] [NEXT]

## 09 solve_five_step_angle｜解出五步角度

也就是五 theta 等於一百八十度，所以 theta 等於三十六度。

請把「五步乘三十六度等於一百八十度」先留在心裡；七步時會出現同樣的骨架。 [PAUSE] [NEXT]

## 10 walk_seven_steps｜把同一個構形多加一層

現在換成七步。落點仍然交替留在同一側的兩條射線上，每一步仍然等長。

先走前兩步，讓新的七步構形在同一把步長尺上開始。

[NEXT]

## 11 continue_seven_step_walk｜走到第五步

接著走第三、第四、第五步。之字路徑現在逐層長出，但還沒有閉合。

[NEXT]

## 12 finish_seven_step_walk｜最後兩步回到 O

第六、第七步補上，路徑最後再次回到 O。這次之字路徑比五步版本多了一層。

不要急著套五步的答案；先看底角會長到第幾倍。 [PAUSE] [NEXT]

## 13 grow_three_layers｜theta、二 theta、三 theta

從出發端開始，第一個等腰三角形把底角標成 theta。

下一個等腰三角形共享同一條射線與前一層的角，所以底角增加一個 theta，成為二 theta。

先停在前兩層。下一步再把同一規則推到第三層。 [PAUSE] [NEXT]

## 14 complete_three_layer_growth｜完成第三層與反向傳遞

再往內一層，同樣的等長與平角關係，把其中一個外層底角推成三 theta。

接著從終點 O 倒著走完同樣三層，另一個外層底角也是三 theta。最外面的三角形因此有 theta、三 theta、三 theta。 [PAUSE] [NEXT]

## 15 reveal_seven_step_angle｜先寫七步外三角形的角和

三角形內角和給我們 theta 加三 theta再加三 theta等於一百八十度。

三個角已經全部放進等式。先不要跳到答案。 [PAUSE] [NEXT]

## 16 solve_seven_step_angle｜解出七步角度

所以七 theta 等於一百八十度，theta 等於一百八十度除以七。

五步對應二層，七步對應三層。接下來要把「層數」換成一般的奇數 n。 [PAUSE] [NEXT]

## 17 name_general_scope｜只一般化來源圖中的同射線家族

現在令總步數 n 是奇數，寫成二 h 加一。於是從中間往外生長的層數是 h，也就是 n 減一除以二。

畫面用九步當代表，但字母 n 指的是所有同樣規則的奇數步構形。

再確認一次範圍：非 O 落點都在兩條指定射線上，而且這是第一次回到 O。這個次序讓角度每一層都沿同一方向增加。 [PAUSE] [NEXT]

## 18 build_angle_recurrence｜先寫角度遞推規則

把第 j 層的底角記成 alpha j。第一層 alpha 一等於 theta。

相鄰兩步等長，所以每一層都是等腰三角形；同射線上的平角把前一層與夾角 theta 接起來。因此 alpha j 加一等於 alpha j 加 theta。

遞推的起點與規則都已經可見。接著讓它逐層運作。 [PAUSE] [NEXT]

## 19 propagate_general_angles｜先讓遞推走過前幾層

同一個高亮三角形依序走到第二層、第三層。每往內一層，底角都多一個 theta。

先停在前幾個具體層次。 [PAUSE] [NEXT]

## 20 complete_general_propagation｜把遞推推到第 h 層

再走到代表圖的最外層，畫面才把 theta、二 theta、三 theta延伸成一般的第 h 層 h theta。

這就是圖形中的角度遞推。 [PAUSE] [NEXT]

## 21 close_outer_triangle｜先關閉最外三角形

把內部之字路徑淡化，只看最外面的三角形。O 點是 theta，另外兩個底角都是 h theta。

所以 theta 加二 h theta等於一百八十度。先把這個外三角形角和停住。 [PAUSE] [NEXT]

## 22 state_scoped_product｜把層數換回 n

因為二 h 加一就是 n，左邊正好是 n theta。

若 theta 的度數記成 m，就得到 m 乘 n 等於一百八十。請注意綠色文字：這個結論只屬於目前的同射線首次閉合家族。 [PAUSE] [NEXT]

## 23 mark_scope_boundary｜先放寬成完整直線

現在只用一頁標出範圍邊界。若把射線放寬成整條直線，落點可以穿過 O 到背後。

右邊先畫出一條使用延長線的五步閉合路徑。它不再屬於剛才的同射線家族。 [PAUSE] [NEXT]

## 24 verify_full_line_counterexample｜核對延長線反例

右邊這條五步等長路徑在七十二度也能閉合，但第三、第四個有號距離是負的，表示落點用了相反延長線。此時五乘七十二等於三百六十，不是一百八十。

所以它是完整直線問題的反例，卻不屬於來源圖中的同射線構形。我們不拿它否定前一頁的限定結論，也不能用前一頁去涵蓋它。 [PAUSE] [NEXT]

## 25 consolidate_scoped_invariant｜先回到正確範圍

最後回到綠色的同射線家族。

九步代表圖重新落在兩條指定射線上，範圍條件也重新出現。 [PAUSE] [NEXT]

## 26 restate_scoped_results｜三個結果在正確範圍內收束

五步時，最外層底角是二 theta，得到 theta 等於三十六度。七步時，底角是三 theta，得到 theta 等於一百八十度除以七。

一般奇數 n 時，層數是 n 減一除以二；在非 O 落點都留在兩條指定射線上的首次閉合構形內，m 乘 n 等於一百八十。

這就是三個問題在正確範圍下連起來的答案。 [PAUSE]
