#   ---------------------------------------------------------------------------------
#   Copyright (c) Hexafuchs. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from sharkey_crawler import SharkeyServer, Post


def crawl_notes_on_waldbewohner_eu(user: str) -> list[Post]:
    return SharkeyServer("waldbewohner.eu").user_notes(
        user, allow_partial=True, with_channel_notes=True, with_renotes=False, with_replies=False
    )


def crawl_varia() -> list[Post]:
    return crawl_notes_on_waldbewohner_eu("9vdsx5h21yqo003k")


def crawl_cero() -> list[Post]:
    return crawl_notes_on_waldbewohner_eu("9svsbjf77hmg007e")


def crawl_yasu() -> list[Post]:
    return crawl_notes_on_waldbewohner_eu("9st8kmrs7hmg0001")


def test_can_crawl_users():
    """
    Tests if the users can be crawled without throwing an error.
    """
    crawl_cero()
    crawl_yasu()
    crawl_varia()
