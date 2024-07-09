#   ---------------------------------------------------------------------------------
#   Copyright (c) Hexafuchs. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This provides a sharkey accessor instance for the /users/notes endpoint."""

from __future__ import annotations

import requests

from pydantic import conint

from .types import Post
from .convert import dict_keys_to_snake_case

__all__ = ["SharkeyServer"]

SharkeyId = str


class SharkeyServer:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        if not self.base_url.startswith("http://") and not self.base_url.startswith("https://"):
            self.base_url = f"https://{self.base_url}"

    def user_notes(
        self,
        user_id: SharkeyId,
        with_channel_notes: bool = False,
        with_renotes: bool = True,
        with_files: bool = False,
        with_replies: bool = False,
        limit: conint(ge=0, le=100) = 10,
        allow_partial: bool = False,
        since_date: int | None = None,
        until_date: int | None = None,
        since_id: SharkeyId | None = None,
        until_id: SharkeyId | None = None,
    ) -> list[Post]:
        """
        This function returns the latest posts about a user.

        WARNING: Because the functionality is not documented, I will take an educated guess about the meaning of the
            arguments. I can only spend looking into other peoples codes for so much time. Please open an issue if I
            got something wrong. If you want to contribute, have a look at the code yourself at
            https://activitypub.software/TransFem-org/Sharkey

        @param user_id: user id you want to crawl
        @param with_channel_notes:
        @param with_renotes: include boosts (boosts that quote something are always included)
        @param with_files: include posts with files
        @param with_replies: include replies to other users
        @param limit: maximum number of posts, between 1 and 100
        @param allow_partial: read only from redis, do not resort to the database to fill the limit
        @param since_date: get posts after or from this date, expressed as milliseconds since epoch,
            do not use with other 'since_' or 'until_' argument
        @param until_date: get posts before or from this date, expressed as milliseconds since epoch,
            do not use with other 'since_' or 'until_' argument
        @param since_id: get posts after this id (and this id), expressed as milliseconds since epoch,
            do not use with other 'since_' or 'until_' argument
        @param until_id: get posts before this id (and this id), expressed as milliseconds since epoch,
            do not use with other 'since_' or 'until_' argument
        @return:
        """
        payload = {
            "userId": user_id,
            "withChannelNotes": with_channel_notes,
            "withRenotes": with_renotes,
            "withFiles": with_files,
            "withReplies": with_replies,
            "limit": limit,
            "allowPartial": allow_partial,
        }
        if since_date:
            payload["sinceDate"] = since_date
        if until_date:
            payload["untilDate"] = until_date
        if since_id:
            payload["sinceId"] = since_id
        if until_id:
            payload["untilId"] = until_id

        response = requests.post(self.base_url + "/api/users/notes", json=payload)

        data = response.json()

        posts = []
        for post in data:
            from pprint import pprint

            pprint(dict_keys_to_snake_case(post))
            posts.append(Post.model_validate(dict_keys_to_snake_case(post)))

        return posts
