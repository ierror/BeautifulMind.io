# -*- coding: utf-8 -*-
from threading import Lock
from sockjs.tornado import SockJSConnection
from tornado.escape import json_decode, json_encode
from .exceptions import HTTPException
from .decorators import check_for_data


class MindmapWebSocketHandler(SockJSConnection):
    _maps_participants = dict()
    _lock = Lock()

    @classmethod
    def _die(cls, *args, **kwargs):
        raise HTTPException(*args, **kwargs)


    def _broadcast_to_map(self, method, data={}):
        data['method'] = method
        self.broadcast(
            clients = [ maps_participant for maps_participant in self._maps_participants[data['map_pk']] if maps_participant != self ],
            message = json_encode(data)
        )


    @check_for_data('map_pk', force_int=True)
    def _register_myself_as_map_participant(self, data):
        self._lock.acquire()
        self._maps_participants.setdefault(data['map_pk'], set()).add(self)
        self._lock.release()


    @check_for_data('map_pk', 'component_pk', 'pos_left', 'pos_top', force_int=True)
    def _update_component_pos(self, data):
        self._broadcast_to_map('update_component_pos', data)


    @check_for_data('map_pk', 'component_pk', force_int=True)
    @check_for_data('title')
    def _update_component_title(self, data):
        self._broadcast_to_map('update_component_title', data)

    @check_for_data('map_pk', 'except_component_pk', 'offset_left', 'offset_top', force_int=True)
    def _add_components_offset_except_one(self, data):
        self._broadcast_to_map('add_components_offset_except_one', data)


    @check_for_data('parent_pk', 'pos_left', 'pos_top', force_int=True)
    @check_for_data('title')
    def _add_component(self, data):
        self._broadcast_to_map('add_component', data)


    def on_message(self, data):
        try:
            data = json_decode(data)
        except ValueError:
            self._die(log_message='Unable to decode json')

        if type(data).__name__ != 'dict' or 'method' not in data:
            self._die(log_message='data is not a dict or no key "method" in data dict found. Data: %s' % data)

        # define available methods
        methods = {
           'register_myself_as_map_participant': self._register_myself_as_map_participant,
           'update_component_pos': self._update_component_pos,
           'update_component_title': self._update_component_title,
           'add_components_offset_except_one': self._add_components_offset_except_one,
           'add_component': self._add_component,
        }

        # call method
        try:
            method = methods.get(data['method'], None)
            method(data)
        except TypeError:
            self._die('Unknown method "%s" called' % data['method'])


    def on_close(self):
        for map_pk in self._maps_participants.keys():
            if self in self._maps_participants.get(map_pk, []):
                self._lock.acquire()

                # remove client from map
                try:
                    self._maps_participants[map_pk].remove(self)
                except KeyError:
                    pass

                # remove map if no participants remains on map
                try:
                    if not len(self._maps_participants[map_pk]):
                        del self._maps_participants[map_pk]
                except KeyError:
                    pass

                self._lock.release()
