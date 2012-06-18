# -*- coding: utf-8 -*-
import datetime
from sockjs.tornado.router import SockJSRouter
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from beautifulmind.mindmap.settings import EXPORTS_SAVE_PATH


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        for exported_file in default_storage.listdir(EXPORTS_SAVE_PATH)[1]:
            if exported_file == 'DONOTDELTETHISFOLDER':
                continue

            exported_file = '%s%s' % (EXPORTS_SAVE_PATH, exported_file)
            modified_time_delta = datetime.datetime.now() - default_storage.modified_time(exported_file)
            if modified_time_delta > datetime.timedelta(days=1):
                default_storage.delete(exported_file)
