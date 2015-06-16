from plugin.sync.core.enums import SyncData, SyncMedia, SyncMode
from plugin.sync.handlers.core import DataHandler, PushHandler, bind
from plugin.sync.handlers.ratings.base import RatingsHandler

import logging

log = logging.getLogger(__name__)


class Base(PushHandler, RatingsHandler):
    def push(self, p_item, t_item, **kwargs):
        # Retrieve properties
        p_rating, t_rating = self.get_operands(p_item, t_item)

        # Determine performed action
        action = self.get_action(p_rating, t_rating)

        if not action:
            # No action required
            return

        # Execute action
        self.execute_action(
            action,

            p_item=p_item,
            p_value=p_rating,
            t_value=t_rating,
            **kwargs
        )


class Movies(Base):
    media = SyncMedia.Movies

    @bind('added', [SyncMode.Push])
    def on_added(self, key, p_guid, p_item, p_value, t_value, **kwargs):
        log.debug('Movies.on_added(%r, ...)', key)

        if t_value:
            return

        self.store_movie('add', p_guid,
            p_item,
            rating=p_value
        )


class Episodes(Base):
    media = SyncMedia.Episodes

    @bind('added', [SyncMode.Push])
    def on_added(self, key, p_guid, identifier, p_show, p_value, t_value, **kwargs):
        log.debug('Episodes.on_added(%r, ...)', key)

        if t_value:
            return

        self.store_episode('add', p_guid,
            identifier, p_show,
            rating=p_value
        )


class Push(DataHandler):
    data = SyncData.Ratings
    mode = SyncMode.Push

    children = [
        Movies,
        Episodes
    ]
