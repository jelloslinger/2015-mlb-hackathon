# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.orm import sessionmaker

from datapro.framework.util import dict_merge


class Connection(object):

    _CONFIG = {
        'db': {
            'admin': {
                'drivername': 'mysql',
                'host': '127.0.0.1',
                'password': 'abc123',
                'username': 'root'
            },
            'common': {
                'drivername': 'mysql',
                'host': '127.0.0.1',
                'password': 'abc123',
                'username': 'root'
            }
        },
        # 'model': {
        #     'schema_prefix': ''
        # }
    }

    def __init__(self, name, config={}):

        try:
            self._config = dict_merge(Connection._CONFIG['db'][name], config)
        except KeyError:
            raise ConnectionException('Connection name, {0}, not defined in configuration'.format(name))

        self._config['database'] = name

        self.url = url.URL(**self._config)
        self.engine = create_engine(self.url, convert_unicode=True, pool_recycle=14400)  # 4-hour recycle


class OrmConnection(Connection):

    def __init__(self, name, config={}, autocommit=False, expire_on_commit=False):
        super(OrmConnection, self).__init__(name)
        self._flush_count = 0
        self.flush_block_size = 10000
        self.session = sessionmaker(bind=self.engine, autocommit=autocommit, expire_on_commit=expire_on_commit)()

    def block_flush(self):
        self._flush_count += 1
        if self._flush_count >= self.flush_block_size:
            self._flush_count = 0
            self.session.flush()
            return True
        return False


class ConnectionException(Exception):
    pass