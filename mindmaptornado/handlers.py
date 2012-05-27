# -*- coding: utf-8 -*-
from sockjs.tornado import SockJSConnection


MAPS_PARTICIPANTS = dict()
MAPS_PARTICIPANTS[0] = set()

class MindmapWebSocketHandler(SockJSConnection):
    def on_open(self, info):
        print 'connect'
        MAPS_PARTICIPANTS[0].add(self)

    def on_message(self, msg):
        self.broadcast(MAPS_PARTICIPANTS[0], msg)

    def on_close(self):
        print 'disconnect'
        MAPS_PARTICIPANTS[0].remove(self)