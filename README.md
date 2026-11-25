# semphyx.github.io

研究紹介サイトのソースです。Hugo(テーマなし・自作レイアウト)で作り、`main` に push すると GitHub Actions で GitHub Pages にデプロイされます。
研究業績(経歴・論文・講演)は researchmap に集約しているため、このサイトには載せません。

## 編集する場所

| 内容 | ファイル |
|---|---|
| 名前・所属・研究分野・お知らせ・連絡先・外部ID | `content/_index.md`(front matter と本文) |
| リンク集 | `content/links.md` の `groups` |
| ページの追加 | `content/*.md`(数式を使うページは front matter に `math: true`) |
| メニュー・サイト名 | `hugo.toml` |
| 見た目 | `assets/css/main.css`、`layouts/` |

`url` や `value` を空にした項目は表示されません。

## ローカルで確認

```bash
hugo server
```
