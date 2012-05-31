# -*- coding: utf-8 -*-
from sockjs.tornado.router import SockJSRouter
from tornado import web
from tornado import ioloop
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from mindmaptornado import handlers


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-o', '--overwrite_existing', dest='overwrite_existing', metavar='overwrite_existing', type='int',
                    help='overwrite existing cache values, default=False', default=1,
                    ),
        make_option('-m', '--manufacturer_slug', dest='manufacturer_slug', type='str', help='manufacturer_slug for family diff, default=ALL',default="ALL",
                    ),

    )

    def handle(self, *args, **options):
        MindmapWebSocketRouter = SockJSRouter(handlers.MindmapWebSocketHandler, '/echo')

        app_kwargs = {}
        if settings.ENVIRONMENT.IS_FOR_DEVELOPMENT:
            app_kwargs['debug'] = True

        app = web.Application(MindmapWebSocketRouter.urls, **app_kwargs)
        app.listen(1234)
        ioloop.IOLoop.instance().start()
