#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""
import shelve

from settings import INDEX_DAT


class IndexData(object):
    """索引数据类
    """

    _data = {}

    @classmethod
    def _load_data(cls):
        """载入数据
        """
        dat = shelve.open(INDEX_DAT)
        for k in dat:
            cls._data[k] = dat[k]
        return cls._data

    @classmethod
    def get_index_data(cls):
        """获取索引信息
        """
        if len(cls._data) == 0:
            cls._load_data()
        return cls._data

    @classmethod
    def reload_index_data(cls):
        """重载数据信息
        """
        cls._load_data()


if __name__ == "__main__":
    pass
