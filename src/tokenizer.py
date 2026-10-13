import os

import MeCab
from dotenv import load_dotenv

load_dotenv()

NEOLOGD_PATH = os.getenv("NEOLOGD_PATH")
MECABRC_PATH = os.getenv("MECABRC")

if not MECABRC_PATH:
    raise RuntimeError("MECABRC is not set.")

if not NEOLOGD_PATH:
    raise RuntimeError("NEOLOGD_PATH is not set.")

TAGGER = MeCab.Tagger(f"-r {MECABRC_PATH} -d {NEOLOGD_PATH}")


def tokenize_sentence(text: str) -> list[str]:
    node = TAGGER.parseToNode(text.strip())

    tokens = []
    current_noun = []

    while node:
        surface = node.surface.replace("　", " ")
        feature = node.feature

        if surface:
            pos = feature.split(",")[0]

            if pos == "名詞":
                current_noun.append(surface)

            else:
                if current_noun:
                    tokens.append("".join(current_noun))
                    current_noun = []

                tokens.append(surface)

        node = node.next

    if current_noun:
        tokens.append("".join(current_noun))

    return tokens
