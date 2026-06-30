# 月光書房 — 十二夜の物語集

彗星の見える夜にだけ路地の奥に現れる古書店「月光書房」。その棚から借り受けた、という体裁の **日本語短編集（全12編）** です。
ジャンルも時代も世界もばらばらの十二編が、共通の「符牒（ミラ彗星・青いマッチ箱・子守唄・現れて消える書店・片方の手袋）」によってゆるやかに繋がっています。各編は文庫本でおよそ24頁以上の分量があります。

そのまま **GitHub Pages** で公開できる、静的サイトとして組み上げてあります。

## 収録作

| # | 作品 | ジャンル |
|---|------|----------|
| 一 | 船の灯台 | SF（世代宇宙船） |
| 二 | 神田の提灯 | 時代小説（人情噺） |
| 三 | 吹雪の宿 | 本格ミステリー（密室） |
| 四 | 存在しない国の地図 | ファンタジー |
| 五 | 十三番目の周波数 | 怪談・ホラー |
| 六 | 閏年の二人 | 恋愛 |
| 七 | 止まった時計 | ヒューマンドラマ |
| 八 | 沈んだ町 | 冒険（深海） |
| 九 | 月を釣る狐 | 寓話・童話 |
| 十 | 危険な手紙 | サスペンス |
| 十一 | 記憶が降る町 | マジックリアリズム |
| 十二 | 夢を編む | 近未来SF（AI） |

※ 正式タイトルは各物語ページを参照（執筆エージェントが命名）。

## ディレクトリ構成

```
index.html              … 目次（トップページ）
about.html              … この本について（序）
connections.html        … 十二をつなぐ符牒（仕掛けの早見表）
stories/01.html 〜 12.html … 各物語
assets/style.css        … スタイル（夜空テーマ／紙テーマ切替）
assets/app.js           … 文字サイズ・縦書き・テーマの切替
.nojekyll               … GitHub Pages の Jekyll 処理を無効化
tools/
  build.py              … サイト生成スクリプト
  manifest.json         … 各編のメタ情報（タイトル・著者名など）
  data/story-01.md 〜 12.md … 各物語の本文（Markdown）
  data/_about.md, _connections.md … 序・符牒ページの本文
```

## ローカルで確認する

```bash
# リポジトリのルートで簡易サーバを起動
python -m http.server 8000
# ブラウザで http://localhost:8000/ を開く
```

## 本文を編集して作り直す

本文は `tools/data/*.md`、メタ情報は `tools/manifest.json` を編集し、再生成します。

```bash
python tools/build.py
```

## GitHub Pages で公開する

1. このフォルダを GitHub のリポジトリとして push する。
   ```bash
   git add -A
   git commit -m "Publish 月光書房 anthology"
   git remote add origin https://github.com/<あなた>/<リポジトリ>.git
   git push -u origin main
   ```
2. GitHub のリポジトリ → **Settings → Pages**。
3. **Build and deployment → Source** を **Deploy from a branch** にし、Branch を **main / (root)** に設定して保存。
4. 数分後、`https://<あなた>.github.io/<リポジトリ>/` で公開されます。

サイトはルート直下の静的 HTML だけで完結しているので、追加のビルド設定は不要です。

## 読み方の工夫

- 右上のボタンで **紙／夜空テーマ**、**文字サイズ**、物語ページでは **縦書き／横書き** を切り替えられます（設定はブラウザに保存されます）。
- 各物語の末尾「この物語にひそむ符牒」を開くと、その編が他の十一編と分かち合っているモチーフが分かります。

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
