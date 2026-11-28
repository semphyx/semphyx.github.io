# semphyx.github.io

研究紹介サイトのソースです。Hugo(テーマなし・自作レイアウト)で作り、`main` に push すると GitHub Actions で GitHub Pages にデプロイされます。
研究業績(経歴・論文・講演)は researchmap に集約しているため、このサイトには載せません。

## 編集する場所

| 内容 | ファイル |
|---|---|
| 名前・所属・研究分野・お知らせ・連絡先・外部ID | `content/_index.md`(front matter と本文) |
| リンク集 | `content/links.md` の `groups` |
| ノート | `content/notes/<分類>/*.md`(数式はそのまま使えます) |
| ノートのタグ | ノートの front matter に `tags: ["pn接合", "Python"]` |
| ノートの分類 | `content/notes/<分類>/_index.md`(`weight` の順にサイドバーへ並ぶ) |
| ページの追加 | `content/*.md`(数式を使うページは front matter に `math: true`) |
| メニュー・サイト名 | `hugo.toml` |
| 見た目 | `assets/css/main.css`、`layouts/` |

`url` や `value` を空にした項目は表示されません。

## ノートの書き方

```bash
hugo new notes/math/fourier-series.md
```

作られたファイルの `draft: true` を `false` にすると公開されます。分類のフォルダ名は
`math`(数学)・`physics`(物理)・`semiconductor`(半導体)・`numerical`(数値計算)・
`computer-engineering`(計算機工学)・`research-writing`(執筆・研究の進め方)・`others`(その他)です。

## 講義ノート(章が続くテキスト)

講義(テキスト)ごとにフォルダを作り、章を順番に並べます。

```
content/lectures/semiconductor-physics/_index.md      ← 講義名(title)と説明(summary)
content/lectures/semiconductor-physics/01-crystal.md  ← weight: 1
content/lectures/semiconductor-physics/02-band.md     ← weight: 2
```

新しい章は次のコマンドで作れます(`weight` に章の番号を入れ、`draft: false` で公開)。

```bash
hugo new lectures/semiconductor-physics/03-carrier.md
```

章は `weight` の順に「第 1 章」「第 2 章」…と番号が付き、前後の章へのリンクもこの順になります。

## ツール(ブラウザで動く計算機など)

ツールごとにフォルダを作り、説明と画面(HTML)を `index.md` に、動きを `.js` に書きます。
同じフォルダの `.js` は自動で読み込まれます。並び順は `weight` です。

```
content/tools/pn-junction/index.md   ← 説明と入力欄・結果欄(HTML)
content/tools/pn-junction/tool.js    ← 計算の処理
```

サイト内のページへのリンクは、`/staging/` でも正しく動くように
`[ノート]({{</* relref "/notes/..." */>}})` の形で書きます。

## 注記ボックス

ノートの中で、次のように書くと色付きのボックスになります。

```markdown
> [!TIP]
> ポイント(結論・覚えておく式)

> [!NOTE]
> 補足(脱線・参考)

> [!WARNING]
> 注意(落とし穴・間違いやすい点)
```

`> [!TIP] 独自の見出し` のように書くと、見出しを変えられます。

## ローカルで確認

```bash
hugo server
```
