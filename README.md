# 月光書房 — 二夜の物語集

彗星の見える夜にだけ路地の奥に現れる古書店「月光書房」。その棚から借り受けた、という体裁の **日本語短編集** です。現在 **二つの夜集（全24編）** を収録し、そのまま **GitHub Pages** で公開できる静的サイトとして組み上げてあります。

各編は文庫本でおよそ24頁以上（全24編で約385,000字）。共通の符牒（ミラ彗星・月光堂の青いマッチ箱・子守唄「眠れ、眠れ、星が海をわたるまで」・現れて消える書店「月光書房」・片方の手袋）で、二つの夜集はゆるやかに繋がっています。

## 二つの夜集

### 第一夜集『十二夜の物語集』── ジャンルの多様
SF／時代小説／本格ミステリー／ファンタジー／怪談／恋愛／ヒューマンドラマ／深海冒険／寓話／サスペンス／マジックリアリズム／近未来AI。
ジャンルも時代も世界も異なる十二編。

### 第二夜集『まなざしの十二夜』── 語りの視点
同じ一夜・同じ星を「語られなかった側」から描く十二編。二人称「あなた」／物（街灯）／死者／一人称複数「わたしたち」／動物（老猫）／場所（映画館）／時間逆行／未来の研究者の註解／管理AIのログ／多声（羅生門型）／取扱説明書の形式／信頼できない語り手。
語りの視点そのものを主役にした、第一夜集の姉妹集。

## ディレクトリ構成

```
index.html                 … 入口（ポータル：二つの夜集）
about.html                 … 月光書房について
vol1/
  index.html               … 第一夜集 目次
  about.html               … この巻について
  connections.html         … 符牒の早見表
  stories/01.html 〜 12.html
vol2/
  index.html               … 第二夜集 目次
  about.html, connections.html
  stories/01.html 〜 12.html
assets/style.css           … 夜空／紙テーマ・縦書き切替などのスタイル
assets/app.js              … 文字サイズ・縦書き・テーマの切替（localStorage 保存）
.nojekyll                  … GitHub Pages の Jekyll 処理を無効化
tools/
  build.py                 … サイト生成スクリプト（site.json + data/ → HTML）
  site.json                … 両夜集のメタ情報（巻・各編のタイトル・著者名など）
  data/_portal.md, _about.md           … 入口・総序の本文
  data/vol1/story-01.md 〜 12.md, _about.md, _connections.md
  data/vol2/story-01.md 〜 12.md, _about.md, _connections.md
```

## ローカルで確認する

```bash
python -m http.server 8000   # リポジトリのルートで実行
# ブラウザで http://localhost:8000/ を開く
```

## 本文を編集して作り直す

本文は `tools/data/<巻>/story-XX.md`、メタ情報は `tools/site.json` を編集し、再生成します。

```bash
python tools/build.py
```

## 公開（GitHub Pages）

すでに公開済みです：**https://makamaika.github.io/gekko-shobo/**

更新するときは、変更を commit して push するだけで自動的に再ビルドされます。

```bash
git add -A
git commit -m "Update stories"
git push
```

新しいリポジトリで一から公開する場合は、GitHub の **Settings → Pages → Deploy from a branch → main / (root)** を設定してください。サイトはルート直下の静的 HTML だけで完結しているので、追加のビルド設定は不要です。

## 読み方の工夫

- 右上のボタンで **紙／夜空テーマ**、**文字サイズ**、物語ページでは **縦書き／横書き** を切り替えられます（設定はブラウザに保存されます）。
- 各物語の末尾「この物語にひそむ符牒」を開くと、その編が他の編と分かち合っているモチーフが分かります。
- 二つの夜集は、どちらから読んでも構いません。同じ星の下で書かれていることに気づくと、二十四の夜がひとつの夜空になります。

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
