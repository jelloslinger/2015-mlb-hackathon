# -*- coding: utf-8 -*-

"""Framework for ETL jobs.

TODO - Generic description to be written here.

Example:
    TODO
"""

import datetime

from datapro.base.interface import IFramework
from datapro.framework.util import dict_merge

STATUS_FAIL = 'failed'
STATUS_RUN = 'running'
STATUS_PAUSE = 'paused'
STATUS_START = 'started'
STATUS_STOP = 'stopped'


class BaseConfig(dict):

    def __init__(self, override={}):
        super().__init__()
        self.merge(override)

    def merge(self, override=None):
        self.update(dict_merge(self, override))


class BaseJob(IFramework):
    """Generalized implementation of an ETL Job
    """
    def __init__(self, identifier, debug=False, profile=False):

        if debug:
            import pdb
            pdb.set_trace()

        if profile:
            import cProfile
            self.profiler = cProfile.Profile()
            self.profiler.enable()
        else:
            self.profiler = None

        self.identifier = identifier
        self.status = None

        self.started_at = None
        self.stopped_at = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    def uptime(self):
        if isinstance(self.started_at, datetime.datetime):
            if isinstance(self.stopped_at, datetime.datetime):
                return self.stopped_at - self.started_at
            return datetime.datetime.utcnow() - self.started_at
        else:
            return datetime.timedelta(0)

    def start(self):
        self.started_at = datetime.datetime.utcnow()
        self.status = STATUS_START

    def stop(self):
        self.status = STATUS_STOP
        self.stopped_at = datetime.datetime.utcnow()
