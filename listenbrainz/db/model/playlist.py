import uuid
import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class PlaylistRecording(BaseModel):
    """A recording that is part of a playlist"""
    # Internal id of the playlist
    id: int
    # What playlist this recording is a part of
    playlist_id: int
    # The position of this item in the playlist
    position: int
    # The item
    mbid: uuid.UUID
    # Who added this item to the playlist
    added_by_id: int
    # When the item was added
    created: datetime.datetime

    artist_credit: Optional[str]
    artist_mbids: Optional[List[uuid.UUID]]
    title: Optional[str]
    # What release would this be if the recording is of more than one?
    release_mbid: Optional[uuid.UUID]
    release_name: Optional[str]
    release_track_number: Optional[int]  # exists in xspf, probably not needed?
    duration_ms: Optional[int]
    image: Optional[str]  # who looks this up on CAA?

    # Computed
    added_by: str


class WritablePlaylistRecording(PlaylistRecording):
    id: int = None
    playlist_id: int = None
    position: int = None
    created: datetime.datetime = None
    added_by: str = None


class Playlist(BaseModel):

    # Database fields
    # The internal ID of the playlist row in the database
    id: int
    # The public-facing uuid of the playlist
    mbid: uuid.UUID
    # The listenbrainz user id who created this playlist
    creator_id: int
    # The name of the playlist
    name: str
    # An optional description of the playlist
    description: Optional[str]
    public: bool = True
    # When the playlist was created
    created: datetime.datetime
    # If the playlist was copied from another one, the id of that playlist
    copied_from_id: Optional[int]
    # If the playlist was created by a bot, the user for who this playlist was created
    created_for_id: Optional[int]
    # If the playlist was created by a bot, some freeform data about it
    algorithm_metadata: Optional[Dict]

    # Computed fields
    created_for: Optional[str]
    creator: str
    recordings: List[PlaylistRecording]


class WritablePlaylist(Playlist):
    id: int = None
    mbid: str = None
    creator: str = None
    recordings: List[PlaylistRecording] = []
    created: datetime.datetime = None