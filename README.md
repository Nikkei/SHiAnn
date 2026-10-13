[English](README.md) | [日本語 (Japanese)](README_ja.md)

# SHiAnn [Subjective and Hierarchical Annotation of Text Difficulty in Japanese]

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)

**SHiAnn** (**S**ubjective and **Hi**erarchical **Ann**otation of Text Difficulty in Japanese) contains subjective difficulty annotations for 61 Japanese newspaper articles at three linguistic levels: document, sentence, and word.
Each article was evaluated by 99 annotators, capturing individual differences in subjective difficulty judgments.

In addition to the difficulty annotation data, this repository provides scripts for reconstructing the full dataset by combining the annotations with the source articles.
The reconstruction process integrates the difficulty labels with the corresponding article, sentence, and word-level text.

## Released Data

This repository provides the following data:

* `data/annotations.json`: difficulty annotations at the document, sentence, and word levels
* `data/users.csv`: annotator attributes such as age group, gender, and occupation

The source article data required to reconstruct SHiAnn is not included in this repository.
Please contact us [here](https://nkbb.nikkei.co.jp/article/corpus/) regarding the use of the articles, which are available for a fee.

To build the dataset, place the source article data at `data/nikkei_newspaper_articles.csv`.
The `nikkei_newspaper_articles.csv` file is expected to contain the following columns:

```csv
article_id,body
hoge,fuga
```

## Environment Setup

This project uses [uv](https://docs.astral.sh/uv/) for Python package management.

[MeCab](https://taku910.github.io/mecab/) and [mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd) are used for morphological analysis.

Run the following setup script to configure the environment:

```bash
bash scripts/setup.sh
```

This script sets up the Python environment, installs mecab-ipadic-NEologd, and verifies that MeCab is working correctly.

## Dataset Construction

Run the following command:

```bash
uv run -m scripts.main \
  --annotations data/annotations.json \
  --source data/nikkei_newspaper_articles.csv \
  --output data/dataset.json
```

If the command completes successfully, the following file will be generated:

```text
data/dataset.json
```

`dataset.json` contains the difficulty annotations provided in this repository together with the text reconstructed from the source article data.

## Data Format

The reconstructed `dataset.json` file has the following JSON structure:

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

The difficulty labels (`article_difficulty`, `sentence_difficulty`, and `word_difficulty`) are defined on a four-point scale, with higher values indicating greater difficulty.

| Value | Difficulty |
|---|---|
| 0 | Very easy |
| 1 | Easy |
| 2 | Difficult |
| 3 | Very difficult |

## License

The annotation data included in this repository is provided under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** License.
Please see [CC BY-NC-SA 4.0](./data/LICENSE) for details.
For the source article data used to construct SHiAnn, please refer to [here](https://nkbb.nikkei.co.jp/article/corpus/).

The code included in this repository is provided under the **MIT** License.
Please see [MIT](./LICENSE) for details.

## Citation

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
