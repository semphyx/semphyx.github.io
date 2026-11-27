---
title: "{{ replace .File.ContentBaseName "-" " " }}"
date: {{ .Date }}
draft: true
summary: ""   # 一覧に出す 1〜2 行の説明
---

## はじめに

本文を Markdown で書きます。数式は $E = mc^2$ や

$$
\frac{\partial u}{\partial t} = D \nabla^2 u
$$

のように書けます。
