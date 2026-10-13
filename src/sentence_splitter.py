import functools

from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import (
    concatenate_matching,
)
from ja_sentence_segmenter.split.simple_splitter import (
    split_newline,
    split_punctuation,
)

from src.cleaning import clean_html

concat_quote_tail = functools.partial(
    concatenate_matching,
    former_matching_rule=r"^(.+[「『])(?P<result>.+)$",
    latter_matching_rule=r"^(?P<result>.*[」』])[。！？]?$",
    remove_former_matched=False,
    remove_latter_matched=False,
)


segmenter = make_pipeline(
    split_newline,
    concat_quote_tail,
    functools.partial(
        split_punctuation,
        punctuations=r"。",
    ),
)


def split_sentences_japanese(text: str) -> list[str]:
    clean_text = clean_html(text)

    sentences = [sentence.strip() for sentence in list(segmenter(clean_text))]

    sentences = [sentence for sentence in sentences if sentence]

    return sentences
