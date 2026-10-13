[English](README.md) | [日本語 (Japanese)](README_ja.md)

# SHiAnn [Subjective and Hierarchical Annotation of Text Difficulty in Japanese]

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)

**SHiAnn** (**S**ubjective and **Hi**erarchical **Ann**otation of Text Difficulty in Japanese)は、日本語新聞記事61件を対象に、文書・文・単語の3つの階層で主観的な難易度をアノテーションしたデータセットです。
各記事に対して99名のアノテータが難易度を評価しており、個人によって異なる難易度判断の違いを含んでいます。

本リポジトリでは、難易度アノテーションデータに加え、構築元の記事データと組み合わせることで難易度ラベルと記事本文・文・単語のテキスト情報を統合したデータセットを再構築するためのスクリプトを提供しています。

## 公開データ

本リポジトリでは、以下のデータを公開しています。

* `data/annotations.json`：文書・文・単語レベルの難易度アノテーション
* `data/users.csv`：アノテータの年齢層，性別，職業などの属性情報

SHiAnn の構築元の記事データは、本リポジトリには含まれていません。
[こちら](https://nkbb.nikkei.co.jp/article/corpus/)より記事データ（有償で利用可能です）の利用についてお問い合わせください。

データセットを構築する際は、取得した元記事データを `data/nikkei_newspaper_articles.csv` として配置してください。
`nikkei_newspaper_articles.csv`は、article_idとbodyのカラムから成るcsvファイルを想定しています。

```csv
article_id,body
hoge,fuga
```

## 環境構築

本プロジェクトでは Python のパッケージ管理に [uv](https://docs.astral.sh/uv/) を使用します。

また、形態素解析には [MeCab](https://taku910.github.io/mecab/) および [mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd) を使用します。

以下の環境構築スクリプトを実行してください。

```bash
bash scripts/setup.sh
```

このスクリプトでは、Python の実行環境の構築、mecab-ipadic-NEologd のセットアップ、および MeCab の動作確認を行います。

## データセットの構築

以下のコマンドを実行してください。

```bash
uv run -m scripts.main \
  --annotations data/annotations.json \
  --source data/nikkei_newspaper_articles.csv \
  --output data/dataset.json
```

実行に成功すると、以下のファイルが生成されます。

```text
data/dataset.json
```

`dataset.json` には、本リポジトリで公開している難易度アノテーション情報と元記事データから復元したテキスト情報が含まれます。

## データ形式

構築後の `dataset.json` は、以下のようなJSON形式になります。

```json
{
  "articles": [
    {
      "article_id": "...",
      "genre": "...",
      "article": "...",
      "article_annotations": [
        {
          "user_id": 1,
          "article_difficulty": 0
        }
      ],
      "sentences": [
        {
          "sentence_index": 1,
          "sentence": "...",
          "sentence_annotations": [
            {
              "user_id": 1,
              "sentence_difficulty": 0
            }
          ],
          "words": [
            {
              "word_index": 0,
              "word": "...",
              "word_annotations": [
                {
                  "user_id": 1,
                  "word_difficulty": 0
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

難易度ラベル（`article_difficulty`、`sentence_difficulty`、`word_difficulty`）は、値が大きいほど難易度が高いことを示し、以下の4段階で定義されます。

| 値 | 難易度 |
|---|---|
| 0 | とても易しい |
| 1 | 易しい |
| 2 | 難しい |
| 3 | とても難しい |

## ライセンス

本リポジトリに含まれるアノテーションデータは、 **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** ライセンスのもとで提供されます。
ライセンスの詳細は、 [CC BY-NC-SA 4.0](./data/LICENSE) をご参照ください。
また、SHiAnn の構築元の記事データにつきましては[こちら](https://nkbb.nikkei.co.jp/article/corpus/)をご確認ください。

本リポジトリに含まれるコードは、 **MIT** ライセンスのもとで提供されます。
ライセンスの詳細は、 [MIT](./LICENSE) をご参照ください。

## 参考文献

```
@InProceedings{maekawa-etal-2026-subjective,
  title     = {Subjective and Hierarchical Annotation of Text Difficulty in Japanese},
  author    = {Daisuke Maekawa and Kazumasa Omura and Sora Tarumoto and Shotaro Ishihara and Tomoyuki Kajiwara},
  booktitle = {Proceedings of the 2026 Conference on Empirical Methods in Natural Language Processing},
  year      = {2026},
  address   = {Budapest, Hungary},
  note      = {(to appear)},
}
```
