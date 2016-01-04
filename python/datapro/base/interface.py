# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class IFramework(object):
    """Framework interface
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
