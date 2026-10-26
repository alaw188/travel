# 2026 澳洲家庭之旅 — Sydney & Melbourne trip 網站

給父母了解及準備 2026 年 12 月澳洲行程嘅單頁式網站（Single-file static site），繁體中文（香港用法）為主，地點名稱保留英文。

- **開啟方式**：直接雙擊 `index.html`（唔使裝任何嘢、唔使 build）
- **行程日期**：2026/12/11（五）– 12/24（四）
- **資料來源**：Wanderlog 行程 PDF（`2026 Family Trip to Sydney & Mel – Wanderlog.pdf`）

## 檔案結構

```
aussie/
├── index.html    # 主網站（HTML + CSS + JS 全部單一檔案）
├── index_.html   # 地圖互動實驗版（POIS 資料驅動，見下）
├── index2.html   # ⚠️ 備份凍結（2026-10 起唔再更新，只作歷史參考）
├── booking.html  # 獨立酒莊團比較頁（唔同 index 互鏈）
├── README.md     # 本檔
└── img/          # 61 張地點圖片（slug 命名，本地檔）
```

## index_.html — 地圖驅動互動版（實驗）

- **資料層**：全部內容抽成 `POIS` 陣列（`id / day / name / time / desc / lat / lng / cat / alt`），
  列表、地圖 pin、連線、篩選器、詳情條全部由同一份資料渲染 → **加減內容只改 `POIS`**。
- **地圖**：自建 SVG 示意圖（按真實經緯度投影，非導航用途）。為何唔用騰訊地圖：
  澳洲唔在騰訊地圖覆蓋範圍、GCJ-02 只適用中國境內，且單檔要離線可開 — 故採用需求書
  §2.6 允許嘅 SVG 降級方案（編號節點 + 分區分色 + 點擊聯動全部保留）。
- **兩個獨立區塊**：`悉尼 Sydney`（日 12–17，含 12/17 出發航班）同 `墨爾本 Melbourne`（日 17–21）
  各自有一套地圖／時間線／詳情條／篩選／導覽，互不干擾；`d17-1`（SYD→MEL 航班）歸悉尼。
- **全覽模式**：每個日期一個編號標記（顯示日號 + 站數），撳一下即入該日；標記有防重疊推開。
- **互動**：點 pin／卡片 → 詳情條更新（含上一站／下一站）、自動導覽（3.6 秒一站，全覽時逐日行）、
  分區膠囊篩選、圖例、地圖 panTo、`←/→` 鍵切換。
- **投影邏輯**：`reproject(list)` 會按「目前可見」嘅點重新 fit 到畫布，
  所以睇單一日會自動放大，唔會所有 pin 疊埋一齊。
- **改內容**：只改 `POIS`（加一個 object）；分區標題／顏色改 `DAYS`；類別顏色改 `CATS`。
- ⚠️ 未經批准前 `index.html` 保持不變；`index_.html` 確認 OK 後才覆蓋。

## index.html 內部結構（日後更新睇呢度）

| 區塊 | 位置 | 用途 |
|------|------|------|
| `<style>` | 頂部 | 版面樣式；`.place .cost` 控制費用標籤、`.place .dish` 招牌必試標籤 |
| HTML sections | 中段 | 行程總覽 / 航班 / 住宿 / 逐日行程（#sydney #melbourne）/ 貼士 / 餐廳攻略 |
| `CATS` | `<script>` 內 | 地點分類 → 圖標同標籤 |
| `DAYS` | `<script>` 內 | **逐日行程資料**（每個地點一個 object：`n` 名、`zh` 中文名、`type` 分類、`d` 簡介、`hours`、`wiki`、`book`） |
| `COSTS` | `<script>` 內 | **費用對照表**（key = 地點名，value = 費用文字；`FREE` 常數顯示綠色） |
| `DISHES` | `<script>` 內 | **招牌必試對照表**（key = 地點名，value = 招牌菜式文字） |
| `CAT_ORDER` | `<script>` 內 | 每日卡片排序：資訊 → 一日遊 → 酒莊 → 景點 → 海灘 → 古蹟 → 咖啡 → 餐廳 → 甜點 → 市場 → 購物 |
| Renderer | `<script>` 內 | `renderDay()` 按 `CAT_ORDER` 排序後產生卡片；圖片用本地 `img/<slug>.jpg` |
| 效果 IIFE | `<script>` 內 | 滾動浮現（IntersectionObserver）、進度條＋回到頂部（rAF 節流）、倒數橫幅 |

### 點樣加／改一個地點

1. 喺 `DAYS` 對應日子嘅陣列入加一個 object：
   `{n:"地點英文名", zh:"中文名", type:"food", wiki:"Wikipedia條目(如適用)", book:true(需訂位才加), hours:"...", d:"簡介"}`
2. 有需要再喺 `COSTS` / `DISHES` 加同名 key。
3. 圖片放入 `img/` 用同一 slug 命名（見下）。
4. ⚠️ `COSTS` / `DISHES` 嘅 key **必須同 `DAYS` 嘅 `n` 完全一致**，改名要同步改。

## 圖片運作

- 全部 61 張圖片已**下載到本地 `img/` 資料夾**，唔依賴任何外部網站，**離線都睇到晒**。
- 檔名 = 地點名 slug：英數以外字元轉 `_`（例：`Toby_s_Estate_Coffee_Roasters.jpg`）；純中文名就用 `d20_0.jpg`（day id + 序數）。
- 渲染時自動搵 `img/<slug>.jpg`，載入失敗會依次試 `.jpeg → .png → .webp`，全部失敗先 fallback 顯示分類圖標（版面唔會爛）。
- HTML 內**已移除**舊嘅 `IMGS` 對照表同 Wikipedia 抓圖程式碼（2026-10 精簡），逐間圖片來源紀錄改保存喺下面。

### 圖片來源分類（誠實聲明）

| 類別 | 內容 |
|------|------|
| ✅ 地標實景（Wikipedia） | 歌劇院、大橋、The Rocks、Bondi、藍山、QVM、State Library、十二門徒石、企鵝、Yarra Valley 等 23 張 |
| ✅ 實店／實場相（Flickr CC via Openverse） | Bondi Surf Seafoods、Paramount、Toby's Estate、The Grounds（兩張）、Baguette Studios、Market Lane、Proud Mary、Bakemono、Patricia、Dukes、Industry Beans、Pidapipó、Vacation、Hardware Société、Lune、Single O、Higher Ground、DeBortoli 酒莊 等 19 張 |
| ✅ 官方圖片（官網 og:image／相片） | 6HEAD、Beta Coffee、ST. ALi、Hareruya、Terror Twilight、Grain Store、Hector's Deli 共 7 張 |
| ⚠️ 代表性相片（搵唔到自由授權嘅實店相） | Pho Thin（河粉）、Cafe Margaret、mimi's、Bar Totti's、The Gidley、BISTECCA、Pizza Bros（薄餅）、Lulu & me（芝士蛋糕）共 8 張 — 建議**旅程影完相後替換**：將自己張相改名做對應 slug 放入 `img/` 覆蓋就得 |
| ✅ 交通 | SYD→MEL：Qantas 787 降落墨爾本機場（Wikipedia） |

### 逐間圖片原始 URL 紀錄

> 由舊 `IMGS` 表遷入（僅作來源紀錄，網站運行已唔需要）。Wikimedia 檔案可喺 `commons.wikimedia.org/wiki/File:<檔名>` 查閱。

| 地點 | 來源 |
|------|------|
| Pho Thin Chatswood | Commons：`3 mushroom curry noodle soup with phở - Pho 2025-11-12.jpg` |
| Cafe Margaret Double Bay | Commons：`Caravan, Clerkenwell, London (5624758902).jpg` |
| mimi's / BISTECCA | Commons：`Cóctel Negroni Campari.jpg` |
| Bondi Surf Seafoods | Commons：`Fish-and-chips-in-a-paper-bag.jpg` |
| 6HEAD Sydney / The Gidley | Commons：`Grilled steak served on a plate with avocado and sauce.jpg` |
| Paramount / The Grounds of Alexandria / Grumpy Barista / Dukes | Commons：`2019 02 Awesome Coffee Shop in Korat.jpg` |
| Single O / Toby's Estate / Grounds Factory / Market Lane / Proud Mary / Patricia / Industry Beans / Vacation | Commons：`Flat White 1.jpg` |
| Bar Totti's | Commons：`Antipasto 01 (RaBoe).jpg` |
| Pizza Bros | Commons：`Eq it-na pizza-margherita sep2005 sml.jpg` |
| Baguette Studios | Commons：`20240817 Paris Baguette at 360 Shopping Plaza (Greenland Metropolis).jpg` |
| Lune Croissanterie | Commons：`Croissant, whole.jpg` |
| South Melbourne Market | Commons：`Shops inside South Melbourne Market.jpg` |
| SYD → MEL 內陸機 | Commons：`Qantas (VH-ZNN) Boeing 787-9 Dreamliner on final at Melbourne Airport (1).jpg` |
| Hareruya Pantry / Bakemono Bakers | Commons：`Melon bread (with chocolate chips) 2023-11-05.jpg` |
| Lulu & me Cheesecakes | Commons：`Cheesecake with slice cut out.jpg` |
| Phillip Island · Penguin Parade | Commons：`Eudyptula minor Bruny 1.jpg` |
| Higher Ground | Commons：`Caravan, Clerkenwell, London (5624758902).jpg` |
| Pidapipó | Commons：`Gelato Cup Ice-cream Cake Cow.jpg` |
| The Hardware Société | Commons：`Burger, fries, and eggs benedict - La Tessa.jpg` |
| Beta Coffee | Commons：`Devonshire Street Surry Hills 001.jpg` |
| Queen Victoria Market | Commons：`Queen Victoria Market, Melbourne shed B.jpg` |
| ST. ALi Coffee Roasters | Commons：`Magic (coffee) at St Ali South Melbourne.jpg` |
| Terror Twilight | 官網 `terrortwilight.com.au`：`TERRORCATERING-180621-WR-106.jpg` |
| Grain Store | 官網 `grainstore.com.au`：`grainstore+62.jpg` |
| 雅拉河谷（兩張 d20） | Commons：`Aerial View - Landschaft Markgräflerland1.jpg` |
| Hector's Deli | Commons：`20240817 Paris Baguette at 360 Shopping Plaza (Greenland Metropolis).jpg` |

## 代碼精簡紀錄（2026-10-23）

- 移除未使用嘅 `IMGS` 對照表（~6.5KB，紀錄遷入本檔）
- 移除冗餘三元運算（兩個分支相同）
- 移除冇人用嘅 `id="pic-..."` 同每張 img 重複嘅 inline style（改入 CSS）
- 移除未使用 CSS：`.grid.c4`、`.hero .sub`（index）、`.flight .route/.meta`、`.tag.green`、`:root` 重複定義
- `p.cost` 改寫共享資料 → 改用局部變數
- scroll handler 加 `requestAnimationFrame` 節流（每個事件只讀一次 layout）
- 倒數器用 `bar.isConnected` 取代重複 DOM 查詢
- 成效：index.html 76KB → 54KB，index2.html 66KB → 45KB

## 待辦 / 後續跟進（Follow-ups）

- [ ] 🛂 **澳洲 ETA（出發前必辦）**：全部家人持 HKSAR 護照，須經「Australian ETA」手機 App 申請 ETA（subclass 601）· A$20／人 · 多數即時獲批 · 12 個月有效期；建議 11 月內辦妥
- [ ] 訂位：Cafe Margaret、6HEAD、Bar Totti's、The Gidley（必訂）；The Grounds、Higher Ground、Grain Store、mimi's（建議訂）
- [ ] 訂團：Klook 獵人谷一日遊（12/15，$1,275／位含午餐）；Yarra Valley 酒莊團（12/20，兩個選項 8:45 / 9:30 出發）
- [ ] 訂票：Sydney Opera House 導賞團；Phillip Island Penguin Parade（12/19 黃昏場）
- [ ] 內陸機 SYD→MEL（12/17 上午，11:00–12:30 到達）買飛
- [ ] ⚠️ Airbnb Swanston Central：11/17 3pm 前免費取消期限已過／將到，留意 12/10 3pm 部分退款期限
- [ ] 費用標籤全部係估計值，出發前想更新的話改 `COSTS` 表就得

## 已知限制

- 費用為預算參考（非實時匯率／價格），匯率以約 1 AUD ≈ 5 HKD 計
- 8 間餐廳／小店暫時用代表性相片（見上表），旅程影相後可替換
- `index.html` 同 `index2.html` 內容會重複（兩個獨立單檔，無共用 JS）；改行程要記住**兩邊都要改**
