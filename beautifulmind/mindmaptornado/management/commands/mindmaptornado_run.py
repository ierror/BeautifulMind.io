# -*- coding: utf-8 -*-
from sockjs.tornado.router import SockJSRouter
from tornado import web
from tornado import ioloop
from django.conf import settings
from django.core.management.base import BaseCommand
from mindmaptornado import handlers


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        MindmapWebSocketRouter = SockJSRouter(handlers.MindmapWebSocketHandler, '/ws')

        app_kwargs = {}
        if settings.ENVIRONMENT.IS_FOR_DEVELOPMENT:
            app_kwargs['debug'] = True

        app = web.Application(MindmapWebSocketRouter.urls, **app_kwargs)
        app.listen(settings.MINDMAPTORNADO_BIND_PORT)

        try:
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            ioloop.IOLoop.instance().stop()
