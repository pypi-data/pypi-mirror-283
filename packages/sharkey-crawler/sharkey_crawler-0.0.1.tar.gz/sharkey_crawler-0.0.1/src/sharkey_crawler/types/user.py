#   ---------------------------------------------------------------------------------
#   Copyright (c) Hexafuchs. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This defines types related to users."""

from __future__ import annotations

from enum import Enum
from datetime import datetime

from pydantic import BaseModel

__all__ = ["UserLite", "OnlineStatus", "AvatarDecoration", "Instance", "BadgeRole"]


SharkeyId = str


class UserLite(BaseModel):
    """Represents a user lite as returned by Sharkey."""

    id: SharkeyId
    name: str | None = None
    description: str | None = None
    username: str
    host: str | None = None
    created_at: datetime | None = None
    avatar_url: str | None = None
    avatar_blurhash: str | None = None
    avatar_decorations: list[AvatarDecoration] = []
    is_bot: bool | None = None
    is_cat: bool | None = None
    instance: Instance | None = None
    emojis: dict[str, str] = {}
    online_status: OnlineStatus
    badge_roles: list[BadgeRole] = []
    noindex: bool = False
    is_silenced: bool = False
    speak_as_cat: bool = False
    approved: bool = False
    followers_count: int = 0
    following_count: int = 0
    notes_count: int = 0


class OnlineStatus(str, Enum):
    unknown = "unknown"
    online = "online"
    active = "active"
    offline = "offline"


class AvatarDecoration(BaseModel):
    id: SharkeyId
    angle: float | int | None = None
    flip_h: bool | None = None
    url: str
    offset_x: float | int | None = None
    offset_y: float | int | None = None


class Instance(BaseModel):
    id: SharkeyId | None = None
    name: str | None = None
    software_name: str | None = None
    software_version: str | None = None
    icon_url: str | None = None
    favicon_url: str | None = None
    theme_color: str | None = None


class BadgeRole(BaseModel):
    name: str
    icon_url: str | None = None
    display_order: int
    behavior: str | None = None
