# -*- coding: utf-8 -*-
from threading import Lock
from sockjs.tornado import SockJSConnection
from tornado.escape import json_decode
from .exceptions import HTTPException
from .decorators import check_for_map_pk_data


class MindmapWebSocketHandler(SockJSConnection):
    _maps_participants = dict()
    _lock = Lock()

    @classmethod
    def _die(cls, *args, **kwargs):
        raise HTTPException(*args, **kwargs)

    @check_for_map_pk_data
    def _register_myself_as_map_participant(self, data):
        self._lock.acquire()
        self._maps_participants.setdefault(data['map_pk'], set()).add(self)
        self._lock.release()

    def on_message(self, data):
        try:
            data = json_decode(data)
        except ValueError:
            raise self._die(log_message='Unable to decode json')

        if type(data).__name__ != 'dict' or 'method' not in data:
            raise self._die(log_message='data is not a dict or no key "method" in data dict found')

        # define available methods
        methods = {
           'register_myself_as_map_participant': self._register_myself_as_map_participant,
           'update_single_component_pos': 'update_single_component_pos',
        }

        # call method
        try:
            methods.get(data['method'], None)(data)
        except TypeError:
            self._die('Unknown method "%s" called' % data['method'])

    def on_close(self):
        for map_pk in self._maps_participants.keys():
            if self in self._maps_participants[map_pk]:
                self._lock.acquire()

                # remove client from map
                try:
                    self._maps_participants[map_pk].remove(self)
                except KeyError:
                    pass

                # remove map if no participants remains on map
                if not len(self._maps_participants[map_pk]):
                    del self._maps_participants[map_pk]

                self._lock.release()
