import argparse
import copy
import csv
import json
from pathlib import Path

from src.sentence_splitter import split_sentences_japanese
from src.tokenizer import tokenize_sentence


def load_annotations(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_source_articles(path: Path) -> dict[str, dict]:
    articles = {}

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            articles[row["article_id"]] = row

    return articles


def reconstruct_article(annotation_article: dict, source_article: dict) -> dict:
    result = copy.deepcopy(annotation_article)

    sentences = split_sentences_japanese(source_article["body"])

    normalized_sentences = [sentence.lstrip("　 ") for sentence in sentences]

    article_text = "".join(
        sentence.replace("　", " ") for sentence in normalized_sentences
    )

    formatted_sentences = []

    for annotation_sentence in result.get("sentences", []):
        sentence_index = annotation_sentence["sentence_index"]
        sentence_text = normalized_sentences[sentence_index - 1]

        tokens = tokenize_sentence(sentence_text)

        formatted_words = []

        for word in annotation_sentence.get("words", []):
            word_index = word["word_index"]

            offset = 0
            matched_token = None

            for token in tokens:
                if offset == word_index:
                    matched_token = token
                    break

                offset += len(token)

            if matched_token is None:
                raise ValueError(
                    f"No token starts at word_index={word_index}: "
                    f"sentence={sentence_text!r}, "
                    f"tokens={tokens}"
                )

            formatted_words.append(
                {
                    "word_index": word_index,
                    "word": matched_token,
                    "word_annotations": word.get(
                        "word_annotations",
                        [],
                    ),
                }
            )

        output_sentence = sentence_text.replace("　", " ")
        formatted_sentences.append(
            {
                "sentence_index": sentence_index,
                "sentence": output_sentence,
                "sentence_annotations": annotation_sentence.get(
                    "sentence_annotations",
                    [],
                ),
                "words": formatted_words,
            }
        )

    return {
        "article_id": result["article_id"],
        "genre": result["genre"],
        "article": article_text,
        "article_annotations": result.get(
            "article_annotations",
            [],
        ),
        "sentences": formatted_sentences,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Script to reconstruct the full dataset by combining the annotations with the source articles"
    )
    parser.add_argument(
        "--source", required=True, type=Path, help="Path to source article data"
    )
    parser.add_argument(
        "--annotations",
        default=Path("data/annotations.json"),
        type=Path,
        help="Path to difficulty annotation data",
    )
    parser.add_argument(
        "--output",
        default=Path("data/dataset.json"),
        type=Path,
        help="Path to output file",
    )

    args = parser.parse_args()

    annotations = load_annotations(args.annotations)
    source_articles = load_source_articles(args.source)

    output = {"articles": []}

    for annotation_article in annotations["articles"]:
        article_id = annotation_article["article_id"]

        if article_id not in source_articles:
            raise ValueError(f"Source corpus does not contain article: {article_id}")

        reconstructed = reconstruct_article(
            annotation_article,
            source_articles[article_id],
        )

        output["articles"].append(reconstructed)

    with args.output.open("w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2,
        )


if __name__ == "__main__":
    main()
