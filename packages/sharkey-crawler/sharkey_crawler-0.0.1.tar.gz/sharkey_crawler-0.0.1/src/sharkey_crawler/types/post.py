#   ---------------------------------------------------------------------------------
#   Copyright (c) Hexafuchs. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This defines types related to posts."""

from __future__ import annotations

from enum import Enum

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .user import UserLite

__all__ = ["Post", "Visibility", "DriveFile", "DriveFolder", "DriveFileProperties", "Channel", "Poll", "PollChoice"]

SharkeyId = str


class Post(BaseModel):
    """Represents a post as returned by Sharkey."""

    model_config = ConfigDict(extra="forbid")

    id: SharkeyId
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    text: str | None = None
    cw: str | None = None
    user_id: SharkeyId
    user: UserLite
    reply_id: SharkeyId | None = None
    renote_id: SharkeyId | None = None
    reply: Post | None = None
    renote: Post | None = None
    is_hidden: bool | None = None
    visibility: Visibility
    mentions: list[SharkeyId] = []
    visible_user_ids: list[SharkeyId] = []
    file_ids: list[SharkeyId] = []
    files: list[DriveFile] = []
    tags: list[str] = []
    poll: Poll | None = None
    emojis: dict[str, str] = {}
    channel_id: SharkeyId | None = None
    channel: Channel | None = None
    local_only: bool | None = None
    reaction_acceptance: str | None = None
    reaction_emojis: dict[str, str] = {}
    reactions: dict[str, int] = {}
    reaction_count: int = 0
    renote_count: int = 0
    replies_count: int = 0
    uri: str | None = None
    url: str | None = None
    reaction_and_user_pair_cache: list[str] = []
    clipped_count: int | None = None
    my_reaction: str | None = None


class Visibility(str, Enum):
    public = "public"
    home = "home"
    followers = "followers"
    specified = "specified"


class DriveFile(BaseModel):
    id: SharkeyId
    created_at: datetime | None = None
    name: str
    type: str
    md5: str
    size: int | float
    is_sensitive: bool | None = None
    blurhash: str | None = None
    properties: DriveFileProperties | None = None
    url: str
    thumbnail_url: str | None = None
    comment: str | None = None
    folder_id: SharkeyId | None = None
    folder: DriveFolder | None = None
    user_id: SharkeyId | None = None
    user: UserLite | None = None


class DriveFolder(BaseModel):
    id: SharkeyId
    created_at: datetime
    name: str
    parent_id: SharkeyId | None = None
    folders_count: int
    files_count: int
    parent: DriveFolder


class DriveFileProperties(BaseModel):
    width: int | float
    height: int | float
    orientation: int | float | None = None
    avg_color: str = None


class Channel(BaseModel):
    id: SharkeyId
    name: str
    color: str
    is_sensitive: bool
    allow_renote_to_external: bool
    user_id: SharkeyId | None = None


class Poll(BaseModel):
    expires_at: datetime | None = None
    multiple: bool
    choices: list[PollChoice] = []


class PollChoice(BaseModel):
    is_voted: bool
    text: str
    votes: int
