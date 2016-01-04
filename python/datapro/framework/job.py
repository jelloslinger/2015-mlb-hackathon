# -*- coding: utf-8 -*-

import logging

from datapro import BaseJob


logger = logging.getLogger(__name__)


class EtlJob(BaseJob):

    def start(self):
        super().start()

    def stop(self):
        super().start()
        # if profiler exists then lets do something about it
