import re

from bs4 import BeautifulSoup


def clean_html(body_text: str) -> str:
    kakomi_matches = re.findall(
        r"<KAKOMI>[^<【]*【関連記事】.*?</KAKOMI>",
        body_text,
        flags=re.DOTALL,
    )

    kanren_matches = re.findall(
        r"<KANREN>[^<【]*【関連記事】.*?</KANREN>",
        body_text,
        flags=re.DOTALL,
    )

    for match in kakomi_matches:
        body_text = body_text.replace(match, "")

    for match in kanren_matches:
        body_text = body_text.replace(match, "")

    soup = BeautifulSoup(body_text, "lxml")
    text = soup.get_text()

    return text
